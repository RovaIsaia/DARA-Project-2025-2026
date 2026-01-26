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
	

### 13) Make moments
mystep = 13
if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	# Click on the Moments tool. This will present the spectral profiler.
	# Draw an ellipse round the core and see the spectrum. Shift-click in
	# the spectral profile tool to select the channels covering the
	# line. Select the zeroth moment (total intensity). Note the start and
	# stop channels (approximately) and click on Collapse.

	# This can be scripted.  For the first moment (velocity-weighted) it
	# is necessary to exclude the noisiest pixels, and the counter-jet is
	# mostly obscured, but you can see the velocity gradient across the
	# core region.

	os.system('rm -rf NGC660line.mom0')
	immoments(imagename='NGC660line.image',
			  moments=[0],
			  chans='33~83',
			  outfile='NGC660line.mom0')

	os.system('rm -rf NGC660line.mom1')
	immoments(imagename='NGC660line.image',
			  moments=[1],
			  chans='33~83',
			  excludepix=[-0.005,1],
			  outfile='NGC660_line.mom1')

	# Look at NGC660_line.clean.mom0 and NGC660_line.clean.mom1 in the viewer    