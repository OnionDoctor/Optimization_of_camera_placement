# ======================================================================================================================
# author:   Xincong YANG
# date:     12 Oct. 2017
# email:    xincong.yang@outlook.com
# name:     Setter_visible
# ======================================================================================================================
from shapely.geometry import Point
import numpy as np
import os
from cvxopt import matrix
from cvxopt.glpk import ilp

from Setter_sensors import Sensor, Sensors
from Setter_visible import visible, clip, discrete
from Setter_plot import plot_visible, plot_background, plot_sensors, plot_points

class model(object):
    def __init__(self, obj_polygon, sensor_types, grid_size=0.5,
                 sensor_buffer=-0.1, max_dist=1.0, min_dist=0.2, alpha_num=8,
                 cover_times=1):
        self.layout = obj_polygon
        self.grid_size = grid_size
        self.cover_times = cover_times

        sensors = Sensors()
        # if configs exist, load directly.
        if os.path.exists('data/configs.csv'):
            sensors.load_configs()
        # or generate all candidate sensors
        else:
            layout_buffer = obj_polygon.buffer(sensor_buffer, 0)
            candidate_locations = clip(layout_buffer, max_dist, min_dist)
            sensors.generate_configs(sensor_types, candidate_locations, alpha_num)
            sensors.save_configs()

        self.sensors = sensors

        self.initialize()

    def initialize(self):
        # discrete layout
        self.layout_points = discrete(self.layout, self.grid_size)
        self.layout_points_mask = np.zeros(len(self.layout_points), np.bool)
        print("==========>>> Discrete layout into {} points ... <<<==========".format(len(self.layout_points)))

        if os.path.exists('data/A.npy') and os.path.exists('data/b.npy') and os.path.exists('data/c.npy'):
            print("==========>>> Load cover A, b, c directly ... <<<==========")
            self.A = np.load('data/A.npy')
            self.b = np.load('data/b.npy')
            self.c = np.load('data/c.npy')
        else:
            print("==========>>> Compute and save cover A, b, c ... <<<==========")
            A = self._cover_A()
            b = self._cover_b(cover_times=self.cover_times)
            c = self._cover_c()
            print("==========>>> Sensor candidates: %d <<<==========" % self.sensors.get_num)
            mask = A.sum(axis=1) > 0
            self.A = A[mask].astype(np.int8)
            self.b = b
            self.c = c[mask]
            np.save('data/A.npy', self.A)
            np.save('data/b.npy', self.b)
            np.save('data/c.npy', self.c)
            self.sensors.update(mask)
            self.sensors.save_configs()
            print("==========>>> Sensor candidates has been decreased to: %d <<<==========" % self.sensors.get_num)

    def _cover_A(self):
        cover_A = []
        for sensor in self.sensors.get_sensors:
            visibile_region = visible(sensor, self.layout)
            if visibile_region == None:
                cover_a = np.zeros(len(self.layout_points))
            else:
                cover_a = [visibile_region.contains(Point(point)) for point in self.layout_points]

            cover_A.append(cover_a)
        return np.array(cover_A)

    def _cover_b(self, cover_times):
        num = len(self.layout_points)
        return np.ones(num) * cover_times

    def _cover_c(self):
        return self.sensors.get_costs

    def compute(self, mode='min', method='ilp', value=0):
        if mode == 'min':
            if method == 'ilp':
                x = min_solver_ilp(self.A, self.b, self.c)

        elif mode == 'max':
            if method == 'dp':
                x = max_solver_dp(self.A, self.b, self.c, value)

        mask = x
        self.sensors.update(mask)

        self.layout_points_mask = np.dot(self.A.T, x) >= 1

    def plot(self, ax, sensor_list=None):

        plot_background(ax, self.layout)

        xs, ys = self.sensors.get_locations

        if sensor_list == None:
            visible_regions = [visible(sensor, self.layout) for sensor in self.sensors.get_sensors]
        else:
            visible_regions = [visible(self.sensors.get_sensors[i], self.layout) for i in sensor_list]
            xs = [xs[i] for i in sensor_list]
            ys = [ys[i] for i in sensor_list]

        plot_visible(ax, visible_regions)
        plot_sensors(ax, xs, ys)

        plot_points(ax, self.layout_points, self.layout_points_mask)

    @property
    def get_coverage(self):
        total_n = len(self.layout_points)
        cover_n = np.sum(self.layout_points_mask)
        return cover_n / total_n

    @property
    def get_cost(self):
        return self.sensors.get_costs

# max problem: =========================================================================================================
# Maximize coverage
# obj. xA - b >= 0
# s.t. xc <= C
def max_solver_dp(A, b, c, C):
    m = c.shape[0]          # x dimension
    n = b.shape[0]          # s.t. dimension
    mat_obj = np.zeros((m, C, n), dtype=np.int)
    mat_x = np.zeros((m, C, m), dtype=np.bool)
    for i in range(m):
        for j in range(C):
            # when the cost of ith is less than total cost
            if c[i] <= j:
                forward_obj = mat_obj[i - 1, int(j - c[i])] + A[i]
                backward_obj = mat_obj[i - 1, j]
                forward_sum = (forward_obj - b >= 0).sum()
                backward_sum = (backward_obj - b >= 0).sum()
                if forward_sum >= backward_sum:
                    mat_obj[i, j] = forward_obj

                    mat_x[i, j] = mat_x[i - 1, int(j - c[i])]
                    mat_x[i, j, i] = True
                else:
                    mat_obj[i, j] = backward_obj

                    mat_x[i, j] = mat_x[i - 1, j]
    return mat_x[-1, -1]

# min problem: =========================================================================================================
# Minimize cost
# obj. xc
# s.t. Ax >= b
def min_solver_ilp(A, b, c):
    # ilp form:
    # obj. min c'x
    # s.t. Gx <= h
    G = matrix((-1) * A.T.astype(np.float))
    h = matrix((-1) * b.astype(np.float))
    c = matrix(c.astype(np.float))
    x_num = len(c)
    (status, x) = ilp(c, G, h, B=set(range(x_num)))
    return np.array(x)

# Multi-object problem: ================================================================================================
# obj. max xA - b >= 0
#      min xc







