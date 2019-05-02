import matplotlib.pyplot as plt
import numpy as np
import argparse
import os

# court size: 15843mm (y) x 27127mm (x)

# TODO find better way to do colors
colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k', 'w', 'r', 'g', 'b', 'c', 'm', 'y', 'k', 'w']
xbounds = [-10000, 10000]
ybounds = [-10000, 10000]


# try 13, 20-22
def main(filename='./data/position13.stream~', slow_flag=False):
    plt.ion()
    ax_list = []
    fig = plt.figure()

    assert os.path.isfile(args.file)

    with open(filename, 'r') as f:
        ids = {}
        trail = 15

        # Fleetwood Gym
        #plt.xlim(0, 28000)
        #plt.ylim(-3000, 17000)

        plt.xlim(xbounds[0], xbounds[1])
        plt.ylim(ybounds[0], ybounds[1])
        plt.draw()

        # for i in range(100):
        for fline in f:
            print('.')

            # grab tag id, xval, and yval
            line = fline.split(" ")
            lineid = hex(int(float(line[0])))
            linex = float(line[1])
            liney = float(line[2])
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
            plt.pause(0.0000001)
            if slow_flag:
                plt.pause(1)

        print('Done')
        plt.waitforbuttonpress()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Stream Visualizer.')
    parser.add_argument('-f', '--file', help='stream file to read from')
    parser.add_argument('-s', '--slow', action='store_true', help='update slowly')
    args = parser.parse_args()
    main(args.file, args.slow)
