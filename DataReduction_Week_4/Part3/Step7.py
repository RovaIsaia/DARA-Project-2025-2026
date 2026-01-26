"""
Script for calibration and imaging of EVN n14c3 data for J1849+3024/1848+283
NME_all.py or the instructions from the web page should first have been.
run to provide a file with Tsys/gain curve, initial delay and bandpass
calibration applied, 1848+283_J1849+3024.ms (or if this is not available,
use 1848+283_J1849+3024.ms.tgz)
The steps are outline on a web page.

See also NME_3C345_skeleton.py (or, if really stuck, NME_3C345.py) for
the other pair of sources.

Original by Anita Richards - April 2016
And updated, revised by Jack Radcliffe - May 2019, 2025
"""

import os, sys

if (sys.platform == 'darwin'): ## this is a bit of code to deal with the viewer issue
	mac = True
	from casagui.apps import run_iclean
else:
	mac = False

# Need: J1640+3946_3C345.ms flag_TarPh.flagcmd
# Data contains:

#  0   J1640+3946    16:40:29.632770 +39.46.46.02836 J2000  ph
#  1   3C345         16:42:58.809965 +39.48.36.99402 J2000  tar

# This script uses variables so that you could modify it to run on
# other similar data.
# NB in some plotms some antenna names are hard-wired for identifying
# bad data, which would have to be changed for other data sets

### INPUTS ####
target='3C345'
phscal='J1640+3946'
antref='EF'                  # refant as origin of phase
flag_table='flag_TarPh.flagcmd'
parallel=False ## Only works for linux atm (need to init with mpicasa -n <cores> casa)
################

# Enter at the CASA prompt the number of the step(s) to run
# and then use execfile
# e.g.
# CASA <2>:runsteps=[1,2]
# CASA <3>:execfile('NME_3C345.py')

thesteps = []
step_title = {1: 'Inspect data',
			  2: 'Remove remaining bad data',
			  3: 'Make first image of phase calibrator',
			  4: 'Derive phase solution interval',
			  5: 'Derive delay and phase only corrections',
			  6: 'Apply all calibration and re-image phase cal',
			  7: 'Derive amplitude solutions',
			  8: 'Apply solutions and re-image phase cal',
			  9: 'Apply calibration to target and split',
			  10: 'First image of target source',
			  11: 'Phase self-calibrate target and apply',
			  12: 'Image phase-self-calibrated target',
			  13: 'Amp self calibrate target and apply',
			  14: 'Image amp and phase self-calibrated target',
			  15: 'Split calibrated data',
			  16: 'Re-weigh data',
			  17: 'Image with natural and uniform weighting'
}

thesteps = []
try:
	print('List of steps to be executed ...', runsteps)
	thesteps = runsteps
except:
	print('global variable mysteps not set')

print(runsteps)

if (thesteps==[]):
	thesteps = range(0,len(step_title))
	print('Executing all steps: ', thesteps)
	

### 7) Derive amplitude solutions
mystep = 7

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	os.system('rm -rf %s_%s.ap'%(phscal,target))
	gaincal(vis='%s_%s.ms'%(phscal,target),
			caltable='%s_%s.ap'%(phscal,target),
			corrdepflags=True,
			field=phscal,
			solint='60s',
			refant=antref,
			gaintype='G',
			minblperant=4,
			solnorm=True,
			calmode='ap',
			gaintable=['%s_%s.K'%(phscal,target),'%s_%s.p'%(phscal,target)],
			interp=['nearest','nearest'],
			parang=False)

	plotms(vis='%s_%s.ap'%(phscal,target),
		   xaxis='time',yaxis='amp',
		   iteraxis='antenna',
		   coloraxis='spw',
		   antenna='SV,ZC,BD,SH,HH,YS',
	       gridrows=2,
		   gridcols=3,
		   plotfile='%s_%s.ap.png'%(phscal,target),
		   highres=True,
		   showgui=False,
		   dpi = 800,
		   width=1500,
		   height=750,
		   overwrite=True)    