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
	

### 2) Plot visibility spectrum, identify continuum, flag bad data
mystep = 2

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	# Plot amplitude against channel
	plotms(vis='NGC660.ms',
		   xaxis='channel',
		   yaxis='amp',
		   avgtime='36000',
		   antenna='EF&*',
		   iteraxis='baseline',
		   avgscan=True,
		   plotfile="spectral_line_pre_flagcal.png",
		   highres=True,
		   showgui=False,
		   dpi = 800,
		   width=1500,
		   height=750,
		   overwrite=True)

	# The end channels have already been flagged and some around 775 have
	# been excised due to rfi.  The absorption is seen in channels
	# 490~535, so select a range well clear for continuum imaging and
	# enter this at the start of the script so all tasks can use the
	# variable.  Search for contchans above the first list of steps.
	# However, here, average all channels as plotms cannot average over
	# gaps.

	plotms(vis='NGC660.ms',
		   xaxis='time',
		   yaxis='amp',
		   avgchannel='801',
		   antenna='EF&*',
		   coloraxis='antenna2',
		   plotfile='NGC660_amp-time_preflag.png',
		   highres=True,
		   showgui=False,
		   dpi = 800,
		   width=1500,
		   height=750,
		   overwrite=True)

	# There are  some dropouts which should be flagged because they
	# will be noisy. The high data on UR and MC can be ignored for now
	# because they will be corrected during self-calibration. This is a
	# tentative judgement, if the final images still seemed too noisy you
	# might flag the data after all.
	# NGC660.flagcmd was written by using Mark and Locate to identify the dropouts.

	flagmanager(vis='NGC660.ms',
				mode='save',
				versionname='prelist')

	flagdata(vis='NGC660.ms',
			 mode='list',
			 inpfile='NGC660.flagcmd.txt')

	plotms(vis='NGC660.ms',
		   xaxis='time',
		   yaxis='amp',
		   avgchannel='801',
		   antenna='EF&*',
		   coloraxis='antenna2',
		   plotfile='NGC660_amp-time_postflag.png',
		   highres=True,
		   showgui=False,
		   dpi = 800,
		   width=1500,
		   height=750,
		   overwrite=True)    