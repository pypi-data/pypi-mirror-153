from typing import Tuple, List
import math

def line_intersection(line1: Tuple[Tuple[float, float], Tuple[float, float]],
                      line2: Tuple[Tuple[float, float], Tuple[float, float]],
                      extend: bool = False):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    # handle meet at ends case:
    if line1[0] in [line2[0], line2[1]]:
        return line1[0]
    elif line1[1] in [line2[0], line2[1]]:
        return line1[1]

    # handle collinear lines
    if collinear_points([line1[0], line1[1], line2[0], line2[1]]):
        raise Exception("Lines are collinear")

    det = lambda a, b: a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div

    between = lambda line, point: (min(line[0][0], line[1][0]) <= point[0] <= max(line[0][0], line[1][0]) ) \
                             and (min(line[0][1], line[1][1]) <= point[1] <= max(line[0][1], line[1][1]))

    if not extend and \
        not all([
            between(line1, (x, y)),
            between(line2, (x, y))
        ]):
        return None

    return x, y

def point_in_polygon(point: Tuple[float, float], poly: List[Tuple[float, float]]):
    # https://en.wikipedia.org/wiki/Point_in_polygon#:~:text=One%20simple%20way%20of%20finding,an%20even%20number%20of%20times.
    # https://en.wikipedia.org/wiki/Even%E2%80%93odd_rule


    # Determine if the point is in the polygon.
    #
    # Args:
    #   x -- The x coordinates of point.
    #   y -- The y coordinates of point.
    #   poly -- a list of tuples [(x, y), (x, y), ...]
    #
    # Returns:
    #   True if the point is in the path or is a corner or on the boundary

    num = len(poly)
    j = num - 1
    c = False
    for i in range(num):
        if (point[0] == poly[i][0]) and (point[1] == poly[i][1]):
            # point is a corner
            return True
        if ((poly[i][1] > point[1]) != (poly[j][1] > point[1])):
            slope = (point[0]- poly[i][0]) * (poly[j][1] - poly[i][1]) - (poly[j][0] - poly[i][0]) * (point[1] - poly[i][1])
            if slope == 0:
                # point is on boundary
                return True
            if (slope < 0) != (poly[j][1] < poly[i][1]):
                c = not c
        j = i
    return c

def collinear_points(points: List[Tuple[float, float]]):

    if len(points) < 3:
        return True

    for ii in range(2, len(points)):
        a = points[ii - 2]
        b = points[ii - 1]
        c = points[ii]
        tri_area = a[0] * (b[1] - c[1]) + b[0] * (c[1] - a[1]) + c[0] * (a[1] - b[1])
        if math.isclose(tri_area, 0):
            continue
        else:
            return False

    return True

if __name__ == "__main__":
    #TEST1
    poly = [
        (2, 2),
        (3, 3),
        (2, 3),
        (3, 2)
    ]

    point = (1, 1)
    print(point_in_polygon(point, poly))
    point = (2.5, 2.5)
    print(point_in_polygon(point, poly))

    #TEST2
    a = (0, 1)
    b = (0, 2)
    c = (0, 3)
    d = (0, 4)
    e = (0, 5)
    f = (0, 6)
    print(collinear_points([a, b, c, d, e, f]))

    #TEST3
    a = (0, 1.000000001)
    b = (0, 1.000000002)
    c = (0, 3)
    print(collinear_points([a, b, c]))

