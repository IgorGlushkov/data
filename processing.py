import pydeck as pdk
import pandas as pd
import numpy as np
import geopandas as gpd

# Generate sample data around Bikini Atoll
# Center coordinates: 11.62°N, 165.27°E
islands = gpd.read_file("bikini.shp").to_crs(epsg=4326)

# ——— 3) DEFINE LAYERS ———
island_layer = pdk.Layer(
    "GeoJsonLayer",
    data=islands.__geo_interface__,
    stroked=True,
    filled=True,
    extruded=True,
    get_elevation=5,            # little slab so islands show in 3D
    get_fill_color=[200, 200, 200, 180],
    get_line_color=[50, 50, 50],
    pickable=False
)

data = gpd.read_file("RMI_GEoradis_Mai.shp")
data=data[['Longitude','Latitude','Dose rate']]
data['Elevation']=data['Dose rate']

geojson = pdk.Layer(
    'GeoJsonLayer',
    'data.geojson',
    opacity=0.8,
    stroked=False,
    filled=True,
    extruded=True,
    wireframe=True,
    get_elevation='properties.Elevation*100',
    get_fill_color='[255, 255, properties.growth * 255]',
    get_line_color=[255, 255, 255],
    pickable=True
)

# Create the layer
layer = pdk.Layer(
    'HexagonLayer',
    data,
    get_position=['Longitude', 'Latitude'],
    auto_highlight=True,
    elevation_scale=100,  # Adjusted for the small elevation values
    pickable=True,
    elevation_range=[min(data['Elevation']), max(data['Elevation'])],  # Adjusted for the elevation range of atolls
    extruded=True,
    coverage=1,
    radius=10  # Size of hexagons in meters
)

# Set the viewport location centered on Bikini Atoll
view_state = pdk.ViewState(
    longitude=165.27,  # Bikini Atoll longitude
    latitude=11.62,    # Bikini Atoll latitude
    zoom=12,          # Closer zoom to see the atoll
    min_zoom=9,
    max_zoom=15,
    pitch=45,         # Adjusted for better 3D view
    bearing=0
)

# Create and render the deck
deck = pdk.Deck(
    layers=[geojson],
    initial_view_state=view_state,
)

# Save to HTML
deck.to_html('bikini-atoll-3d.html', notebook_display=False)

# If you want to see the first few rows of generated data:
print("Sample of generated data:")
print(data.head())
