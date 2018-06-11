# -*- coding: utf-8 -*-
from shapely.geometry import Point, LineString, Polygon
from create_geometries import createPointGeom, createLineGeom, createPolyGeom
import pandas as pd
import os

cols = ['from_x', 'from_y', 'to_x', 'to_y']
travel_times = pd.read_csv("travelTimes_2015_Helsinki.txt", 
                           sep=";",
                           usecols=cols)

orig_points = [Point(float(row[0]), float(row[1])) for row in travel_times]
dest_points = []



