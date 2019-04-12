import myo
from collections import deque


#f, ((ax_emg, ax_orientation), (ax_acceleration, ax_gyroscope)) = plt.subplots(2, 2)

class MyoListener(myo.DeviceListener):
    def __init__(self, emg_filename='myo_emg.csv', orientation_filename='myo_orientation.csv'):
        self.emg_file = emg_filename
        self.orientation_file = orientation_filename
        self.EMG_DATA = deque()
        self.ORIENTATION_DATA = deque()

    def on_connected(self, event):
        print("A myo has connected!")
        event.device.stream_emg(True)

    def on_paired(self, event):
        print("Hello, {}!".format(event.device_name))
        event.device.vibrate(myo.VibrationType.short)

    def on_unpaired(self, event):
        #self.write_emg_data()
        #self.write_orientation_data()
        print('myo_helpers unpaired')
        return False

    def on_orientation(self, event):
        orientation = event.orientation
        acceleration = event.acceleration
        gyroscope = event.gyroscope
        vals = [event.timestamp, orientation[0], orientation[1], orientation[2], orientation[3],
                acceleration[0],acceleration[1], acceleration[2], gyroscope[0],
                gyroscope[1], gyroscope[2]]

        if len(vals) >= 11:
            print("stored orientation")
            self.ORIENTATION_DATA = deque(vals)
            #self.write_orientation_data()

    def on_emg(self, event):
        emg = event.emg
        emgVals = list()
        emgVals.append(event.timestamp)
        emgVals.append(emg[0])
        emgVals.append(emg[1])
        emgVals.append(emg[2])
        emgVals.append(emg[3])
        emgVals.append(emg[4])
        emgVals.append(emg[5])
        emgVals.append(emg[6])
        emgVals.append(emg[7])

        if len(emgVals) >= 9:
            print("stored emg")
            self.EMG_DATA = deque(emgVals)

    def on_pose(self, event):
        #print(event.pose)
        return

    def get_orientation(self):
        print(self.ORIENTATION_DATA)
        return self.ORIENTATION_DATA

    def get_emgVals(self):
        #print(self.EMG_DATA)
        return self.EMG_DATA
