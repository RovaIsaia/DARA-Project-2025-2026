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
	
### 11)
mystep = 11
if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	# Clean the line channels. When the viewer appears, use the animator
	# to view a central channel e.g. 60 and set a mask for `all channels`.
	# Double check that the mask appears in more than one channel

	os.system('rm -rf NGC660line.*')
	if mac == False:
		tclean(vis='NGC660shift.contsub.ms',
			   imagename='NGC660line',
			   field='NGC660',
			   specmode='cube',
			   threshold=0,
			   start=450,
			   width=1,
			   nchan=100,
			   outframe='LSRK',
			   restfreq='1.420410GHz',
			   imsize=[320,320],
			   cell=cellsize,
			   weighting='briggs',
			   robust=0,
			   niter=1000,
			   interactive=True,
			   cycleniter=25)
	else:
		run_iclean(vis='NGC660shift.contsub.ms',
				   imagename='NGC660line',
				   field='NGC660',
				   specmode='cube',
				   threshold=0,
				   start=450,
				   width=1,
				   nchan=100,
				   outframe='LSRK',
				   restfreq='1.420410GHz',
				   imsize=[320,320],
				   cell=cellsize,
				   weighting='briggs',
				   robust=0,
				   niter=1000,
				   cycleniter=25)

	rms=imstat(imagename='NGC660line.image',
			   box=offbox)['rms'][0]
	peak=imstat(imagename='NGC660line.image',
			   box=onbox)['min'][0]
	peakchan=imstat(imagename='NGC660line.image',
					box=onbox)['minpos'][3]

	print('Max. absorption %6.4f mJy/beam, in chan %3i, rms %6.4f mJy/beam, S/N %6.0f' % (peak*1e3, peakchan, rms*1e3, abs(peak/rms)))

	#Max. absorption -0.0614, in chan  60, rms 0.0005, S/N    113    