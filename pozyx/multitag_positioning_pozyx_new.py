
#!/usr/bin/env python
"""
The Pozyx ready to localize tutorial (c) Pozyx Labs
Please read the tutorial that accompanies this sketch:
https://www.pozyx.io/Documentation/Tutorials/ready_to_localize/Python

This tutorial requires at least the contents of the Pozyx Ready to Localize kit. It demonstrates the positioning capabilities
of the Pozyx device both locally and remotely. Follow the steps to correctly set up your environment in the link, change the
parameters and upload this sketch. Watch the coordinates change as you move your device around!

"""
from time import sleep, time
from pypozyx import (PozyxConstants, Coordinates, POZYX_SUCCESS, POZYX_ANCHOR_SEL_AUTO, version,
                     DeviceCoordinates, PozyxSerial, get_first_pozyx_serial_port, SingleRegister, SensorData)
from pythonosc.udp_client import SimpleUDPClient
from pypozyx.definitions.bitmasks import POZYX_INT_MASK_IMU
from pypozyx.tools.version_check import perform_latest_version_check

#add files with settings for anchors and which tags to include

class MultitagPositioning(object):
    """Continuously performs multitag positioning"""

    def __init__(self, pozyx, osc_udp_client, tag_ids, anchors, algorithm=PozyxConstants.POSITIONING_ALGORITHM_UWB_ONLY,
                 dimension=PozyxConstants.DIMENSION_3D, height=1000):
        self.pozyx = pozyx
        self.osc_udp_client = osc_udp_client

        self.tag_ids = tag_ids
        self.anchors = anchors
        self.algorithm = algorithm
        self.dimension = dimension
        self.height = height
        self.current_time=time()
        self.current_data = []
        global c_index
        c_index=0

    def setup(self):
        """Sets up the Pozyx for positioning by calibrating its anchor list."""
        print("------------POZYX MULTITAG POSITIONING V{} -------------".format(version))
        print("")
        print(" - System will manually calibrate the tags")
        print("")
        print(" - System will then auto start positioning")
        print("")
        if None in self.tag_ids:
            for device_id in self.tag_ids:
                self.pozyx.printDeviceInfo(device_id)
        else:
            for device_id in [None] + self.tag_ids:
                self.pozyx.printDeviceInfo(device_id)
        print("")
        print("------------POZYX MULTITAG POSITIONING V{} -------------".format(version))
        print("")

        self.setAnchorsManual()

        #self.printPublishAnchorConfiguration()

    def loop(self):
        """Performs positioning and prints the results."""
        global c_index
        #print(c_index)
        current_data=[]
        i = 0
        tag_id = self.tag_ids[c_index]
        position = Coordinates()
        sensor_data=SensorData()
        calibration_status=SingleRegister()
        status = self.pozyx.doPositioning(position, self.dimension, self.height, self.algorithm, remote_id=tag_id)
        if status == POZYX_SUCCESS:
            c_time= str(time())
        status = self.pozyx.getAllSensorData(sensor_data, tag_id)
        #status &= self.pozyx.getCalibrationStatus(calibration_status, tag_id)
        #print(status)
        if status == POZYX_SUCCESS:
            if tag_id:
                #print("in tagid")
                current_data.append([tag_id, position.x, position.y, position.z] + list(sensor_data))
                #print(tag_id)
                position_str = "{},{},{},".format(position.x, position.y, position.z)
                #current_data[i]+=list(sensor_data)
                print(hex(tag_id)+": "+position_str)

                #with open(outfile, 'a+') as file:
                #    file.write(c_time+","+hex(tag_id)+","+position_str+str(sensor_data)+"\n")
            #self.printPublishPosition(position, tag_id)
        #else:
        #    self.printPublishErrorCode("positioning", tag_id)
        c_index+=1
        if c_index == len(self.tag_ids):
            c_index=0
        return current_data
    def printPublishPosition(self, position, network_id):
        """Prints the Pozyx's position and possibly sends it as a OSC packet"""
        if network_id is None:
            network_id = 0
        s = "POS ID: {}, x(mm): {}, y(mm): {}, z(mm): {}".format("0x%0.4x" % network_id,
                                                                 position.x, position.y, position.z)
        print(s)
        if self.osc_udp_client is not None:
            self.osc_udp_client.send_message(
                "/position", [network_id, position.x, position.y, position.z])

    def setAnchorsManual(self, save_to_flash=False):
        """Adds the manually measured anchors to the Pozyx's device list one for one."""
        for tag_id in self.tag_ids:
            status = self.pozyx.clearDevices(tag_id)
            for anchor in self.anchors:
                status &= self.pozyx.addDevice(anchor, tag_id)
            if len(self.anchors) > 4:
                status &= self.pozyx.setSelectionOfAnchors(PozyxConstants.ANCHOR_SELECT_AUTO, len(self.anchors),
                                                           remote_id=tag_id)
            # enable these if you want to save the configuration to the devices.
            if save_to_flash:
                self.pozyx.saveAnchorIds(tag_id)
                self.pozyx.saveRegisters([POZYX_ANCHOR_SEL_AUTO], tag_id)
            self.printPublishConfigurationResult(status, tag_id)

    def printPublishConfigurationResult(self, status, tag_id):
        """Prints the configuration explicit result, prints and publishes error if one occurs"""
        if tag_id is None:
            tag_id = 0
        if status == POZYX_SUCCESS:
            print("Configuration of tag %s: success" % tag_id)
        else:
            self.printPublishErrorCode("configuration", tag_id)

    def printPublishErrorCode(self, operation, network_id):
        """Prints the Pozyx's error and possibly sends it as a OSC packet"""
        error_code = SingleRegister()
        status = self.pozyx.getErrorCode(error_code, network_id)
        if network_id is None:
            network_id = 0
        if status == POZYX_SUCCESS:
            print("Error %s on ID %s, %s" %
                  (operation, "0x%0.4x" % network_id, self.pozyx.getErrorMessage(error_code)))
            if self.osc_udp_client is not None:
                self.osc_udp_client.send_message(
                    "/error_%s" % operation, [network_id, error_code[0]])
        else:
            # should only happen when not being able to communicate with a remote Pozyx.
            self.pozyx.getErrorCode(error_code)
            print("Error % s, local error code %s" % (operation, str(error_code)))
            if self.osc_udp_client is not None:
                self.osc_udp_client.send_message("/error_%s" % operation, [0, error_code[0]])

    def printPublishAnchorConfiguration(self):
        for anchor in self.anchors:
            print("ANCHOR,0x%0.4x,%s" % (anchor.network_id, str(anchor.pos)))
            if self.osc_udp_client is not None:
                self.osc_udp_client.send_message(
                    "/anchor", [anchor.network_id, anchor.pos.x, anchor.pos.y, anchor.pos.z])
                sleep(0.025)

def getOptions(opts, vars):
    
    pass

def getChannelNames(opts, vars):
    
    return { 'position' : 'XYZ coordinates' }


def initChannel(name, channel, types, opts, vars):

    
    if name == 'position':
        channel.dim =  28
        channel.type = types.FLOAT
        channel.sr = 10
    else:
        print('unkown channel name')


def connect(opts, vars):
    
    check_pypozyx_version = False
    if check_pypozyx_version:
        perform_latest_version_check()

    # shortcut to not have to find out the port yourself.
    serial_port = get_first_pozyx_serial_port()
    if serial_port is None:
        print("No Pozyx connected. Check your USB cable or your driver!")
        quit()

    # enable to send position data through OSC
    use_processing = True

    # configure if you want to route OSC to outside your localhost. Networking knowledge is required.
    ip = "127.0.0.1"
    network_port = 8888


    # IDs of the tags to position, add None to position the local tag as well.
    tag_ids = [0x6730, 0x6717]
    #[0x675c, 0x0212, 0x6728, 0x6735, 0x6724, 0x6743, 0x6730, 0x6717, 0x6737, 0x675b] 
    # 0x6e58, 0x0221, 0x694c, 0x6704, 0x6756 

    # necessary data for calibration
    anchors = [DeviceCoordinates(0x6767, 1, Coordinates(28041, 0, 2362)),
               DeviceCoordinates(0x676e, 1, Coordinates(28041, 15849, 2362)),
               DeviceCoordinates(0x6e71, 1, Coordinates(0, 15849, 2362)),
               DeviceCoordinates(0x6956, 1, Coordinates(0, 0, 2362))] # the origin
    # positioning algorithm to use, other is PozyxConstants.POSITIONING_ALGORITHM_TRACKING
    algorithm = PozyxConstants.POSITIONING_ALGORITHM_UWB_ONLY
    # positioning dimension. Others are PozyxConstants.DIMENSION_2D, PozyxConstants.DIMENSION_2_5D
    dimension = PozyxConstants.DIMENSION_3D
    # height of device, required in 2.5D positioning
    height = 1000

    osc_udp_client = None
    if use_processing:
        osc_udp_client = SimpleUDPClient(ip, network_port)

    pozyx = PozyxSerial(serial_port)
    global r 

    r = MultitagPositioning(pozyx, osc_udp_client, tag_ids, anchors,
                            algorithm, dimension, height)

    labels = "time,id, position_x, position_y, position_z, pressure, acceleration_0, acceleration_1, acceleration_2, magnetic_0, magnetic_1, magnetic_2, angular_vel_0, angular_vel_1, angular_vel_2, euler_angles_0, euler_angles_1, euler_angles_2, quaternion_0, quaternion_1, quaternion_2, quaternion_3, linear_acceleration_0, linear_acceleration_1, linear_acceleration_2, gravity_vector_0, gravity_vector_1, gravity_vector_2, temperature"

    r.setup()
    ctime = str(time())
    #print("connected")

        
def read(name, sout, reset, board, opts, vars):    

    cur_data = r.loop()
    #print("Number:", sout.num)
    #print("Dimensions",sout.dim)
    #print(cur_data)
    for a in range(len(cur_data)):
        c_data = cur_data[a]
        #print(len(cur_data[a]))
        for b in range(sout.dim):
            #print(cur_data[b])
            sout[a,b]=float(cur_data[a][b])

def disconnect(opts, vars):
    pass
    

