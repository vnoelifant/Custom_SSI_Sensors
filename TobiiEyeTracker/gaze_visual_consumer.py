import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import math

# TODO: See if you need to adjust the figure size
fig = ""
ax = []
hits_array = np.empty((1080, 1920))
flag = True
monitor_size = [1080, 1920]

def getOptions(opts, vars):
    opts['monitor_size'] = [1080, 1920]

def consume_enter(sins, board, opts, vars):
    global hits_array
    hits_array = np.zeros((math.ceil(opts["monitor_size"][0]/100), math.ceil(opts["monitor_size"][1]/100)))
    monitor_size[0] = opts["monitor_size"][0]
    monitor_size[1] = opts["monitor_size"][1]
    print(hits_array.shape)

def consume(info, sins, board, opts, vars):
    if sins[0][1] != 0:
        main(sins[0])

def consume_flush(sins, board, opts, vars):
    pass

def main(data):
    global fig
    global ax
    global hits_array
    global flag
    if flag:
        global monitor_size
        plt.ion()
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_title('Gaze Color Map')
        plt.draw()
        flag = False


    x_coord = int(data[0])
    y_coord = int(data[1])
    hits_array[int(y_coord/100), int(x_coord/100)] += 100
    plt.imshow(hits_array)
    plt.pause(0.000000001)