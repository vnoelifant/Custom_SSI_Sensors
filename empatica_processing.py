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

deviceIDS = 'a71af2' #Spain

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

f = open("multi_test_final.txt", "w+")

#if acc:
infoRotator = 0
	
def getOptions(opts, vars):
	opts['sr_acc']   = 32 #sampling rate in hertz
	opts['sr_bvp']   = 64 #ssampling rate <-
	opts['sr_gsr']   = 4 #sampling rate  <- 
	opts['sr_temp']  = 4 #sampling rate
	opts['dim_acc']  = 5 #id, time, x y z  
	opts['dim_bvp']  = 3 #id, time, value
	opts['dim_gsr']  = 3 #id, time, value
	opts['dim_temp'] = 3 #id, time, value
 
def getChannelNames(opts,vars):
	return {'acc'  :'3-axis acceleration',
			'bvp'  : 'Blood Volume Pulse',
			'gsr'  : 'Galvanic Skin Response (Electrodermal Activity)',
			'temp' : 'Temperature' }
	
def initChannel(name, channel, types, opts, vars):
	if name == 'acc':
		channel.dim = opts['dim_acc']
		channel.type = types.FLOAT
		channel.sr = opts ['sr_acc']
	elif name == 'bvp':
		channel.dim = opts['dim_bvp']
		channel.type = types.FLOAT
		channel.sr = opts['sr_bvp']
	elif name == 'gsr':
		channel.dim = opts['dim_gsr']
		channel.type = types.FLOAT
		channel.sr = opts['sr_gsr']
	elif name == 'temp':
		channel.dim = opts['dim_temp']
		channel.type = types.FLOAT
		channel.sr = opts['sr_temp']
	else:
		print('unknown channel name')

def connect(opts, vars):
	pass
	 
def read(name, sout, reset, board, opts, vars):
	
	cur_data = []
	
	global infoRotator 
	
	if infoRotator == 0:
		s.send(b'device_subscribe acc ON\r\n')
		infoACC = pylsl.StreamInfo('acc','ACC',3,32,'float32','ACC-empatica_e4');
		outletACC = pylsl.StreamOutlet(infoACC) 	
		infoRotator = 1
	elif infoRotator == 1:
		s.send(b'device_subscribe bvp ON\r\n')
		infoBVP = pylsl.StreamInfo('bvp','BVP',1,64,'float32','BVP-empatica_e4');
		outletBVP = pylsl.StreamOutlet(infoBVP) 
		infoRotator = 2
	elif infoRotator == 2:
		s.send(b'device_subscribe gsr ON\r\n')
		infoGSR = pylsl.StreamInfo('gsr','GSR',1,4,'float32','GSR-empatica_e4');
		outletGSR = pylsl.StreamOutlet(infoGSR)
		infoRotator = 3
	else:
		s.send(b'device_subscribe tmp ON\r\n')
		infoTemp = pylsl.StreamInfo('tmp','Temp',1,4,'float32','Temp-empatica_e4');
		outletTemp = pylsl.StreamOutlet(infoTemp) 
		infoRotator = 0
				
	time.sleep(1)

	try: 
		response = s.recv(bufferSize)
		print("response")
		print(response)
			
		cur_data.insert(0, response)
			
		####################################################
		if name == "acc":
			cur_data = process_data_acc(cur_data)
			cur_data.insert(0, float(int(deviceID,16)))
			print("acc") 
			print(cur_data)
			if len(cur_data) > 3:
	
				f.write("acc" + str(cur_data))
				
				for i in range(len(cur_data)):
					sout[0, i] = float(cur_data[i])
				
		######################################################		
		
		if name == "bvp":
			cur_data = process_data_bvp(cur_data)
			cur_data.insert(0, float(int(deviceID,16)))
			print("bvp") 
			print(cur_data)
			if len(cur_data) > 1:
				f.write("bvp" + str(cur_data))
				
				for i in range(len(cur_data)):
					sout[0, i] = float(cur_data[i])
				
		######################################################		
	 
		if name == "gsr":
			cur_data = process_data_gsr(cur_data)
			cur_data.insert(0, float(int(deviceID,16)))
			print("gsr") 
			print(cur_data)		
			if len(cur_data) > 1:
				f.write("gsr" + str(cur_data))
				
				for i in range(len(cur_data)):
					sout[0, i] = float(cur_data[i])
				
		######################################################		
		
		if name == "temp":
			cur_data = process_data_temp(cur_data)
			cur_data.insert(0, float(int(deviceID,16)))
			print("temp")
			print(cur_data)
			if len(cur_data) > 1:
				f.write("temp" + str(cur_data))
				
				for i in range(len(cur_data)):
					sout[0, i] = float(cur_data[i])
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
