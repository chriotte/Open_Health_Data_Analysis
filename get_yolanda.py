#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 21:46:43 2017

@author: christopher.ottesen
"""

import pandas as pd 

yolanda_src = 'data/yolanda/Yolanda-Christopher .csv'

yolanda_data = pd.read_csv(yolanda_src)
yolanda_data['Muscle Mass'] = yolanda_data['Muscle Mass'].map(lambda x: float(str(x).strip('Kg')))
yolanda_data['Body Fat'] = yolanda_data['Body Fat'].map(lambda x: float(str(x).strip('%')))

yolanda_data['Measuring time'] = pd.to_datetime(yolanda_data['Measuring time'])

yolanda_data.plot(x='Muscle Mass',y='Measuring time' )
yolanda_data.plot(x='Measuring time', y=['Muscle Mass','Body Fat'])
yolanda_data.plot(x='Measuring time', y=['Body Fat'])

