"""
Script for initial calibration of EVN n14c3 data.

Changelog:
v1 - amsr@jb.man.ac.uk April 2016
v2 - Updated by J. Radcliffe April 2019 to CASA v5 & fringe fitting
v3 - Updated by J. Radcliffe Nov 2021 to CASA v6
v4 - Updated by J. Radcliffe Feb 2025 to CASA v6.5 
A web page/pdf (http://www.jb.man.ac.uk/DARA/unit4/Workshops/EVN_continuum_part_1.html) of instructions is also available.
"""

# Need:
# n14c3_1_1.IDI1, n14c3_1_1.IDI2
# n14c3.antab # Tsys measurements *corrected by amsr*
# gc.py, append_tsys.py (folder casavlbitools) ## helper scripts from Mark Kettenis
# flagSH.flagcmd


#  0   J1640+3946    16:40:29.632770 +39.46.46.02836 J2000  ph
#  1   3C345         16:42:58.809965 +39.48.36.99402 J2000  tar
#  2   J1849+3024    18:49:20.103406 +30.24.14.23712 J2000  tar
#  3   1848+283      18:50:27.589825 +28.25.13.15523 J2000  ph
#  4   2023+336      20:25:10.842114 +33.43.00.21435 J2000  (SH v. low el.)
# Data contain two phase-ref - target pairs
# 1848+283 has good data on all good antennas
import inspect, os, sys, json

#filename = inspect.getframeinfo(inspect.currentframe()).filename
sys.path.append(os.path.dirname(os.path.realpath('NME_all.py')))
from casavlbitools.fitsidi import append_tsys, append_gc

bpcal='1848+283'
target1='3C345'
phscal1='J1640+3946'
target2='J1849+3024'
phscal2='1848+283'
inbase='n14c3'

# ENTER IN THE CASA PROMPT THE NUMBER OF THE STEP(s) TO RUN
#
# e.g.
# CASA <2>:runsteps=[1,2]
# CASA <3>:execfile('NME_all.py')

thesteps = []
step_title = {1: 'Append Tsys and gaincurve information',
			  2: 'Convert data to measurement set',
			  3: 'Fix antenna tables',
			  4: 'A priori calibration',
			  5: 'Inspect and flag data',
			  6: 'Fringe fit: instrumental and multi-band delays',
			  7: 'Bandpass calibration',
			  8: 'Split out each phase-cal - target pair'
}
thesteps = []
try:
	print('List of steps to be executed ...', runsteps)
	thesteps = runsteps
except:
	print('global variable mysteps not set')

print(runsteps)

if (thesteps==[]):
	thesteps = list(range(0,len(step_title)))
	print('Executing all steps: ', thesteps)

# NB 'JD' is a dummy entry, no data
ants=  ['EF','WB','JB','ON','NT','TR','SV','ZC','BD','SH','HH','YS','JD']
diams= [100.0,25.0,75.0,25.0,32.0,32.0,32.0,32.0,32.0,25.0,24.0,40.0,25.0]
axoffs=[[0.013,4.95,0.,2.15,1.831,0.,-0.007,-0.008,-0.004,-0.002,6.692,2.005,0.],
		[0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.],
		[0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.]]

### 1) Prepare datasets by appending Tsys information and make gaincurves
mystep = 1

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	for i in ['n14c3_1_1.IDI1','n14c3_1_1.IDI2']:
		append_tsys(antabfile='n14c3.antab', idifiles=i)
		append_gc(antabfile='n14c3.antab', idifile=i)

### 2) Convert data to measurement set and list
mystep = 2

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	# Convert fitsidi files to Measurement Sets (MS)
	# Ignore warnings about DIAMETER and POLCALA/B and zero/negative scan Nos

	os.system('rm -rf %s.ms' % inbase)
	os.system('rm -rf %s.ms.flagversions' % inbase)
	importfitsidi(fitsidifile=['%s_1_1.IDI1' % inbase, '%s_1_1.IDI2' % inbase],
				  vis='%s.ms' % inbase,
				  constobsid=True,
				  scanreindexgap_s=15)

	os.system('rm -rf %s.ms.listobs' % inbase)
	listobs(vis='%s.ms' % inbase,
			listfile='%s.ms.listobs' % inbase)

#############

### 3) Fix antenna table
mystep = 3
if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])
	# Enter antenna diameters and axis offsets
	# NOT USUALLY NEEDED but awaiting full EVN compatibility
	# Use browsetable to examine MS

	tb.open('%s.ms/ANTENNA' % inbase, nomodify=False)
	#antdiams=tb.getcol('DISH_DIAMETER') # if you want to see existing values
	tb.putcol('DISH_DIAMETER', diams)
	tb.putcol('OFFSET',axoffs)
	tb.close()

### 4) Generate a priori calibration tables
mystep = 4
if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	# Create Tsys correction table
	os.system('rm -rf %s.tsys' % inbase)
	gencal(vis='%s.ms' % inbase,
		   caltable='%s.tsys' % inbase,
		   caltype='tsys',
		   uniform=False)

	## Create gaincurve table
	os.system('rm -rf %s.gcal' % inbase)
	gencal(vis='%s.ms' % inbase, 
		   caltable= '%s.gcal' % inbase,
		   caltype='gc')

	# Plot Tsys
	# Three antennas do not have Tsys measurements, but the .gc (gain curve) table provides 
	# a scaled gain-elevation correction which scales the visibility amplitudes 
	# but without any allowance for weather or source contribution

	plotms(vis='%s.tsys' % inbase,
		   xaxis='frequency',
		   yaxis='tsys',
		   coloraxis='corr',
		   iteraxis='antenna',
		   gridrows=2,
		   gridcols=3,
		   plotfile='%s_freq.tsys.png' % inbase,
		   highres=True,
		   showgui=False,
		   dpi = 800,
		   width=1500,
		   height=750,
		   overwrite=True)

	plotms(vis='%s.tsys' % inbase,
		   xaxis='time',
		   yaxis='tsys',
		   coloraxis='corr',
		   iteraxis='antenna',
		   gridrows=2,
		   gridcols=3,
		   plotfile='%s_time.tsys.png' % inbase,
		   highres=True,
		   showgui=False,
		   dpi = 800,
		   width=1500,
		   height=750,
		   overwrite=True)


### 5) Inspect and flag data
mystep = 5

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	# Flag autocorrelations (ignore processor warning)
	flagdata(vis='%s.ms' % inbase,
			 mode='manual',
			 autocorr=True)

	# Plot visibilities.
	plotms(vis='%s.ms' % inbase,
		   xaxis='frequency',yaxis='amp',
		   field=phscal2,
		   avgtime='3600',   # will stop at scan ends
		   antenna='EF&*',
		   correlation='RR,LL',
		   coloraxis='antenna2',
		   plotfile='%s.ms.amp-freq.png' % inbase,
		   highres=True,
		   showgui=False,
		   dpi = 800,
		   width=1500,
		   height=750,
		   overwrite=True)

	plotms(vis='%s.ms' % inbase,
		   xaxis='frequency',yaxis='amp',
		   field=phscal2,
		   avgtime='3600',   # will stop at scan ends
		   antenna='SV&*',
		   correlation='RR,LL',
		   coloraxis='corr',
		   plotfile='%s.ms.amp-freq_SV.png' % inbase,
		   highres=True,
		   showgui=False,
		   dpi = 800,
		   width=1500,
		   height=750,
		   overwrite=True)

	# see i) end channels need flagging ii) one baseline has bad data
	# mark and locate shows that this is SV.
	# mark some of the brightest data, this is EF-JB;
	# plot this to see end chans more clearly:
	plotms(vis='%s.ms' % inbase,
		   xaxis='channel',
		   yaxis='amp',
		   field=phscal2,
		   gridcols=8,
		   avgtime='3600',
		   antenna='EF&JB',
		   iteraxis='spw',
		   correlation='RR,LL',
		   plotfile='%s.edge_chans.png' % inbase,
		   highres=True,
		   showgui=False,
		   dpi = 800,
		   width=1500,
		   height=750,
		   overwrite=True)


	# A backup of previous flags is made every time flagdata is run but
	# with a non-memorable name so us flagmanager yourself any time you
	# think you might need to change your mind about flagging; use a
	# different versionname each time.
	flagmanager(vis='%s.ms' % inbase,
				mode='save',
				versionname='preSVandEndChans')

	# Flag bad pol on SV.
	# A backup of previous flags is made every time flagdata is run
	flagdata(vis='%s.ms' % inbase,
			 mode='manual',
			 correlation='RR',
			 antenna='SV')

	# Flag end channels. Odd and even No spw behave differently
	# NB python is zero-indexed.
	flagdata(vis='%s.ms' % inbase,
			 mode='manual',
			 spw='0:0~5;29~31,2:0~5;29~31,4:0~5;29~31,6:0~5;29~31,\
				  1:0~2;27~31,3:0~2;27~31,5:0~2;27~31,7:0~2;27~31')

	# Plot v. time - average central channels only
	plotms(vis='%s.ms' % inbase,
		   xaxis='time',yaxis='amp',
		   field=phscal2,
		   spw='0~7:13~20',
		   avgchannel='8',
		   antenna='EF&*',
		   coloraxis='baseline',
		   correlation='RR,LL',
		   plotfile='%s.ms.amp-time.png' % inbase,
		   highres=True,
		   showgui=False,
		   dpi = 800,
		   width=1500,
		   height=750,
		   overwrite=True)

	# First 1 or 2 integrations of each scan are bad
	flagdata(vis='%s.ms' % inbase,
			 mode='quack',
			 quackinterval=5)

	# Still some bad data. Interactively go through baselines. Since each
	# is self-scaled and these are raw data, slight or slow variation is
	# normal and the polarisations may be offset.
	# The last scan is lower but not by much, leave it in but remember
	# Note some bad data:
	# HH scans 62, 64.  Probably also intervening target? Check

	plotms(vis='%s.ms' % inbase,
		   xaxis='time',yaxis='amp',
		   scan='60~70',
		   spw='0~7:13~20',
		   avgchannel='8',
		   antenna='EF&HH',
		   coloraxis='field',
		   correlation='RR,LL',
		   plotfile='%s.ms.HHbad-scans.png' % inbase,
		   highres=True,
		   showgui=False,
		   dpi = 800,
		   width=1500,
		   height=750,
		   overwrite=True)

	# Target in brown is around zero for 2 scans; flag 62~65
	flagdata(vis='%s.ms' % inbase,
			 antenna='HH',
			 mode='manual',
			 scan='62~65')

	# Now look at SH
	plotms(vis='%s.ms' % inbase,
		   xaxis='time',yaxis='amp',
		   field=phscal2,
		   spw='0~7:13~20',
		   avgchannel='8',
		   antenna='EF&SH',
		   coloraxis='spw',
		   correlation='RR,LL',
		   plotfile='%s.ms.SHbad-data.png' % inbase,
		   highres=True,
		   showgui=False,
		   dpi = 800,
		   width=1500,
		   height=750,
		   overwrite=True)

	# Many short periods, write flag list (NB stop time is 1 s after last
	# bad integration, occasionally start has to be 1 s before first)
	# All less than one scan so no need to flag target also here (but watch out
	# for bad data on the affected antennas).
	flagdata(vis='%s.ms' % inbase,
			 mode='list',
			 inpfile='flagSH.flagcmd')

	# Check bad data are all gone
	plotms(vis='%s.ms' % inbase,
		   xaxis='time',yaxis='amp',
		   field=phscal2,
		   spw='0~7:13~20',
		   avgchannel='8',
		   antenna='EF&*',
		   coloraxis='corr',
		   correlation='RR,LL',
		   plotfile='%s.ms.flagged_raw.png' % inbase,
		   highres=True,
		   showgui=False,
		   dpi = 800,
		   width=1500,
		   height=750,
		   overwrite=True)


### 6) Fringe fitting for instrumental and time-variable delays
mystep = 6

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	## Fringe fitting
	# Plot phase against frequency - see delay errors
	plotms(vis='%s.ms' % inbase,
		   xaxis='frequency',
		   yaxis='phase',
		   ydatacolumn='data',
		   antenna="EF",
		   correlation='LL',
		   coloraxis='baseline',
		   timerange='13:53:20.0~13:54:20.0',
		   averagedata=True,
		   avgtime='120',
		   plotfile=inbase+'pre_ff.png',
		   highres=True,
		   showgui=False,
		   dpi = 800,
		   width=1500,
		   height=750,
		   overwrite=True)

	# Fringe fit to get instrumental delays (i.e. delays per spw due to receiver elec.)
	os.system('rm -rf '+inbase+'.sbd')
	fringefit(vis="%s.ms" % inbase,
			  caltable= "%s.sbd" % inbase,
			  timerange='13:53:20.0~13:54:20.0',
			  solint='inf',
			  zerorates=True,
			  refant='EF',
			  corrdepflags=True,
			  minsnr=50,
			  gaintable=['%s.gcal' % inbase, '%s.tsys' % inbase],
			  interp=['nearest','nearest,nearest'],
			  parang=True)

	# Apply to data to be able to plot effects of instrumental delay
	applycal(vis='%s.ms' % inbase,
			 gaintable=['%s.gcal' % inbase, '%s.tsys' % inbase, '%s.sbd' % inbase],
			 interp=['nearest','nearest,nearest','nearest'],
			 parang=True)

	# Plot to see instrumental delay correction (on same scan)
	plotms(vis='%s.ms' % inbase,
		   xaxis='frequency',
		   yaxis='phase',
		   ydatacolumn='corrected',
		   antenna="EF",
		   correlation='LL',
		   coloraxis='baseline',
		   timerange='13:53:20.0~13:54:20.0',
		   averagedata=True,
		   avgtime='120',
		   highres=True,
		   showgui=False,
		   dpi = 800,
		   width=1500,
		   height=750,
		   overwrite=True,
		   plotfile='%s_sbd_ff.png' % inbase)

	# Plot on other scan to show delay is time variable
	plotms(vis='%s.ms' % inbase,
		   xaxis='frequency',
		   yaxis='phase',
		   ydatacolumn='corrected',
		   antenna="EF",
		   correlation='LL',
		   coloraxis='baseline',
		   timerange='13:18:00~13:20:00',
		   averagedata=True,
		   avgtime='120',
		   highres=True,
		   showgui=False,
		   dpi = 800,
		   width=1500,
		   height=750,
		   overwrite=True,
		   plotfile='%s_sbd_ff_different_scan.png' % inbase)

	# Multi-band delay - solve delay/rates/phases versus time
	os.system('rm -rf %s.mbd' % inbase)
	fringefit(vis='%s.ms' % inbase,
			  field='%s,%s' % (phscal1,phscal2),
			  caltable='%s.mbd' % inbase,
			  combine='spw',
			  solint='60s',
			  zerorates=False,
			  corrdepflags=True,
			  refant='EF',
			  minsnr=10,
			  gaintable=['%s.gcal' % inbase, '%s.tsys' % inbase,'%s.sbd' % inbase],
			  interp=['nearest','nearest,nearest','nearest'],
			  parang=True)

	for m in ['delay','phase','rate']:
		plotms(vis='n14c3.mbd',   
		       xaxis='time',     
			   yaxis=m,
			   gridrows=2,  
			   gridcols=3,   
			   coloraxis='corr',  
	 		   iteraxis='antenna',
			   highres=True,
			   showgui=False,
			   dpi = 800,
			   width=1500,
			   height=750,
			   overwrite=True,
			   plotfile='%s_mbd_%s.png' % (inbase,m))

	## Apply all to data (remembering spwmap for multi-band delay)
	applycal(vis='%s.ms'%inbase,
			 gaintable=['%s.gcal'%inbase, '%s.tsys'%inbase, '%s.sbd'%inbase,'%s.mbd'%inbase],
			 spwmap=[[],[],[], 8*[0]],
			 interp=['nearest','nearest,nearest','nearest','linear'],
			 parang=True)

	## Plot effect of sbd and mbd corrections causing phase alignment (on sbd scan)
	plotms(vis='%s.ms' % inbase,
		   xaxis='frequency',
		   yaxis='phase',
		   ydatacolumn='corrected',
		   antenna="EF",
		   correlation='ll',
		   coloraxis='baseline',
		   timerange='13:53:20.0~13:54:20.0',
		   averagedata=True,
		   avgtime='120',
		   highres=True,
		   showgui=False,
		   dpi = 800,
		   width=1500,
		   height=750,
		   overwrite=True,
		   plotfile='%s_mbd_ff.png' % inbase)

	## And on other scan
	plotms(vis='%s.ms' % inbase,
		   xaxis='frequency',
		   yaxis='phase',
		   ydatacolumn='corrected',
		   antenna="EF",
		   correlation='ll',
		   coloraxis='baseline',
		   timerange='13:18:00~13:20:00',
		   averagedata=True,
		   avgtime='120',
		   highres=True,
		   showgui=False,
		   dpi = 800,
		   width=1500,
		   height=750,
		   overwrite=True,
		   plotfile='%s_mbd_ff_different_scan.png' % inbase)

### 7) Bandpass correction
mystep = 7

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	plotms(vis='n14c3.ms',
		   xaxis='frequency',
		   yaxis='amplitude',
		   ydatacolumn='corrected',
		   antenna='EF',
		   correlation='LL,RR',
		   coloraxis='baseline',
		   timerange='13:53:20.0~13:54:20.0',
		   avgtime='60',
		   highres=True,
		   showgui=False,
		   dpi = 800,
		   width=1500,
		   height=750,
		   overwrite=True,
		   plotfile='%s_pre_bandpass.png' % inbase)

	## Derive bandpass corrections
	os.system('rm -r %s.bpass'%inbase)
	bandpass(vis='n14c3.ms',
			 caltable='%s.bpass'%inbase,
			 field='1848+283',
			 gaintable=["%s.gcal"%inbase, "%s.tsys"%inbase, "%s.sbd"%inbase , "%s.mbd"%inbase],
			 interp=['nearest','nearest,nearest','nearest','linear'],
			 solnorm=True,
			 solint='inf',
			 refant='EF',
			 bandtype='B',
			 corrdepflags=True,
			 spwmap=[[],[],[],8*[0]],
			 parang=True)

	plotms(vis='%s.bpass'%inbase,   
	       xaxis='frequency',     
		   yaxis='phase',
		   gridrows=2,  
		   gridcols=3,   
		   coloraxis='corr',  
 		   iteraxis='antenna',
		   highres=True,
		   showgui=False,
		   dpi = 800,
		   width=1500,
		   height=750,
		   overwrite=True,
		   plotfile='%s_bpass_phase.png' % inbase)

	plotms(vis='%s.bpass'%inbase,   
	       xaxis='frequency',     
		   yaxis='amp',
		   gridrows=2,  
		   gridcols=3,   
		   coloraxis='corr',  
 		   iteraxis='antenna',
		   highres=True,
		   showgui=False,
		   dpi = 800,
		   width=1500,
		   height=750,
		   overwrite=True,
		   plotfile='%s_bpass_amp.png' % inbase)

	## Apply solutions to sources
	applycal(vis='%s.ms'%inbase,
			 gaintable=['%s.gcal'%inbase, '%s.tsys'%inbase, '%s.sbd'%inbase,
			 			'%s.mbd'%inbase, '%s.bpass'%inbase],
			 spwmap=[[],[],[], 8*[0],[],[]],
			 interp=['nearest','nearest,nearest','nearest','linear','nearest'],
			 parang=True)

	## Plot effect of bandpass correction on data in amplitude
	plotms(vis='%s.ms' % inbase, 
		   xaxis='frequency', 
		   yaxis='amp',
           ydatacolumn='corrected',
           antenna='EF',
           correlation='LL',
           coloraxis='baseline',
           field='1848+283',
           plotfile='%s_corrected_amp_freq.png' % inbase,
		   highres=True,
		   showgui=False,
		   dpi = 800,
		   width=1500,
		   height=750,
		   overwrite=True)

	## And in phase
	plotms(vis='n14c3.ms',
		   xaxis='frequency',
		   yaxis='phase',
           ydatacolumn='corrected',
           antenna='EF',
           correlation='LL',
           coloraxis='baseline',
           field='1848+283',
           plotfile='%s_corrected_phase_freq.png' % inbase,
		   highres=True,
		   showgui=False,
		   dpi = 800,
		   width=1500,
		   height=750,
		   overwrite=True)

### 8) Split semi-calibrated data into two phase-target pairs
mystep = 8

if(mystep in thesteps):
	print('Step ', mystep, step_title[mystep])

	## Split target 1, phase cal 1 (3C345, J1640+3946)
	os.system('rm -rf %s_%s.ms' % (phscal1,target1))
	os.system('rm -rf %s_%s.ms.flagversions' % (phscal1,target1))
	split(vis='%s.ms' % inbase,
		  outputvis='%s_%s.ms' % (phscal1,target1),
		  field='%s,%s' % (phscal1,target1),
		  datacolumn='corrected')

	## Split target 2, phase cal 2 (J1849+3024, 1848+283)
	os.system('rm -rf %s_%s.ms' % (phscal2,target2))
	os.system('rm -rf %s_%s.ms.flagversions' % (phscal2,target2))
	split(vis='%s.ms' % inbase,
		  outputvis='%s_%s.ms' % (phscal2,target2),
		  field='%s,%s' % (phscal2,target2),
		  datacolumn='corrected')

	# Listobs each of these
	os.system('rm -rf %s_%s.ms.listobs' % (phscal1,target1))
	listobs(vis='%s_%s.ms' % (phscal1,target1),
			listfile='%s_%s.ms.listobs' % (phscal1,target1))

	os.system('rm -rf %s_%s.ms.listobs' % (phscal2,target2))
	listobs(vis='%s_%s.ms' % (phscal2,target2),
			listfile='%s_%s.ms.listobs' % (phscal2,target2))


