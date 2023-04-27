#!/usr/bin/env python3

import pandas as pd
import geopandas as gpd
import time

# read in GeoJSON files (reduce years for testing because the whole decade takes a while)
datasets = [gpd.read_file('data/311_City_Service_Requests_in_%i.geojson' % year)
            for year in range(2022, 2024)]

print('files read in')

# create a dataframe of just the TSI requests
request_data = pd.concat(datasets)

request_data[request_data.SERVICECODEDESCRIPTION.str.contains('Public Space Litter')][['SERVICECODEDESCRIPTION', 'SERVICECODE']].value_counts()
request_data[['SERVICECODEDESCRIPTION', 'SERVICECODE', 'ADDDATE', 'RESOLUTIONDATE']].sort_values('ADDDATE')


# create an add_date column
request_data['add_date'] = request_data.ADDDATE.str.slice(stop=10)

# create an and_date column
request_data['end_date'] = request_data.RESOLUTIONDATE.str.slice(stop=10)

can_install_data = request_data[request_data.SERVICECODE == 'LCANINS']
pd.crosstab(can_install_data.add_date, can_install_data.end_date)

old_req_data = request_data[request_data.SERVICECODE == 'S0216']

