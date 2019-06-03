import socket
import time
import pylsl
import array

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

serverAddress = '127.0.0.1'
serverPort = 9999
bufferSize = 4096
optionDevice = 0

deviceIDS = 'BC3864' 

acc = True      # 3-axis acceleration
bvp = True      # Blood Volume Pulse
gsr = True      # Galvanic Skin Response (Electrodermal Activity)
tmp = True      # Temperature

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(3)

deviceID  = deviceIDS

print("Connecting to server")
s.connect((serverAddress, serverPort))
print("Connected to server\n")

z = 'device_connect ' + deviceID + '\r\n'
z = z.encode()
print(z)
s.send(z)
response = s.recv(bufferSize)
print(response)
start_time = str(time.time())+".txt"
f = open(start_time, "w+")

#if acc:
	
def getOptions(opts, vars):
	opts['sr_acc']   = 32 #sampling rate in hertz
	opts['sr_bvp']   = 64 #ssampling rate <-
	opts['sr_gsr']   = 4 #sampling rate  <- 
	opts['sr_temp']  = 4 #sampling rate
	opts['sr_tag']  = 32 #sampling rate
	opts['dim_acc']  = 4 #id, time, x y z  
	opts['dim_bvp']  = 2 #id, time, value
	opts['dim_gsr']  = 2 #id, time, value
	opts['dim_temp'] = 2 #id, time, value
	opts['dim_tag'] = 2 #id, time, value

def getChannelNames(opts,vars):
	return {'acc'  :'3-axis acceleration',
			'bvp'  : 'Blood Volume Pulse',
			'gsr'  : 'Galvanic Skin Response (Electrodermal Activity)',
			'temp' : 'Temperature',
			'tag': "Button Presses" }
	
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

def connect(opts, vars):
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
		response = s.recv(bufferSize).lower()
		response = str(response, "utf-8")
		#print(response)
		split_data =response.split('\r\n')
		#print(sout.num)
		#print(split_data, "ok" in split_data)
		for d in range(len(split_data)):
			if 'e4' in split_data[d]:
				split_entries = split_data[d].split()
				c_data = split_entries[1:]
				empatica_data_type = split_entries[0].split("_")
				if c_data[0] == 'device_subscribe':
					continue
				#if name in split_data[d]:
				f.write(",".join([empatica_data_type[1]]+c_data+["\n"]))
				if name in empatica_data_type:
					for i in range(len(c_data)):
					 	#print(float(c_data[i]))
					 	sout[d, i] = float(c_data[i])
				#print(name, c_data)
	except:
		print("")
				
			
def process_data_acc(data_in):
	output = []
	data_out = data_in[0]
	data_out = str(data_out, "utf-8")
	data_out = data_out.split()
	
	if data_out[0] == "E4_Acc":
		output = data_out[1:5]
		
	return output
	
def process_data_bvp(data_in):
	output = []
	data_out = data_in[0]
	data_out = str(data_out, "utf-8")
	data_out = data_out.split()
	
	if data_out[0] == "E4_Bvp":
		output = data_out[1:3]
		
	return output
	
def process_data_gsr(data_in):
	output = []
	data_out = data_in[0]
	data_out = str(data_out, "utf-8")
	data_out = data_out.split()
	
	if data_out[0] == "E4_Gsr":
		output = data_out[1:3]
		
	return output
	
def process_data_temp(data_in):
	output = []
	data_out = data_in[0]
	data_out = str(data_out, "utf-8")
	data_out = data_out.split()
	
	if data_out[0] == "E4_Temperature":
		output = data_out[1:3]
		
	return output	

def disconnect(opts, vars):
	s.send(b'device_disconnect\r\n')
	s.close()
	f.close()
	pass
