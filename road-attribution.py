#!/usr/bin/env python3

import geopandas as gpd

bike_lanes = gpd.read_file("data/Bicycle_Lanes.geojson")
roadway_blocks = gpd.read_file("data/Roadway_Block.geojson")

# projecting to miles
ECKERT_IV_PROJ4_STRING = "+proj=eck4 +lon_0=0 +x_0=0 +y_0=0 +datum=WGS84 +units=mi +no_defs"
bike_lanes_eckert4 = bike_lanes.to_crs(ECKERT_IV_PROJ4_STRING)
roadway_blocks_eckert4 = roadway_blocks.to_crs(ECKERT_IV_PROJ4_STRING)

# creating attributes for geometry length/area
bike_lanes_eckert4['geolength'] = bike_lanes_eckert4.geometry.length
roadway_blocks_eckert4['geolength'] = roadway_blocks_eckert4.geometry.length

bike_lanes_eckert4['geolength_feet'] = bike_lanes_eckert4.geometry.length * 5280
roadway_blocks_eckert4['geolength_feet'] = roadway_blocks_eckert4.geometry.length * 5280

bike_lanes_eckert4['area_feet'] = bike_lanes_eckert4.geolength_feet * bike_lanes_eckert4.TOTALBIKELANEWIDTH
bike_lanes_eckert4['area_miles'] = bike_lanes_eckert4.area_feet / 27878400

roadway_blocks_eckert4['area_feet'] = roadway_blocks_eckert4.geolength_feet * roadway_blocks_eckert4.TOTALCROSSSECTIONWIDTH
roadway_blocks_eckert4['area_miles'] = roadway_blocks_eckert4.area_feet / 27878400

# getting the sum of length by existing ward attribute
# bike_lanes_eckert4.groupby(['WARD_ID']).geolength.sum()
# roadway_blocks_eckert4.groupby(['WARD_ID']).geolength.sum()