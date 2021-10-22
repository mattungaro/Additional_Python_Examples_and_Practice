# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 22:13:42 2020

@author: 11e
"""

# Chapter 3 Helsinki

# Import necessary modules
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import geopy

# Filepath
fp = r"C:\Users\11e\Desktop\send_to_other_comp\addresses.txt"

# Read the data
data = pd.read_csv(fp, sep=';')

# Import the geocoding tool
from geopandas.tools import geocode

# Key for our Google Geocoding API
# Notice: only the cloud computers of our course can access and
# successfully execute the following
key = 'AIzaSyAwNVHAtkbKlPs-EEs3OYqbnxzaYfDF2_8'

# Geocode addresses
geo = geocode(data['address'], api_key=key)

geo.head(2)

# ---------------

# Join tables by using a key column 'address'
    # only possible to do if I get the google api key
join = geo.merge(data, on='address')

# Let's see what we have
join.head()

type(join)
# Output file path
outfp = r"/home/geo/addresses.shp"

# Save to Shapefile
join.to_file(outfp)

# ----------------------

# Reprojecting Data

import geopandas as gpd
# Filepath to the addresses Shapefile

fp = "/home/geo/addresses.shp"

# Read data
data = gpd.read_file(fp)

data.crs

data['geometry'].head()

#Let’s convert those geometries into ETRS GK-25 projection 
#(EPSG: 3879). Changing the projection is really easy to do 
# in Geopandas with .to_crs() -function. As an input for the 
# function, you should define the column containing the 
# geometries, i.e. geometry in this case, and a epgs value of 
# the projection that you want to use.

# Let's take a copy of our layer
data_proj = data.copy()

# Reproject the geometries by replacing the values with projected ones
data_proj['geometry'] = data_proj['geometry'].to_crs(epsg=3879)

data_proj['geometry'].head()


# And here we go, the numbers have changed! Now we have successfully
# changed the projection of our layer into a new one.

import matplotlib.pyplot as plt

# Plot the WGS84
data.plot(markersize=6, color="red");

# Add title
plt.title("WGS84 projection");

# Remove empty white space around the plot
plt.tight_layout()

# Plot the one with ETRS GK-25 projection
data_proj.plot(markersize=6, color="blue");

# Add title
plt.title("ETRS GK-25 projection");

# Remove empty white space around the plot
plt.tight_layout()

# Indeed, they look different and our re-projected one 
# looks much better in Finland (not so stretced as in WGS84).

#Now we still need to change the crs of our GeoDataFrame into 
#EPSG 3879 as now we only modified the values of the geometry 
# column. We can take use of fiona’s from_epsg -function.

from fiona.crs import from_epsg

# Determine the CRS of the GeoDataFrame
data_proj.crs = from_epsg(3879)

# Let's see what we have
data_proj.crs

#The above works for most EPSG codes but as ETRS GK-25 projection 
# is a rather rare one, we still need to make sure that .prj file 
# is having correct coordinate system information. We do that by 
# passing a proj4 dictionary (below) into it (otherwise the .prj 
# file of the Shapefile might be empty):
    
# Pass the coordinate information
data_proj.crs = {'y_0': 0, 'no_defs': True, 'x_0': 25500000, 'k': 1, 'lat_0': 0, 'units': 'm', 'lon_0': 25, 'ellps': 'GRS80', 'proj': 'tmerc'}

# Check that it changed
data_proj.crs

# Ouput file path
outfp = r"/home/geo/addresses_epsg3879.shp"

# Save to disk
data_proj.to_file(outfp)


# -----------------------------------
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, Polygon
import geopy


# Create Point objects
p1 = Point(24.952242, 60.1696017)
p2 = Point(24.976567, 60.1612500)

# Create a Polygon
coords = [(24.950899, 60.169158), (24.953492, 60.169158), (24.953510, 60.170104), (24.950958, 60.169990)]
poly = Polygon(coords)

# Check if p1 is within the polygon using the within function
p1.within(poly)


# Check if p2 is within the polygon
p2.within(poly)

# Our point
print(p1)

# The centroid
print(poly.centroid)

# Does polygon contain p1?
poly.contains(p1)


# Does polygon contain p2?
poly.contains(p2)


#Which one should you use then? Well, it depends:

#if you have many points and just one polygon and you try to find 
# out which one of them is inside the polygon:

# you need to iterate over the points and check one at a time if
# it is within() the polygon specified

#if you have many polygons and just one point and you want to
# find out which polygon contains the point

# you need to iterate over the polygons until you find a polygon
# that contains() the point specified (assuming there are no 
# overlapping polygons)

# INTERSECT

from shapely.geometry import LineString, MultiLineString

# Create two lines
line_a = LineString([(0, 0), (1, 1)])
line_b = LineString([(1, 1), (0, 2)])

line_a.intersects(line_b)
line_a.touches(line_b)


# Create a MultiLineString
multi_line = MultiLineString([line_a, line_b])

# Does the line touch with itself?
line_a.touches(line_a)

# Does the line intersect with itself?
line_a.intersects(line_a)

# so contains, within, intersects, and touches

# -------------------------------------

# Spatial Join

#Luckily, spatial join (gpd.sjoin() -function) is already 
#implemented in Geopandas, thus we do not need to create it 
#ourselves. There are three possible types of join that can be 
#applied in spatial join that are determined with op -parameter:

# "intersects"
# "within"
# "contains"
# Sounds familiar?

import geopandas as gpd

# Filepath - Use https://automating-gis-processes.github.io/2016/Lesson3-spatial-join.html
# to import. 
fp = "/home/geo/Pop15/Vaestotietoruudukko_2015.shp"

# Read the data
pop = gpd.read_file(fp)

# Change the name of a column
pop = pop.rename(columns={'ASUKKAITA': 'pop15'})

# See the column names and confirm that we now have a column called 'pop15'
pop.columns

# Columns that will be sected
In [4]: selected_cols = ['pop15', 'geometry']

# Select those columns
In [5]: pop = pop[selected_cols]

# Let's see the last 2 rows
In [6]: pop.tail(2)

## Join the layers

In [7]: addr_fp = r"/home/geo/addresses_epsg3879.shp"

# Read data
In [8]: addresses = gpd.read_file(addr_fp)

# Check the head of the file
In [9]: addresses.head(2)
Out[9]: 
                                 address    id  \
0  Kampinkuja 1, 00100 Helsinki, Finland  1001   
1   Kaivokatu 8, 00101 Helsinki, Finland  1002   

                                      geometry  
0  POINT (25496123.30852197 6672833.941567578)  
1  POINT (25496774.28242895 6672999.698581985)  

# Check the crs of address points
In [10]: addresses.crs
Out[10]: 
{'ellps': 'GRS80',
 'k': 1,
 'lat_0': 0,
 'lon_0': 25,
 'no_defs': True,
 'proj': 'tmerc',
 'units': 'm',
 'x_0': 25500000,
 'y_0': 0}

# Check the crs of population layer
In [11]: pop.crs
# Do they match? - We can test that
In [12]: addresses.crs == pop.crs

# Make a spatial join
In [13]: join = gpd.sjoin(addresses, pop, how="inner", op="within")

# Let's check the result
In [14]: join.head()

# Make a spatial join
In [13]: join = gpd.sjoin(addresses, pop, how="inner", op="within")

# Let's check the result
In [14]: join.head()

In [15]: import matplotlib.pyplot as plt

# Plot the points with population info
In [16]: join.plot(column='pop15', cmap="Reds", markersize=7, scheme='natural_breaks', legend=True);

# Add title
In [17]: plt.title("Amount of inhabitants living close the the point");

# Remove white space around the figure
In [18]: plt.tight_layout()

