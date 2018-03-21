# ======================================================================================================================
# author:   Xincong YANG
# date:     12 Oct. 2017
# email:    xincong.yang@outlook.com
# name:     Setter_sample
# ======================================================================================================================
import numpy as np
from shapely.geometry import Polygon

sensor_tpye1 = {'type': 'D_90', 'min_rho': 0, 'max_rho': 1.5, 'theta': 90 * np.pi / 180,
                'isOmni': 0, 'isThrough': 0, 'cost': 10}
sensor_tpye2 = {'type': 'D_60', 'min_rho': 0, 'max_rho': 2, 'theta': 60 * np.pi / 180,
                'isOmni': 0, 'isThrough': 0, 'cost': 20}
sensor_tpye3 = {'type': 'O_2', 'min_rho': 0, 'max_rho': 2, 'theta': np.pi * 2,
                'isOmni': 1, 'isThrough': 0, 'cost': 30}
sensor_tpye4 = {'type': 'T_3', 'min_rho': 0, 'max_rho': 2, 'theta': 60 * np.pi / 180,
                'isOmni': 0, 'isThrough': 1, 'cost': 40}

SENSOR_TYPES = [sensor_tpye1, sensor_tpye2, sensor_tpye3]

ext = [(0, 0), (8, 0), (8, 5), (0, 5)]
int1 = [(1, 1), (3, 1), (3, 2), (2, 2), (2, 3), (1, 3)][::-1]
int2 = [(3, 3), (4, 3), (4, 2), (5, 2), (5, 3), (6, 3), (6, 4), (3, 4)][::-1]
int3 = [(6, 1), (7, 1), (7, 2), (6, 2)][::-1]

OBJ_POLYGON = Polygon(ext, [int1, int2, int3])

