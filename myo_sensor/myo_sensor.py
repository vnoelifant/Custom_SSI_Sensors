import myo
from myo_helpers import main
import threading


def getOptions(opts, vars):
    opts['sr'] = 1.0

    myo.init(sdk_path='.\\myo_sensor\\myo_helpers\\myo-sdk-win-0.9.0')

    vars['hub'] = myo.Hub
    vars['listener'] = main.MyoListener()

    vars['hub'].run_in_background(vars['listener'].on_event, 500)


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
    if name == 'emg':
        emg = vars['listener'].get_emgVals()
        if len(emg) != 9:
            return
        for i in range(9):
            sout[0, i] = emg.popleft()
    elif name == 'orientation':
        orientation = vars['listener'].get_orientation()
        if len(orientation) != 11:
            return
        for i in range(11):
            sout[0, i] = orientation.popleft()
    else:
        print('unknown channel name')


def disconnect(opts, vars):
    vars['hub'].stop()

