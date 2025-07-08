#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  1 11:55:00 2025

@author: lget
"""

import matplotlib.pyplot as plt

#Plot
x_line = [1, 2, 3, 4, 5];
y_line = [2, 4, 6, 8, 10];


plt.plot(x_line, y_line, '-o')
plt.xlabel("x_line")
plt.ylabel("y_line")

plt.title('Line Plot')
plt.show()

#Barplot
x_bar = ['A', 'B', 'C', 'D']
y_bar = [1, 2, 3, 4]

plt.bar(x_bar, y_bar)
plt.xlabel('Categories')
plt.ylabel('Values')
plt.title('Bar Plot Example')
plt.show()

#Scatter
x_scatter = [1, 2, 3, 4, 5]
y_scatter = [2, 4, 6, 8, 10]

plt.scatter(x_scatter, y_scatter)
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Scatter Plot Example')
plt.show()

#Histplot
x_histogram = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5]

plt.hist(x_histogram, bins=range(min(x_histogram), max(x_histogram) + 1), edgecolor='black')
plt.xlabel('Values')
plt.ylabel('Frequency')
plt.title('Histogram Example')
plt.show()

