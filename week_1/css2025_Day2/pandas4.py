#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  1 10:36:51 2025

@author: lget
"""
import pandas as pd
df = pd.read_csv("data_02/time_series_data.csv")
print(df)

# Convert the 'Date' column to datetime
df['Date'] = pd.to_datetime(df['Date'])
print(df)

#For example, if your date string is in the "DD-MM-YYYY" format, you would specify the format like this:
df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')
print(df)

# Split the 'Date' column into separate columns for year, month, and day
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month
df['Day'] = df['Date'].dt.day
print(df)

