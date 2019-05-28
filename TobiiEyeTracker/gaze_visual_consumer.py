import matplotlib.pyplot as plt
import numpy as np
import math

# TODO: See if you need to adjust the figure size
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_title('Gaze Color Map')
hits_array = np.empty((768, 1024))


def getOptions(opts, vars):
    opts['monitor_size'] = [768, 1024]

def consume_enter(sins, board, opts, vars):
    print("Setting up hits array...")
    global hits_array
    hits_array = np.zeros((math.ceil(opts["monitor_size"][0]/10), math.ceil(opts["monitor_size"][1]/10)))
    print("Finished setting up hits array...")

def consume(info, sins, board, opts, vars):
    print("Consume called...")
    if sins[0][1] != 0:
        main(sins[0])


def consume_flush(sins, board, opts, vars):
    pass


def main(data):
    global fig
    global ax
    global hits_array


    x_coord = int(data[0])
    y_coord = int(data[1])

    hits_array[int(x_coord/10), int(y_coord/10)] += 1
    plt.imshow(hits_array)
    plt.pause(2)