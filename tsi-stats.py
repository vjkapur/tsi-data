#!/usr/bin/env python3

import pandas as pd
import geopandas as gpd
import time

print('reading in data files; could take a while')

# read in GeoJSON files (reduce years for testing because the whole decade takes a while)
datasets = [gpd.read_file('data/311_City_Service_Requests_in_%i.geojson' % year)
            for year in range(2013, 2024)]

print('files read in')

# create a dataframe of just the TSI requests
tsi_311_data = pd.concat(datasets)
tsi_311_data = tsi_311_data[tsi_311_data.SERVICECODE == 'SPSTDAMA']

print('data combined')

# date attributes and their corresponding number of characters within the ADDDATE attribute
date_attrs = {'year': 4, 'month': 7, 'date': 10}

# exporting CSVs of counts
for target_attr in date_attrs:
    tsi_311_data[target_attr] = tsi_311_data.ADDDATE.str.slice(stop=date_attrs[target_attr])
    tsi_311_data[target_attr].value_counts(dropna=False).to_csv('tsi_counts_by_%s.csv'%target_attr, header=True, index=True)

# rolling 7-day count
tsi_311_data.date.value_counts().sort_index().rolling(7).sum().to_csv('tsi_counts_by_7day.csv', header=True)