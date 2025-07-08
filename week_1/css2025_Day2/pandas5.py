#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  1 10:43:57 2025

@author: lget
"""

import pandas as pd

df = pd.read_csv('data_02/patient_data_dates.csv')

# Allows you to see all rows
pd.set_option('display.max_rows',None)

print(df)

# Now the index column is redundant and we do not need it. We can remove it with drop method in the following way:
df.drop(['Index'],inplace=True,axis=1)
print(df)

# Fill the Nan Values as mean of the Calories Column in the Calories Column
x = df["Calories"].mean()

df["Calories"].fillna(x, inplace = True)
print(df)

# Drop directly the Nan values in the rows
df.dropna(inplace = True)
# Drop the index like we have done before to the new dataframe
df = df.reset_index(drop=True)

# Change the value of the duration in the row 7 to 45 instead of 450
df.loc[7, 'Duration'] = 45
print(df)

# Drop the duplicates rows(row 11 and row 12)
df.drop_duplicates(inplace = True)
print(df)