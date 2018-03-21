# ======================================================================================================================
# author:   Xincong YANG
# date:     12 Oct. 2017
# email:    xincong.yang@outlook.com
# name:     Setter_sample
# ======================================================================================================================
import numpy as np
from shapely.geometry import Polygon

sensor_tpye1 = {'type': 'B1', 'min_rho': 0, 'max_rho': 11.7, 'theta': 81.2 * np.pi / 180, 'isOmni': 0, 'isThrough': 0, 'cost': 40}
sensor_tpye2 = {'type': 'B2', 'min_rho': 0, 'max_rho': 15.0, 'theta': 67.4 * np.pi / 180, 'isOmni': 0, 'isThrough': 0, 'cost': 45}
sensor_tpye3 = {'type': 'B3', 'min_rho': 0, 'max_rho': 25.0, 'theta': 43.6 * np.pi / 180, 'isOmni': 0, 'isThrough': 0, 'cost': 50}
sensor_tpye4 = {'type': 'B4', 'min_rho': 0, 'max_rho': 33.3, 'theta': 33.4 * np.pi / 180, 'isOmni': 0, 'isThrough': 0, 'cost': 55}
sensor_tpye5 = {'type': 'B5', 'min_rho': 0, 'max_rho': 50.0, 'theta': 22.6 * np.pi / 180, 'isOmni': 0, 'isThrough': 0, 'cost': 60}
sensor_tpye6 = {'type': 'B6', 'min_rho': 0, 'max_rho': 66.7, 'theta': 17.1 * np.pi / 180, 'isOmni': 0, 'isThrough': 0, 'cost': 65}
sensor_tpye7 = {'type': 'O1', 'min_rho': 0, 'max_rho': 8.0, 'theta': 2 * np.pi, 'isOmni': 1, 'isThrough': 0, 'cost': 38}
sensor_tpye8 = {'type': 'O2', 'min_rho': 0, 'max_rho': 10.0, 'theta': 2 * np.pi, 'isOmni': 1, 'isThrough': 0, 'cost': 42}

SENSOR_TYPES = [sensor_tpye1, sensor_tpye2, sensor_tpye3, sensor_tpye4, sensor_tpye5, sensor_tpye6, sensor_tpye7, sensor_tpye8]

ext = [(11.84, 33.44), (16.50, 30.75), (20.92, 30.25), (88.42, 5.69), (90.52, 6.19), (92.34, 8.05), (102.84, 53.01),
       (98.20, 68.88), (85.30, 83.47), (57.31, 99.56), (33.52, 99.56), (26.98, 95.39), (11.84, 38.00)]
int1 = [(56.41, 17.68), (69.31, 12.97), (69.67, 13.94), (89.41, 17.51), (86.91, 31.39), (54.97, 25.48)][::-1]
int2 = [(60.54, 29.17), (65.24, 30.01), (64.17, 36.01), (69.48, 36.95), (68.61, 41.84), (53.01, 39.06),
        (53.87, 34.39), (59.43, 35.38)][::-1]
int3 = [(47.47, 47.45), (67.04, 48.19), (67.04, 53.60), (47.47, 52.97)][::-1]
int4 = [(30.23, 60.66), (34.11, 59.68), (36.50, 69.15), (32.62, 70.13)][::-1]
int5 = [(18.12, 58.41), (24.00, 56.93), (31.40, 86.26), (25.53, 87.74)][::-1]

OBJ_POLYGON = Polygon(ext, [int1, int2, int3, int4, int5])

if __name__ == '__main__':
    pass
