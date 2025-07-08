#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  2 10:37:40 2025

@author: lget
"""

import numpy as np
import plotly.graph_objs as go
import webbrowser

# Generate synthetic frequency data (in MHz) and intensity (arbitrary units)
frequencies = np.linspace(0.1, 1000, 1000)  # 0.1 MHz to 1000 MHz
intensities = np.sin(frequencies / 50) ** 2 + np.random.normal(0, 0.05, frequencies.shape)

# Create a plotly figure
fig = go.Figure()

# Add the power spectrum as a line plot
fig.add_trace(go.Scatter(
    x=frequencies,
    y=intensities,
    mode='lines',
    name='Power Spectrum',
    line=dict(color='blue')
))

# Customize the layout
fig.update_layout(
    title="Radio Signal Power Spectrum",
    xaxis_title="Frequency (MHz)",
    yaxis_title="Intensity (arbitrary units)",
    # template="plotly_dark"
)

# Save the plot to an HTML file
fig.write_html("plot.html")

# Automatically open the plot in the default web browser
webbrowser.open("plot.html")