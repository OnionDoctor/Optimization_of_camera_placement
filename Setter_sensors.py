# ======================================================================================================================
# author:   Xincong YANG
# date:     12 Oct. 2017
# email:    xincong.yang@outlook.com
# name:     Setter_sensors
# ======================================================================================================================

from __future__ import division, print_function, absolute_import
import numpy as np
import csv

# sample config
SENSOR_TYPE1 = {'type': 'FL 2.8', 'min_rho': 2, 'max_rho': 4, 'theta': 70 * np.pi / 180,
                'isOmini': 0, 'isThrough': 0, 'cost': 40}
SENSOR_TYPE2 = {'type': 'FL 2.8', 'min_rho': 2, 'max_rho': 4, 'theta': np.pi * 2,
                'isOmini': 1, 'isThrough': 0, 'cost': 40}
TYPES = [SENSOR_TYPE1, SENSOR_TYPE2]
LOCATIONS = np.array([[1, 2], [2, 3]])
ALPHA_NUM = 8

class Sensor(object):
    def __init__(self, sensor_type):
        self.type = sensor_type['type']
        self.min_rho = float(sensor_type['min_rho'])
        self.max_rho = float(sensor_type['max_rho'])
        self.theta = float(sensor_type['theta'])
        self.isOmini = int(sensor_type['isOmini'])
        self.isThrough = int(sensor_type['isThrough'])
        self.cost = float(sensor_type['cost'])

        assert self.isOmini == int(self.theta == np.pi * 2), "Please input correct sensor configuration"

        self.FOD = [self.min_rho, self.max_rho]

    def place(self, *args):
        self.x = float(args[0])
        self.y = float(args[1])
        # if sensor is directional, orientation is required
        if not self.isOmini:
            self.alpha = float(args[2])
        else:
            self.alpha = 0

        self.FOV = [self.alpha - self.theta / 2, self.alpha + self.theta / 2]

    @property
    def get_config(self):
        config = {}
        try:
            # global parameters
            config['type'] = self.type
            config['min_rho'] = self.min_rho
            config['max_rho'] = self.max_rho
            config['theta'] = self.theta
            config['isOmini'] = self.isOmini
            config['isThrough'] = self.isThrough
            config['cost'] = self.cost
            # local parameters
            config['x'] = self.x
            config['y'] = self.y
            config['alpha'] = self.alpha

            return config
        except:
            raise Exception("Please place the sensor first!")

    @property
    def get_FOV(self):
        return self.FOV

    @property
    def get_FOD(self):
        return self.FOD

class Sensors(object):
    def __init__(self):
        self.sensors = []

    def generate_configs(self, types, locations, alpha_num):
        sensors = []
        alphas = np.array([i * 2 *  np.pi / alpha_num for i in range(alpha_num)])
        for location in locations:
            for type in types:
                # if sensor is Omini
                if int(type['isOmini']):
                    sensor = Sensor(type)
                    sensor.place(location[0], location[1])
                    sensors.append(sensor)
                else:
                    for alpha in alphas:
                        sensor = Sensor(type)
                        sensor.place(location[0], location[1], alpha)
                        sensors.append(sensor)

        self.sensors = sensors
        print("==========>>> Generate %d sensor candidates <<<==========" % len(sensors))

    def save_configs(self, configs_file='data/configs.csv'):
        # the keys of config_file
        fieldnames = ['type', 'min_rho', 'max_rho', 'theta', 'isOmini', 'isThrough', 'cost', 'x', 'y', 'alpha']
        with open(configs_file, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for sensor in self.sensors:
                dict = sensor.get_config
                writer.writerow(dict)
        print("==========>>> Save config file: {} <<<========== ".format(configs_file))

    def load_configs(self, configs_file='data/configs.csv'):
        sensors = []
        with open(configs_file, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # initialize a sensor
                sensor = Sensor(row)
                # place the sensor
                sensor.place(row['x'], row['y'], row['alpha'])
                sensors.append(sensor)
        self.sensors = sensors
        print("==========>>> Load config file: {} <<<==========".format(configs_file))

    def update(self, mask):
        sensors = []
        for i, sensor in enumerate(self.sensors):
            if mask[i]:
                sensors.append(sensor)
        self.sensors = sensors

    @property
    def get_sensors(self):
        return self.sensors

    @property
    def get_locations(self):
        xs = [sensor.x for sensor in self.sensors]
        ys = [sensor.y for sensor in self.sensors]
        return np.array(xs), np.array(ys)

    @property
    def get_num(self):
        return len(self.sensors)

    @property
    def get_costs(self):
        costs = np.array([sensor.cost for sensor in self.sensors])
        return costs

if __name__ == '__main__':
    sensors = Sensors()
    sensors.generate_configs(TYPES, LOCATIONS, ALPHA_NUM)
    sensors.save_configs()
