"""
Script to image and self-calibrate the continuum of NGC660, subtract
the continuum and image the hydrogen line.
amsr@jb.man.ac.uk April 2016

Updated significantly by Jack Radcliffe 10/11/2021 & 2025

A web page/pdf of instructions is also available.
"""

import os, sys

if (sys.platform == 'darwin'): ## this is a bit of code to deal with the viewer issue
	mac = True
	from casagui.apps import run_iclean
else:
	mac = False

# Need:
# NGC660.FITS
# NGC660.flagcmd

# NGC660 is the only source in these data, already mostly calibrated.

# ENTER AT THE CASA PROMPT THE NUMBER OF THE STEP(s) TO RUN
#
# e.g.
# CASA <2>:runsteps=[1,2]
# CASA <3>:execfile('NME_all.py')

contchans='0:100~450;550~900'  # see step 2
cellsize='0.0018arcsec'       # see step 3
boxsize ='391, 949, 430, 1000' # see step 5
offbox='23,202,296,304'       # see step 6
onbox='137,134,179,185'      # see step 6

thesteps = []
step_title = {1:'Convert data to MS, sort and list',
			  2:'Plot the data, identify continuum, flag bad data',
			  3:'Plot against uv distance and establish imaging parameters',
			  4:'Make first image of NGC660 continuum',
			  5:'Find the peak position',
			  6:'Shift the uv phase to centre on the peak and image',
			  7:'Measure image rms',
			  8:'Self-calibrate',
			  9:'Apply calibration and image',
			  10:'Subtract the continuum and check HI frequency',
			  11:'Image the absorption cube',
			  12:'Make position-velocity plot',
			  13:'Make moments',
			  14:'Extract and plot spectra',
			  15:'Make optical depth map'
			 }

thesteps = []
try:
	print('List of steps to be executed ...', runsteps)
	thesteps = runsteps
except:
	print('global variable mysteps not set')

if (thesteps==[]):
	thesteps = range(0,len(step_title))
	print('Executing all steps: ', thesteps)
	
### 14) Extract and plot spectra
mystep = 14
if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	# Click on the spectral profile tool.  This is useful for getting an
	# idea of the spectrum but it is better to script the extraction and
	# plotting.

	# Use the viewer on the continuum image to identify 3 locations to
	# extract spectra. In the Regions pane, convert units to pixels and
	# use the same radius for all except the rms.

	rgns={'jet':'circle[[152pix, 169pix], 6pix]',
		  'core':'circle[[161pix, 160pix], 6pix]',
		  'cjet':'circle[[168pix, 153pix], 6pix]',
		  'rms':'box[[10pix,10pix],[100pix,50pix]]'}

	ia.open('NGC660line.image')
	for r in rgns:
		outfile=open(r+'.spec', 'w')
		f=ia.getprofile(axis = 3, function = 'flux', region = rgns[r], unit='km/s', spectype='radio velocity')
		for z in  zip(f['coords'],f['values']):
			print(z[0], z[1], file=outfile)
		outfile.close()

	ia.close()

	import matplotlib.pyplot as plt
	cols={'jet':'b','core':'g','cjet':'r','rms':'k'} # The colors for each spectrum (use help(plt.colors) for others)
	fig = plt.figure(1,figsize=(9,4.5))
	ax = fig.add_subplot(111)
	for i in range(len(rgns)):
		v=[];f=[]
		for l in open(list(rgns.keys())[i]+'.spec'):  # Read the disk files back into arrays
			v.append(float(l.split()[0])) # Array of velocities for x-axis
			f.append(float(l.split()[1])) # Array of flux density values for y-axis
		ax.plot(v,f,color=cols[list(rgns.keys())[i]],label=r'%s'%list(rgns.keys())[i])  # Plot the spectra
	ax.set_xlabel('Velocity (LSR, km/s)')
	ax.set_ylabel('Flux density per channel per 10.8-mas radius')
	ax.set_title('NGC660 HI velocity profiles')
	ax.legend() # add the legend to show what each line stands for
	fig.savefig('NGC660_HIvelocityprofiles.pdf',bbox_inches='tight') # Write the plot to a pdf
	plt.clf()    