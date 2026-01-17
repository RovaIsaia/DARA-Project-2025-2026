#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  2 10:39:11 2025

@author: lget
"""

import pandas as pd
import matplotlib.pyplot as plt

# Read the Data
df=pd.read_csv('student_marks.csv')
print(df)

# Give the first empty column a name to "Persons"
df = df.rename(columns={df.columns[0]: "Name"})
print(df)

# Stastical informations
print(df.describe())

# Information about the Data
print(df.info())

#To check the missing Values in the Data
print(df.isna().sum())

### Plots for the Data student marks

# Plot Maths marks vs. Names
df.plot(x="Name", y="Maths", kind="bar", legend=False)
plt.title("Maths Marks by Student")
plt.ylabel("Marks")
plt.xticks(rotation=45) # Rotate names for readability
plt.show()

# Select all subjects to plot
subjects = ['Maths', 'Physics', 'Chemistry', 'English', 
            'Biology', 'Economics', 'History', 'Civics']

df.plot(x='Name', y=subjects, kind='bar', figsize=(12, 6))
plt.title('Subject Marks by Student')
plt.ylabel('Marks')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

