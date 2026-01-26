"""
Script for calibration and imaging of EVN n14c3 data for J1849+3024/1848+283
NME_all.py or the instructions from the web page should first have been.
run to provide a file with Tsys/gain curve, initial delay and bandpass
calibration applied, 1848+283_J1849+3024.ms)

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
antref='EF'         # refant is antenna where phase terms are relative to
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

### 1) Image phase calibrator
mystep = 1

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	# Image the phase calibrator with tclean

	os.system('rm -r '+phscal+'_p0.*')
	if mac==False:
		tclean(vis=phscal+'_'+target+'.ms',
			imagename='phasecal1p0',
			stokes='pseudoI',
			psfcutoff=0.5,
			specmode='mfs',
			threshold=0,
			field='xxx',
			imsize=['xxx','xxx'],
			cell=['xxx'],
			gridder='xxx',
			deconvolver='xxx',
			niter='xxx',
			interactive=True)
	else:
		run_iclean(vis=phscal+'_'+target+'.ms',
				   imagename='phasecal1p0',
				   stokes='pseudoI',
				   specmode='mfs',
				   threshold=0,
				   field='xxx',
				   imsize=['xxx','xxx'],
				   cell=['xxx'],
				   gridder='xxx',
				   deconvolver='xxx',
				   niter='xxx')

### 2) Get image information
mystep = 2

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	# Measure the signal-to-noise
	rms=imstat(imagename='phasecal1p0.image',
			   box='xxx,xxx,xxx,xxx')['rms'][0]
	peak=imstat(imagename='phasecal1p0.image',
			   box='xxx,xxx,xxx,xxx')['max'][0]

	print('Peak %6.3f Jy/beam, rms %6.3f Jy/beam, S/N %6.0f' % (peak, rms, peak/rms))

### 3) Generate model column for self-cal
mystep = 3

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	# Fourier transform model into the visibilities
	ft(vis=phscal+'_'+target+'.ms',
	   field='xxx',
	   model='xxx',
	   usescratch=True)

### 4) Refine delay calibration 
mystep = 4

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	# Gain calibration of phases only
	os.system('rm -r '+phscal+'_'+target+'.K')
	gaincal(vis=phscal+'_'+target+'.ms',
			field='xxx',
			caltable=phscal+'_'+target+'.K',
			corrdepflags=True,
			solint='xxx',
			refant='xxx',
			minblperant='xxx',
			gaintype='xxx',
			parang='xxx')

	plotms(vis=phscal+'_'+target+'.K',
		   gridrows=2,
		   gridcols=3,
		   yaxis='xxx',
		   xaxis='xxx',
		   iteraxis='xxx',
		   coloraxis='xxx')

### 5) Refine phase calibration
mystep = 5

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	# Gain calibration of phases only
	os.system('rm -r '+phscal+'_'+target+'.p')
	gaincal(vis=phscal+'_'+target+'.ms',
			field=phscal,
			caltable=phscal+'_'+target+'.p',
			corrdepflags=True,
			solint='xxx',
			refant='xxx',
			gaintype='xxx',
			minblperant='xxx',
			calmode='xxx',
			gaintable=['xxx'],
			parang='xxx')

	plotms(vis=phscal+'_'+target+'.p',
		   gridrows=2,
		   gridcols=3,
		   plotrange=[0,0,-180,180],
		   yaxis='xxx',
		   xaxis='xxx',
		   iteraxis='xxx',
		   coloraxis='xxx')

# 6) Apply delay and phases
mystep = 6

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	# Apply these solutions to the phase cal
	applycal(vis=phscal+'_'+target+'.ms',
			 field='xxx',
			 gaintable=['xxx','xxx'],
			 gainfield=['xxx','xxx'],
			 interp=['xx','xx'],
			 applymode='xxx',
			 parang=False)

### 7) Image phase calibrator again!
mystep = 7

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	os.system('rm -r phasecal1p1.*')
	if mac==False:
		tclean(vis=phscal+'_'+target+'.ms',
			   imagename='phasecal1_p1',
			   stokes='pseudoI',
			   psfcutoff=0.5,
			   specmode='mfs',
			   threshold=0,
			   field='xxx',
			   imsize=['xxx','xxx'],
			   cell=['xxx'],
			   gridder='xxx',
			   deconvolver='xxx',
			   niter='xxx',
			   interactive=True)
	else:
		run_iclean(vis=phscal+'_'+target+'.ms',
				   imagename='phasecal1p1',
				   stokes='pseudoI',
				   specmode='mfs',
				   threshold=0,
				   field='xxx',
				   imsize=['xxx','xxx'],
				   cell=['xxx'],
				   gridder='xxx',
				   deconvolver='xxx',
				   niter='xxx')

	# Measure the signal-to-noise
	rms=imstat(imagename='phasecal1p1.image',
			   box='xxx,xxx,xxx,xxx')['rms'][0]
	peak=imstat(imagename='phasecal1p1.image',
			    box='xxx,xxx,xxx,xxx')['max'][0]

	ft(vis=phscal+'_'+target+'.ms',
	   field='xxx',
	   model='xxx',
	   usescratch=True)
	
	print('Peak %6.3f Jy/beam, rms %6.3f mJy/beam, S/N %6.0f' % (peak, rms*1e3, peak/rms))

### 8) Derive amplitude solutions
mystep = 8

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])
	os.system('rm -rf'+phscal+'_'+target+'.ap')
	gaincal(vis=phscal+'_'+target+'.ms',
			caltable=phscal+'_'+target+'.ap',
			corrdepflags=True,
			field='xxx',
			solint='xxx',
			refant='xxx',
			solnorm='xxx',
			gaintype='xxx',
			minblperant='xxx',
			calmode='xxx',
			gaintable=['xxx','xxx'],
			gainfield=['xxx','xxx'],
			interp=['linear','linear'],
			parang=False)

	plotms(vis=phscal+'_'+target+'.ap',
		   gridrows=2,
		   gridcols=3,
		   yaxis='xxx',
		   xaxis='xxx',
		   iteraxis='antenna',
		   coloraxis='spw')

### 9) Apply all calibration to the phase calibrator
mystep = 9

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	applycal(vis=phscal+'_'+target+'.ms',
			 field='xxx',
			 gaintable=['xxx','xxx','xxx'],
			 gainfield=['xxx','xxx','xxx'],
			 interp=['xxx','xxx','xxx'],
			 parang=False)

### 10) Image phase calibrator for last time
mystep = 10

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])
	os.system('rm -r phasecal1ap1.*')
	if mac==False:
		tclean(vis=phscal+'_'+target+'.ms',
			   imagename='phasecal1ap1',
			   stokes='pseudoI',
			   psfcutoff=0.5,
			   specmode='mfs',
			   threshold=0,
			   field='xx',
			   imsize=['xx','xx'],
			   cell=['xxx'],
			   gridder='standard',
			   deconvolver='xxx',
			   niter='xxx',
			   interactive=True)
	else:
		run_iclean(vis=phscal+'_'+target+'.ms',
				   imagename='phasecal1ap1',
				   stokes='pseudoI',
				   specmode='mfs',
				   threshold=0,
				   field='xx',
				   imsize=['xx','xx'],
				   cell=['xxx'],
				   gridder='standard',
				   deconvolver='xxx',
				   niter='xxx')

	# Measure the signal to noise
	rms=imstat(imagename='phasecal1ap1.image',
			   box='xxx,xxx,xxx,xxx')['rms'][0]
	peak=imstat(imagename='phasecal1ap1.image',
			   box='xxx,xxx,xxx,xxx')['max'][0]

	print('Peak %6.3f Jy/beam, rms %6.4f mJy/beam, S/N %6.0f' % (peak, rms*1e3, peak/rms))

### 11) Apply refined solutions to the target source
mystep = 11

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])
	delmod(vis=phscal+'_'+target+'.ms')
	applycal(vis=phscal+'_'+target+'.ms',
			 field='xxx',
			 gaintable=['xxx','xxx','xxx'],
			 gainfield=['xxx','xxx','xxx'],
			 interp=['xxx','xxx','xxx'],
			 applymode='calonly',
			 parang=False)

### 12) Split target data out from the measurement set
mystep = 12

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])
	os.system('rm -rf '+target+'.ms')
	os.system('rm -rf '+target+'.ms.flagversions')
	split(vis=phscal+'_'+target+'.ms',
		  outputvis=target+'.ms',
		  field='xxx',
		  correlation='xx,xx',
		  datacolumn='xxx')


#############################
### Now for target only!! ###
#############################

### 13) First image of the target
mystep = 13

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])
	
	os.system('rm -r target1phsref*')
	if mac==False:
		tclean(vis=target+'.ms',
			   imagename='target1phsref',
			   stokes='pseudoI',
			   psfcutoff=0.5,
			   specmode='mfs',
			   threshold=0,
			   imsize=['xxx','xxx'],
			   cell=['xxx'],
			   gridder='standard',
			   deconvolver='xxx',
			   niter='xxx',
			   interactive=True)
	else:
		run_iclean(vis=target+'.ms',
				   imagename='target1phsref',
				   stokes='pseudoI',
				   specmode='mfs',
				   threshold=0,
				   imsize=['xxx','xxx'],
				   cell=['xxx'],
				   gridder='standard',
				   deconvolver='xxx',
				   niter='xxx')
		
	ft(vis=target+'.ms',
	   model='target1phsref.model',
	   usescratch=True)

	# Measure the signal to noise
	rms=imstat(imagename='target1phsref.image',
			   box='xx,xx,xx,xx')['rms'][0]
	peak=imstat(imagename='target1phsref.image',
			   box='xx,xx,xx,xx')['max'][0]

	print('Peak %6.3f mJy/beam, rms %6.4f mJy/beam, S/N %6.0f' % (peak*1e3, rms*1e3, peak/rms))

### 14) Get phase solution interval for phase self-calibration
mystep = 14

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	plotms(vis=target+'.ms',
		   xaxis='xxx',
		   yaxis='xxx',
		   correlation='xx',
		   antenna='xxx',
		   iteraxis='xxx',
		   avgtime='xx',
		   avgchannel='xx')

### 15) Derive phase self-calibration solutions
mystep = 15

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	os.system('rm -rf '+target+'.p')
	gaincal(vis=target+'.ms',
			caltable=target+'.p',
			corrdepflags=True,
			solint='xx',
			refant='xx',
			gaintype='xx',
			calmode='xx',
			parang=False)

	plotms(vis=target+'.p',
		   gridrows=2,
		   gridcols=3,
		   plotrange=[0,0,-180,180],
		   yaxis='xxx',
		   xaxis='xxx',
		   iteraxis='xxx',
		   coloraxis='xxx')

### 16) Apply and image target again
mystep = 16

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])
	applycal(vis=target+'.ms',
			 gaintable=[target+'.p'],
			 interp=['xx'],
			 applymode='calonly',
			 parang=False)

	os.system('rm -r target1p*')
	if mac==False:
		tclean(vis=target+'.ms',
			   imagename='target1p',
			   stokes='pseudoI',
			   psfcutoff=0.5,
			   gridmode='mfs',
			   threshold=0,
			   imsize=['xxx','xxx'],
			   cell=['xxx'],
			   gridder='standard',
			   deconvolver='clark',
			   niter='xxx',
			   interactive=True)
	else:
		run_iclean(vis=target+'.ms',
				   imagename='target1p',
				   stokes='pseudoI'
				   gridmode='mfs',
				   threshold=0,
				   imsize=['xxx','xxx'],
				   cell=['xxx'],
				   gridder='standard',
				   deconvolver='clark',
				   niter='xxx')
	
	ft(vis=target+'.ms',
	   model='xxx',
	   usescratch=True)

	# Measure the signal to noise
	rms=imstat(imagename='target1p.image',
			   box='xx,xx,xx,xx')['rms'][0]
	peak=imstat(imagename='target1p.image',
			   box='xx,xx,xx,xx')['max'][0]

	print('Peak %6.3f Jy/beam, rms %6.4f mJy/beam, S/N %6.0f' % (peak, rms*1e3, peak/rms))

### 17) Look at structure of target
mystep = 17

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])
	plotms(vis=target+'.ms',
		   xaxis='uvwave',
		   yaxis='amp',
		   ydatacolumn='corrected',
		   coloraxis='antenna2',
		   avgchannel='32',
		   avgtime='30',
		   correlation='RR,LL',
		   plotfile=target+'.amp_vs_uv_scp.png',
		   overwrite=True)

	plotms(vis=target+'.ms',
		   xaxis='uvwave',
		   yaxis='amp',
		   ydatacolumn='model',
		   field=target,
		   correlation='RR,LL',
		   coloraxis='antenna2',
		   avgchannel='32',
		   plotfile=target+'.amp_vs_uv-model_scp.png',
		   overwrite=True)

	plotms(vis=target+'.ms',
		   xaxis='uvwave',
		   yaxis='phase',
		   ydatacolumn='corrected',
		   field=target,
		   correlation='RR,LL',
		   coloraxis='antenna2',
		   avgchannel='32',
		   avgtime='30',
		   plotfile=target+'.p_vs_uv_scp.png',
		   overwrite=True)

### 18) Derive amplitude solutions
mystep = 18
if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	os.system('rm -rf '+target+'.ap')

	gaincal(vis=target+'.ms',
			caltable=target+'.ap',
			corrdepflags=True,
			solint='xx',
			refant='xx',
			gaintype='xx',
			solnorm='xx',
			calmode='xx',
			gaintable=['xx'],
			parang=False)

	plotms(vis=target+'.ap',
		   gridrows=2,
		   gridcols=3,
		   yaxis='xxx',
		   xaxis='xxx',
		   iteraxis='xxx',
		   coloraxis='xxx')

	applycal(vis=target+'.ms',
			 gaintable=['xx','xx'],
			 applymode='calonly',
			 parang=False)

### 19) Final imaging of target
mystep = 19
if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	os.system('rm -r target1ap.*')
	if mac==False:
		tclean(vis=target+'.ms',
			   imagename='target1ap',
			   stokes='pseudoI',
			   psfcutoff=0.5,
			   specmode='mfs',
			   threshold=0,
			   imsize=['xx','xx'],
			   cell=['xx'],
			   gridder='standard',
			   deconvolver='clark',
			   niter='xx',
			   interactive=True)
	else:
		run_iclean(vis=target+'.ms',
				   imagename='target1ap',
				   stokes='pseudoI',
				   specmode='mfs',
				   threshold=0,
				   imsize=['xx','xx'],
				   cell=['xx'],
				   gridder='standard',
				   deconvolver='clark',
				   niter='xx')

	ft(vis=target+'.ms',
	   model='target1ap.model',
	   usescratch=True)

	# Measure the signal to noise
	rms=imstat(imagename='target1ap.image',
			   box='xx,xx,xx,xx')['rms'][0]
	peak=imstat(imagename='target1ap.image',
			   box='xx,xx,xx,xx')['max'][0]

	print('Peak %6.3f Jy/beam, rms %6.4f mJy/beam, S/N %6.0f' % (peak, rms*1e3, peak/rms))

	plotms(vis=target+'.ms',
		   xaxis='uvdist',
		   yaxis='amp',
		   ydatacolumn='corrected',
		   coloraxis='antenna2',
		   avgchannel='32',
		   avgtime='30',
		   correlation='RR,LL',
		   plotfile=target+'.amp_vs_uv_scap.png',
		   overwrite=True)

	plotms(vis=target+'.ms',
		   xaxis='uvdist',
		   yaxis='amp',
		   ydatacolumn='model',
		   field=target,
		   correlation='RR,LL',
		   coloraxis='antenna2',
		   avgchannel='32',
		   plotfile=target+'.amp_vs_uv-model_scap.png',
		   overwrite=True)

	plotms(vis=target+'.ms',
		   xaxis='uvdist',
		   yaxis='phase',
		   ydatacolumn='corrected',
		   coloraxis='antenna2',
		   avgchannel='32',
		   avgtime='30',
		   correlation='RR,LL',
		   plotfile=target+'.phase_vs_uv_scap.png',
		   overwrite=True)