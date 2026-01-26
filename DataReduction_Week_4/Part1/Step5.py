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