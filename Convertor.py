# ======================================================================================================================
# author:   Xincong YANG
# date:     18 Oct. 2017
# email:    xincong.yang@outlook.com
# name:     Convertor
# ======================================================================================================================

import numpy as np
import csv

def npy2csv(npy_file):
    data = np.load(npy_file)
    shape = data.shape
    file_name = npy_file.split('.npy')[0] + '.csv'
    with open(file_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if len(shape) == 1:
            writer.writerow(data.tolist())
        elif len(shape) == 2:
            for row in data:
                writer.writerow(row.tolist())

    print("Convert .npy file to .csv file: {}".format(file_name))

if __name__ == '__main__':
    npy2csv('data/A.npy')