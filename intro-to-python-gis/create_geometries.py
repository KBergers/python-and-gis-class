# -*- coding: utf-8 -*-
from shapely.geometry import Point, LineString, Polygon

def createPointGeom(x_coord, y_coord):
    return Point(x_coord, y_coord)

def createLineGeom(points):
    #Check first if input list really contains Shapely Points
    if isinstance(points[0], Point):
        line = LineString(points)
        return line
    else:
        print("Input list doesn't contain Shapely Points!")

def createPolyGeom(points):
    if isinstance(points[0], Point):
        poly = Polygon([[p.x, p.y] for p in points])
        return poly
    elif isinstance(points[0], tuple):
        poly = Polygon(points)
        return poly
    else:
        print("Input list doesn't contain Shapely Points or coordinates tuples!")

if __name__ == "__main__":
    point1 = createPointGeom(2.2, 5.1)
    point2 = Point(2, 6.7)
    point3 = Point(6, 1)
    print("point1: " + str(point1))
    print("point2: " + str(point2))
    print("point3: " + str(point3))
    
    points1 = [point1, point2, point3]
    line1 = createLineGeom(points1)
    points2 = "no-shapely-points"
    line2 = createLineGeom(points2)
    print("line1: " + str(line1))
    print("line2: " + str(line2))
    
    points_tuple = ([(2.2, 4.2), (7.2, -25.1), (9.26, -2.456)])
    poly1 = createPolyGeom(points_tuple)
    poly2 = createPolyGeom(points1)
    poly3 = createPolyGeom("no tuple coord or shapely points")
    print("poly1: " + str(poly1))
    print("poly2: " + str(poly2))
    print("poly3: " + str(poly3))
    
    