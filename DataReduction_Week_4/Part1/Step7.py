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