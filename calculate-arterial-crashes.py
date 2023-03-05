#!/usr/bin/env python3

import pandas as pd
import time

# exec(open('calculate-arterial-crashes.py').read())

crashes = pd.read_csv('data/Crashes_in_DC.csv')
crashes['year'] = crashes.REPORTDATE.str.slice(stop=4)

arterials = ['RHODE ISLAND', 'NEW YORK', 'SOUTH DAKOTA', 'FLORIDA', 'NORTH CAPITOL', 'BLADENSBURG', 'MICHIGAN']

for arterial in arterials:
    print('%s,%i'%(arterial, crashes[(crashes.ADDRESS.str.contains(arterial) == True) & (crashes.WARD.str.contains('5')) & ((crashes.year == '2021') | (crashes.year == '2022'))].shape[0]))
