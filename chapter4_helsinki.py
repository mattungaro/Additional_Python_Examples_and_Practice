# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 21:09:00 2020

@author: 11e
"""
# Overlay analysis


import geopandas as gpd

import descartes

import matplotlib.pyplot as plt

# File paths
border_fp = r"C:\Users\11e\Documents\GIS_Helsinki\ch4\data\Helsinki_borders.shp"
grid_fp = r"C:\Users\11e\Documents\GIS_Helsinki\ch4\data\TravelTimes_to_5975375_RailwayStation.shp"

# Read files
grid = gpd.read_file(grid_fp)
hel = gpd.read_file(border_fp)

hel.crs
grid.crs

basemap = hel.plot()

grid.plot(ax=basemap, linewidth=0.02); # makes helsinki plot the 
# basemap. Weird way to do this. So they are just on top of each 
# other.

# Use tight layout
plt.tight_layout()


result = gpd.overlay(grid, hel, how='intersection')
# the intersection - therefore just keeps what's within both
# also, union; identity; symmetric_difference; difference

result.plot(color="b")
# Use tight layout
plt.tight_layout() # recall that you need to run this and the previous


result.head()


len(result)


len(grid)


resultfp = r"C:\Users\11e\Documents\GIS_Helsinki\ch4\data\TravelTimes_to_5975375_RailwayStation_Helsinki.geojson"

# Use GeoJSON driver
result.to_file(resultfp, driver="GeoJSON")

## Aggregating data

# Aggregating data can also be useful sometimes. What we mean by aggregation
# is that we basically merge Geometries together by some common 
# identifier. Suppose we are interested in studying continents, but we only 
# have country-level data like the country dataset. By aggregation we would 
# convert this into a continent-level dataset.

# Let’s aggregate our travel time data by car travel times, i.e. the grid cells
# that have the same travel time to Railway Station will be merged together.
result_aggregated = result.dissolve(by="car_r_t")

# the argument used is defaulting to aggfunc = "first" as seen in the link below.
# Not really what I would have done to aggregate. I would have summed them
# That's also functions:

# ‘last’
# 
# ‘min’
# 
# ‘max’
# 
# ‘sum’
# 
# ‘mean’
# 
# ‘median’
#

# https://geopandas.org/aggregation_with_dissolve.html


result_attempt = result.dissolve(by ="car_r_t", aggfunc = "median")
# hey that worked! my hypothesis was correct.

# -------------------------------------------------------------

# Data Reclassification

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

fp = r"C:\Users\11e\Documents\GIS_Helsinki\ch4\data\Corine2012_Uusimaa.shp"

data = gpd.read_file(fp)

data.head(2)

selected_cols = ['Level1', 'Level1Eng', 'Level2', 'Level2Eng', 'Level3', 'Level3Eng', 'Luokka3', 'geometry']

data = data[selected_cols]

data.columns

data.plot(column='Level3', linewidth=0.05)

list(data['Level3Eng'].unique())
# gets unique entries for the column Level3Eng
lakes = data.loc[data['Level3Eng'] == 'Water bodies'].copy()
# ix didn't work - used loc
lakes.head(2)

# Calculations in DataFrames

# Okey now we have our lakes dataset ready. The aim
# was to classify those lakes into small and big 
# lakes based on the average size of all lakes in 
# our study area. Thus, we need to calculate the 
# average size of our lakes.

data.crs

# Calculate the area of lakes
lakes['area'] = lakes.area

# What do we have?
lakes['area'].head(2)

lakes['area_km2'] = lakes['area'] / 1000000

# What is the mean size of our lakes?
l_mean_size = lakes['area_km2'].mean()

l_mean_size

# note = extra stuff

# Sum two columns
data['sum_of_columns'] = data['col_1'] + data['col_2']

# Calculate the difference of three columns
data['difference'] = data['some_column'] - data['col_1'] + data['col_2']

# =============================================================================
# 
# Classifying data
# Creating a custom classifier
# Let’s create a function where we classify the 
# geometries into two classes based on a given 
# threshold -parameter. If the area of a polygon 
# is lower than the threshold value (average size
# of the lake), the output column will get a value
#  0, if it is larger, it will get a value 1. This
#  kind of classification is often called a binary
#  classification.
# 
# First we need to create a function for our classification 
# task. This function takes a single row of the GeoDataFrame 
# as input, plus few other parameters that we can use.
#
def binaryClassifier(row, source_col, output_col, threshold):
    # If area of input geometry is lower that the threshold value
    if row[source_col] < threshold:
        # Update the output column with value 0
        row[output_col] = 0
    # If area of input geometry is higher than the threshold value update with value 1
    else:
        row[output_col] = 1
    # Return the updated row
    return row

# Lets create a new column 

lakes['small_big'] = None

lakes = lakes.apply(binaryClassifier, 
                    source_col='area_km2', 
                    output_col='small_big', 
                    threshold=l_mean_size, axis=1)

plt.rcParams["figure.dpi"] = 144

plt.rcParams["figure.dpi"] = 216 # this is the best dpi setting, imo.
# this is needed for future python work

lakes.plot(column='small_big', linewidth=0.05, cmap="seismic")
plt.tight_layout()
plt.legend(loc = "upper left") # this doesn't seem to work


# Multicriteria data classification


def customClassifier2(row, src_col1, src_col2, threshold1, threshold2, 
                      output_col):
    # 1. If the value in src_col1 is LOWER than the threshold1 value
    # 2. AND the value in src_col2 is HIGHER than the threshold2 value,
    # give value 1, otherwise give 0
    if row[src_col1] < threshold1 and row[src_col2] > threshold2:
        # Update the output column with value 0
        row[output_col] = 1
    # If area of input geometry is higher than the threshold value update with value 1
    else:
        row[output_col] = 0

    # Return the updated row
    return row



fp = r"C:\Users\11e\Documents\GIS_Helsinki\ch4\data\TravelTimes_to_5975375_RailwayStation_Helsinki.geojson"

# Read the GeoJSON file similarly as Shapefile
acc = gpd.read_file(fp)

# Let's see what we have
acc.head(2)

# =============================================================================
# Okey we have plenty of different variables (see from here the description 
#                                             for all attributes) but 
# what we are interested in are columns called pt_r_tt which is telling
#  the time in minutes that it takes to reach city center from different 
#  parts of the city, and walk_d that tells the network distance by 
#  roads to reach city center from different parts of the city (almost 
#  equal to Euclidian distance).
# 
# The NoData values are presented with value -1. Thus we need to remove 
# those first.
# =============================================================================

acc = acc.loc[acc['pt_r_tt'] >=0]


# =============================================================================
# Okey so from this figure we can see that the travel times are lower 
# in the south where the city center is located but there are some areas 
# of “good” accessibility also in some other areas (where the color is red).
# 
# Let’s also make a plot about walking distances
# =============================================================================

acc.plot(column="walk_d", scheme="Fisher_Jenks", k=9, cmap="RdYlBu", linewidth=0);

# Use tight layour
plt.tight_layout();

# =============================================================================
# Okey, from here we can see that the walking distances (along road network) 
# reminds more or less Euclidian distances.
# 
# Let’s finally do our classification based on two criteria and find 
# out grid cells where the travel time is lower or equal to 20 minutes 
# but they are further away than 4 km (4000 meters) from city center.
# 
# Let’s create an empty column for our classification results called 
# “Suitable_area”.
# =============================================================================

acc["Suitable_area"] = None

acc = acc.apply(customClassifier2, 
                         src_col1='pt_r_tt', src_col2='walk_d', 
                         threshold1=20, threshold2=4000, 
                         output_col="Suitable_area", axis=1)

acc.head()

acc['Suitable_area'].value_counts()


# Plot
acc.plot(column="Suitable_area", linewidth=0);

# Use tight layour
plt.tight_layout();


# =============================================================================
# Classification based on common classifiers
# Pysal -module is an extensive Python library including various 
# functions and tools to do spatial data analysis. It also includes 
# all of the most common data classifiers that are used commonly e.g. 
# when visualizing data. Available map classifiers in pysal -module 
# are (see here for more details):
# 
# Box_Plot
# Equal_Interval
# Fisher_Jenks
# Fisher_Jenks_Sampled
# HeadTail_Breaks
# Jenks_Caspall
# Jenks_Caspall_Forced
# Jenks_Caspall_Sampled
# Max_P_Classifier
# Maximum_Breaks
# Natural_Breaks
# Quantiles
# Percentiles
# Std_Mean
# User_Defined
# Let’s apply one of those classifiers into our data and classify the 
# travel times by public transport into 9 classes.
# 
# =============================================================================

import pysal as ps
import mapclassify


# Define the number of classes
n_classes = 9

#The classifier needs to be initialized first with make() function that takes
# the number of desired classes as input parameter.

# Create a Natural Breaks classifier
classifier = mapclassify.NaturalBreaks.make(k=n_classes)
# matt - had to modify this last command a bit
# Now we can apply that classifier into our data quite similarly as in 
# our previous examples.

# Classify the data
classifications = acc[['pt_r_tt']].apply(classifier)

# Let's see what we have
classifications.head()

# Okey, so we have a DataFrame where our input column was classified
# into 9 different classes (numbers 1-9) based on Natural Breaks classification.

# Now we want to join that reclassification into our original data 
# but let’s first rename the column so that we recognize it later on.

# Rename the column so that we know that it was classified with natural breaks
classifications.columns = ['nb_pt_r_tt']

# Join with our original data (here index is the key
acc = acc.join(classifications)

# Let's see how our data looks like
acc.head()

# Great, now we have those values in our accessibility GeoDataFrame. 
# Let’s visualize the results and see how they look.

# Plot
acc.plot(column="nb_pt_r_tt", linewidth=0, legend=True);

# Use tight layour
plt.tight_layout()