# -*- coding: utf-8 -*-
from shapely.geometry import Point, LineString, Polygon
from create_geometries import createPointGeom, createLineGeom, createPolyGeom

def getCentroid(geom):
    if isinstance(geom, Point):
        return geom
    elif isinstance(geom, LineString) or isinstance(geom, Polygon):
        return geom.centroid

def getArea(poly):
    return poly.area

def getLength(geom):
    if isinstance(geom, LineString) or isinstance(geom, Polygon):
        return geom.length
    else:
        print("Error: LineString or Polygon geometries required!")

if __name__ == "__main__":
    point1 = createPointGeom(2.2, 5.1)
    point2 = createPointGeom(2, 6.7)
    point3 = createPointGeom(6, 1)
    
    points1 = [point1, point2, point3]
    line1 = createLineGeom(points1)
    
    points_tuple = ([(2.2, 4.2), (7.2, -25.1), (9.26, -2.456)])
    poly1 = createPolyGeom(points_tuple)
    poly2 = createPolyGeom(points1)
    
    point_centroid = getCentroid(point1)
    print("Point1 centroid: " + str(point_centroid))
    line_centroid = getCentroid(line1)
    print("Line1 centroid: " + str(line_centroid))
    poly_centroid = getCentroid(poly1)
    print("Poly1 centroid: " + str(poly_centroid))
    
    poly_area = getArea(poly2)
    print("Poly2 area: " + str(poly_area))
    
    line_length = getLength(line1)
    print("Line1 length: " + str(line_length))
    poly_length = getLength(poly1)
    print("Poly1 length: " + str(poly_length))
    invalid_length = getLength(point3) 
    
    
    