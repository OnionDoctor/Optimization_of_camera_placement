# ======================================================================================================================
# author:   Xincong YANG
# date:     12 Oct. 2017
# email:    xincong.yang@outlook.com
# name:     Setter_visible
# ======================================================================================================================
import matplotlib.pyplot as plt
import numpy as np
import time, os

from Setter_model import model
from sample.Setter_sample import SENSOR_TYPES, OBJ_POLYGON
# from sample.Setter_layout import SENSOR_TYPES, OBJ_POLYGON
from MOP_algorithms.NSGA_ii import Problem, NSGA_ii

def analyse_max():

    for g_s in range(2, 4, 8):
        for a_n in range(4, 6, 8):

            compute_times = []
            coverage_ratios = []

            save_path = 'result/g{}a{}'.format(g_s, a_n)
            os.mkdir(save_path)

            for i in range(50, 1001, 50):

                print("==========>>> Total cost :{} <<<==========".format(i))
                setter = model(obj_polygon=OBJ_POLYGON, sensor_types=SENSOR_TYPES,
                               grid_size=g_s,
                               sensor_buffer=-0.1, max_dist=4, min_dist=1, alpha_num=a_n,
                               cover_times=1)

                start = time.time()

                setter.compute(mode='max', method='dp', value=i)

                compute_time = time.time() - start
                compute_times.append(compute_time)

                coverage_ratios.append(setter.get_coverage)

                fig = plt.figure(figsize=(9, 6))
                ax = fig.add_subplot(111)

                setter.plot(ax)

                ax.set_xlim(0, 110)
                ax.set_ylim(0, 110)
                ax.set_aspect('equal')

                fig.savefig(save_path + '/' + str(i) + '.png', dpi=300)

                plt.close()

            clear_tmp_data()

            np.save(save_path + '/' + 'times.npy', np.array(compute_times))
            np.save(save_path + '/' + 'coverage.npy', np.array(coverage_ratios))

def analyse_min():
    compute_times = []

    costs = []

    for i in (5, 10, 15, 20):
        for j in (4, 6, 8):
            print("==========>>> Grid size: {}; Alpha num: {}; <<<==========".format(i, j))
            setter = model(obj_polygon=OBJ_POLYGON, sensor_types=SENSOR_TYPES,
                           grid_size=i,
                           sensor_buffer=-0.1, max_dist=4, min_dist=1, alpha_num=j,
                           cover_times=1)

            start = time.time()

            setter.compute(mode='min', method='ilp')

            compute_time = time.time() - start
            compute_times.append(compute_time)

            costs.append(setter.get_cost)

            fig = plt.figure(figsize=(9, 6))
            ax = fig.add_subplot(111)

            setter.plot(ax)

            ax.set_xlim(0, 110)
            ax.set_ylim(0, 110)
            ax.set_aspect('equal')

            fig.savefig('result/g' + str(i) + 'a' + str(j) + '.png', dpi=300)

            clear_tmp_data()

    np.save('result/times.npy', np.array(compute_times))
    np.save('result/costs.npy', np.array(costs))

def analyse_mop():

    compute_times = []

    for i in (5, 10, 15, 20):
        for j in (4, 6, 8):
            print("==========>>> Grid size: {}; Alpha num: {}; <<<==========".format(i, j))
            setter = model(obj_polygon=OBJ_POLYGON, sensor_types=SENSOR_TYPES,
                           grid_size=i,
                           sensor_buffer=-0.1, max_dist=4, min_dist=1, alpha_num=j,
                           cover_times=1)

            W = np.load('data/A.npy').T
            b = np.load('data/b.npy')
            c = np.load('data/c.npy')

            fig = plt.figure(figsize=(6, 4))
            ax = fig.add_subplot(111)

            problem = Problem(W=W, b=b, c=c)
            start = time.time()
            nsga = NSGA_ii(problem=problem, population_size=200, select_size=20, mutate_size=20)
            population, _ = nsga.evolve(num_of_generations=50, ax=ax)

            compute_times.append(time.time() - start)

            ax.set_xlabel("Coverage ratio")
            ax.set_ylabel("Cost")

            plt.savefig('result/mop_g' + str(i) + 'a' + str(j) + '.png', dpi=300)

            clear_tmp_data()

    np.save('result/mop_times.npy', np.array(compute_times))

def clear_tmp_data():
    os.remove('data/A.npy')
    os.remove('data/b.npy')
    os.remove('data/c.npy')
    os.remove('data/configs.csv')

def main():
    clear_tmp_data()
    setter = model(obj_polygon=OBJ_POLYGON, sensor_types=SENSOR_TYPES,
                   grid_size=0.5,
                   sensor_buffer=-0.1, max_dist=1, min_dist=0.5, alpha_num=4,
                   cover_times=1)
    setter.compute(mode='max', method='dp', value=200)
    fig = plt.figure(figsize=(9, 6))
    ax = fig.add_subplot(111)

    setter.plot(ax)

    ax.set_xlim(0, 8)
    ax.set_ylim(0, 5)
    ax.set_aspect('equal')

    plt.show()

if __name__ == '__main__':
    main()