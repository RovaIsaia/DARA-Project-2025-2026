#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  2 09:45:19 2025

@author: lget
"""

import plotly.express as px

x_bar = ['A', 'B', 'C', 'D']
y_bar = [1, 2, 3, 4]
fig = px.bar(x=x_bar, y=y_bar, labels={'x': 'Categories', 'y': 'Values'}, title='Bar Plot')
fig.write_html("plot.html")

# This is used to automatically open up a browser of your plot
import webbrowser
webbrowser.open("plot.html")