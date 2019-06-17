import os
import sys
sys.path.append(os.environ.get('PYTHONPATH', ''))



def getOptions(opts, vars):
    
    pass

def getChannelNames(opts, vars):
    
    return { 'audio' : 'Audio','camera' : 'Camera' }


def initChannel(name, channel, types, opts, vars):

    if name == 'audio':
        channel.dim =  1
        channel.type = types.FLOAT
        channel.sr = 44100

    elif name == 'camera':
        channel.dim =  1
        channel.type = types.FLOAT
        channel.sr = 44100
    else:
        print('unkown channel name')


def connect(opts, vars):
    pass

        
def read(name, sout, reset, board, opts, vars): 
    time = sout.time
    delta = 1.0 / sout.sr   

    vars['audio'] = 0
    audio = vars['audio']
    vars['camera'] = 0
    camera = vars['camera']    
    print("audio:",audio)
    print("camera:",camera)

    if name == 'audio':
        for n in range(sout.num):
            for d in range(sout.dim):
                sout[n,d] = audio
            time += delta

    elif name == 'camera':
        for n in range(sout.num):
            for d in range(sout.dim):
                sout[n,d] = audio
            time += delta

    else:
        print('unkown channel name')

def disconnect(opts, vars):
    pass
