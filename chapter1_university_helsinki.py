# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 21:58:05 2020

@author: 11e
"""
#https://automating-gis-processes.github.io/2016/Lesson1-Geometric-Objects.html

from shapely.geometry import Point, LineString, Polygon

point1 = Point(2.2, 4.2)
point2 = Point(7.2, -25.1)
point3 = Point(9.26, -2.456)
point3D = Point(9.26, -2.456, 0.57)
point_type = type(point1)

#We can see that the type of the point is shapely’s Point 
#which is represented in a specific format that is based on 
# GEOS C++ library that is one of the standard libraries in 
# GIS. It runs under the hood e.g. in Quantum GIS. 3D-point
# can be recognized from the capital Z -letter in front of 
# the coordinates.

point_coords = point1.coords
type(point_coords)

xy = point_coords.xy
x = point1.x
y = point1.y

print(xy)
# Calculate the distance between point1 and point2
point_dist = point1.distance(point2)
# the returned distance is based on the projection of the 
# points (degrees in WGS84, meters in UTM)

# create lines
line = LineString([point1, point2, point3])
print(line)

#We can extract the coordinates of a LineString similarly as with Point

lxy = line.xy
print(lxy)
# Okey, we can see that the coordinates are again stored as a
# numpy arrays where first array includes all x-coordinates 
# and the second all the y-coordinates respectively.

line_x = lxy[0]
line_y = lxy[1]
print(line_x)
print(line_y)

# get length of line
l_length = line.length

# Get the centroid of the line
l_centroid = line.centroid


centroid_type = type(l_centroid)

# Print the outputs
print("Length of our line: {0:.2f}".format(l_length))
# Length of our line: 52.46

print("Centroid of our line: ", l_centroid)
#Centroid of our line:  POINT (6.229961354035622 -11.89241115757239)

print("Type of the centroid:", centroid_type)
# Type of the centroid: <class 'shapely.geometry.point.Point'>


# polygons

# Create a Polygon from the coordinates
poly = Polygon([(2.2, 4.2), (7.2, -25.1), (9.26, -2.456)])

# We can also use our previously created Point objects (same outcome)
# --> notice that Polygon object requires x,y coordinates as input
poly2 = Polygon([[p.x, p.y] for p in [point1, point2, point3]])

# Geometry type can be accessed as a String
poly_type = poly.geom_type

# Using the Python's type function gives the type in a different format
poly_type2 = type(poly)

# Let's see how our Polygon looks like
print(poly)
#POLYGON ((2.2 4.2, 7.2 -25.1, 9.26 -2.456, 2.2 4.2))

print("Geometry type as text:", poly_type)
print("Geometry how Python shows it:", poly_type2)

# Let's create a bounding box of the world and make a hole in it
# First we define our exterior
world_exterior = [(-180, 90), (-180, -90), (180, -90), (180, 90)]

# Let's create a single big hole where we leave ten decimal degrees at the boundaries of the world
# Notice: there could be multiple holes, thus we need to provide a list of holes
hole = [[(-170, 80), (-170, -80), (170, -80), (170, 80)]]

# World without a hole
world = Polygon(shell=world_exterior)

# Now we can construct our Polygon with the hole inside
world_has_a_hole = Polygon(shell=world_exterior, holes=hole)

# Get the centroid of the Polygon
world_centroid = world.centroid

# Get the area of the Polygon
world_area = world.area

# Get the bounds of the Polygon (i.e. bounding box)
world_bbox = world.bounds

# Get the exterior of the Polygon
world_ext = world.exterior

# Get the length of the exterior
world_ext_length = world_ext.length

# EXTRAS

# Geometry collections can be constructed in a following manner:

from shapely.geometry import MultiPoint, MultiLineString, MultiPolygon, box

# Create a MultiPoint object of our points 1,2 and 3
multi_point = MultiPoint([point1, point2, point3])

# It is also possible to pass coordinate tuples inside
multi_point2 = MultiPoint([(2.2, 4.2), (7.2, -25.1), (9.26, -2.456)])

# We can also create a MultiLineString with two lines
line1 = LineString([point1, point2])

line2 = LineString([point2, point3])

multi_line = MultiLineString([line1, line2])

# MultiPolygon can be done in a similar manner
# Let's divide our world into western and eastern hemispheres with a hole on the western hemisphere
# --------------------------------------------------------------------------------------------------
# Let's create the exterior of the western part of the world
west_exterior = [(-180, 90), (-180, -90), (0, -90), (0, 90)]

# Let's create a hole --> remember there can be multiple holes, thus we need to have a list of hole(s).
# Here we have just one.
west_hole = [[(-170, 80), (-170, -80), (-10, -80), (-10, 80)]]

# Create the Polygon
west_poly = Polygon(shell=west_exterior, holes=west_hole)

# Let's create the Polygon of our Eastern hemisphere polygon using bounding box
# For bounding box we need to specify the lower-left corner coordinates and upper-right coordinates
min_x, min_y = 0, -90
max_x, max_y = 180, 90

# Create the polygon using box() function
east_poly_box = box(minx=min_x, miny=min_y, maxx=max_x, maxy=max_y)

# Let's create our MultiPolygon. We can pass multiple Polygon -objects into our MultiPolygon as a list
multi_poly = MultiPolygon([west_poly, east_poly_box])

# Convex Hull of our MultiPoint --> https://en.wikipedia.org/wiki/Convex_hull
convex = multi_point.convex_hull

# How many lines do we have inside our MultiLineString?
lines_count = len(multi_line)

# Let's calculate the area of our MultiPolygon
multi_poly_area = multi_poly.area

# We can also access different items inside our geometry collections. We can e.g. access a single polygon from
# our MultiPolygon -object by referring to the index
# Let's calculate the area of our Western hemisphere (with a hole) which is at index 0
west_area = multi_poly[0].area

# We can check if we have a "valid" MultiPolygon. MultiPolygon is thought as valid if the individual polygons
# does notintersect with each other. Here, because the polygons have a common 0-meridian, we should NOT have
# a valid polygon. This can be really useful information when trying to find topological errors from your data
valid = multi_poly.is_valid