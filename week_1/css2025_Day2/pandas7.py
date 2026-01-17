#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  1 11:03:43 2025

@author: lget
"""

import pandas as pd

# Read the CSV files into dataframes
df1 = pd.read_csv("data_02/person_split1.csv")
print(df1)
df2 = pd.read_csv("data_02/person_split2.csv")
print(df2)

# Concatenate the dataframes 
df = pd.concat([df1, df2], ignore_index=True)
print(df)
