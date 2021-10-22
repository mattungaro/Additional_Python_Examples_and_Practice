# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 21:35:46 2020

@author: 11e
"""
import pandas

import geopandas as gpd

fp = r"C:\Users\11e\Documents\GIS_Helsinki\ch2\Data\DAMSELFISH_distributions.shp"

# Read file using gpd.read_file()
data = gpd.read_file(fp)

type(data)

data.head()

data.plot();

data.crs

# Create a output path for the data

out = r"C:\Users\11e\Documents\GIS_Helsinki\ch2\Data\DAMSELFISH_distributions_SELECTION.shp"

# Select first 50 rows
selection = data[0:50]

# Write those rows into a new Shapefile (the default output file format is Shapefile)
selection.to_file(out)

# It is possible to use only specific columns by specifying the column name within square brackets []
data['geometry'].head()

# Make a selection that contains only the first five rows
selection = data[0:5]


for index, row in selection.iterrows():
    poly_area = row['geometry'].area
    print("Polygon area at index {0} is: {1:.3f}".format(index, poly_area))
   
   # Empty column for area
data['area'] = None

# Iterate rows one at the time
for index, row in data.iterrows():
    # Update the value in 'area' column with area information at index
    data.loc[index, 'area'] = row['geometry'].area
    
data['area'].head(2)
 
max_area = data['area'].max()

# Minimum area
min_area = data['area'].mean()

print("Max area: %s\nMean area: %s" % (round(max_area, 2), round(min_area, 2)))

# Let’s create an empty GeoDataFrame.

# Import necessary modules first
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, Polygon
import fiona

# Create an empty geopandas GeoDataFrame
newdata = gpd.GeoDataFrame()

# Let's see what's inside
newdata

# Create a new column called 'geometry' to the GeoDataFrame
newdata['geometry'] = None

# Let's see what's inside
newdata


# Coordinates of the Helsinki Senate square in Decimal Degrees
coordinates = [(24.950899, 60.169158), (24.953492, 60.169158), (24.953510, 60.170104), (24.950958, 60.169990)]

# Create a Shapely polygon from the coordinate-tuple list
poly = Polygon(coordinates)

# Let's see what we have
poly

# Insert the polygon into 'geometry' -column at index 0
newdata.loc[0, 'geometry'] = poly

# Let's see what we have now
newdata

# Add a new column and insert data
newdata.loc[0, 'Location'] = 'Senaatintori'

# Let's check the data
newdata

print(newdata.crs)

# Import specific function 'from_epsg' from fiona module
from fiona.crs import from_epsg

# Set the GeoDataFrame's coordinate system to WGS84
newdata.crs = from_epsg(4326)
# this makes the shapefile work for WGS84 - like, if you bring it
# into qgis, they'll work when you apply wgs84 to it. However,
# it doesn't hold on to the information for what projected coord.
# system its grabbing.

# Let's see how the crs definition looks like
newdata.crs

# Determine the output path for the Shapefile
outfp = r"C:\Users\11e\Documents\GIS_Helsinki\ch2\Data\Senaatintori.shp"

# Write the data into that Shapefile
newdata.to_file(outfp)

# Group the data by column 'binomial'
grouped = data.groupby('BINOMIAL')

# Let's see what we got
grouped

# Iterate over the group object
for key, values in grouped:
       individual_fish = values
   

# Let's see what is the LAST item that we iterated
individual_fish

type(individual_fish)

print(key)

# Determine outputpath
outFolder = r"/home/geo/Data"

import os
# Create a new folder called 'Results' (if does not exist) to that folder using os.makedirs() function
resultFolder = os.path.join(outFolder, 'Results')
if not os.path.exists(resultFolder):
    os.makedirs(resultFolder)

# Iterate over the
for key, values in grouped:
    # Format the filename (replace spaces with underscores)
    outName = "%s.shp" % key.replace(" ", "_")

    # Print some information for the user
    print("Processing: %s" % key)

    # Create an output path
    outpath = os.path.join(resultFolder, outName)

    # Export the data
    values.to_file(outpath)
    
