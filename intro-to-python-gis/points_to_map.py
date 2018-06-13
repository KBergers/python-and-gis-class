# -*- coding: utf-8 -*-
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, LineString
from fiona.crs import from_epsg

#Import data
fp = "C:\\Git\\python-and-gis-class\\intro-to-python-gis\\Kruger\\social_media_posts.txt"
data = pd.read_csv(fp)

print("Creating Point objects...")
#Create empty geometry column and insert Point objects
data["geometry"] = None
for i, row in data.iterrows():
    data.loc[i, "geometry"] = Point(data.loc[i, "lat"], data.loc[i, "lon"])

print("Creating GeoDataFrame...")
#Convert DataFrame to GeoDataFrame
geodata = gpd.GeoDataFrame(data, geometry="geometry", crs = from_epsg(4326))

#Output to shapefile and plot
outfp = "C:\\temp\\shp\\Kruger.shp"
geodata.to_file(outfp)

print("Reprojecting GeoDataFrame...")
#Reproject data and sort values
geodata_reproj = geodata.to_crs(epsg=32735)
geodata_reproj.sort_values(["userid", "timestamp"], inplace=True)

print("Grouping by userid...")
#Group data by userid
grouped = geodata_reproj.groupby("userid")

#Create empty GeoDataFrame
movements = gpd.GeoDataFrame(columns=["userid", "geometry"], crs=32735)

print("Creating LineString objects...")
#For each user create LineString objects based on points and add the 
#geometries and the userid to GeoDataFrame movements
#First, iterate over user:
for i, group in enumerate(grouped):
    points = []
    #Second, iterate over each row of the user
    for j, rows in enumerate(group):
        #The GeoDataFrame for each user is in the second index of each row
        if j==1:
            #Iterate over the GeoDataFrame
            for line in rows.iterrows():
                #Extract the Point object and add to points-list
                points.append(line[1][4])
    #Create LineString if possible
    if len(points) > 1:
        line = LineString(points)
    else:
        line = points[0]
    #Append userid and LineString to movements GeoDataFrame
    row_to_append = {"userid":group[0], "geometry":line}
    movements = movements.append(row_to_append, ignore_index=True)

print("Calculing distances...")
#Calculate distance of each line to new column
movements.crs = from_epsg(32735)
movements["distance"] = movements["geometry"].length

movements_nozero = movements[movements["distance"]!=0]

#Output to shapefile
outfp = "C:\\temp\\shp\\Kruger_distances.shp"
movements_nozero.to_file(outfp)

print("Shortest distance travelled: " + str(movements_nozero["distance"].min()))
print("Maximum distance travelled: " + str(movements_nozero["distance"].max()))
print("Mean distance travelled: " + str(movements_nozero["distance"].mean()))