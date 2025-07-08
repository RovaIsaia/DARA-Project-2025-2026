#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  1 08:32:09 2025

@author: lget
"""

import pandas as pd

df = pd.read_csv("data_02/country_data_index.csv")
print(df)

# To open the csv file
df1 = pd.read_csv("data_02/iris.csv")
column_names = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'class']
print(df1)

# To open the txt file
df2 = pd.read_csv("data_02/Geospatial Data.txt",sep=";")
print(df2)

# To open the excel file
df3 = pd.read_excel("data_02/residentdoctors.xlsx")
print(df3)

# To open the json file
df4 = pd.read_json("data_02/student_data.json")
print(df4)