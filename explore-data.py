#!/usr/bin/env python3

import pandas as pd
import geopandas as gpd
import json
import datetime

# read in OpenDataDC 311 data
# downloaded as CSV from https://opendata.dc.gov/datasets/DCGIS::311-city-service-requests-in-2022/
# to data/2022-311.csv navigating from where this is run
sr_data = pd.read_csv("data/2022-311.csv")

# GeoJSON works too
sr_data = gpd.read_file("data/2021-311.geojson")

# data by year:
# 2021: https://opendata.dc.gov/datasets/DCGIS::311-city-service-requests-in-2021/
# 2022: https://opendata.dc.gov/datasets/DCGIS::311-city-service-requests-in-2022/
# 2023: https://opendata.dc.gov/datasets/DCGIS::311-city-service-requests-in-2023/

# create a dataframe of just the TSI requests
tsi_311_data = sr_data[sr_data.SERVICECODE == 'SPSTDAMA']

# list populated columns
print(*tsi_311_data.dropna(axis=1, how='all').columns.to_list(), sep='\n')

# make a list of columns that contain the same value (or lack thereof) for every record
unhelpful_columns = [column for column in tsi_311_data.columns if len(tsi_311_data[column].unique()) == 1]

# make a list of columns that contain more than one value (or lack: some nulls and some populated the same qualifies)
helpful_columns = [column for column in tsi_311_data.columns if len(tsi_311_data[column].unique()) > 1]

# drop columns that contain the same value throughout the reduced set (stuff all TSI requests have in common)
tsi_311_data.drop(columns=unhelpful_columns, inplace=True)

# unresolved SRs
tsi_311_data[pd.isna(tsi_311_data.RESOLUTIONDATE)].SERVICEREQUESTID

# crosstab of ADDDATE and RESOLUTIONDATE months
pd.crosstab(tsi_311_data.ADDDATE.str.slice(stop=7), tsi_311_data.RESOLUTIONDATE.str.slice(stop=7))

# unresolved SRs, counts of open date
tsi_311_data[pd.isna(tsi_311_data.RESOLUTIONDATE)].ADDDATE.str.slice(stop=10).value_counts()

# unresolved SRs, counts of open date, sorted by chronology
tsi_311_data[pd.isna(tsi_311_data.RESOLUTIONDATE)].ADDDATE.str.slice(stop=10).value_counts().sort_index()

# read in scraped TSInput data
tsi_data = pd.read_csv("data/raw-tsi-data.csv")

# 153 total columns
print(*tsi_data.columns.to_list(), sep='\n')

# 102 columns with any data
len(tsi_data.dropna(axis=1, how='all').columns.to_list())

# 51 totally empty columns
len([x for x in tsi_data.columns.to_list() if x not in tsi_data.dropna(axis=1, how='all').columns.to_list()])

# check frequencies on an attribute
tsi_data.Ward_ID.value_counts(dropna=False)

# check unique values of an attribute
tsi_data.Ward_ID.unique(dropna=False)

# check for cases of mismatch between two attributes that appear the same
tsi_data[tsi_data.LongLabel != tsi_data.ShortLabel][['LongLabel', 'ShortLabel']].dropna(how='all')

# check frequences for permutations of two or more attributes
tsi_data[['WARD', 'Ward_ID']].value_counts()

# pretty-print one record by SR#
print(json.dumps(tsi_data[tsi_data.CSRNumber == '22-00573062'].to_dict(), indent=4))

# running the date range of an epoch date field
datetime_column = 'datetimeinit'
desired_format = '%m/%d/%Y'
start_date = datetime.datetime.fromtimestamp(tsi_data[datetime_column].sort_values()[0]/1000).strftime(desired_format)
end_date = datetime.datetime.fromtimestamp(tsi_data[datetime_column].sort_values()[-1:].values[0]/1000).strftime(desired_format)
print('date range: %s - %s' % (start_date, end_date))

# create a human-readable column out of an epoch date field
tsi_data['readable_init'] = [datetime.datetime.fromtimestamp(tsi_data[datetime_column].sort_values()[i]/1000).strftime(desired_format) for i in range(0, tsi_data.shape[0])]

# first (chronological) request:
tsi_data[tsi_data.datetimeinit == tsi_data[datetime_column].sort_values()[0]][['CSRNumber', 'Match_addr', 'INSPGEOADDRESS']]

# last (chronological) request:
tsi_data[tsi_data.datetimeinit == tsi_data[datetime_column].sort_values()[-1:].values[0]][['CSRNumber', 'Match_addr', 'INSPGEOADDRESS']]