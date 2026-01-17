#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 23 19:24:09 2025

@author: asfs9
"""

import pandas as pd
import matplotlib.pyplot as plt

# Loading and Labelling the Sky Data


sky_data = "b_0_l_360_spectrum.txt"

sky_df = pd.read_csv(sky_data, delim_whitespace=True, header=None)

sky_df.columns = ['channels', 'raw_data']

'''
# Load and Label the RF Load Data

load_file = "g25p4_spectrum.txt"

load_df = pd.read_csv(load_file, delim_whitespace=True, header=None)

load_df.columns = ['channels', 'load_data']

# Combining DataFrames

combined_df = pd.concat([sky_df, load_df['load_data']],axis=1)

# Normalization

combined_df['normalized'] = combined_df['raw_data'] / combined_df['load_data']

# Computing the Brightness Temperature

combined_df['brightness_temp'] = combined_df['normalized'] * 303 

# Computing Radial Velocity

combined_df['radial_vel'] = combined_df['channels'] * (-1.69) 
'''
# Saving
output_file = 'b_0_l_360_spectrum_named.txt'

sky_df.to_csv(output_file, sep='\t', index=False)

#Plotting channels verses normalized spectra
"""
plt.figure(figsize=(10,5))
plt.plot(combined_df['channels'], combined_df['normalized'] , color = 'k' , linewidth=1.5)
plt.title('Normalized 21cm Hydrogen Line Spectrum')
plt.xlabel('FFT Channel Numbers')
plt.ylabel('Normalized Power')
plt.grid(True)
plt.tight_layout()
plt.show()

# PLotting Radial Velocity verses Brightness Temperature

plt.figure(figsize=(10,5))
plt.plot(combined_df['radial_vel'], combined_df['brightness_temp'] , color = 'g' , linewidth=1.5)
plt.title('b_0_l_0_21cm Spectrum')
plt.xlabel('Radial Velocity (km/s)')
plt.ylabel('Brightness Temperature (K)')
plt.grid(True)
plt.tight_layout()
plt.show()

output_plot = "b_0_l_0_spectrum_plot.png"
plt.savefig(output_plot, dpi=1080)
"""



