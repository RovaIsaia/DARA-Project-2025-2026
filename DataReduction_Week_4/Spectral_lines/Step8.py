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
	

### 8) Self-calibrate
mystep = 8
if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	# The data are mostly well calibrated but there are the discrepant
	# amplitudes noted above, so solve for amplitude and phase. Note that
	# the parallactic angle correction was applied prior to creating the
	# data set we loaded.

	gaincal(vis='NGC660shift.ms',
			caltable='NGC660.ap1',
			solint='30s',
			minsnr=1,
			minblperant=2,
			solnorm=True)

	plotms(vis='NGC660.ap1',
		   xaxis='time',
		   yaxis='amp',
		   iteraxis='antenna',
		   coloraxis='corr',
		   gridcols=3,
		   gridrows=2,
		   plotfile='NGC660.ap1.png',
		   highres=True,
		   showgui=False,
		   dpi = 800,
		   width=1500,
		   height=750,
		   overwrite=True)

	applycal(vis='NGC660shift.ms',
			 gaintable='NGC660.ap1',
			 applymode='calonly')    