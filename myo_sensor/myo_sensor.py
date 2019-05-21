import myo
from myo_helpers import main
from collections import deque
import time
import threading


def getOptions(opts, vars):
    opts['sr'] = 30

    myo.init(sdk_path='./myo_sensor/myo_helpers/myo-sdk-win-0.9.0')

    vars['hub'] = myo.Hub()
    vars['listener'] = main.MyoListener()


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
    vars['hub'].run(handler=vars['listener'].on_event, duration_ms=10)
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
        for i in range(9):
            sout[0, i] = emg.popleft()
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
        for i in range(11):
            sout[0, i] = orientation.popleft()
            #print(sout[0,i])
        #print(sout)
    else:
        print('unknown channel name')


def disconnect(opts, vars):
    vars['hub'].stop()

