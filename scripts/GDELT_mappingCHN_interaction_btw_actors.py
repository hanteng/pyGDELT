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

df_geo=df_working[['a1_geo_lat', 'a1_geo_long','a2_geo_lat', 'a2_geo_long']]   #--> select all lat and long geographic coordinates of actors 1 and 2

interaction_counts = defaultdict(int)  # Defaultdict with (lat, long) as key
interaction_counts_na = 0
for index, row in df_geo.iterrows():
    try:
        interaction_counts[((float(row['a1_geo_lat']), float(row['a1_geo_long'])),(float(row['a2_geo_lat']), float(row['a2_geo_long'])))] += 1
    except:
        interaction_counts_na+=1
        pass
print "Total data points without proper geographic coordinates: {0}".format( interaction_counts_na )

# Get some summary statistics
import numpy as np
counts = np.array(interaction_counts.values())
print "Total data points (pairs of interaction between actor 1 and 2: {0}".format( len(counts) )
print "Min events: {0}".format( counts.min() )
print "Max events: {0}".format( counts.max() )
print "Mean events: {0}".format( counts.mean() )
print "Median points: {0}".format( np.median(counts) )


max_val = np.log10(counts.max())

def get_alpha(count):
    ##  Convert a count to an alpha val.
    ##  Log-scaled
    scale = np.log10(count)
    return (scale/max_val) * 0.33


# Note that we're drawing on a regular matplotlib figure, so we set the 
# figure size just like we would any other.
plt.figure(figsize=(12,12))

# Create the Basemap
event_map = Basemap(projection='merc', 
                    resolution='l', area_thresh=1000.0, # Low resolution
                    lat_0 = 0, lon_0=103.5, # Map center of China 35°50'41"N 103°27'08"E #lat_0 = 55.0, lon_0=60.0, # Map center of Russia
                    #lat_0 = 36.0, lon_0=103.5, # Map center of China 35°50'41"N 103°27'08"E #lat_0 = 55.0, lon_0=60.0, # Map center of Russia
                    llcrnrlon=-180, llcrnrlat=-60, # Lower left corner
                    urcrnrlon=180, urcrnrlat=75) # Upper right corner

# Draw important features
# Very time-consuming for event_map.shadedrelief()
#event_map.shadedrelief()
event_map.drawcoastlines(linewidth=0.1)             # better commented when shadedrelief() is active
event_map.drawcountries()
event_map.fillcontinents(color='0.9', lake_color='0.9')  # Light gray, # better commented when shadedrelief() is active
event_map.drawmapboundary()


# Draw the points on the map:
for arc, count in interaction_counts.iteritems():
    point1, point2 = arc
    y1, x1 = point1
    y2, x2 = point2

##    if x1<-30:
##        x1=x1+360
##    if x2<-30:
##        x2=x2+360
        
    # Only plot lines where both points are on our map:
    if ((y1 > -60 and y1 < 75) and (y2 > -60 and y2 < 75)):
        line_alpha = get_alpha(count)
        #line, =
        event_map.drawgreatcircle(x1, y1, x2, y2, linewidth=3, color='r', alpha=line_alpha)
'''
        p = line.get_path()
        # find the index which crosses the dateline (the delta is large)
        cut_point = np.where(np.abs(np.diff(p.vertices[:, 0])) > 200)[0]
        if cut_point:
            cut_point = cut_point[0]
            # create new vertices with a nan inbetween and set those as the path's vertices
            new_verts = np.concatenate(
                                       [p.vertices[:cut_point, :], 
                                        [[np.nan, np.nan]], 
                                        p.vertices[cut_point+1:, :]]
                                       )
            p.codes = None
            p.vertices = new_verts
'''            

# ==PREPARING==
import os
path_local_script = os.path.dirname(os.path.realpath(__file__))
path_local_map = os.path.abspath(os.path.join(path_local_script, os.pardir, "map"))

plt.savefig(os.path.join(path_local_map, "event_maps_interact_CHN.png"),bbox_inches='tight')  # or event_maps_CHN.tiff
