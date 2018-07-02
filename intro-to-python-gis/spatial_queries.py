# -*- coding: utf-8 -*-
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, MultiPoint
import geocoder
from fiona.crs import from_epsg
from shapely.ops import nearest_points

pd.set_option('display.expand_frame_repr', False)


"""
PROBLEM 1: GEOCODE SHOPPING CENTERS
"""

fp = r"shopping_centers.txt"

def createGdf(fp):
    data = pd.read_csv(fp, sep=';')

    #Get lat and lon based on adresses using OSM as provider
    geo_latlng = [geocoder.osm(adress).latlng for adress in data["addres"]]
    #Convert to Point geometry
    geo_point = [Point(addr[1], addr[0]) for addr in geo_latlng]
    
    #Add points to new column "geometry" in GeoDataFrame
    geo = gpd.GeoDataFrame(data)
    geo["geometry"] = geo_point
    #Set CRS to WGS84 (lat-lon)
    geo.crs = from_epsg(4326)
    #Reproject to ETRS GK-25 (EPSG: 3879)
    geo["geometry"] = geo["geometry"].to_crs(epsg=3879)
    return geo

geo = createGdf(fp)

#Output to shapefile
fp = "C:\\temp\\shp\\helsinkin_shopping_centers.shp"
geo.to_file(fp)


"""
PROBLEM 2: CREATE BUFFERS AROUND SHOPPING CENTERS
"""
geo["buffer"] = None
for i, row in geo.iterrows():
    geo.loc[i, "buffer"] = geo.loc[i, "geometry"].buffer(5000)
geo["geometry"] = geo["buffer"]

    
"""
PROBLEM 3: HOW MANY PEOPLE LIVE WITHIN 5KM FROM SHOPPING CENTERS?
"""
#Read and prepare population grid into a GeoDataFrame
fp = "Data\\Vaestotietoruudukko_2015.shp"
pop = gpd.read_file(fp)
pop = pop.rename(columns={'ASUKKAITA': 'pop15'})
pop = pop[["pop15", "geometry"]]
pop["geometry"] = pop["geometry"].to_crs(epsg=3879)

#Join between buffered point layer and population grid layer
join = gpd.sjoin(pop, geo, how="right", op="within")
#Group and calculate population according to spatial join
group = join.groupby(["id", "name"]).sum()


"""
PROBLEM 4: WHAT IS THE CLOSEST SHOPPING CENTER?
"""
fp = r"activity_locations.txt"
data = pd.read_csv(fp, sep=';')

#Get lat and lon based on adresses using OSM as provider
geo_latlng = [geocoder.osm(address).latlng for address in data["addr"]]
#Convert to Point geometry
geo_point = [Point(addr[1], addr[0]) for addr in geo_latlng]

#Add points to new column "geometry" in GeoDataFrame
geo_activity = gpd.GeoDataFrame(data)
geo_activity["geometry"] = geo_point
#Set CRS to WGS84 (lat-lon)
geo_activity.crs = from_epsg(4326)
#Reproject to ETRS GK-25 (EPSG: 3879)
geo_activity["geometry"] = geo_activity["geometry"].to_crs(epsg=3879)

#Make multipoint out of shopping centers
fp = r"shopping_centers.txt"
geo_shopping = createGdf(fp)
destinations = MultiPoint(geo_shopping["geometry"])
nearest_geoms0 = nearest_points(geo_shopping["geometry"][0], destinations)
nearest_geoms1 = nearest_points(geo_shopping["geometry"][1], destinations)
