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