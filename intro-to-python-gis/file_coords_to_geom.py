# -*- coding: utf-8 -*-
from shapely.geometry import Point, LineString, Polygon
from create_geometries import createPointGeom, createLineGeom, createPolyGeom
import pandas as pd
import os

cols = ['from_x', 'from_y', 'to_x', 'to_y']
travel_times = pd.read_csv("travelTimes_2015_Helsinki.txt", 
                           sep=";",
                           usecols=cols)

#List origin and destination points
orig_points = [Point(row[0], row[1]) for i, row in travel_times.iterrows()]
dest_points = [Point(row[2], row[3]) for i, row in travel_times.iterrows()]

#Create lines using origin and destination points
lines = [LineString([orig_point, dest_points[i]]) for i, orig_point in enumerate(orig_points)]

def meanDistanceLines(listOfLines):
    total_distance = 0
    for line in listOfLines:
        total_distance += line.length
    return total_distance/len(listOfLines)

