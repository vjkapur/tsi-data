#!/usr/bin/env python3

import pandas as pd

# read in the crashes file
crashes = pd.read_csv('data/Crashes_in_DC.csv')

# create a datetime column to capture the date for comparison purposes
crashes['date'] = pd.to_datetime(crashes.FROMDATE.str.slice(stop=10), format='%Y/%m/%d')

# reduce to only crashes on or after 2017-01-02 (288,226 down to 143,879)
crashes = crashes[crashes.date >= '2017-01-02']

# reduce to only crashes where the address contains WHEELER or ALABAMA (143,879 down to 3060)
crashes = crashes[crashes.ADDRESS.str.contains('WHEELER') | crashes.ADDRESS.str.contains('ALABAMA')]

injury_attributes = ['MAJORINJURIES_BICYCLIST', 'MINORINJURIES_BICYCLIST', 'UNKNOWNINJURIES_BICYCLIST', 'FATAL_BICYCLIST', 'MAJORINJURIES_DRIVER', 'MINORINJURIES_DRIVER', 'UNKNOWNINJURIES_DRIVER', 'FATAL_DRIVER', 'MAJORINJURIES_PEDESTRIAN', 'MINORINJURIES_PEDESTRIAN', 'UNKNOWNINJURIES_PEDESTRIAN', 'FATAL_PEDESTRIAN', 'FATALPASSENGER', 'MAJORINJURIESPASSENGER', 'MINORINJURIESPASSENGER', 'UNKNOWNINJURIESPASSENGER']

# counts for unique non-zero values for any injury attributes
for injury_attribute in injury_attributes:
    print(crashes[crashes[injury_attribute] > 0][injury_attribute].value_counts())

# sum totals for the filtered set
crashes[injury_attributes].sum()