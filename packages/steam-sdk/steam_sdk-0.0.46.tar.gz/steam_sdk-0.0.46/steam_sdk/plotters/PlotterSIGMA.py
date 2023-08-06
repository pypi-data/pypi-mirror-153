import matplotlib.lines as lines
import matplotlib.patches as patches
import numpy as np

def plot_multiple_areas(ax, areas, color=None):
    for area in areas:
        if color:
            plot_area(ax, area, color)
        else:
            plot_area(ax, area)

def plot_area(ax, area, color=None):
    if not color:
        color = 'black'
    points = []
    hls = area.getHyperLines()
    for hl in hls:
        last_dot_index = hl.toString().rfind('.')
        at_index = hl.toString().find('@')
        class_name = hl.toString()[last_dot_index + 1:at_index]
        if class_name == 'Line':
            points.append([hl.getKp1().getX(), hl.getKp1().getY()])
            points.append([hl.getKp2().getX(), hl.getKp2().getY()])
        elif class_name == 'Arc':
            start_angle = np.arctan2(hl.getKp1().getY() - hl.getKpc().getY(),
                                     hl.getKp1().getX() - hl.getKpc().getX()) * 180 / np.pi
            end_angle = start_angle + hl.getDTheta() * 180 / np.pi
            r = np.sqrt((hl.getKp1().getY() - hl.getKpc().getY()) ** 2 + (hl.getKp1().getX() - hl.getKpc().getX()) ** 2)
            ax.add_patch(patches.Arc([hl.getKpc().getX(), hl.getKpc().getY()], 2 * r, 2 * r, 0,
                                     min(start_angle, end_angle), max(start_angle, end_angle), color=color))
        elif class_name == 'Circumference':
            r = hl.getRadius()
            ax.add_patch(patches.Arc([hl.getCenter().getX(), hl.getCenter().getY()], 2 * r, 2 * r, 0, 0, 360))
        else:
            raise ValueError('Not supported Hyperline object!')

    ax.add_line(lines.Line2D([points[0][0], points[3][0]], [points[0][1], points[3][1]], color=color))
    ax.add_line(lines.Line2D([points[1][0], points[2][0]], [points[1][1], points[2][1]], color=color))