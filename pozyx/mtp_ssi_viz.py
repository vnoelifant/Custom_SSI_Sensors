import matplotlib.pyplot as plt
import numpy as np
import argparse
import os

# court size: 15843mm (y) x 27127mm (x)

# TODO find better way to do colors
colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k', 'w', 'r', 'g', 'b', 'c', 'm', 'y', 'k', 'w']
xbounds = [-1000, 8500]
ybounds = [-1000, 6500]
flag = True

fig = ""
ids = {}
trail = 5
ax_list = []
print("GLOBALS INITIALIZED")


def getOptions(opts, vars):
    pass


def getEventAddress(opts, vars):
    pass


def consume_enter(sins, board, opts, vars):
    print("HELLO CONSUME_ENTER JUST RAN!!!!!!")


def consume(info, sins, board, opts, vars): 
    #setup()
    # print("------------------------------ ", list(sins[0]) )
    # print("Flag: ", flag)
    # flag += 1
    if sins[0][1] != 0:
        main(sins[0])


def consume_flush(sins, board, opts, vars):
    pass


# plt.ion()
# gl_fig = plt.figure()
# ids = {}
# trail = 15
# ax_list = []
# plt.xlim(xbounds[0], xbounds[1])
# plt.ylim(ybounds[0], ybounds[1])
# plt.draw()


def setup():
    pass


def main(dataset):
    global flag
    global fig
    global ids
    global trail
    global ax_list
    # print(flag)

    if flag:
        plt.ion()
        fig = plt.figure()
        plt.xlim(xbounds[0], xbounds[1])
        plt.ylim(ybounds[0], ybounds[1])
        plt.draw()
        flag = False

    print('.')

    # grab tag id, xval, and yval

    lineid = hex(int(float(dataset[0])))
    linex = float(dataset[1])
    liney = float(dataset[2])
    placement = 0

    # if its a new tag add it to the list
    if lineid not in list(ids.keys()):
        ids[lineid] = {
            'x': [0] * trail,
            'y': [0] * trail
        }
        ax_list.append(plt.axes())

    placement = list(ids.keys()).index(lineid)

    ids[lineid]['x'].append(np.array(linex))
    ids[lineid]['x'].pop(0)

    ids[lineid]['y'].append(np.array(liney))
    ids[lineid]['y'].pop(0)

    ax_list[placement].clear()

    plt.xlim(xbounds[0], xbounds[1])
    plt.ylim(ybounds[0], ybounds[1])

    for ilineid in ids.keys():
        ax_list[list(ids.keys()).index(ilineid)].scatter(
            ids[ilineid]['x'],
            ids[ilineid]['y'],
            color=colors[list(ids.keys()).index(ilineid)],
            label=ilineid)
        ax_list[list(ids.keys()).index(ilineid)].legend(loc='best')

    fig.canvas.draw_idle()
    plt.pause(0.000000001)

    # plt.waitforbuttonpress()
