import myo
from myo_helpers import main
import threading


def getOptions(opts, vars):
    opts['sr'] = 1.0
    #opts['dim'] = 1


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


def hub_thread(vars):
    while vars['hub'].run(vars['listener'].on_event, 500) and vars['done'] == False:
        pass


def connect(opts, vars):
    myo.init(sdk_path='./myo_helpers/myo-sdk-win-0.9.0/')
    vars['hub'] = myo.Hub()
    vars['done'] = False
    vars['listener'] = main.MyoListener()

    threading.Thread(target=hub_thread, args=[vars]).start()


def read(name, sout, reset, board, opts, vars):
    if name == 'emg':
        emg = vars['listener'].get_emgVals()
        if len(emg) != 9:
            return
        for i in range(0, 8):
            sout[0, i] = emg.popleft()
    elif name == 'orientation':
        orientation = vars['listener'].get_orientation()
        if len(orientation) != 11:
            return
        for i in range(0, 10):
            sout[0, i] = orientation.popleft()
    else:
        print('unkown channel name')


def disconnect(opts, vars):
    vars['done'] = True
