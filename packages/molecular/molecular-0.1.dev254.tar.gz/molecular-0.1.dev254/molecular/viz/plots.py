
from molecular.geometry import angle

import matplotlib.pyplot as plt
from matplotlib import patches
import numpy as np


def plot_vector_angle(u, v, color=(0, 0.5, 1)):
    plt.xkcd()
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot([0, 0], [0, 0])
    ax.arrow(0, 0, u[0], u[1], linewidth=2., head_width=0.05, head_length=0.03, fc=color, ec=color, zorder=2)
    ax.arrow(0, 0, v[0], v[1], linewidth=2., head_width=0.05, head_length=0.03, fc=color, ec=color, zorder=2)
    angles = 360. - np.array([angle(u, [1., 0.]), angle(v, [1., 0.])]) * 180. / np.pi
    angles[angles >= 360] -= 360
    angles_min = np.min(angles)
    angles_max = np.max(angles)
    if angles_max - angles_min > (360 - angles_max) + angles_min:
        theta1 = np.max(angles)
        theta2 = theta1 + (360 - angles_max) + angles_min
    else:
        theta1 = np.min(angles)
        theta2 = theta1 + angles_max - angles_min
    e1 = patches.Arc([0., 0.], 1., 1., angle=0., theta1=theta1, theta2=theta2, color=color, zorder=2)
    ax.add_patch(e1)
    ax.spines['left'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['bottom'].set_position('zero')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_xlim([-1.1, 1.1])
    ax.set_ylim([-1.1, 1.1])
    ax.set_aspect('equal')
    plt.show()


def heatmap(x, y):
    # plt.plot()
    # plt.imshow(, cmap='rainbow')
    # plt.show()
    pass
