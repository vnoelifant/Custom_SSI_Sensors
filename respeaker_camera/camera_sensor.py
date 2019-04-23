from imagetake_5 import Camera

import time
import threading


def getOptions(opts, vars):
        opts['sr'] = 50.0
        #opts['channels'] = 8


def getChannelNames(opts, vars):

    return {'video': 'images of the videos stream'}


def initChannel(name, channel, types, opts, vars):
    if name == 'video':
        #channel.dim = 1
        channel.type = 4
        channel.sr = opts['sr']
    else:
        print('unknown channel name')


def connect(opts, vars):
    vars['cam'] = Camera()
    pass


def read(name, sout, reset, board, opts, vars):
    #time.sleep(opts['sr']/4)
    #print("reading {0}".format(name))
    if name == 'video':
        image = vars['cam'].process_camera_data()
        print(image)
        print(type(image))
        sout = image
        #print(sout)
    else:
        print('unknown channel name')


def disconnect(opts, vars):
    pass

