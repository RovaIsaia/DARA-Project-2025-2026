"""
Script for calibration and imaging of EVN n14c3 data for J1849+3024/1848+283
NME_all.py or the instructions from the web page should first have been.
run to provide a file with Tsys/gain curve, initial delay and bandpass
calibration applied, 1848+283_J1849+3024.ms (or if this is not available, use 1848+283_J1849+3024.ms.tgz)

This script is to be used as a guide if you are struggling to fill the skeleton script.

amsr@jb.man.ac.uk April 2016
Modified by Jack Radcliffe 2019 & 2021 to casa v6 then in 2025 to v6.5
"""

import os, sys

if (sys.platform == 'darwin'): ## this is a bit of code to deal with the viewer issue
	mac = True
	from casagui.apps import run_iclean
else:
	mac = False

# Need: 1848+283_J1849+3024.ms,
# Data contains:

#  0   J1849+3024    18:49:20.103406 +30.24.14.23712 J2000  tar
#  1   1848+283      18:50:27.589825 +28.25.13.15523 J2000  ph

# This script uses variables so that you could modify it to run on
# other similar data.
# NB in some plotms some antenna names are haard-wired for identifying
# bad data, which would have to be changed for other data sets

# Usage
# Enter at the CASA prompt the number of the step(s) to run
# and then use execfile
# e.g.
# CASA <2>:runsteps=[1,2]
# CASA <3>:execfile('NME_J1849.py')

### Inputs ###########
target='J1849+3024'
phscal='1848+283'
antref='EF'                  # refant as origin of phase
######################


thesteps = []
step_title = {1: 'Image phase cal',
			  2: 'Obtain image information',
			  3: 'FT phase cal to generate model',
			  4: 'Refine delay calibration',
			  5: 'Refine phase calibration',
			  6: 'Apply all calibration to phasecal',
			  7: 'Re-image phasecal',
			  8: 'Phasecal selfcal in amp and phase',
			  9: 'Apply solutions to phasecal',
			  10: 'Re-image phasecal with selfcal done',
			  11: 'Apply solutions to target',
			  12: 'Split target from ms',
			  13: 'Image target w/ calibration from phase referencing',
			  14: 'Look at structure of target',
			  15: 'Phase only self-cal on target',
			  16: 'Apply + generate new model',
			  17: 'Look at structure of target w/ phase self-cal',
			  18: 'Amp+phase self-cal on target',
			  19: 'Apply and make science image'
}

try:
	print('List of steps to be executed ...', runsteps)
	thesteps = runsteps
except:
	print('global variable runsteps not set')

print(runsteps)

if (thesteps==[]):
	thesteps = range(0,len(step_title))
	print('Executing all steps: ', thesteps)
	
### 7) Image phase calibrator again!
mystep = 7

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	os.system('rm -r phasecal1p1.*')
	if mac==False:
		tclean(vis='%s_%s.ms'% (phscal,target),
			   imagename='phasecal1p1',
			   stokes='pseudoI',
			   psfcutoff=0.5,
			   specmode='mfs',
			   threshold=0,
			   field='%s'%phscal,
			   imsize=[640,640],
			   cell=['0.24mas'],
			   gridder='standard',
			   deconvolver='clark',
			   niter=1000,
			   interactive=True)
	else:
		run_iclean(vis='%s_%s.ms'% (phscal,target),
				   imagename='phasecal1p1',
			   	   stokes='pseudoI',
				   specmode='mfs',
				   threshold=0,
				   field='%s'%phscal,
				   imsize=[640,640],
				   cell=['0.24mas'],
				   gridder='standard',
				   deconvolver='clark',
				   niter=1000)

	# Measure the signal to noise
	rms=imstat(imagename='phasecal1p1.image',
			   box='60,60,580,240')['rms'][0]
	peak=imstat(imagename='phasecal1p1.image',
			   box='300,300,340,340')['max'][0]

	ft(vis='%s_%s.ms'% (phscal,target),
	   field='%s'%phscal,
	   model='phasecal1p1.model',
	   usescratch=True)
	
	print('Peak %6.3f Jy/beam, rms %6.3f Jy/beam, S/N %6.0f' % (peak, rms, peak/rms))
