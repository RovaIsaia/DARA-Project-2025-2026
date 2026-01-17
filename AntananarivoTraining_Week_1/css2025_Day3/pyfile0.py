#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  2 09:46:11 2025

@author: lget
"""

data = px.data.gapminder()

# Create a choropleth world map
fig = px.choropleth(
    data_frame=data,
    locations="iso_alpha",
    color="gdpPercap",
    hover_name="country",
    animation_frame="year",
    title="World Map Choropleth",
    color_continuous_scale=px.colors.sequential.Plasma,
    projection="natural earth"
)