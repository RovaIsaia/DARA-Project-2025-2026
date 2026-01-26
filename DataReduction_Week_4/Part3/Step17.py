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
	

### 17) Clean image using uniform, natural and robust weighting
mystep = 17
if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	os.system('rm -r target2uniform.*')
	if mac==False:
		tclean(vis='%s_calibrated.ms'%(target),
			   stokes='pseudoI',
			   psfcutoff=0.5,
			   specmode='mfs',
			   threshold=0,
			   cell='0.1mas',
			   imagename='target2uniform',
			   weighting='uniform',
			   imsize=[640,640],
			   deconvolver='clark',
			   niter=1000,
			   interactive=True,
			   parallel=parallel)
	else:
		run_iclean(vis='%s_calibrated.ms'%(target),
				   stokes='pseudoI',
				   specmode='mfs',
				   threshold=0,
				   cell='0.1mas',
				   imagename='target2uniform',
				   weighting='uniform',
				   imsize=[640,640],
				   deconvolver='clark',
				   niter=1000,
				   parallel=parallel)

	rms_u=imstat(imagename='target2uniform.image',
			   box='60,60,580,240')['rms'][0]
	peak_u=imstat(imagename='target2uniform.image',
			   box='300,300,340,340')['max'][0]

	os.system('rm -r target2natural.*')
	if mac==False:
		tclean(vis='%s_calibrated.ms'%(target),
			   stokes='pseudoI',
			   psfcutoff=0.5,
			   specmode='mfs',
			   threshold=0,
			   cell='0.24mas',
			   imagename='target2natural',
			   weighting='natural',
			   imsize=[640,640],
			   deconvolver='clark',
			   niter=1400,
			   interactive=True,
			   parallel=parallel)
	else:
		run_iclean(vis='%s_calibrated.ms'%(target),
				   stokes='pseudoI',
				   specmode='mfs',
				   threshold=0,
				   cell='0.24mas',
				   imagename='target2natural',
				   weighting='natural',
				   imsize=[640,640],
				   deconvolver='clark',
				   niter=1400,
				   parallel=parallel)

	rms_n=imstat(imagename='target2natural.image',
			   box='60,60,580,240')['rms'][0]
	peak_n=imstat(imagename='target2natural.image',
			   box='300,300,340,340')['max'][0]

	os.system('rm -r target2robust.*')
	if mac==False:
		tclean(vis='%s_calibrated.ms'%(target),
			   stokes='pseudoI',
			   psfcutoff=0.5,
			   specmode='mfs',
			   threshold=0,
			   cell='0.1mas',
			   imagename='target2robust',
			   weighting='briggs',
			   robust=0.5,
			   imsize=[640,640],
			   deconvolver='clark',
			   niter=1000,
			   interactive=True,
			   parallel=parallel)
	else:
		run_iclean(vis='%s_calibrated.ms'%(target),
				   stokes='pseudoI',
				   specmode='mfs',
				   threshold=0,
				   cell='0.1mas',
				   imagename='target2robust',
				   weighting='briggs',
				   robust=0.5,
				   imsize=[640,640],
				   deconvolver='clark',
				   niter=1000,
				   parallel=parallel)	

	rms_r=imstat(imagename='target2robust.image',
			   box='60,60,580,240')['rms'][0]
	peak_r=imstat(imagename='target2robust.image',
			   box='300,300,340,340')['max'][0]

	print('Uniform weighting:   Peak %6.3f Jy/beam, rms %6.3f mJy/beam, S/N %6.0f' % (peak_u, rms_u*1e3, peak_u/rms_u))
	print('Natural weighting:   Peak %6.3f Jy/beam, rms %6.3f mJy/beam, S/N %6.0f' % (peak_n, rms_n*1e3, peak_n/rms_n))
	print('Robust 0.5 weighting:Peak %6.3f Jy/beam, rms %6.3f mJy/beam, S/N %6.0f' % (peak_r, rms_r*1e3, peak_r/rms_r))