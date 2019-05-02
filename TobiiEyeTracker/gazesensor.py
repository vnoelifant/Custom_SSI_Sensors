#!/usr/bin/env python

from time import sleep, time
import socket
import subprocess


PATH_TO_C_EXECUTABLE = 'C:\\Users\\sespwalkup\\source\\repos\\TobiiReceiver\\TobiiReceiver\\bin\\Debug\\TobiiReceiver.exe'


def getOptions(opts, vars):
    opts['host'] = '127.0.0.1'
    opts['port'] = 5555
    pass

def getChannelNames(opts, vars):
    return { 'gaze' : 'x, y, timestamp' }


def initChannel(name, channel, types, opts, vars):
    # to sync, launch the c#
    if name == 'gaze':
        channel.dim = 3
        channel.type = types.FLOAT
        channel.sr = 50
    else:
        print('unkown channel name')


def connect(opts, vars):
    # print('calling c# program......')
    # subprocess.Popen([PATH_TO_C_EXECUTABLE])
    # print('c# program has been called....')
    
    # time.sleep(50)

    HOST = "127.0.0.1"
    PORT = 5555

    # global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    vars['socket'] = s
    print('Connected to a server...')

def read(name, sout, reset, board, opts, vars):
    s = vars['socket']

    if name == "gaze":
        data = s.recv(45).decode('ascii')
        # print('data: ', data)

        for s in range(sout.num):
            d = data.split(',')
            for n in range(len(d)):
                # print(float(d[n]))
                sout[s, n] = float(d[n])

def disconnect(opts, vars):
    pass