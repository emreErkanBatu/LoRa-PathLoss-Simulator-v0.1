# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 04:28:19 2024

@author: emree
"""

from pandas import read_csv
import numpy as np


# from pandas import DataFrame
# from pandas import concat
# import pandas as pd

# load dataset

datasetName="dataSet_9L"
dataset= read_csv(datasetName+".csv", header=0)

dataset3L = dataset.copy()
dataset5L = dataset.copy()

dataset3L = dataset3L.drop(['rssi1', 'rssi2','rssi4', 'rssi6','rssi7', 'rssi9'], axis=1)
fmt = ["%.3f","%.3f","%.3f","%.3f","%.3f"]
np.savetxt("dataSet_3L.csv", dataset3L, fmt=fmt, delimiter=",", header="rssi1,rssi2,rssi3,x,y",comments='')


dataset5L = dataset5L.drop(['rssi2', 'rssi4','rssi6', 'rssi8'], axis=1)
fmt = ["%.3f","%.3f","%.3f","%.3f","%.3f","%.3f","%.3f"]
np.savetxt("dataSet_5L.csv", dataset5L, fmt=fmt, delimiter=",", header="rssi1,rssi2,rssi3,rssi4,rssi5,x,y",comments='')
