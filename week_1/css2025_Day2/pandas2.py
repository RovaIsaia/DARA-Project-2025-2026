#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  1 09:35:06 2025

@author: lget
"""
import pandas as pd
df = pd.read_csv("data_02/patient_data.csv")
print(df)

# Create a list with the heading names you want and add use the parameters "header=None" and "names=column_names":
column_names = ["duration", "pulse", "max_pulse", "calories"]

df1 = pd.read_csv("data_02/patient_data.csv", header=None, names=column_names) # To add columns_name
print(df1)

#We have some errors here beacause of This is a text file with the data separate with a semi-colon, Pandas is expecting a comma. So we use the parameter sep=";"
#df2 = pd.read_csv("data_02/Geospatial Data.txt")
#print(df)

#Also note that the file name has a space in it, which is not recommended.
df3 = pd.read_csv("data_02/Geospatial Data.txt",sep=";")
print(df3)

