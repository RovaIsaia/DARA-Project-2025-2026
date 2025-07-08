#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  1 10:57:33 2025

@author: lget
"""
import pandas as pd
# To open the csv file
df = pd.read_csv("data_02/iris.csv")
column_names = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'class']
print(df)

# To group all the unique value in the class columns
grouped = df.groupby('class')

# Calculate mean, sum, and count for the squared values
mean_squared_values = grouped['sepal_length'].mean()
sum_squared_values = grouped['sepal_length'].sum()
count_squared_values = grouped['sepal_length'].count()

# Display the results
print("Mean of Sepal Length Squared:")
print(mean_squared_values)

print("\nSum of Sepal Length Squared:")
print(sum_squared_values)

print("\nCount of Sepal Length Squared:")
print(count_squared_values)

# Filter data for females (class == 'Iris-versicolor')
iris_versicolor = df[df['class'] == 'Iris-versicolor']

# Calculate the average iris_versicolor_sep_length
avg_iris_versicolor_sep_length = iris_versicolor['sepal_length'].mean()
print(avg_iris_versicolor_sep_length)

# Replace the name with Iris- (remove the Iris- in the class columns)
df['class'] = df['class'].str.replace('Iris-', '')
print(df)


# Apply the square to sepal length using a lambda function
df['sepal_length_sq'] = df['sepal_length'].apply(lambda x: x**2)
print(df)