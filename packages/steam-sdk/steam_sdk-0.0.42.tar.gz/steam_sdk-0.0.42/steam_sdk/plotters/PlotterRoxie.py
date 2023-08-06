import copy
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as lines
import matplotlib.patches as patches
from mpl_toolkits.axes_grid1 import make_axes_locatable

from steam_sdk.data import DataRoxieParser as pd
from steam_sdk.utils.misc import displayWaitAndClose


def arcCenterFromThreePoints(a, b, c):
    ab = [a.x - b.x, a.y - b.y]
    ac = [a.x - c.x, a.y - c.y]
    sac = [a.x * a.x - c.x * c.x, a.y * a.y - c.y * c.y]
    sba = [b.x * b.x - a.x * a.x, b.y * b.y - a.y * a.y]
    yy = (sac[0] * ab[0] + sac[1] * ab[0] + sba[0] * ac[0] + sba[1] * ac[0]) / \
         (2 * ((c.y - a.y) * ab[0] - (b.y - a.y) * ac[0]))
    xx = (sac[0] * ab[1] + sac[1] * ab[1] + sba[0] * ac[1] + sba[1] * ac[1]) / \
         (2 * ((c.x - a.x) * ab[1] - (b.x - a.x) * ac[1]))
    return [-xx, -yy]


def plotIronGeometry(iron, selectedFont):
    plt.figure(figsize=(7.5, 7.5))
    ax = plt.axes()

    max_x = 0
    max_y = 0

    for point_name, point in iron.key_points.items():
        max_x = max(point.x, max_x)
        max_y = max(point.y, max_y)

    for line_name, line in iron.hyper_lines.items():
        if line.type == 'line':
            ax.add_line(lines.Line2D([iron.key_points[line.kp1].x, iron.key_points[line.kp2].x],
                                     [iron.key_points[line.kp1].y, iron.key_points[line.kp2].y],
                                     color='black', linewidth=1))

        elif line.type == 'arc':
            pt1 = iron.key_points[line.kp1]
            pt2 = iron.key_points[line.kp2]
            center = arcCenterFromThreePoints(pt1, iron.key_points[line.kp3], pt2)
            radius = (np.sqrt(np.square(pt1.x - center[0]) + np.square(pt1.y - center[1])) +
                      np.sqrt(np.square(pt2.x - center[0]) + np.square(pt2.y - center[1]))) / 2
            if pt1.x < pt2.x and pt1.x < center[0] and pt1.y < pt2.y and pt1.y < center[1]:
                th1 = - np.arctan2(pt1.y - center[1], pt1.x - center[0]) * 180 / np.pi
            else:
                th1 = np.arctan2(pt1.y - center[1], pt1.x - center[0]) * 180 / np.pi
            th2 = np.arctan2(pt2.y - center[1], pt2.x - center[0]) * 180 / np.pi
            ax.add_patch(patches.Arc((center[0], center[1]), width=2 * radius, height=2 * radius, angle=0,
                                     theta1=min(th1, th2), theta2=max(th1, th2), color='blue', linewidth=1))

        # elif line.type == 'ellipticArc':
        #     pt1 = iron.key_points[line.kp1]
        #     pt2 = iron.key_points[line.kp2]
        #     r1 = (pt1.x - pt2.x) / (2 * line.arg1)
        #     r2 = (pt1.y - pt2.y) / (2 * line.arg2)
        #     a1 = np.arctan2(- r1 / r2)  # (t1 + t2) / 2
        #     a2 = np.arcsin(np.sqrt(r1**2 + r2**2))  # (t1 - t2) / 2
        #     center = [pt1.x - line.arg1 * np.cos(a1 + a2), pt1.y - line.arg2 * np.sin(a1 + a2)]
        #
        #     if pt1.x < pt2.x and pt1.x < center[0] and pt1.y < pt2.y and pt1.y < center[1]:
        #         th1 = - np.arctan2(pt1.y - center[1], pt1.x - center[0]) * 180 / np.pi
        #     else:
        #         th1 = np.arctan2(pt1.y - center[1], pt1.x - center[0]) * 180 / np.pi
        #     th2 = np.arctan2(pt2.y - center[1], pt2.x - center[0]) * 180 / np.pi
        #     ax.add_patch(patches.Arc((center[0], center[1]), width=2 * line.arg1, height=2 * line.arg2, angle=0,
        #                              theta1=min(th1, th2), theta2=max(th1, th2), color='purple', linewidth=1))

        elif line.type == 'circle':
            pt1 = iron.key_points[line.kp1]
            pt2 = iron.key_points[line.kp2]
            center = [(pt1.x + pt2.x) / 2, (pt1.y + pt2.y) / 2]
            radius = (np.sqrt(np.square(pt1.x - center[0]) + np.square(pt1.y - center[1])) +
                      np.sqrt(np.square(pt2.x - center[0]) + np.square(pt2.y - center[1]))) / 2
            ax.add_patch(patches.Circle((center[0], center[1]),
                                        radius=radius, fill=False, edgecolor='green', linewidth=1))

    ax.set_xlim(0, 1.1 * max_x)
    ax.set_ylim(0, max_y + 0.1 * max_x)
    plt.xlabel('x [m]', **selectedFont)
    plt.ylabel('y [m]', **selectedFont)
    plt.title('Iron Yoke', **selectedFont)
    plt.set_cmap('jet')
    plt.rcParams.update({'font.size': 12})


# def plotCoilGeometry(roxie_data, ax):
#     max_x = 0
#     max_y = 0
#     for coil_nr, coil in roxie_data.coil.coils.items():
#         for pole_nr, pole in coil.poles.items():
#             for layer_nr, layer in pole.layers.items():
#                 for winding_key, winding in layer.windings.items():
#                     for block_key, block in winding.blocks.items():
#                         for halfTurn_nr, halfTurn in block.half_turns.items():
#                             iL = halfTurn.corners.insulated.iL
#                             iR = halfTurn.corners.insulated.iR
#                             oL = halfTurn.corners.insulated.oL
#                             oR = halfTurn.corners.insulated.oR
#                             max_x = max(oL.x, oR.x, max_x)
#                             max_y = max(oL.y, oR.y, max_y)
#
#                             ax.add_line(lines.Line2D([iL.x, iR.x], [iL.y, iR.y], color='red'))
#                             ax.add_line(lines.Line2D([oL.x, oR.x], [oL.y, oR.y], color='red'))
#                             ax.add_line(lines.Line2D([oR.x, iR.x], [oR.y, iR.y], color='red'))
#                             ax.add_line(lines.Line2D([iL.x, oL.x], [iL.y, oL.y], color='red'))
#     # cc = roxie_data.coil.coils[1].bore_center
#     # ax.set_xlim((len(roxie_data.coil.coils) == 1) * 2 * cc.x - (1.1 * (max_x - cc.x) + cc.x),
#     #             1.1 * (max_x - cc.x) + cc.x)
#     # ax.set_ylim((len(roxie_data.coil.coils) == 1) * 2 * cc.y - (max_y + 0.1 * (max_x - cc.x)),
#     #             max_y + 0.1 * (max_x - cc.x))


# Plot conductors and their numbers
def plotEdges(xPos, yPos, xBarePos, yBarePos, iPos, selectedFont):
    plt.figure(figsize=(10, 10))
    # Plot edges
    for c, (cXPos, cYPos) in enumerate(zip(xPos, yPos)):
        pt1, pt2, pt3, pt4 = (cXPos[0], cYPos[0]), (cXPos[1], cYPos[1]), (cXPos[2], cYPos[2]), (cXPos[3], cYPos[3])
        if iPos[c] > 0:
            line = plt.Polygon([pt1, pt2, pt3, pt4], closed=True, fill=True, facecolor='r', edgecolor='k', alpha=.25)
        else:
            line = plt.Polygon([pt1, pt2, pt3, pt4], closed=True, fill=True, facecolor='b', edgecolor='k', alpha=.25)
        plt.gca().add_line(line)

        # Plot conductor numbers
        x_ave_cond, y_ave_cond = sum(cXPos) / len(cXPos), sum(cYPos) / len(cYPos)
        plt.text(x_ave_cond, y_ave_cond, '{}'.format(c + 1))

    # Plot edges of bare conductors
    for c, (cXBarePos, cYBarePos) in enumerate(zip(xBarePos, yBarePos)):
        pt1, pt2, pt3, pt4 = (cXBarePos[0], cYBarePos[0]), (cXBarePos[1], cYBarePos[1]), \
                             (cXBarePos[2], cYBarePos[2]), (cXBarePos[3], cYBarePos[3])
        if iPos[c] > 0:
            line = plt.Polygon([pt1, pt2, pt3, pt4], closed=True, fill=False, facecolor='r', edgecolor='k', alpha=.25)
        else:
            line = plt.Polygon([pt1, pt2, pt3, pt4], closed=True, fill=False, facecolor='b', edgecolor='k', alpha=.25)
        plt.gca().add_line(line)

    plt.xlabel('x [m]', **selectedFont)
    plt.ylabel('y [m]', **selectedFont)
    plt.title('Conductors and their numbers', **selectedFont)
    plt.set_cmap('jet')
    plt.rcParams.update({'font.size': 12})
    plt.axis('equal')
    plt.grid()



def plot_all(roxie_data: pd.APIdata):
    """
        Plot all default plots
    """
    selectedFont = {'fontname': 'DejaVu Sans', 'size': 14}

    if roxie_data.iron:
        plotIronGeometry(roxie_data.iron, selectedFont)
    # plotCoilGeometry(roxie_data, ax)

    xPos = []
    yPos = []
    xBarePos = []
    yBarePos = []
    iPos = []
    for coil_nr, coil in roxie_data.coil.coils.items():
        for pole_nr, pole in coil.poles.items():
            for layer_nr, layer in pole.layers.items():
                for winding_key, winding in layer.windings.items():
                    for block_key, block in winding.blocks.items():
                        for halfTurn_nr, halfTurn in block.half_turns.items():
                            insu = halfTurn.corners.insulated
                            bare = halfTurn.corners.bare

                            xPos.append([insu.iL.x, insu.oL.x, insu.oR.x, insu.iR.x])
                            yPos.append([insu.iL.y, insu.oL.y, insu.oR.y, insu.iR.y])
                            xBarePos.append([bare.iL.x, bare.oL.x, bare.oR.x, bare.iR.x])
                            yBarePos.append([bare.iL.y, bare.oL.y, bare.oR.y, bare.iR.y])
                            iPos.append(block.current_sign)
    plotEdges(xPos, yPos, xBarePos, yBarePos, iPos, selectedFont)

    displayWaitAndClose(waitTimeBeforeMessage=.1, waitTimeAfterMessage=10)
