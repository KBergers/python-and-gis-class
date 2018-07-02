# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 15:34:47 2018

@author: SWP679
"""
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import pysal as ps
from fiona.crs import from_epsg

"""
PROBLEM 1: JOIN ACCESSIBILITY DATASETS INTO A GRID AND VISUALISE THEM BY
USING A CLASSIFIER
"""
#Read travel time files
def read_file(fp):
    data = pd.read_csv(fp, sep=";")
    data = data[["pt_r_tt", "car_r_t", "from_id", "to_id"]]
    geodata = gpd.GeoDataFrame(data)
    return geodata

jumbo = read_file("Data\\TravelTimes_to_5878070_Jumbo.txt")
dixi = read_file("Data\\TravelTimes_to_5878087_Dixi.txt")
myyr = read_file("Data\\TravelTimes_to_5902043_Myyrmanni.txt")
itis = read_file("Data\\TravelTimes_to_5944003_Itis.txt")
forum = read_file("Data\\TravelTimes_to_5975373_Forum.txt")
iso = read_file("Data\\TravelTimes_to_5978593_Iso_omena.txt")
ruo = read_file("Data\\TravelTimes_to_5980260_Ruoholahti.txt")

#Read shapefile with polygons of metropole
grid = gpd.read_file("Data\\MetropAccess_YKR_grid_EurefFIN.shp")

#Merge travel times to Jumbo with grid
jumbo_grid = pd.merge(jumbo, 
                      grid, 
                      how="inner", 
                      left_on="from_id", 
                      right_on="YKR_ID")

#Create function for classification
def classify(gdf, column, n_classes):
    classifier = ps.Natural_Breaks.make(k=n_classes)
    classifications = gdf[[column]].apply(classifier)
    classifications.rename(columns={column: "c_"+column}, inplace=True)
    gdf = gdf.join(classifications)
    return gdf

#Apply function on merged geodataframe and plot
jumbo_grid = classify(jumbo_grid, "pt_r_tt", 10)
jumbo_grid = classify(jumbo_grid, "car_r_t", 10)
jumbo_grid.plot("c_pt_r_tt", legend=True)
plt.tight_layout()

"""
PROBLEM 2: CALCULATE AND VISUALIZE THE DOMINANCE AREAS OF SHOPPING CENTERS
"""
#Rename columns and join with grid
grid_join = grid
dfs =[jumbo, dixi, myyr, itis, forum, iso, ruo]
for i, df in enumerate(dfs):
    cols = [col + "_" + str(df["to_id"][0]) for col in df.columns]
    df.columns = cols
    grid_join = pd.merge(df, 
                         grid_join, 
                         how="right", 
                         left_on=cols[2], 
                         right_on="YKR_ID")

#Find minimum distance and dominant service for each row in grid
cols_to_check = [col for col in grid_join.columns if "pt_r_tt" in col]
for i, row in grid_join.iterrows():
    dominant = 0
    min_travel = 99999
    for col in cols_to_check:
        if row[col] < min_travel:
            min_travel = row[col]
            dominant = col[len(col)-7:]        
    grid_join.loc[i, "min_time_pt"] = min_travel
    grid_join.loc[i, "dominant_service"] = int(dominant)
    
#Visualise the travel times of min_time_pt
tt_classified = classify(grid_join, "min_time_pt", 5)
tt_classified.plot("c_min_time_pt", legend=True)
plt.tight_layout()

#Visualise the dominant service
tt_classified.plot("dominant_service", legend=True)
plt.tight_layout() 

"""
PROBLEM 3: HOW MANY PEOPLE LIVE UNDER THE DOMINANTS AREAS?
"""
#Read and prepare population grid into a GeoDataFrame
fp = "Data\\Vaestotietoruudukko_2015.shp"
pop = gpd.read_file(fp)
pop = pop.rename(columns={'ASUKKAITA': 'pop15'})
pop = pop[["pop15", "geometry"]]
pop["geometry"] = pop["geometry"].to_crs(epsg=3879)

#Prepare grid for spatial join
grid_join = grid_join[["geometry", "min_time_pt", "dominant_service"]]
dissolved_grid = grid_join.dissolve(by="dominant_service") #Group geometries by dominant_service
dissolved_grid.reset_index(inplace=True)
dissolved_grid.crs = from_epsg(3047)
dissolved_grid["geometry"] = dissolved_grid["geometry"].to_crs(epsg=3879)

#Spatial join and groupby population
join = gpd.sjoin(pop, dissolved_grid, how="left", op="within")
join.groupby("dominant_service").sum()["pop15"]

