#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 16 11:20:28 2025

@author: juotca
"""


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
import matplotlib.colors as mcolors

#PART I: Plot the RFI Signals

#Load multiple CSV files into separate DataFrames (df to df16)
#Insert your .csv files here.    

df=pd.read_csv()
df2=pd.read_csv()
df3=pd.read_csv()
df4=pd.read_csv()
df5=pd.read_csv()
df6=pd.read_csv()
df7=pd.read_csv()
df8=pd.read_csv()
df9=pd.read_csv()
df10=pd.read_csv()
df11=pd.read_csv()
df12=pd.read_csv()
df13=pd.read_csv()
df14=pd.read_csv()
df15=pd.read_csv()
df16=pd.read_csv()


df = df.iloc[41:674, 0:2]
df.columns=['Frequency', 'E-V']
dffreq=df['Frequency']

df2=df2.iloc[41:674,0:2]
df2.columns=['Frequency', 'Amplitude']
df2ex=df2["Amplitude"]
df = pd.concat([df, df2ex.rename("E-H")], axis=1)


df3=df3.iloc[41:674,0:2]
df3.columns=['Frequency', 'Amplitude']
df3ex=df3["Amplitude"]
df = pd.concat([df, df3ex.rename("N-H")], axis=1)

df4=df4.iloc[41:674,0:2]
df4.columns=['Frequency', 'Amplitude']
df4ex=df4["Amplitude"]
df = pd.concat([df, df4ex.rename("N-V")], axis=1)

df5=df5.iloc[41:674,0:2]
df5.columns=['Frequency', 'Amplitude']
df5ex=df5["Amplitude"]
df = pd.concat([df, df5ex.rename("S-H")], axis=1)

df6=df6.iloc[41:674,0:2]
df6.columns=['Frequency', 'Amplitude']
df6ex=df6["Amplitude"]
df = pd.concat([df, df6ex.rename("S-V")], axis=1)

df7=df7.iloc[41:674,0:2]
df7.columns=['Frequency', 'Amplitude']
df7ex=df7["Amplitude"]
df = pd.concat([df, df7ex.rename("W-H")], axis=1)


df8=df8.iloc[41:674,0:2]
df8.columns=['Frequency', 'Amplitude']
df8ex=df8["Amplitude"]
df = pd.concat([df, df8ex.rename("W-V")], axis=1)

df9=df9.iloc[41:674,0:2]
df9.columns=['Frequency', 'Amplitude']
df9ex=df9["Amplitude"]
df = pd.concat([df, df9ex.rename("NW-V")], axis=1)

df10=df10.iloc[41:674,0:2]
df10.columns=['Frequency', 'Amplitude']
df10ex=df10["Amplitude"]
df = pd.concat([df, df10ex.rename("NW-H")], axis=1)

df11=df11.iloc[41:674,0:2]
df11.columns=['Frequency', 'Amplitude']
df11ex=df11["Amplitude"]
df = pd.concat([df, df11ex.rename("NE-V")], axis=1)

df12=df12.iloc[41:674,0:2]
df12.columns=['Frequency', 'Amplitude']
df12ex=df12["Amplitude"]
df = pd.concat([df, df12ex.rename("NE-H")], axis=1)


df13=df13.iloc[41:674,0:2]
df13.columns=['Frequency', 'Amplitude']
df13ex=df13["Amplitude"]
df = pd.concat([df, df13ex.rename("SE-V")], axis=1)

df14=df14.iloc[41:674,0:2]
df14.columns=['Frequency', 'Amplitude']
df14ex=df14["Amplitude"]
df = pd.concat([df, df14ex.rename("SE-H")], axis=1)

df15=df15.iloc[41:674,0:2]
df15.columns=['Frequency', 'Amplitude']
df15ex=df15["Amplitude"]
df = pd.concat([df, df15ex.rename("SW-V")], axis=1)

df16=df16.iloc[41:674,0:2]
df16.columns=['Frequency', 'Amplitude']
df16ex=df16["Amplitude"]
df = pd.concat([df, df16ex.rename("SW-H")], axis=1)

df = df.astype(float)
clrs = ['lightcoral','red','darkorange','goldenrod','olive','gold','darkolivegreen','lawngreen',
        'mediumturquoise','dodgerblue','navy','slateblue','blueviolet','plum','purple','deeppink']
df = df.drop(df[df['Frequency'] <= 4e7].index)


df.plot(x='Frequency',y=['E-V','E-H','W-V','W-H','S-H','S-V', 'N-V','N-H','NW-H','NW-V','SW-V','SW-H','NE-H', 'NE-V','SE-H','SE-V'],linewidth=0.5,color=clrs)
plt.ylabel('Amplitude dB', fontsize="xxxx", fontweight="xxxx")
plt.xlabel('Frequency Hz', fontsize="xxxx", fontweight="xxxx")
plt.ylim(-110,10)
plt.gca().legend(bbox_to_anchor=(1,1), 
                 fontsize = "xxxx")
plt.grid("xxxx")  
plt.savefig("xxxx")
plt.show()

#PART II
theta = [90, 90, 270, 270, 180, 180, 0, 0, 315, 315, 225, 225, 45, 45, 135, 135]
theta = np.radians(theta)
labels = ['E-V', 'E-H', 'W-V', 'W-H', 'S-H', 'S-V', 
          'N-V', 'N-H', 'NW-H', 'NW-V', 'SW-V', 'SW-H',
          'NE-H', 'NE-V', 'SE-H', 'SE-V']
maxamp = df[labels].max() + 60
max_idx = np.argmax(maxamp)
max_label = labels[max_idx]
max_theta = theta[max_idx]
max_r = maxamp[max_idx]

fig = plt.figure(figsize=(), facecolor='white')
ax = fig.add_subplot(projection='polar')
ax.scatter(theta, maxamp, c=clrs, s=100, edgecolors='black', linewidths=0.5, zorder=3)
label_angle = max_theta - 0.01  
label_radius = max_r + 2.5       
real_maxamp = df[labels].max()       
maxamp = real_maxamp + 60
max_r_real = real_maxamp[max_idx]    
ax.text(label_angle, label_radius,
        f"{max_label}\n({max_r_real:.1f} dB)",  
        ha='center', va='bottom',
        fontsize='xxxx', fontweight='xxxx',
        color=clrs[max_idx])
ax.set_theta_zero_location('N')
ax.set_theta_direction(-1)
ax.set_rlabel_position(135)
ax.set_title("Maximum RFI Amplitude by Direction", fontsize="xxxx", fontweight='xxxx', pad=20)
ax.grid(color='gray', linestyle='--', linewidth=0.5)
ax.set_facecolor('#f9f9f9')
compass_labels = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
angles = np.linspace(0, 2*np.pi, len(compass_labels), endpoint=False)
for ang, lab in zip(angles, compass_labels):
    ax.text(ang, ax.get_rmax() + 5, lab, ha='center', va='center', fontsize=10, fontweight='bold', color='gray')
from matplotlib.lines import Line2D
peak_info = []
for label in labels:
    series = df[label]
    amp = series.max()
    freq = df.loc[series.idxmax(), 'Frequency']
    peak_info.append((label, amp, freq))
peak_info_sorted = sorted(peak_info, key=lambda x: x[1], reverse=True)
def identify_rfi_source(freq_hz):
    freq_mhz = freq_hz / 1e6
    if 87 <= freq_mhz <= 108:
        return "FM Radio"
    elif 174 <= freq_mhz <= 230:
        return "VHF TV"
    elif 470 <= freq_mhz <= 862:
        return "UHF TV"
    elif 880 <= freq_mhz <= 960:
        return "2G GSM (Mobile)"
    elif 1500 <= freq_mhz <= 1600:
        return "GPS / Sat Comms"
    elif 2400 <= freq_mhz <= 2500:
        return "Wi-Fi / Bluetooth"
    elif 5100 <= freq_mhz <= 5900:
        return "5 GHz Wi-Fi / Radar"
    elif freq_mhz > 6000:
        return "High-band Radar / Sat"
    else:
        return "Unknown / Local Device"
print("\n📡 RFI Source Summary by Direction:")
for label, amp, freq in peak_info_sorted:
    source = identify_rfi_source(freq)
    print(f"{label:<6}: {amp:>6.1f} dB at {freq/1e6:>7.2f} MHz → {source}")
color_map = dict(zip(labels, clrs))
legend_elements = [
    Line2D([0], [0],
           marker='o',
           color='w',
           label=f"{label} ({amp:.1f} dB @ {freq/1e6:.1f} MHz)",
           markerfacecolor=color_map[label],
           markeredgecolor='black',
           markersize="xxxx")
    for label, amp, freq in peak_info_sorted]
ax.legend(handles=legend_elements,
          loc='upper right',
          fontsize="xxxx",
          title="Direction (Descending Signal Strength)",
          title_fontsize="xxxx",
          frameon=False,
          bbox_to_anchor=(1.3, 1.05))  
ax.grid("xxxx")
plt.savefig("xxxx")
plt.tight_layout()
plt.show()
#PART III

peak_df = pd.DataFrame(peak_info_sorted, columns=["Direction", "Amplitude", "Frequency"])
peak_df["Frequency_MHz"] = peak_df["Frequency"] / 1e6
peak_df["Source"] = peak_df["Frequency"].apply(identify_rfi_source)
peak_df = peak_df.sort_values(by="Amplitude", ascending=False)

source_list = peak_df["Source"].unique()
color_palette = cm.get_cmap('tab20', len(source_list))
source_color_map = {src: mcolors.to_hex(color_palette(i)) for i, src in enumerate(source_list)}
peak_df["Color"] = peak_df["Source"].map(source_color_map)

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(peak_df["Direction"], peak_df["Amplitude"], color=peak_df["Color"])
for i, row in peak_df.iterrows():
    ax.text(row["Amplitude"] + 1, i, f'{row["Frequency_MHz"]:.1f} MHz\n{row["Source"]}', 
            va='center', fontsize=8)
ax.invert_yaxis()
ax.set_xlabel("Max Amplitude (dB)", fontsize="xxxx")
ax.set_title("Identified RFI Sources by Direction", fontsize="xxxx", fontweight='xxxx')
ax.grid("xxxx")

legend_elements = [
    Line2D([0], [0], marker='o', color='w', label=src, 
           markerfacecolor=clr, markersize=10)
    for src, clr in source_color_map.items()]
ax.legend(handles=legend_elements, title="RFI Source", loc='lower right', frameon=False, fontsize=9)
ax.grid("xxxx")
plt.savefig("xxxx")
plt.tight_layout()
plt.show()


























