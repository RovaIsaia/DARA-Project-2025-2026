#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  1 09:54:25 2025

@author: lget
"""

import pandas as pd
df = pd.read_excel("data_02/residentdoctors.xlsx")
print(df)
print(df.columns)

# Step 1: Extract the lower end of the age range (digits only)
df['LOWER_AGE'] = df['AGEDIST'].str.extract('(\d+)-') # Here we used .extract() to extract certain information from a string.
print(df)
# Step 2: Convert the new column to float
df['LOWER_AGE'] = df['LOWER_AGE'].astype(float)
print(df)

# Filtering data
print(df[df['AGE'] > 30])