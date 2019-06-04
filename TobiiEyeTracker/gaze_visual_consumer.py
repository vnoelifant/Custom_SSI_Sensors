import matplotlib.pyplot as plt
import numpy as np
import math

# TODO: See if you need to adjust the figure size
fig = ""
ax = []
hits_array = np.empty((1920, 1080))
flag = True
monitor_size = [1920, 1080]

def getOptions(opts, vars):
    opts['monitor_size'] = [1920, 1080]

def consume_enter(sins, board, opts, vars):
    global hits_array
    hits_array = np.zeros((math.ceil(opts["monitor_size"][0]/10), math.ceil(opts["monitor_size"][1]/10)))
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
        # plt.xlim(0, monitor_size[0] + 2)
        # plt.ylim(0, monitor_size[1] + 2)
        ax = fig.add_subplot(111)
        ax.set_title('Gaze Color Map')
        plt.draw()
        flag = False


    x_coord = int(data[0])
    y_coord = int(data[1])

    print("x_coord: ", x_coord)
    print("y_coord: ", y_coord)

    hits_array[int(x_coord/10), int(y_coord/10)] += 100
    plt.imshow(hits_array)
    plt.pause(0.000000001)