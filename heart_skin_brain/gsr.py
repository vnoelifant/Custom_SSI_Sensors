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
    
    return { 'gsr' : 'A photoplethysmogram signal' }


def initChannel(name, channel, types, opts, vars):

    if name == 'gsr':
        channel.dim =  1
        channel.type = types.FLOAT
        channel.sr = 9600
    else:
        print('unkown channel name')


def connect(opts, vars):
    pass

        
def read(name, sout, reset, board, opts, vars): 
    time = sout.time
    delta = 1.0 / sout.sr   
    ser_bytes = ser.readline()
    decoded_bytes = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
    #print(decoded_bytes)
    vars['decoded_bytes'] = decoded_bytes
    gsr = vars['decoded_bytes']
    #gsr = vars['ser_bytes']
    print("gsr:",gsr)

    if name == 'gsr':
        for n in range(sout.num):
            for d in range(sout.dim):
                sout[n,d] = gsr
            time += delta

    else:
        print('unkown channel name')

def disconnect(opts, vars):
    pass
