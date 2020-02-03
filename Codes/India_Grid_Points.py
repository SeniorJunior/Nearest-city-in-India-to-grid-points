``` Python

# DECLARATION 
import geopandas as gpd
import pandas as pd
from shapely.geometry import Polygon
import numpy as np
import os
import math 
import matplotlib.patches as patches
import pylab
import matplotlib.pyplot as plt
import shapely.geometry
import pyproj
from osgeo import ogr
from geopandas import GeoDataFrame
import descartes
import geopandas as gpd
from shapely.geometry import Point, Polygon
%matplotlib inline

# CREATING THE GRID AND THE STEP SIZE AND SAVING IT INTO A CSV FILE

# Set up projections
p_ll = pyproj.Proj(init='epsg:4326')
p_mt = pyproj.Proj(init='epsg:3857') # metric; same as EPSG:900913

# Create corners of rectangle to be transformed to a grid
nw = shapely.geometry.Point((68.0, 6.5))
se = shapely.geometry.Point((98.0, 36.0))

stepsize = 30000 # 30 km grid step size

# Project corners to target projection
s = pyproj.transform(p_ll, p_mt, nw.x, nw.y) # Transform NW point to 3857
e = pyproj.transform(p_ll, p_mt, se.x, se.y) # .. same for SE

# Iterate over 2D area
gridpoints = []
x = s[0]
while x < e[0]:
    y = s[1]
    while y < e[1]:
        p = shapely.geometry.Point(pyproj.transform(p_mt, p_ll, x, y))
        gridpoints.append(p)
        y += stepsize
    x += stepsize

with open('/Users/williamadriel/Desktop/Yara/grid.csv', 'w') as of:
    of.write('lon;lat;id\n')
    for p in gridpoints:
        of.write('{:.2f};{:.2f}\n'.format(p.x, p.y))


# READING THE CSV FILE TO DISPLAY THE GRIDS

# Reading the grid file in Pandas
grid = pd.read_csv("/Users/williamadriel/Desktop/Yara/grid.csv", delimiter=";")

# Reading the India district shape file to get the map of India
india_district = gpd.read_file('/Users/williamadriel/Desktop/Yara/gadm36_IND_2.shp')
india_district.head()

geometry = [Point(xy) for xy in zip(grid["lon"],grid['lat'])]
geometry[:3]
crs={'init' : 'epsg:4326'}
# Print the grid dataframe 
grid_gdf=gpd.GeoDataFrame(grid,crs=crs,geometry=geometry)
grid_gdf.head()


# READ THE GRID DATAFRAME AND DISTRICTS DATAFRAME

# Read the grids dataframe by geometry, lon, lat, and id
grids = grid_gdf[['geometry', 'lon', 'lat', 'id']]
# Read the districts dataframe by geometry, state, district, and country
districts = india_district[['geometry', 'NAME_1', 'NAME_2', 'NAME_0']]


# MERGE GRID POINTS WITH INDIA DISTRICT POINTS

merged_grid = gpd.sjoin(grids, districts, how="inner", op='intersects')
merged_grid.head()

# To plot the grid into the india district map 
fig,ax=plt.subplots(figsize=(18,18))
india_district.plot(ax=ax)
merged_grid.plot(ax=ax,marker='+',color='red', linewidth = 0.5, markersize = 2, alpha=1)
plt.xlim(67,99)
plt.ylim(6,38)

# Save the merged_grid file to the csv file
merged_grid.drop('geometry',axis=1).to_csv(r'/Users/williamadriel/Desktop/Yara/merged_grid.csv')


```
