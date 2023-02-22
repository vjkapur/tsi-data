#!/usr/bin/env python3

import pandas as pd
import geopandas as gpd
import time

# exec(open('check-311.py').read())
apikey = '' # pull from file
# target = '(28|29|27|30)\d\d 26TH STREET NE'
# target = '(23|24|25)\d\d GIRARD STREET NE'

targets = ['(23|24|25)\d\d GIRARD PLACE NE']

print('gathering info for %s' % targets)

# read in GeoJSON files (reduce years for testing because the whole decade takes a while)
datasets = [gpd.read_file('data/311_City_Service_Requests_in_%i.geojson' % year)
            for year in range(2021, 2024)]

print('files read in')

# create a dataframe of just the TSI requests
tsi_311_data = pd.concat(datasets)
tsi_311_data = tsi_311_data[tsi_311_data.SERVICECODE == 'SPSTDAMA']

print('data combined')

# eliminate cruft (only worth the CPU cycles if you're manually exploring)
# unhelpful_columns = [column for column in tsi_311_data.columns if len(tsi_311_data[column].unique()) == 1]
# tsi_311_data.drop(columns=unhelpful_columns, inplace=True)
# tsi_311_data['year'] = tsi_311_data.ADDDATE.str.slice(stop=4)

# create an add_date column
tsi_311_data['add_date'] = tsi_311_data.ADDDATE.str.slice(stop=10)

# create an and_date column
tsi_311_data['end_date'] = tsi_311_data.RESOLUTIONDATE.str.slice(stop=10)

print('preparing CSV reports')

for target in targets:
    results = tsi_311_data[tsi_311_data.STREETADDRESS.str.contains(target) == True][[
        'SERVICEREQUESTID', 'STREETADDRESS', 'add_date', 'end_date']].sort_values(by=['STREETADDRESS', 'add_date'])

    results['description'] = ''
    for index, result in results.iterrows():
        print('waiting before querying SR %s' % result.SERVICEREQUESTID)
        url = 'https://dc311-api.herokuapp.com/311/v4/request/%s.json?api_key=%s' % (
            result.SERVICEREQUESTID, apikey)
        print('url: %s' % url)
        time.sleep(10)
        results.loc[results.SERVICEREQUESTID == result.SERVICEREQUESTID,
                    'description'] = pd.read_json(url).description[0]
        # print('%s: %s'%(result.SERVICEREQUESTID, results.at[results.SERVICEREQUESTID == result.SERVICEREQUESTID, 'description']))

    csv_path = 'data/%s.csv' % ''.join(filter(str.isalnum, target))
    results.to_csv(csv_path, index=False, header=True)
