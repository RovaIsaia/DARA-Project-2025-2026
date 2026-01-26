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

### 1) Image phase calibrator
mystep = 1

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	# Image the phase calibrator with tclean

	os.system('rm -r phasecal1p0.*')
	if mac==False:
		tclean(vis='%s_%s.ms'% (phscal,target),
			   imagename='phasecal1p0',
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
				   imagename='phasecal1p0',
				   stokes='pseudoI',
				   specmode='mfs',
				   threshold=0,
				   field='%s'%phscal,
				   imsize=[640,640],
				   cell=['0.24mas'],
				   gridder='standard',
				   deconvolver='clark',
				   niter=1000)

### 2) Get image information
mystep = 2

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	# Measure the signal-to-noise
	rms=imstat(imagename='phasecal1p0.image',
			   box='60,60,580,240')['rms'][0]
	peak=imstat(imagename='phasecal1p0.image',
			   box='300,300,340,340')['max'][0]

	print('Peak %6.3f Jy/beam, rms %6.3f Jy/beam, S/N %6.0f' % (peak, rms, peak/rms))

### 3) Generate model column for self-cal
mystep = 3

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	# Fourier transform model into the visibilities
	ft(vis='%s_%s.ms'% (phscal,target),
	   field='%s'%phscal,
	   model='phasecal1p0.model',
	   usescratch=True)

### 4) Refine delay calibration 
mystep = 4

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	# Gain calibration of phases only
	os.system('rm -r %s_%s.K'%(phscal,target))
	gaincal(vis='%s_%s.ms'% (phscal,target),
			field='%s'%phscal,
			caltable='%s_%s.K'%(phscal,target),
			corrdepflags=True,
			solint='inf',
			refant=antref,
			minblperant=3,
			gaintype='K',
			parang=False)

	plotms(vis=phscal+'_'+target+'.K',
		   gridrows=2,
		   gridcols=3,
		   yaxis='delay',
		   xaxis='time',
		   iteraxis='antenna',
		   coloraxis='spw')

### 5) Refine phase calibration
mystep = 5

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	# Gain calibration of phases only
	os.system('rm -r %s_%s.p'%(phscal,target))
	gaincal(vis='%s_%s.ms'% (phscal,target),
			field='%s'%phscal,
			caltable='%s_%s.p'%(phscal,target),
			corrdepflags=True,
			solint='20s',
			refant=antref,
			minblperant=3,
			gaintype='G',
			calmode='p',
			gaintable=['%s_%s.K'%(phscal,target)],
			parang=False)

	plotms(vis='%s_%s.p'%(phscal,target),
		   gridrows=2,
		   gridcols=3,
		   plotrange=[0,0,-180,180],
		   yaxis='phase',
		   xaxis='time',
		   iteraxis='antenna',
		   coloraxis='spw')

# 6) Apply delay and phases
mystep = 6

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	# Apply these solutions to the phase cal and image
	applycal(vis='%s_%s.ms'% (phscal,target),
			 field=phscal,
			 gaintable=['%s_%s.K'%(phscal,target),'%s_%s.p'%(phscal,target)],
			 gainfield=[phscal,phscal],
			 interp=['linear','linear'],
			 applymode='',
			 parang=False)

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

### 8) Derive amplitude solutions
mystep = 8

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])
	os.system('rm -rf %s_%s.ap'% (phscal,target))
	gaincal(vis='%s_%s.ms'% (phscal,target),
			caltable='%s_%s.ap'% (phscal,target),
			corrdepflags=True,
			field=phscal,
			solint='inf',
			refant=antref,
			solnorm=True,
			gaintype='G',
			minblperant=4,
			calmode='ap',
			gaintable=['%s_%s.K'%(phscal,target),'%s_%s.p'%(phscal,target)],
			gainfield=[phscal,phscal],
			interp=['linear','linear'],
			parang=False)

	plotms(vis='%s_%s.ap'%(phscal,target),
		   gridrows=2,
		   gridcols=3,
		   yaxis='amp',
		   xaxis='time',
		   iteraxis='antenna',
		   coloraxis='spw')

### 9) Apply all calibration to the phase calibrator
mystep = 9

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	applycal(vis='%s_%s.ms'% (phscal,target),
			 field=phscal,
			 gaintable=['%s_%s.K'%(phscal,target),'%s_%s.p'%(phscal,target),'%s_%s.ap'%(phscal,target)],
			 gainfield=[phscal,phscal,phscal],
			 interp=['linear','linear','linear'],
			 parang=False)

### 10) Image phase calibrator for last time
mystep = 10

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])
	os.system('rm -r phasecal1ap1.*')
	if mac==False:
		tclean(vis='%s_%s.ms'% (phscal,target),
			   imagename='phasecal1ap1',
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
				   imagename='phasecal1ap1',
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
	rms=imstat(imagename='phasecal1ap1.image',
			   box='60,60,580,240')['rms'][0]
	peak=imstat(imagename='phasecal1ap1.image',
			   box='300,300,340,340')['max'][0]

	print('Peak %6.3f Jy/beam, rms %6.4f mJy/beam, S/N %6.0f' % (peak, rms*1e3, peak/rms))

### 11) Apply refined solutions to the target source
mystep = 11

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])
	delmod(vis='%s_%s.ms'% (phscal,target))
	applycal(vis='%s_%s.ms'% (phscal,target),
			 field=target,
			 gaintable=['%s_%s.K'%(phscal,target),'%s_%s.p'%(phscal,target),'%s_%s.ap'%(phscal,target)],
			 gainfield=[phscal],
			 interp=['linear','linear','linear'],
			 applymode='calonly',
			 parang=False)

### 12) Split target data out from the measurement set
mystep = 12

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])
	os.system('rm -rf %s.ms'%target)
	os.system('rm -rf %s.ms.flagversions'%target)
	split(vis='%s_%s.ms'% (phscal,target),
		  outputvis='%s.ms'%target,
		  field=target,
		  correlation='RR,LL',
		  datacolumn='corrected')


#############################
### Now for target only!! ###
#############################

### 13) First image of the target
mystep = 13

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])
	
	os.system('rm -r target1phsref*')
	if mac==False:
		tclean(vis='%s.ms'% target,
			   imagename='target1phsref',
			   stokes='pseudoI',
			   psfcutoff=0.5,
			   specmode='mfs',
			   threshold=0,
			   imsize=[640,640],
			   cell=['0.24mas'],
			   gridder='standard',
			   deconvolver='clark',
			   niter=1000,
			   interactive=True)
	else:
		run_iclean(vis='%s.ms'% target,
				   imagename='target1phsref',
				   stokes='pseudoI',
				   specmode='mfs',
				   threshold=0,
				   imsize=[640,640],
				   cell=['0.24mas'],
				   gridder='standard',
				   deconvolver='clark',
				   niter=1000)

	ft(vis=target+'.ms',
	   model='target1phsref.model',
	   usescratch=True)

	# Measure the signal to noise
	rms=imstat(imagename='target1phsref.image',
			   box='60,60,580,240')['rms'][0]
	peak=imstat(imagename='target1phsref.image',
			   box='300,300,340,340')['max'][0]

	print('Peak %6.3f mJy/beam, rms %6.4f mJy/beam, S/N %6.0f' % (peak*1e3, rms*1e3, peak/rms))

### 14) Get phase solution interval for phase self-calibration
mystep = 14

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	plotms(vis=target+'.ms',
		   xaxis='time',
		   yaxis='phase',
		   correlation='LL',
		   antenna='%s&*'%antref,
		   iteraxis='baseline',
		   avgchannel='32',
		   avgtime='')

### 15) Derive phase self-calibration solutions
mystep = 15

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	os.system('rm -rf '+target+'.p')
	gaincal(vis='%s.ms'%target,
			caltable='%s.p'%target,
			corrdepflags=True,
			solint='20s',
			refant=antref,
			gaintype='G',
			calmode='p',
			parang=False)

	plotms(vis=target+'.p',
		   gridrows=2,
		   gridcols=3,
		   plotrange=[0,0,-180,180],
		   yaxis='phase',
		   xaxis='time',
		   iteraxis='antenna',
		   coloraxis='spw')

### 16) Apply and image target again
mystep = 16

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])
	applycal(vis='%s.ms'% (target),
			 gaintable=['%s.p'%(target)],
			 interp=['linear'],
			 applymode='calonly',
			 parang=False)

	os.system('rm -r target1p')
	if mac==False:
		tclean(vis='%s.ms'% target,
			   imagename='target1p',
			   stokes='pseudoI',
			   psfcutoff=0.5,
			   specmode='mfs',
			   threshold=0,
			   imsize=[640,640],
			   cell=['0.24mas'],
			   gridder='standard',
			   deconvolver='clark',
			   niter=1000,
			   interactive=True)
	else:
		run_iclean(vis='%s.ms'% target,
				   imagename='target1p',
				   stokes='pseudoI',
				   specmode='mfs',
				   threshold=0,
				   imsize=[640,640],
				   cell=['0.24mas'],
				   gridder='standard',
				   deconvolver='clark',
				   niter=1000)

	ft(vis='%s.ms'% target,
	   model='target1p.model',
	   usescratch=True)

	# Measure the signal to noise
	rms=imstat(imagename='target1p.image',
			   box='60,60,580,240')['rms'][0]
	peak=imstat(imagename='target1p.image',
			   box='300,300,340,340')['max'][0]

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

	os.system('rm -rf %s.ap'%target)

	gaincal(vis=target+'.ms',
			caltable=target+'.ap',
			corrdepflags=True,
			solint='60s',
			refant=antref,
			gaintype='G',
			solnorm=True,
			calmode='ap',
			gaintable=[target+'.p'],
			parang=False)

	plotms(vis=target+'.ap',
		   gridrows=2,
		   gridcols=3,
		   yaxis='amp',
		   xaxis='time',
		   iteraxis='antenna',
		   coloraxis='spw')

	applycal(vis=target+'.ms',
			 gaintable=[target+'.p',target+'.ap'],
			 applymode='calonly',
			 parang=False)

### 19) Final imaging of target
mystep = 19
if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	os.system('rm -r target1ap*')
	if mac==False:
		tclean(vis='%s.ms'% target,
			   imagename='target1ap',
			   stokes='pseudoI',
			   psfcutoff=0.5,
			   specmode='mfs',
			   threshold=0,
			   imsize=[640,640],
			   cell=['0.24mas'],
			   gridder='standard',
		 	   deconvolver='clark',
			   niter=1000,
			   interactive=True)
	else:
		run_iclean(vis='%s.ms'% target,
				   imagename='target1ap',
				   stokes='pseudoI',
				   specmode='mfs',
				   threshold=0,
				   imsize=[640,640],
				   cell=['0.24mas'],
				   gridder='standard',
		 		   deconvolver='clark',
				   niter=1000)

	ft(vis='%s.ms'% target,
	   model='target1ap.model',
	   usescratch=True)

	# Measure the signal to noise
	rms=imstat(imagename='target1ap.image',
			   box='60,60,580,240')['rms'][0]
	peak=imstat(imagename='target1ap.image',
			   box='300,300,340,340')['max'][0]

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