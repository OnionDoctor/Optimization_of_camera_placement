# Optimization_of_camera_placement

## Requirements
- Python 3.x
- Numpy
- Matplotlib
- cvxopt 1.1.9
- Shapely 1.6.1
- descartes 1.1.0

## Content
- ```data```: Temporal folder for camera candidates
- ```MOP_algorithms```: Folder for MOP algorithms, revised NSGA ii
- ```sample```: Folder for objective layout
- ```Convertor.py```: csv reader and convertor
- ```Setter_sensors.py```: sensor class
- ```Setter_visible.py```: visibile region computing
- ```Setter_plot.py```: plot lib.
- ```Setter_model.py```: placement model
- ```Setter_main.py```: main program

## Useage
### Sample
Run ```python Setter_main.py```

### Customized layout and sensor types
#### Construct the objective layout
1. Open ```sample/Setter_sample.py```

2. Add or modify the camera types as follows (a dict).
```{'type':x, 'min_rho': 0, 'max_rho': x, 'theta': x, 'isOmni': x, 'isThrough': x, 'cost': x}```
Please replace ```x``` with your data.
If the camera is a Bullet/Dome camera, please input ```{'isOmni':0}```
If the camera is a 360-Omni camera, please input ```{'isOmni':1}```
If the sensor can through objects, like RFID readers, please input ```{'isThrough':1}``` otherwise ```{'isThrough':0}```
```'type'``` should be a string.
```'theta'``` refers to visible angle in rad
And combine them as a list:
```SENSOR_TYPES = [sensor_tpye1, sensor_tpye2, sensor_tpye3, ...]```

3. Modify the objective layout as follows:
```ext = [(x1, y1), (x2, y2), ...]``` is the outliner of objective layout, please input the points anti-clock-wise
```int1 = [(x1, y1), (x2, y2), ...]``` is the holes of objective layout, please input the points clock-wise
```OBJ_POLYGON = Polygon(ext, [int1, int2, int3, ...])``` is the final objective layout, please take care of the order of input points

4. Run the main program
Open the setter_main.py and edit as follows:
```
clean_tmp_data()
setter = model(obj_polygon=OBJ_POLYGON,
			   sensor_types=SENSOR_TYPES,
               grid_size=0.5,
               sensor_buffer=-0.1,
               max_dist=1,
               min_dist=0.5,
               alpha_num=4,
               cover_times=1)
```
Here ```grid_size``` is the size of grids, ```sensor_buffer``` is the buffer positions for camera installation, ```max_dist``` and ```min_dist``` is the maximum and minimum distance between potential camera installation positions in buffer space. ```Alpha_num``` is the divided number of 360. For example, if the cameras can be installed in the directions of 0, 90, 180, 270 degrees, Alpha_num should be settled as 4. ```cover_num``` is the coverage requirements of positions.

5. Customized the target vector (if the objective layout is required to be covered homogeneous, skip)
After step 4, temporary files ```A.npy```, ```b.npy```, ```c.npy```are generated in data file. A is the coverage coefficient matrix, b is the target vector and c is the cost vector. If different points on objective layout required to be cvered with different numbers of cameras, please modify the cover times in b.

6. Run the computation
For maximum-coverage problem: Maximize the cover areas with a limited budget.
```setter.compute(mode='max', method='dp', value=200)```
Please modify the limited budget according to your requirement.
For minimum-cost problem: Minimize the cost given an objective layout that each point is covered.
```setter.compute(mode='min', method='ilp')```
For MOP problem: get the pareto fronts of cost and coverage ratio.
```
W = np.load('data/A.npy').T
b = np.load('data/b.npy')
c = np.load('data/c.npy')
problem = Problem(W=W, b=b, c=c)
nsga = NSGA_ii(problem=problem, population_size=200, select_size=20, mutate_size=20)
population, _ = nsga.evolve(num_of_generations=50)
```
Please modify the population_size, select_size and mutate_size

7. Plot result, just run
```
fig = plt.figure()
ax = fig.add_subplot（111）
setter.plot(ax) 
plt.show()
```

## Results
- Maximun coverage problem, cost from 10 to 1000, grid size = 4, orientations = 0, 90, 180, 270
![g4a4.gif](https://github.com/OnionDoctor/Optimization_of_camera_placement/blob/master/result/max/g4a4.gif)

- Maximun coverage problem, cost from 10 to 1000, grid size = 8, orientations = 0, 90, 180, 270
![g8a4.gif](https://github.com/OnionDoctor/Optimization_of_camera_placement/blob/master/result/max/g8a4.gif)

- Maximun coverage problem, cost from 10 to 1000, grid size = 8, orientations = 0, 45, 90, 135, 180, 225, 270, 315
![g8a8.gif](https://github.com/OnionDoctor/Optimization_of_camera_placement/blob/master/result/max/g8a8.gif)

- Minimum cost problem, grid size = 6 to 20 , orientations = 0, 90, 180, 270
![g6-20a4.gif](https://github.com/OnionDoctor/Optimization_of_camera_placement/blob/master/result/min/g6-20a4.gif)

- Minimum cost problem, grid size = 6 to 20 , orientations = 0, 45, 90, 135, 180, 225, 270, 315
![g6-20a8.gif](https://github.com/OnionDoctor/Optimization_of_camera_placement/blob/master/result/min/g6-20a8.gif