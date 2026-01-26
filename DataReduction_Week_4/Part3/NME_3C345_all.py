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


### 1) Inspect data to remove remaining bad data
mystep = 1

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	plotms(vis='%s_%s.ms'%(phscal,target),
		   xaxis='time',
		   yaxis='amp',
		   field='%s,%s'%(phscal,target),
		   correlation='RR,LL',
		   coloraxis='field',
		   avgchannel='32',
		   antenna='*&*',
		   iteraxis='baseline',
		   plotfile='inspect_data.png',
		   highres=True,
		   showgui=False,
		   dpi = 800,
		   width=1500,
		   height=750,
		   overwrite=True)

### 2) Apply flagtable and check bad data is gone
mystep = 2

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	flagmanager(vis='%s_%s.ms'%(phscal,target),
				mode='save',versionname='pre_flagging')

	flagdata(vis='%s_%s.ms'%(phscal,target),
			 mode='list',
			 inpfile=flag_table)

	# Check the bad data have gone
	plotms(vis='%s_%s.ms'%(phscal,target),
		   xaxis='time',
		   yaxis='amp',
		   ydatacolumn='data',
		   field=phscal,
		   antenna='%s&*'%antref,
		   correlation='RR,LL',
		   coloraxis='antenna2',
		   avgchannel='32',
		   plotfile='%s_%s.pre-amp-cal.png'%(phscal,target),
		   highres=True,
		   showgui=False,
		   dpi = 800,
		   width=1500,
		   height=750,
		   overwrite=True)

### 3) Initial imaging from fringe fitting of phase calibrator
mystep = 3

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	os.system('rm -r phasecal2p0.*')
	if mac == False:
		tclean(vis='%s_%s.ms'%(phscal,target),
			   stokes='pseudoI',
			   psfcutoff=0.5,
			   specmode='mfs',
			   threshold=0,
			   cell='0.24mas',
			   field=phscal,
			   imagename='phasecal2p0',
			   imsize=[640,640],
			   deconvolver='clark',
			   niter=1000,
			   cycleniter=50,
			   interactive=True,
			   parallel=parallel)
	else:
		run_iclean(vis='%s_%s.ms'%(phscal,target),
				   stokes='pseudoI',
				   specmode='mfs',
				   threshold=0,
				   cell='0.24mas',
				   field=phscal,
				   imagename='phasecal2p0',
				   imsize=[640,640],
				   deconvolver='clark',
				   niter=1000,
				   cycleniter=50,
				   parallel=parallel)

	ft(vis='%s_%s.ms'%(phscal,target),
	   field=phscal,
	   model='phasecal2p0.model',
	   usescratch=True)

	# A source! with mainly symmetric artefacts characteristic of amplitude errors.
	# Measure the signal-to-noise
	rms=imstat(imagename='phasecal2p0.image',
			   box='60,60,580,240')['rms'][0]
	peak=imstat(imagename='phasecal2p0.image',
			   box='300,300,340,340')['max'][0]

	print('Peak %6.3f Jy/beam, rms %6.3f mJy/beam, S/N %6.0f' % (peak, rms*1e3, peak/rms))

### 4) Get the solution interval for phase calibrator
mystep = 4

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	# Plot target and phase-ref, phase against time, averaging channels
	plotms(vis='%s_%s.ms'%(phscal,target),
		   xaxis='time',
		   yaxis='phase',
		   spw='1',
		   field='%s,%s'%(phscal,target),
		   correlation='RR,LL',
		   coloraxis='field',
		   avgchannel='32',
		   antenna='%s&*'%antref,
		   iteraxis='baseline',
		   plotfile='phase_cal_target_phases.png',
		   highres=True,
		   showgui=False,
		   dpi = 800,
		   width=1500,
		   height=750,
		   overwrite=True)

### 5) Derive solutions and plot
mystep = 5

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	os.system('rm -rf %s_%s.ms.K'%(phscal,target))
	gaincal(vis='%s_%s.ms'%(phscal,target),
			caltable='%s_%s.K'%(phscal,target),
			corrdepflags=True,
			field=phscal,
			solint='60s',
			refant=antref,
			gaintype='K',
			parang=False)

	plotms(vis='%s_%s.K'%(phscal,target),
		   xaxis='time',yaxis='delay',
		   iteraxis='antenna',
		   coloraxis='spw',
		   antenna='SV,ZC,BD,SH,HH,YS',
		   gridrows=2,
		   gridcols=3,
		   plotfile='%s_%s_K.png'%(phscal,target),
		   highres=True,
		   showgui=False,
		   dpi = 800,
		   width=1500,
		   height=750,
		   overwrite=True)

	# Time-dependent phase correction of phase cal, applying delay solutions

	os.system('rm -rf %s_%s.p'%(phscal,target))
	gaincal(vis='%s_%s.ms'%(phscal,target),
			caltable='%s_%s.p'%(phscal,target),
			corrdepflags=True,
			field=phscal,
			solint='20s',
			refant=antref,
			gaintype='G',
			calmode='p',
			gaintable=['%s_%s.K'%(phscal,target)],
			interp=['nearest'],
			parang=False)

	plotms(vis='%s_%s.p'%(phscal,target),
		   xaxis='time',yaxis='phase',
		   iteraxis='antenna',
		   coloraxis='spw',
		   antenna='SV,ZC,BD,SH,HH,YS',
		   gridrows=2,
		   gridcols=3,
		   plotfile='%s_%s_p.png'%(phscal,target),
		   highres=True,
		   showgui=False,
		   dpi = 800,
		   width=1500,
		   height=750,
		   overwrite=True)


### 6) Apply phase solutions and clean phase-reference
mystep = 6

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	# Apply these solutions to the phase cal and image
	applycal(vis='%s_%s.ms'%(phscal,target),
			 field=phscal,
			 gaintable=['%s_%s.K'%(phscal,target),'%s_%s.p'%(phscal,target)],
			 gainfield=[phscal,phscal],
			 interp=['nearest','linear'],
			 applymode='calflag',
			 parang=False)

	os.system('rm -r phscal2p1.*')
	if mac==False:
		tclean(vis='%s_%s.ms'%(phscal,target),
			   stokes='pseudoI',
		       psfcutoff=0.5,
			   specmode='mfs',
			   threshold=0,
			   cell='0.24mas',
			   field=phscal,
			   imagename='phscal2p1',
			   imsize=[640,640],
			   deconvolver='clark',
			   niter=1000,
			   cycleniter=50,
			   interactive=True,
			   parallel=parallel)
	else:
		run_iclean(vis='%s_%s.ms'%(phscal,target),
				   stokes='pseudoI',
				   specmode='mfs',
				   threshold=0,
				   cell='0.24mas',
				   field=phscal,
				   imagename='phscal2p1',
				   imsize=[640,640],
				   deconvolver='clark',
				   niter=1000,
				   cycleniter=50,
				   parallel=parallel)

	ft(vis='%s_%s.ms'%(phscal,target),
	   field=phscal,
	   model='phscal2p1.model',
	   usescratch=True)

	rms=imstat(imagename='phscal2p1.image',
			   box='60,60,580,240')['rms'][0]
	peak=imstat(imagename='phscal2p1.image',
			   box='300,300,340,340')['max'][0]

	print('Peak %6.3f Jy/beam, rms %6.3f mJy/beam, S/N %6.0f' % (peak, rms*1e3, peak/rms))

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

### 8) Apply amp solutions and clean phase reference again
mystep = 8

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	# Apply these solutions to the phase cal and image
	applycal(vis='%s_%s.ms'%(phscal,target),
			 field=phscal,
			 gaintable=['%s_%s.K'%(phscal,target),'%s_%s.p'%(phscal,target),'%s_%s.ap'%(phscal,target)],
			 gainfield=[phscal,phscal,phscal],
			 interp=['nearest','nearest','nearest'],
			 applymode='calflag',
			 parang=False)

	os.system('rm -r phasecal2ap.*')
	if mac == False:
		tclean(vis='%s_%s.ms'%(phscal,target),
			   stokes='pseudoI',
			   psfcutoff=0.5,
			   specmode='mfs',
			   threshold=0,
			   cell='0.24mas',
			   field=phscal,
			   imagename='phasecal2ap',
			   imsize=[640,640],
			   deconvolver='clark',
			   niter=1000,
			   cycleniter=50,
			   interactive=True,
			   parallel=parallel)
	else:
		run_iclean(vis='%s_%s.ms'%(phscal,target),
				   stokes='pseudoI',
				   cell='0.24mas',
				   field=phscal,
				   specmode='mfs',
			       threshold=0,
				   imagename='phasecal2ap',
				   imsize=[640,640],
				   deconvolver='clark',
				   niter=1000,
				   cycleniter=50,
				   parallel=parallel)

	rms=imstat(imagename='phasecal2ap.image',
			   box='60,60,580,240')['rms'][0]
	peak=imstat(imagename='phasecal2ap.image',
			   box='300,300,340,340')['max'][0]

	print('Peak %6.3f Jy/beam, rms %6.3f mJy/beam, S/N %6.0f' % (peak, rms*1e3, peak/rms))

### 9) Apply solutions to target and split
mystep = 9

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	# Apply these solutions to the phase cal and image
	applycal(vis='%s_%s.ms'%(phscal,target),
			 field='',
			 gaintable=['%s_%s.K'%(phscal,target),'%s_%s.p'%(phscal,target),'%s_%s.ap'%(phscal,target)],
			 gainfield=[phscal,phscal,phscal],
			 interp=['linear','linear','linear'],
			 applymode='calflag',
			 parang=False)

	os.system('rm -r %s.ms'%target)
	split(vis='%s_%s.ms'%(phscal,target),
		  field=target,
		  outputvis='%s.ms'%target)

### 10) Image target (set timerange due to non-phase referenced parts
mystep = 10

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	os.system('rm -r target2p0.*')
	if mac==False:
		tclean(vis='%s.ms'%(target),
			   stokes='pseudoI',
			   psfcutoff=0.5,
			   specmode='mfs',
			   threshold=0,
			   cell='0.24mas',
			   field=target,
			   imagename='target2p0',
			   timerange='12:15:00~13:17:00',
			   imsize=[640,640],
			   deconvolver='clark',
			   niter=1000,
			   interactive=True,
			   parallel=parallel)
	else:
		run_iclean(vis='%s.ms'%(target),
				   stokes='pseudoI',
				   specmode='mfs',
				   threshold=0,
				   cell='0.24mas',
				   field=target,
				   imagename='target2p0',
				   timerange='12:15:00~13:17:00',
				   imsize=[640,640],
				   deconvolver='clark',
				   niter=1000,
				   parallel=parallel)

	ft(vis='%s.ms'%(target),
	   model='target2p0.model',
	   usescratch=True)

	rms=imstat(imagename='target2p0.image',
			   box='60,60,580,240')['rms'][0]
	peak=imstat(imagename='target2p0.image',
			   box='300,300,340,340')['max'][0]
	print('Peak %6.3f Jy/beam, rms %6.3f mJy/beam, S/N %6.0f' % (peak, rms*1e3, peak/rms))

### 11) Get phase corrections
mystep = 11

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	os.system('rm -rf %s.p'%(target))
	gaincal(vis='%s.ms'%(target),
			caltable='%s.p'%(target),
			corrdepflags=True,
			solint='20s',
			refant=antref,
			gaintype='G',
			minsnr=2,
			calmode='p',
			parang=False)

	plotms(vis='%s.p'%(target),
		   xaxis='time',yaxis='phase',
		   iteraxis='antenna',
		   coloraxis='spw',
	       gridrows=2,
		   gridcols=3,
		   plotfile='%s.p.png'%(target),
		   highres=True,
		   showgui=False,
		   dpi = 800,
		   width=1500,
		   height=750,
		   overwrite=True)

### 12) Apply and image
mystep = 12

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	# Apply these solutions to the phase cal and image
	applycal(vis='%s.ms'%(target),
			 field=target,
			 gaintable=['%s.p'%(target)],
			 gainfield=[target],
			 interp=['linear'],
			 applymode='calflag',
			 parang=False)

	os.system('rm -r target2p1.*')
	if mac==False:
		tclean(vis='%s.ms'%(target),
			   stokes='pseudoI',
			   psfcutoff=0.5,
			   specmode='mfs',
			   threshold=0,
			   cell='0.24mas',
			   imagename='target2p1',
			   imsize=[640,640],
			   deconvolver='clark',
			   niter=1000,
			   interactive=True,
			   parallel=parallel)
	else:
		run_iclean(vis='%s.ms'%(target),
				   stokes='pseudoI',
				   specmode='mfs',
				   threshold=0,
				   cell='0.24mas',
				   imagename='target2p1',
				   imsize=[640,640],
				   deconvolver='clark',
				   niter=1000,
				   parallel=parallel)
		
	ft(vis='%s.ms'%(target),
	   field=target,
	   model='target2p1.model',
	   usescratch=True)

	rms=imstat(imagename='target2p1.image',
			   box='60,60,580,240')['rms'][0]
	peak=imstat(imagename='target2p1.image',
			   box='300,300,340,340')['max'][0]

	print('Peak %6.3f Jy/beam, rms %6.3f mJy/beam, S/N %6.0f' % (peak, rms*1e3, peak/rms))

### 13) Derive amplitude solutions
mystep = 13

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	os.system('rm -rf %s.ap'%(target))
	gaincal(vis='%s.ms'%(target),
			caltable='%s.ap'%(target),
			corrdepflags=True,
			field=target,
			solint='inf',
			refant=antref,
			gaintype='G',
			minblperant=4,
			minsnr=2,
			solnorm=True,
			calmode='ap',
			gaintable=['%s.p'%(target)],
			interp=['linear'],
			parang=False)

	plotms(vis='%s.ap'%(target),
		   xaxis='time',yaxis='amp',
		   iteraxis='antenna',
		   coloraxis='spw',
		   gridrows=2,
		   gridcols=3,
		   plotfile='%s.ap.png'%(target),
		   highres=True,
		   showgui=False,
		   dpi = 800,
		   width=1500,
		   height=750,
		   overwrite=True)

### 14) Apply and image
mystep = 14

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	# Apply these solutions to the phase cal and image
	applycal(vis='%s.ms'%(target),
			 field=target,
			 gaintable=['%s.p'%(target),'%s.ap'%target],
			 gainfield=[target,target],
			 interp=['linear','linear'],
			 applymode='calflag',
			 parang=False)

	os.system('rm -r target2ap.*')
	if mac==False:
		tclean(vis='%s.ms'%(target),
			   stokes='pseudoI',
			   psfcutoff=0.5,
			   specmode='mfs',
			   threshold=0,
			   cell='0.24mas',
			   imagename='target2ap',
			   imsize=[640,640],
			   deconvolver='clark',
			   niter=1200,
			   interactive=True,
			   parallel=parallel)
	else:
		run_iclean(vis='%s.ms'%(target),
				   stokes='pseudoI',
				   specmode='mfs',
				   threshold=0,
				   cell='0.24mas',
				   imagename='target2ap',
				   imsize=[640,640],
				   deconvolver='clark',
				   niter=1200,
				   parallel=parallel)

	rms=imstat(imagename='target2ap.image',
			   box='60,60,580,240')['rms'][0]
	peak=imstat(imagename='target2ap.image',
			   box='300,300,340,340')['max'][0]

	print('Peak %6.3f Jy/beam, rms %6.3f mJy/beam, S/N %6.0f' % (peak, rms*1e3, peak/rms))

### 15) Split calibrated data
mystep = 15

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])
	os.system('rm -r %s_calibrated.ms'%target)
	split(vis='%s.ms'%target,
		  outputvis='%s_calibrated.ms'%target)

### 16) Re-weigh data
mystep = 16

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])
	statwt(vis='%s_calibrated.ms'%target,
		   datacolumn='data')
	plotms(vis='%s_calibrated.ms'%target,
		   xaxis='uvwave',
		   yaxis='wt',
		   antenna='ON&*',
		   correlation='LL,RR',
		   coloraxis='antenna2',
		   plotfile='%s_statwt_uvdist.png'%(target),
		   highres=True,
		   showgui=False,
		   dpi = 800,
		   width=1500,
		   height=750,
		   overwrite=True)

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
