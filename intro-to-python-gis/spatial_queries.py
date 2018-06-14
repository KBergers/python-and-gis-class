# -*- coding: utf-8 -*-
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import geocoder
from fiona.crs import from_epsg

fp = r"shopping_centers.txt"
data = pd.read_csv(fp, sep=';')

#Get lat and lon based on adresses using OSM as provider
geo_latlng = [geocoder.osm(adress).latlng for adress in data["addres"]]
#Convert to Point geometry
geo_point = [Point(addr[0], addr[1]) for addr in geo_latlng]

#Add points to new column "geometry" in GeoDataFrame
geo = gpd.GeoDataFrame(data)
geo["geometry"] = geo_point
geo.crs = from_epsg(3879)

#Output to shapefile
fp = "C:\\temp\\shp\\helsinkin_shopping_centers.shp"
geo.to_file(fp)