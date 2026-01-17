#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  1 11:16:44 2025

@author: lget
"""
import pandas as pd
df1 = pd.read_csv('data_02/person_education.csv')
print(df1)
df2 = pd.read_csv('data_02/person_work.csv')
print(df2)

## inner join
df_merge = pd.merge(df1,df2,on='id')
print(df_merge)

# outer join
df_merge1 = pd.merge(df1, df2, on='id', how='outer')
print(df_merge1)