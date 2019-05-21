import myo
from myo_helpers import main
from collections import deque
import time
import threading


def getOptions(opts, vars):
    opts['sr'] = 10

    myo.init(sdk_path='myo_helpers/myo-sdk-win-0.9.0')

    vars['hub'] = myo.Hub()
    vars['listener'] = main.MyoListener()
    vars["time"] = -1.0


def getChannelNames(opts, vars):

    return {'emg': 'the emg data',
            'orientation': 'the orientation data'}


def initChannel(name, channel, types, opts, vars):
    if name == 'emg':
        channel.dim = 9
        channel.type = types.FLOAT
        channel.sr = opts['sr']
    elif name == 'orientation':
        channel.dim = 11
        channel.type = types.FLOAT
        channel.sr = opts['sr']
    else:
        print('unknown channel name')


def connect(opts, vars):
    pass


def read(name, sout, reset, board, opts, vars):
    if reset == 1:
        return
    if sout.time != vars["time"]:
        vars["time"] = sout.time
        vars['hub'].run(handler=vars['listener'].on_event, duration_ms=90)
    #time.sleep(opts['sr']/4)
    #print("reading {0}".format(name))
    if name == 'emg':
        emg = vars['listener'].get_emgVals()
        #print(len(emg))
        #print("EMG DATA:")
        if len(emg) != 9:
            print(emg)
            emgVals = [0, 0, 0, 0, 0, 0, 0, 0, 0]
            emg = deque(emgVals)
        timestamp = emg.popleft()
        sout[0, 0] = sout.time
        for i in range(8):
            sout[0, i+1] = emg.popleft()
            #print(sout[0,i])
        #print(sout)
    elif name == 'orientation':
        orientation = vars['listener'].get_orientation()
        #print("ORIENTATION DATA: ")
        #print(len(orientation))
        if len(orientation) != 11:
            print(orientation)
            ori = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            orientation = deque(ori)
        timestamp = orientation.popleft()
        sout[0, 0] = sout.time
        for i in range(10):
            sout[0, i+1] = orientation.popleft()
            #print(sout[0,i])
        #print(sout)
    else:
        print('unknown channel name')


def disconnect(opts, vars):
    vars['hub'].stop()

