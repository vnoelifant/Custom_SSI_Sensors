#!/usr/bin/env python

from time import sleep
import socket
import subprocess
import sys


PATH_TO_C_EXECUTABLE = 'C:\\Users\\TIILTMAINPC\\Documents\\Github\\Custom_SSI_Sensors\\TobiiEyeTracker\\TobiiReceiver\\TobiiReceiver\\bin\\Debug\\TobiiReceiver.exe'



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
        channel.sr = 90
    else:
        print('unkown channel name')


def connect(opts, vars):
    print('calling c# program......')
    subprocess.Popen([PATH_TO_C_EXECUTABLE])
    print('c# program has been called....')
    
    sleep(1)

    HOST = "127.0.0.1"
    PORT = 5555

    # global s
    DQ = []
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # s.setblocking(0)
    s.connect((HOST, PORT))
    vars['socket'] = s
    vars['DQ'] = DQ
    vars['pos'] = 0
    print('Connected to a server...')

def read(name, sout, reset, board, opts, vars):
    s = vars['socket']
    DQ = vars['DQ']
    all_data = s.recv(int(405)).decode('ascii')
    start=0
    finish=45
    if name == "gaze" and not reset:
        for n in range(sout.num):
            ar_to_write = data = all_data[start:finish].split(',')[:-1]
            start+=45
            finish+=45
            if len(ar_to_write) == 3:# 
                for d in range(sout.dim):
                    sout[n, d] = float(ar_to_write[d])
    vars['socket'] = s

def disconnect(opts, vars):
    pass