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


##########
### 1) Convert data to measurement set and list
mystep = 1

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	os.system('rm -rf NGC660.ms*')
	importuvfits(fitsfile='NGC660.FITS',
				 vis='NGC660.ms')

	os.system('rm -rf NGC660.ms.listobs')
	listobs(vis='NGC660.ms',
			listfile='NGC660.ms.listobs')


#############
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


#############
### 3) Plot amp v. uvdistance, establish imaging parameters
mystep = 3
if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	plotms(vis='NGC660.ms',
		   xaxis='uvwave',
		   yaxis='amp',
		   avgchannel='801',
		   avgtime='30',
		   coloraxis='antenna1',
		   plotfile='NGC660_amp-uv.png',
		   highres=True,
		   showgui=False,
		   dpi = 800,
		   width=1500,
		   height=750,
		   overwrite=True)

	# Read off the approx. maximum baseline and use that and the
	# wavelength to estimate the synthesised beam resolution and thus a
	# suitable imaging cell size (see CASA_1848+283_J1849+3024 step 3).
	# Set the cellsize variable at the start of the script.

#############
### 4) Make the first image and find position
mystep = 4
if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	# The galaxy position was only known to about an arcsec so we make a
	# 2-arcsec image

	os.system('rm -rf NGC660cont0.*')
	if mac == False:
		tclean(vis='NGC660.ms',
			   imagename='NGC660cont0',
			   field='NGC660',
			   specmode='mfs',
			   threshold=0,
			   spw=contchans,
			   deconvolver='clark',
			   imsize=[1280,1280],
			   cell=cellsize,
			   weighting='natural',
			   niter=100,
			   interactive=True,
			   cycleniter=25)
	else:
		run_iclean(vis='NGC660.ms',
				   imagename='NGC660cont0',
				   field='NGC660',
				   specmode='mfs',
				   threshold=0,
				   spw=contchans,
				   deconvolver='clark',
				   imsize=[1280,1280],
				   cell=cellsize,
				   weighting='natural',
				   niter=100,
				   cycleniter=25)


#############
### 5) Find the peak position
mystep = 5
if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	# Find position - use viewer/CARTA to estimate corners (blc, trc) round
	# source. Enter this as boxsize at the top of the script.
	# You can measure the position accurately, by fitting a 2-D
	# Gaussian component, interactively in the viewer, but it is more
	# convenient to use the task `imfit` which produces a log file, from
	# which you can read the position.

	imfit(imagename='NGC660cont0.image',
		  box=boxsize,
		  logfile='NGC660_contpeakpos.txt')

	#ra='01:43:02.319403 dec=+013.38.44.905554'


#############
### 6) Shift the uv phase to centre on the peak and make an image
mystep = 6
if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	# Enter the position as the phase centre (note the syntax)
	os.system('rm -rf NGC660shift.ms')
	phaseshift(vis='NGC660.ms',
		       outputvis='NGC660shift.ms',
		       phasecenter='J2000 01h43m02.319403s +13d38m44.905554s')

	# From now on until continuum subtraction, work on NGC660shift.ms

	# Image again. This time, a smaller imsize is used as the source is in
	# the centre of the field.

	os.system('rm -rf NGC660cont1.*')
	if mac == False:
		tclean(vis='NGC660shift.ms',
			   imagename='NGC660cont1',
			   field='NGC660',
			   specmode='mfs',
			   threshold=0,
			   spw=contchans,
			   deconvolver='clark',
			   imsize=[320,320],
			   cell=cellsize,
			   weighting='natural',
			   niter=50,
			   interactive=True,
			   cycleniter=25)
	else:
		run_iclean(vis='NGC660shift.ms',
				   imagename='NGC660cont1',
				   field='NGC660',
				   specmode='mfs',
				   threshold=0,
				   spw=contchans,
				   deconvolver='clark',
				   imsize=[320,320],
				   cell=cellsize,
				   weighting='natural',
				   niter=50,
				   cycleniter=25)

	ft(vis='NGC660shift.ms',
	   field='NGC660',
	   model='NGC660cont1.model',
	   usescratch=True)


### 7) Set boxes for imstat
mystep = 7
if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	if mac == False:
		imview()
	else:
		print('MacOS detected ... please use CARTA to look at the image - NGC660cont1.image')

	# Load the image you just made and set blc and trc of a largeish box
	# well clear of the source
	# offbox='offblcx,offblcy,offtrcx,offtrcy'
	# Set blc and trc to enclose the source
	# onbox='onblcx,onblcy,ontrcx,ontrcy'
	# (enter your own values for the 4 corners in each case and fill these
	# in at the start of the script just above the list of steps)

	rms=imstat(imagename='NGC660cont1.image',
			   box=offbox)['rms'][0]
	peak=imstat(imagename='NGC660cont1.image',
				box=onbox)['max'][0]

	print('Peak %6.3f mJy/beam, rms %6.3f mJy/beam, S/N %6.0f' % (peak*1e3, rms*1e3, peak/rms))


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


### 9) Image the continuum at high resolution
mystep = 9
if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	# contchans were identified in step 2

	# Robust=0 gives higher weight to interpolation into the missing
	# spacings, which favours the long baselines and produces a smaller
	# synthesized beam, in order to separate core and jet.

	os.system('rm -rf NGC660contap1.*')
	if mac == False:
		tclean(vis='NGC660shift.ms',
			   imagename='NGC660contap1',
			   field='NGC660',
			   spw=contchans,
			   specmode='mfs',
			   threshold=0,
			   deconvolver='clark',
			   imsize=[320,320],
			   weighting='briggs',
			   robust=0,
			   cell=cellsize,
			   niter=200,
			   interactive=True,
			   cycleniter=50)
	else:
		run_iclean(vis='NGC660shift.ms',
				   imagename='NGC660contap1',
				   field='NGC660',
				   spw=contchans,
				   specmode='mfs',
				   threshold=0,
				   deconvolver='clark',
				   imsize=[320,320],
				   weighting='briggs',
				   robust=0,
				   cell=cellsize,
				   niter=200,
				   cycleniter=50)

	rms=imstat(imagename='NGC660contap1.image',
			   box=offbox)['rms'][0]
	peak=imstat(imagename='NGC660contap1.image',
			   box=onbox)['max'][0]

	print('Peak %6.4f mJy/beam, rms %6.4f mJy/beam, S/N %6.0f' % (peak*1e3, rms*1e3, peak/rms))

	# The lower peak is due to the smaller beam size.
	# Peak 0.0760, rms 0.0003, S/N    231


### 10) Subtract the continuum and check the HI frequency
mystep = 10
if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	ft(vis='NGC660shift.ms',
	   model='NGC660contap1.model',
	   usescratch=True)

	os.system('rm -rf NGC660shift.contsub.ms*')
	uvcontsub(vis='NGC660shift.ms',
			  outputvis="NGC660shift.contsub.ms",
			  fitspec=contchans,
			  fitorder=1)

# If you can't remember the H rest frequency, use
	slsearch(freqrange=[1.408376,1.424376],
			 rrlinclude=False,
			 logfile='NGC660_HIrest.log',
			 verbose=True,
			 append=False)


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


### 12) Make PV plot
mystep = 12
if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	# Click on the PV tool and draw a line parallel to the jet. In the
	# Regions PV tab, note the coordinates in pixels and set the width to
	# 11 pixels and create the Position-Velocity image.

	# This can be scripted:
	impv(imagename='NGC660line.image',
		  outfile='NGC660.pv',
		  start=[182,142],
		  end=[133,182],
		  width=11)

	# Look at NGC660.pv using imview/CARTA


### 13) Make moments
mystep = 13
if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	# Click on the Moments tool. This will present the spectral profiler.
	# Draw an ellipse round the core and see the spectrum. Shift-click in
	# the spectral profile tool to select the channels covering the
	# line. Select the zeroth moment (total intensity). Note the start and
	# stop channels (approximately) and click on Collapse.

	# This can be scripted.  For the first moment (velocity-weighted) it
	# is necessary to exclude the noisiest pixels, and the counter-jet is
	# mostly obscured, but you can see the velocity gradient across the
	# core region.

	os.system('rm -rf NGC660line.mom0')
	immoments(imagename='NGC660line.image',
			  moments=[0],
			  chans='33~83',
			  outfile='NGC660line.mom0')

	os.system('rm -rf NGC660line.mom1')
	immoments(imagename='NGC660line.image',
			  moments=[1],
			  chans='33~83',
			  excludepix=[-0.005,1],
			  outfile='NGC660_line.mom1')

	# Look at NGC660_line.clean.mom0 and NGC660_line.clean.mom1 in the viewer


### 14) Extract and plot spectra
mystep = 14
if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	# Click on the spectral profile tool.  This is useful for getting an
	# idea of the spectrum but it is better to script the extraction and
	# plotting.

	# Use the viewer on the continuum image to identify 3 locations to
	# extract spectra. In the Regions pane, convert units to pixels and
	# use the same radius for all except the rms.

	rgns={'jet':'circle[[152pix, 169pix], 6pix]',
		  'core':'circle[[161pix, 160pix], 6pix]',
		  'cjet':'circle[[168pix, 153pix], 6pix]',
		  'rms':'box[[10pix,10pix],[100pix,50pix]]'}

	ia.open('NGC660line.image')
	for r in rgns:
		outfile=open(r+'.spec', 'w')
		f=ia.getprofile(axis = 3, function = 'flux', region = rgns[r], unit='km/s', spectype='radio velocity')
		for z in  zip(f['coords'],f['values']):
			print(z[0], z[1], file=outfile)
		outfile.close()

	ia.close()

	import matplotlib.pyplot as plt
	cols={'jet':'b','core':'g','cjet':'r','rms':'k'} # The colors for each spectrum (use help(plt.colors) for others)
	fig = plt.figure(1,figsize=(9,4.5))
	ax = fig.add_subplot(111)
	for i in range(len(rgns)):
		v=[];f=[]
		for l in open(list(rgns.keys())[i]+'.spec'):  # Read the disk files back into arrays
			v.append(float(l.split()[0])) # Array of velocities for x-axis
			f.append(float(l.split()[1])) # Array of flux density values for y-axis
		ax.plot(v,f,color=cols[list(rgns.keys())[i]],label=r'%s'%list(rgns.keys())[i])  # Plot the spectra
	ax.set_xlabel('Velocity (LSR, km/s)')
	ax.set_ylabel('Flux density per channel per 10.8-mas radius')
	ax.set_title('NGC660 HI velocity profiles')
	ax.legend() # add the legend to show what each line stands for
	fig.savefig('NGC660_HIvelocityprofiles.pdf',bbox_inches='tight') # Write the plot to a pdf
	plt.clf()


### 15) Make an optical depth map
mystep = 15
if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	os.system('rm -rf NGC660line.mean')
	immoments(imagename='NGC660line.image',
			  moments=[-1],
			  chans='55~69',    # main peak FWHM
			  excludepix=[-0.005,1],
			  outfile='NGC660line.mean')

	os.system('rm -rf NGC660.tau')
	immath(imagename=['NGC660contap1.image','NGC660line.mean'],
		   mode='evalexpr',
		   expr='-1.*log(-1.*IM1/IM0)',
		   outfile='NGC660.tau')

	# look at NGC660.tau in the viewer/CARTA