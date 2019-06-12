import os
import sys
sys.path.append(os.environ.get('PYTHONPATH', ''))

import serial

# serial port obtained via Arduino board
ser = serial.Serial('COM3')
ser.flushInput()


def getOptions(opts, vars):
    
    pass

def getChannelNames(opts, vars):
    
    return { 'ecg' : 'A photoplethysmogram signal' }


def initChannel(name, channel, types, opts, vars):

    if name == 'ecg':
        channel.dim =  1
        channel.type = types.FLOAT
        channel.sr = 9600 # sample rate in Hz
    else:
        print('unkown channel name')


def connect(opts, vars):
    pass

        
def read(name, sout, reset, board, opts, vars): 
    time = sout.time
    delta = 1.0 / sout.sr   
    ser_bytes = ser.readline()
    decoded_bytes = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
    #print("decoded_bytes",decoded_bytes)
    vars['decoded_bytes'] = decoded_bytes
    #print("vars['decoded_bytes']",vars['decoded_bytes'])
    ecg = vars['decoded_bytes']
    #ecg = vars['ser_bytes']
    print("ecg:",ecg)

    if name == 'ecg':
        for n in range(sout.num): # num = 960
            #print("n",n) # nth value of stream
            for d in range(sout.dim): # dim = 1
                #print("d",d) # dth dimension
                sout[n,d] = ecg #sout is d’th dimension value of the n’th sample (3 digit number here)
                #print("sout[n,d]",sout[n,d])
            time += delta
            #print("time",time)
    else:
        print('unkown channel name')

def disconnect(opts, vars):
    pass
