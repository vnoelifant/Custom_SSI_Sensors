import socket
import time
import pylsl
import array

# look here for more information on specific commands for empatica streaming signals
# https://support.empatica.com/hc/en-us/articles/201608896-Data-export-and-formatting-from-E4-connect-

#Device ID Table 
# Label: Chile, e4: A02081, DeviceID: BC3864
# Label: USA, e4:A02067 , DeviceID: 329718
# Label: Brazil, e4: A01FCC, DeviceID: 3b3764
# Label: south korea, e4: A01A57, DeviceID: 4c3a64
# Label: , e4: , DeviceID: 5619f2
# Label: , e4: , DeviceID: 584d5c
# Label: , e4: , DeviceID: 6519f2
# Label: Argentina, e4: A01FDC, DeviceID: 7e9318
# Label: Spain, e4: A01C42, DeviceID: a71af2
# Label: , e4: , DeviceID: d817f2


#--- Errors, not allowed 
# Label:Germany e4: A00C65, Device ID: DD01BC
# Label:Mexico e4: A00569, Device ID: 7101BC


#setup server values 
serverAddress = '127.0.0.1'
serverPort = 9999
bufferSize = 4096

#substitute device ID here
deviceIDS = '329718' 
deviceID  = deviceIDS

#conditions for capturing these data streams
acc = True      # 3-axis acceleration
bvp = True      # Blood Volume Pulse
gsr = True      # Galvanic Skin Response (Electrodermal Activity)
tmp = True      # Temperature

#opening the server and connecting 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(3)

print("Connecting to server")
s.connect((serverAddress, serverPort))
print("Connected to server\n")

z = 'device_connect ' + deviceID + '\r\n'
z = z.encode()
print(z)
s.send(z)
response = s.recv(bufferSize)
print(response)

#create the output files 
start_time = str(time.time())+".txt"
f = open(start_time, "w+")

#if acc:
	
	
#options set by each type of data stream we try to collect
#sr stands for sampling rate
# dim is dimensions i.e. each data value we are trying to output to the ssi stream file
# default are acc = 3, and for the rest 1, extra value is to include time or id depending on what you want to capture 
def getOptions(opts, vars):
	opts['sr_acc']   = 32 #sampling rate in hertz
	opts['sr_bvp']   = 64 #sampling rate <-
	opts['sr_gsr']   = 4 #sampling rate  <- 
	opts['sr_temp']  = 4 #sampling rate
	opts['sr_tag']  = 32 #sampling rate
	opts['dim_acc']  = 4 #id, time, x y z  
	opts['dim_bvp']  = 2 #id, time, value
	opts['dim_gsr']  = 2 #id, time, value
	opts['dim_temp'] = 2 #id, time, value
	opts['dim_tag'] = 2 #id, time, value

# identifies channel names
def getChannelNames(opts,vars):
	return {'acc'  :'3-axis acceleration',
			'bvp'  : 'Blood Volume Pulse',
			'gsr'  : 'Galvanic Skin Response (Electrodermal Activity)',
			'temp' : 'Temperature',
			'tag': "Button Presses" }

# initialization of data channels 
def initChannel(name, channel, types, opts, vars):
	if name == 'acc':
		channel.dim = opts['dim_acc']
		channel.type = types.DOUBLE
		channel.sr = opts ['sr_acc']
	elif name == 'bvp':
		channel.dim = opts['dim_bvp']
		channel.type = types.DOUBLE
		channel.sr = opts['sr_bvp']
	elif name == 'gsr':
		channel.dim = opts['dim_gsr']
		channel.type = types.DOUBLE
		channel.sr = opts['sr_gsr']
	elif name == 'temp':
		channel.dim = opts['dim_temp']
		channel.type = types.DOUBLE
		channel.sr = opts['sr_temp']
	elif name == 'tag':
		channel.dim = opts['dim_tag']
		channel.type = types.DOUBLE
		channel.sr = opts['sr_tag']
	else:
		print('unknown channel name')

# Connect to the Empatica server data
def connect(opts, vars):
	#subscribe to channels 
	s.send(b'device_subscribe acc ON\r\n')
	time.sleep(4)
	s.send(b'device_subscribe gsr ON\r\n')
	time.sleep(4)
	s.send(b'device_subscribe tag ON\r\n')
	time.sleep(4)
	#s.send(b'device_subscribe bvp ON\r\n')
	#time.sleep(1)
	#s.send(b'device_subscribe tmp ON\r\n')
	#time.sleep(1)


	#Identify data stream format 
	infoACC = pylsl.StreamInfo('acc','ACC',3,32,'float32','ACC-empatica_e4');
	outletACC = pylsl.StreamOutlet(infoACC) 	
	# infoBVP = pylsl.StreamInfo('bvp','BVP',1,64,'float32','BVP-empatica_e4');
	# outletBVP = pylsl.StreamOutlet(infoBVP) 
	infoGSR = pylsl.StreamInfo('gsr','GSR',1,4,'float32','GSR-empatica_e4');
	outletGSR = pylsl.StreamOutlet(infoGSR)
	infoGSR = pylsl.StreamInfo('tag','TAG',1,32,'float32','GSR-empatica_e4');
	outletGSR = pylsl.StreamOutlet(infoGSR)
	# infoTemp = pylsl.StreamInfo('tmp','Temp',1,4,'float32','Temp-empatica_e4');
	# outletTemp = pylsl.StreamOutlet(infoTemp) 
	 
def read(name, sout, reset, board, opts, vars):
	
	cur_data = []
	
	try: 
		# get response from buffer, whatever is there
		response = s.recv(bufferSize).lower()
		# convert it to a string 
		response = str(response, "utf-8")

		#split the values based on \r\n 
		split_data =response.split('\r\n')

		for d in range(len(split_data)):
			if 'e4' in split_data[d]:
				split_entries = split_data[d].split()
				c_data = split_entries[1:]
				empatica_data_type = split_entries[0].split("_")
				if c_data[0] == 'device_subscribe':
					continue
				
				#write to the files
				f.write(",".join([empatica_data_type[1]]+c_data+["\n"]))
				if name in empatica_data_type:
					for i in range(len(c_data)):
					 	sout[d, i] = float(c_data[i])
	except:
		print("")
				
def disconnect(opts, vars):
	s.send(b'device_disconnect\r\n')
	s.close()
	f.close()
	pass
