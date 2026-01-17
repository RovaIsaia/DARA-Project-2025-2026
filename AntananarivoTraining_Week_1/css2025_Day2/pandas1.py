#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  1 09:15:51 2025

@author: lget
"""
import pandas as pd
df = pd.read_csv("data_02/country_data_index.csv")
print(df)
#This will read the CSV file and use the first column as the index, preventing the appearance of the "Unnamed: 0" column in your DataFrame.
df1 = pd.read_csv("data_02/country_data_index.csv",index_col=0)
print(df1)

# We get an error because the number of columns in your CSV file is not consistent across all rows.
#df2 = pd.read_csv("data_02/insurance_data.csv")
#print(df2)

# We can resolve this by using the "skiprows" parameter to just skip first 5 rows:
df3 = pd.read_csv("data_02/insurance_data.csv",skiprows=5)
print(df3)

# Create a list with the heading names you want and add use the parameters "header=None" and "names=column_names":
column_names = ["duration", "pulse", "max_pulse", "calories"]

df4 = pd.read_csv("data_02/patient_data.csv", header=None, names=column_names)