#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  3 12:20:35 2025

@author: lget
"""

import pandas

file = pandas.read_csv("/home/lget/DARA/Rova_Isaia/css2025_Day1/data_01/country_data.csv")

print(file)

print(file.info())

print(file.describe())

