# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in

import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import folium
from folium import plugins
import os
import json
import requests
# from folium.plugins import MeasureControl
# from folium.plugins import FloatImage
# from folium.plugins import HeatMap

# test data for vincent/vega and altair/vegalite markers:
url = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data'
vis1 = json.loads(requests.get(f'{url}/vis1.json').text)
vis2 = json.loads(requests.get(f'{url}/vis2.json').text)
vis3 = json.loads(requests.get(f'{url}/vis3.json').text)


#df_traffic = pd.read_csv('../input/ukTrafficAADF.csv')
# df_acc = pd.read_csv('accidents_2005_to_2007.csv', dtype=object)

t_list = ["Stamen Terrain", "Stamen Toner", "MapQuest Open Aerial"]
tea_map = folium.Map(location=[6.957236, 80.618474],
                     tiles=t_list[0],
                     zoom_start=13)

# Adds tool to the top right
tea_map.add_child(plugins.MeasureControl())

# Add logo or image
img_path = ('sheflogo.png')
plugins.FloatImage(img_path, bottom=5, left=5).add_to(tea_map)

# for Heat Maps:
# # Ensure you're handing it floats
# df_acc['Latitude'] = df_acc['Latitude'].astype(float)
# df_acc['Longitude'] = df_acc['Longitude'].astype(float)

# # Filter the DF for rows, then columns, then remove NaNs
# heat_df = df_acc[df_acc['Speed_limit']=='30'] # Reducing data size so it runs faster
# heat_df = heat_df[heat_df['Year']=='2007'] # Reducing data size so it runs faster
# heat_df = heat_df[['Latitude', 'Longitude']]
# # drop rows with null values using .dropna():
# # more info: https://www.geeksforgeeks.org/python-pandas-dataframe-dropna/
# heat_df = heat_df.dropna(axis=0, subset=['Latitude','Longitude'])

# # List comprehension to make out list of lists
# heat_data = [[row['Latitude'],row['Longitude']] for index, row in heat_df.iterrows()]
# print(heat_data)
# Plot it on the map
# HeatMap([[6.960031, 80.617387]]).add_to(tea_map)
# the above shows that the heat map just shows "heat" as s function
# of how many times a particular lat/lon is in the list passed into
# the HeatMap() function.

# Marker clusters: could be used to show estates, or
# maybe the OFDs on any one estate, or both!
mcg = folium.plugins.MarkerCluster(control=False, options={
                                   "disableClusteringAtZoom": 14, "maxClusterRadius": 100, "zoomToBoundsOnClick": True, "spiderfyOnMaxZoom": False})
tea_map.add_child(mcg)

# define layer groups:
lndmrks = folium.plugins.FeatureGroupSubGroup(tea_map, 'Landmarks')
tea_map.add_child(lndmrks)
OFDs = folium.plugins.FeatureGroupSubGroup(tea_map, 'On Field Sensors')
tea_map.add_child(OFDs)
Radii = folium.plugins.FeatureGroupSubGroup(mcg, 'Sensor Radii')
tea_map.add_child(Radii)
sensor_hMap = folium.plugins.FeatureGroupSubGroup(tea_map, 'Sensor Heat Map')
tea_map.add_child(sensor_hMap)
dat_grphs = folium.plugins.FeatureGroupSubGroup(
    tea_map, 'Vega/Altair Data Visualisations')
tea_map.add_child(dat_grphs)

# landmark markers:
folium.Marker([6.960031, 80.617387],
              popup='Mount Vernon Tea Factory',
              icon=folium.Icon(color='blue', icon='university', prefix='fa')).add_to(lndmrks)
folium.Marker([6.957236, 80.618474],
              popup="Mount Vernon Estate",
              icon=folium.Icon(color="green", icon="leaf")).add_to(lndmrks),

# random markers to represent OFDs:
N = 25
data = np.array(
    [
        # Random latitudes in Europe.
        np.random.uniform(low=6.941236, high=6.960031, size=N),
        # Random longitudes in Europe.
        np.random.uniform(low=80.607387, high=80.620474, size=N)
    ]
)
popups = [str(i) for i in range(N)]  # Popups texts are simple numbers.

# m = folium.Map([45, 3], zoom_start=4)
plugins.MarkerCluster(data, popups=popups, options={
                      "disableClusteringAtZoom": 14, "maxClusterRadius": 100, "zoomToBoundsOnClick": True, "spiderfyOnMaxZoom": False}).add_to(OFDs)

datalist = data.tolist()
for row in datalist:
    # use Circle instead of CircleMarker for radius in meters:
    folium.Circle(
        radius=75,
        location=row,
        popup='This is the sensing radius',
        color='#3186cc',
        fill=True,
        fill_color='#3186cc'
    ).add_to(Radii)


# test markers for vega/altair visualization:
folium.Marker(
    location=[6.942236, 80.615474],
    icon=folium.Icon(color='blue', icon='bar-chart',
                     prefix='fa'),
    popup=folium.Popup(max_width=500).add_child(
        folium.Vega(vis1, width=500, height=250))
).add_to(dat_grphs)

folium.Marker(
    location=[6.941506, 80.619474],
    icon=folium.Icon(color='blue', icon='bar-chart',
                     prefix='fa'),
    popup=folium.Popup(max_width=500).add_child(
        folium.Vega(vis2, width=500, height=250))
).add_to(dat_grphs)

folium.Marker(
    location=[6.942936, 80.610974],
    icon=folium.Icon(color='blue', icon='bar-chart',
                     prefix='fa'),
    popup=folium.Popup(max_width=500).add_child(
        folium.Vega(vis3, width=500, height=250))
).add_to(dat_grphs)

plugins.HeatMap(datalist).add_to(sensor_hMap)

# add layer control:
folium.LayerControl(collapsed=True).add_to(tea_map)

# enable lat/lon popovers for convenience
tea_map.add_child(folium.LatLngPopup())

# vector drawing
plugins.Draw(
    export=False,
    filename='my_data.geojson',
    position='topleft',
    draw_options={'polyline': {'allowIntersection': False}},
    edit_options={'poly': {'allowIntersection': False}}
).add_to(tea_map)

# m.save(os.path.join('results', 'Plugins_1.html'))

tea_map.save("tea_map.html")
print("...all done..!")
