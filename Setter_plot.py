# ======================================================================================================================
# author:   Xincong YANG
# date:     12 Oct. 2017
# email:    xincong.yang@outlook.com
# name:     Setter_plot
# ======================================================================================================================
from descartes.patch import PolygonPatch
import numpy as np

# color identification
BLUE = '#58D2E8'
GREEN = '#61FF69'
RED = '#F2B6B6'
YELLOW = '#E8ED51'
BLACK = '#1A1A1A'

DARK_90 = '#1a1a1a'
DARK_75 = '#404040'
DARK_50 = '#808080'
DARK_25 = '#bfbfbf'

def plot_visible(ax, visible_regions):
    for visibile_region in visible_regions:
        visible_patch =  PolygonPatch(visibile_region,
                                      facecolor=DARK_50, edgecolor=DARK_90, alpha=0.6, zorder=2)
        ax.add_patch(visible_patch)

def plot_background(ax, obj_polygon):
    background_patch = PolygonPatch(obj_polygon,
                                    facecolor=DARK_25, edgecolor=DARK_90, alpha=0.4, zorder=2)
    ax.add_patch(background_patch)

def plot_sensors(ax, x, y):
    ax.scatter(x, y, color=DARK_90, marker='o')

def plot_points(ax, points, cover_mask):
    xs, ys = points.T
    ax.scatter(np.ma.masked_array(xs, cover_mask),
               np.ma.masked_array(ys, cover_mask), color=DARK_75, marker='+')

    ax.scatter(np.ma.masked_array(xs, ~cover_mask),
               np.ma.masked_array(ys, ~cover_mask), color=DARK_25, marker='+')