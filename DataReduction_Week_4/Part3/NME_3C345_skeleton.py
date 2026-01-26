"""
Script for calibration and imaging of EVN n14c3 data for J1849+3024/1848+283
NME_all.py or the instructions from the web page should first have been.
run to provide a file with Tsys/gain curve, initial delay and bandpass
calibration applied, 1848+283_J1849+3024.ms (or if this is not available,
use 1848+283_J1849+3024.ms.tgz)
The steps are outline on a web page.

This is the skeleton file. If you really get stuck then use the
NME_3C345_all.py file.

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
target='**'
phscal='**'
antref='**'                  # refant as origin of phase
flag_table='**'   ## wait until step 2 to set this!
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


### 1) Inspect data to remove remaining bad data
mystep = 1

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	## Hints - we want to look for bad data i.e. when amp goes to zero.
	## You want to look on both the time and frequency axis, but remember to
	## average data so that plotting isn't slow.
	## Look at the flag_template.flagcmd file for the parameters we want to note
	## down when we identify bad data i.e. field, spw, time range and fill this
	## file in for the next step.
	listobs(vis='J1640+3946_3C345.ms',
    	    listfile='J1640+3946_3C345.listobs.txt',)
	plotms(vis='J1640+3946_3C345.ms',
		   xaxis='time',
		   yaxis='amp',
		   antenna='EF&*')

### 2) Apply flagtable and check bad data is gone
mystep = 2

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	### Backup the flags (remember you can use this to restore the flags after)
	flagmanager('**')

	### Hints: Use the help functions or the CASA docs to see the correct inputs for flagdata
	flagdata('**')

	### Check the bad data have gone
	plotms('**')

### 3) Initial imaging from fringe fitting of phase calibrator
mystep = 3

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	#os.system('rm -r %s_phs_ref.*'%phscal)
	### Hints: we need a task that will image the phase cal (i.e., tclean for linux users and run_iclean for macOS)
	### And a task to FT the phs cal model into the measurement set

	# Measure the S/N to track calibration! This has been given, just set the boxes
	rms=imstat(imagename='xx',
			   box='xx,xx,xx,xx')['rms'][0]
	peak=imstat(imagename='xx',
			   box='xx,xx,xx,xx')['max'][0]

	print('Peak %6.3f, rms %6.3f, S/N %6.0f' % (peak, rms, peak/rms))

### 4) Get the solution interval for phase calibrator
mystep = 4

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	### Hints: Plot target and phase-ref, phase against time, averaging channels
	

### 5) Derive solutions and plot
mystep = 5

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	### Hints: We need to derive delay and phase calibration solutions against time.
	### We need to plot these solution tables also. 
	### You should need to use four commands, comprising of two tasks. 


### 6) Apply phase solutions and clean phase-reference again
mystep = 6

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	### Hints: We want to now apply these solutions to the phase calibrator ONLY
	### Then we want to image the phase calibrator again and FT the model into the data.
	### Make sure that the image name makes some implicit reference to the calibration step 
	### so you can distinguish it.
	### Remember to include the peak, rms code from earlier to track the S/N improvement.
	### You should need 4 CASA tasks to do these.


### 7) Derive amplitude solutions
mystep = 7

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	### Hints: we want to derive amplitude solutions
	### Remember these change slower & need higher S/N
	### Per scan solution intervals should be ok.
	### Remember these should be plotted and solutions need to be normalised!
	### (as we set the fluxscale earlier!)
	### You should need 2 tasks only!

### 8) Apply amp solutions and clean phase reference again
mystep = 8

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	### Hints: this step is similar to part 6
	### Apply all of the calibration derived so far to the phase calibrator
	### Image the phase cal again, and assess the calibration by deriving the S/N
	### You need 3 tasks to do this and inputs should be *almost* identical to part 6

### 9) Apply solutions to target and split
mystep = 9

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	### Hints: Apply the calibration solutions to the phase cal and image
	### remember about the appropriate interpolation
	### We also want to split out the calibrated target data for the self-cal stages
	### You will need two tasks to do these
	

### 10) Image target
mystep = 10

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	### Hints: We want to image our target using the new measurement set
	### We also want to include the model into the visibilties for self-cal
	### And we want to track the improvements in S/N again (check that the boxes are still good!)
	### You'll need 4 tasks for this step
	### Remember to set timerange due to non-phase referenced scans!

### 11) Get phase corrections
mystep = 11

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	### Hints: We now want to use the model to derive phase self-cal solutions
	### You'll need two tasks as we want to plot the solutions too
	### Remember that the solution interval should allow us to track the phase
	### *within* each scan

### 12) Apply and image again
mystep = 12

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	### Hints: We want to apply these solutions, image the improvements,
	### FT the new model into the visibilties and track S/N improvements
	### The parameters can be similar to before but remember to apply to the new ms (3C345.ms)
	### You'll need 5 tasks to do this part!
	

### 13) Derive amplitude solutions
mystep = 13

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	### Hints: In this part we want to derive amplitude solutions
	### The new model should be in the data 
	### We want to also plot these solutions so a total of 2 tasks are needed for this step
	

### 14) Apply and image
mystep = 14

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	### Hints: We should now see if these solutions improve the data
	### Use 3 tasks to apply these solutions, image the data and then track the S/N

### 15) Split calibrated data
mystep = 15

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])
	os.system('rm -r '+target+'_calibrated.ms')
	split(vis='xx',
		  outputvis=target+'_calibrated.ms')

### 16) Re-weigh data
mystep = 16

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])
	statwt(vis=target+'_calibrated.ms',
		   datacolumn='data')
	### Type in parameters to plot weight vs uvwave for all baselines to Onsala (ON)
	plotms('**')

### 17) Clean image using uniform, natural and robust weighting
mystep = 17
if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	os.system('rm -r target2uniform.*')
	if mac==False:
		tclean(vis=target+'_calibrated.ms',
			   imagename='target2uniform',
			   specmode='mfs',
			   threshold=0,
			   cell='**',
			   weighting='**')
	else:
		run_iclean(vis=target+'_calibrated.ms',
				   imagename='target2uniform',
				   specmode='mfs',
				   threshold=0,
				   cell='**',
				   weighting='**')	

	rms_u=imstat(imagename='target2uniform.image',
			   box='**,**,**,**')['rms'][0]
	peak_u=imstat(imagename='target2uniform.image',
			   box='**,**,**,**')['max'][0]

	os.system('rm -r target2natural.*')
	if mac==False:
		tclean(vis=target+'_calibrated.ms',
			   imagename='target2natural',
			   specmode='mfs',
			   threshold=0,
			   cell='**',
			   weighting='**')
	else:
		run_iclean(vis=target+'_calibrated.ms',
				   imagename='target2natural',
				   specmode='mfs',
				   threshold=0,
				   cell='**',
				   weighting='**')

	rms_n=imstat(imagename='target2natural.image',
			   box='**,**,**,**')['rms'][0]
	peak_n=imstat(imagename='target2natural.image',
			   box='**,**,**,**')['max'][0]

	os.system('rm -r target2robust.*')
	if mac==False:
		tclean(vis=target+'.ms',
			   imagename='target2robust',
			   specmode='mfs',
			   threshold=0,
			   cell='**',
			   weighting='**')
	else:
		run_iclean(vis=target+'.ms',
				   imagename='target2robust',
				   specmode='mfs',
				   threshold=0,
				   cell='**',
				   weighting='**')

	rms_r=imstat(imagename='target2robust.image',
			   box='**,**,**,**')['rms'][0]
	peak_r=imstat(imagename='target2robust.image',
			   box='**,**,**,**')['max'][0]
	
	print('Uniform weighting:   Peak %6.3f Jy/beam, rms %6.3f mJy/beam, S/N %6.0f' % (peak_u, rms_u*1e3, peak_u/rms_u))
	print('Natural weighting:   Peak %6.3f Jy/beam, rms %6.3f mJy/beam, S/N %6.0f' % (peak_n, rms_n*1e3, peak_n/rms_n))
	print('Robust 0.5 weighting:Peak %6.3f Jy/beam, rms %6.3f mJy/beam, S/N %6.0f' % (peak_r, rms_r*1e3, peak_r/rms_r))