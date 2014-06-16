#!/usr/bin/env python
# -*- coding: utf-8 -*-
#歧視無邊，回頭是岸。鍵起鍵落，情真情幻。
# Adapted from http://nbviewer.ipython.org/github/dmasad/GDELT_Intro/blob/master/GDELT_Mapping.ipynb

import datetime as dt
from collections import defaultdict

import matplotlib.pyplot as plt

from mpl_toolkits.basemap import Basemap

# Getting all CHN-related events directly from the working tsv file
import GDELT_easy
df_working =GDELT_easy.load()
# df_working.columns                                --> list all column labels
# df_geo.ix[:3]                                     --> first three rows

df_geo=df_working[['ac_geo_lat', 'ac_geo_long']]   #--> select all lat and long geographic coordinates

point_counts = defaultdict(int) # Defaultdict with (lat, long) as key
point_counts_na = 0
for index, row in df_geo.iterrows():
    try:
        pair=(float(row['ac_geo_lat']), float(row['ac_geo_long']))
        point_counts[pair] += 1
    except:
        point_counts_na+=1
        pass
print "Total data points without proper geographic coordinates: {0}".format( point_counts_na )

# Get some summary statistics
import numpy as np
counts = np.array(point_counts.values())
print "Total data points: {0}".format( len(counts) )
print "Min events: {0}".format( counts.min() )
print "Max events: {0}".format( counts.max() )
print "Mean events: {0}".format( counts.mean() )
print "Median points: {0}".format( np.median(counts) )


def get_size(count):
    ##Convert a count to a point size.
    ##Log-scaled.
    scale_factor = 2
    return np.log10(count + 1) * scale_factor

# Note that we're drawing on a regular matplotlib figure, so we set the 
# figure size just like we would any other.
plt.figure(figsize=(12,12))

# Create the Basemap
event_map = Basemap(projection='merc', 
                    resolution='l', area_thresh=1000.0, # Low resolution
                    lat_0 = 0, lon_0=103.5, # Map center of China 35°50'41"N 103°27'08"E #lat_0 = 55.0, lon_0=60.0, # Map center of Russia
                    #lat_0 = 36.0, lon_0=103.5, # Map center of China 35°50'41"N 103°27'08"E #lat_0 = 55.0, lon_0=60.0, # Map center of Russia
                    llcrnrlon=-30, llcrnrlat=-60, # Lower left corner
                    urcrnrlon=330, urcrnrlat=75) # Upper right corner

# Draw important features
# Very time-consuming for event_map.shadedrelief()
#event_map.shadedrelief()
event_map.drawcoastlines(linewidth=0.1)             # better commented when shadedrelief() is active
event_map.drawcountries()
event_map.fillcontinents(color='0.9', lake_color='0.9')  # Light gray, # better commented when shadedrelief() is active
event_map.drawmapboundary()


# Draw the points on the map:
for point, count in point_counts.iteritems():

    if point[1]<-30:
        x, y = event_map(point[1]+360, point[0]) # Convert lat, long to y,x
    else:
        x, y = event_map(point[1], point[0]) # Convert lat, long to y,x
    
    marker_size = get_size(count) * 3                            #x3: slighly bigger on the world map
    event_map.plot(x,y, 'ro', markersize=marker_size, alpha=0.5) #alpha:  http://zh.wikipedia.org/wiki/RGBA 
    

# ==PREPARING==
import os
path_local_script = os.path.dirname(os.path.realpath(__file__))
path_local_map = os.path.abspath(os.path.join(path_local_script, os.pardir, "map"))

plt.savefig(os.path.join(path_local_map, "event_maps_CHN.png"),bbox_inches='tight')  # or event_maps_CHN.tiff
