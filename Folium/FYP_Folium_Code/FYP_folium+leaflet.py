import folium

# create map object
m = folium.Map(location=(42.3601, -71.0589), zoom_start=12)

# global tooltip variable
tooltip = "Click for more info"

# create a custom marker
logoIcon = folium.features.CustomIcon('logo.png', icon_size=(50, 50))

# create markers
marker1 = folium.Marker([42.363600, -71.099500],
                        popup="</strong>this is more info. Any HTML can go here<strong>",
                        tooltip=tooltip)
marker1.add_to(m)

folium.Marker([42.363600, -71.109500],
              popup="</strong>demo for cloud icon<strong>",
              tooltip=tooltip,
              icon=folium.Icon(icon="cloud")).add_to(m)
folium.Marker([42.377120, -71.062400],
              popup="</strong>demo for icon colour<strong>",
              tooltip=tooltip,
              icon=folium.Icon(color="purple")).add_to(m)
folium.Marker([42.377120, -71.1222410],
              popup="</strong>demo for different icon<strong>",
              tooltip=tooltip,
              icon=folium.Icon(color="green", icon="leaf")).add_to(m),
folium.Marker([42.363600, -71.1522410],
              popup="</strong>demo for custom icon<strong>",
              tooltip=tooltip,
              icon=logoIcon).add_to(m)

# create a circle marker
folium.CircleMarker(
    location=[42.466470, -70.942110],
    radius=50,
    popup='Area Marker',
    colour='#830bff',
    fill=True,
    fill_color='#830bff'
).add_to(m)

# choropleth maps are what you want to use for colour/grid overlays
# for example:
# m.choropleth(
#     geo_data = some_datapoints,
#     name = 'choropleth',
#     data = the_sensordata
#     key_on = 'the_featureID',
#     fill_color = 'YlGn',
#     fill_opacity =  0.7,
#     line_opacity = 0.2,
#     legend_name = 'some_name'
# )
# folium.Layer_Conrtol().add_to(m)

# example functions:


# generate map
m.save("map.html")
