# ======================================================================================================================
# author:   Xincong YANG
# date:     12 Oct. 2017
# email:    xincong.yang@outlook.com
# name:     Setter_visible
# ======================================================================================================================
import numpy as np
from shapely.geometry import Polygon, Point

# precision of visibility region
EPSILON = 0.01

def visible(sensor, obj_polygon):
    """
    generate sensor visible region in obj_polygon
    :param sensor:
    :param obj_polygon:
    :return: visible region
    """
    ext_ring = np.array(obj_polygon.exterior.coords)
    int_rings = [np.array(int_ring.coords) for int_ring in obj_polygon.interiors]

    config = sensor.get_config

    x0, y0 = config['x'], config['y']

    ray_start = [x0, y0]

    min_angle, max_angle = sensor.get_FOV
    min_rho, max_rho = sensor.get_FOD

    if config['isOmini'] or min_rho > 0:
        ray_ends = []
    else:
        ray_ends = [ray_start]

    angle = min_angle
    while True:
        if angle > max_angle:
            break

        x, y = x0 + max_rho * np.cos(angle), y0 + max_rho * np.sin(angle)

        # ray line segment
        ray_end = [x, y]
        ray = [ray_start, ray_end]
        length = max_rho

        if config['isThrough']:
            # if sensor can pass through objects
            pass

        else:
            # if sensor can not pass through objects
            # intersect with ext_ring
            for i in range(len(ext_ring) - 1):
                start = ext_ring[i]
                end = ext_ring[i + 1]
                line = [start, end]

                intersect = ray_casting(ray, line)
                if distance(ray_start, intersect) <= length:
                    ray_end = intersect
                    length = distance(ray_start, intersect)

            # intersect with int_rings
            for int_ring in int_rings:
                for i in range(len(int_ring) - 1):
                    start = int_ring[i]
                    end = int_ring[i + 1]
                    line = [start, end]

                    intersect = ray_casting(ray, line)
                    if distance(ray_start, intersect) <= length:
                        ray_end = intersect
                        length = distance(ray_start, intersect)

        ray_ends.append(ray_end)

        angle += EPSILON

    visible_region = Polygon(ray_ends)

    if min_rho > 0:
        try:
            invisible_region = Point((x0, y0)).buffer(distance=min_rho)
            visible_region = visible_region.symmetric_difference(invisible_region)
        except:
            visible_region = None

    return visible_region

def distance(start, end):
    """
    generate the distance between point start and end
    :param start:               [x1, y1]
    :param end:                 [x2, y2]
    :return:
    """
    x1, y1 = start
    x2, y2 = end
    return np.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)

def ray_casting(ray, line):
    """

    :param ray:                 [p0, p]
    :param line:                [p1, p2]
    :return:
    """
    p0, p = ray
    p1, p2 = line
    if isIntersect(ray, line):
        return line_intersect(ray, line)
    else:
        return p

def isIntersect(line1, line2):
    """
    determine whether two lines intersect
    :param line1:               [p11, p12]
    :param line2:               [p21, p22]
    :return:
    """
    p11, p12 = line1
    p21, p22 = line2
    return isCCW(p11, p12, p21) != isCCW(p11, p12, p22) and isCCW(p21, p22, p11) != isCCW(p21, p22, p12)

def isCCW(point1, point2, point3):
    """
    determine whether three points are in counter clock wise - k component of cross product (1->2 and 1->3) should be +
    :param point1:              [x1, y1]
    :param point2:              [x2, y2]
    :param point3:              [x3, y3]
    :return:
    """
    x1, y1 = point1
    x2, y2 = point2
    x3, y3 = point3
    return (x2 - x1) * (y3 - y1) > (y2 - y1) * (x3 - x1)

def isCollinear(point1, point2, point3):
    """
    determine whether three points are collinear - slopes equal
    :param point1:              [x1, y1]
    :param point2:              [x2, y2]
    :param point3:              [x3, y3]
    :return:
    """
    x1, y1 = point1
    x2, y2 = point2
    x3, y3 = point3
    return (y3 - y1) * (x2 - x1) == (y2 - y1) * (x3 - x1)

def line_intersect(line1, line2):
    """
    generate the intersect of two line segments
    :param line1:               [p11, p12]
    :param line2:               [p21, p22]
    :return:
    """
    p11, p12 = line1
    p21, p22 = line2
    x1, y1 = p11
    x2, y2 = p12
    x3, y3 = p21
    x4, y4 = p22

    Dx11 = x1 * y2 - x2 * y1
    Dx12 = x1 - x2
    Dx21 = x3 * y4 - x4 * y3
    Dx22 = x3 - x4
    Dx = Dx11 * Dx22 - Dx12 * Dx21

    Dy11 = x1 * y2 - x2 * y1
    Dy12 = y1 - y2
    Dy21 = x3 * y4 - x4 * y3
    Dy22 = y3 - y4
    Dy = Dy11 * Dy22 - Dy12 * Dy21

    D11 = x1 - x2
    D12 = y1 - y2
    D21 = x3 - x4
    D22 = y3 - y4
    D = D11 * D22 - D12 * D21

    if D != 0:
        Px = Dx / D
        Py = Dy / D
        return (Px, Py)
    else:
        return None

def clip(obj_polygon, max_dist, min_dist):
    """
    clip the obj_polygon edges into points
    :param obj_polygon:
    :param max_dist:
    :param min_dist:
    :return:
    """
    ext_coords = np.array(obj_polygon.exterior.coords)
    int_coords_list = [np.array(int_ring.coords) for int_ring in obj_polygon.interiors]

    points = []

    ext_n = len(ext_coords)
    for i in range(ext_n - 1):
        start = ext_coords[i]
        end = ext_coords[i + 1]
        dist = distance(start, end)

        if dist > max_dist:
            n = int(dist / max_dist)
            xs = np.linspace(start[0], end[0], num=n, endpoint=False)
            ys = np.linspace(start[1], end[1], num=n, endpoint=False)
            for x, y in zip(xs, ys):
                points.append((x, y))
        elif dist > min_dist:
            points.append(start)

    for int_coords in int_coords_list:
        int_n = len(int_coords)
        for i in range(int_n - 1):
            start = int_coords[i]
            end = int_coords[i + 1]
            dist = distance(start, end)

            if dist > max_dist:
                n = int(dist / max_dist)
                xs = np.linspace(start[0], end[0], num=n, endpoint=False)
                ys = np.linspace(start[1], end[1], num=n, endpoint=False)
                for x, y in zip(xs, ys):
                    points.append((x, y))
            elif dist > min_dist:
                points.append(start)

    return np.array(points)

def discrete(obj_polygon, grid_size):
    """
    discrete the layout into points
    :param obj_polygon:
    :param grid_size:
    :return:
    """
    ext_coords = np.array(obj_polygon.exterior.coords)
    max_x, max_y = ext_coords.max(axis=0)
    min_x, min_y = ext_coords.min(axis=0)

    grid_num_x = int(np.ceil((max_x - min_x) / grid_size))
    grid_num_y = int(np.ceil((max_y - min_y) / grid_size))

    xs = np.linspace(min_x, max_x, num=grid_num_x, endpoint=True)
    ys = np.linspace(min_y, max_y, num=grid_num_y, endpoint=True)

    points = []
    for x in xs:
        for y in ys:
            if obj_polygon.contains(Point([x, y])):
                points.append([x, y])

    return np.array(points)





