#!/home/chris/anaconda2/bin/python2.7
# @file    queueGenerate.py
# @author  Chris Shen
# @date    2018-08-15
# @version 1.0

from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

import os
import sys
import optparse
# import subprocess
# import random
# import time

# for debuging
# import logging

# for JSON parsing
# import json

# for parsing XML
# import xml.etree.ElementTree as ET

def optionsSet():
	optParser = optparse.OptionParser()
	optParser.add_option("-p", "--ScriptPrefix",
							type=str,
							dest="prefix",
							default="ESTN",
							help="Provide the prefix for this script for file generation."
							)

	optParser.add_option("-n", "--SchemeName",
							type=str,
							dest="name",
							default="CTR",
							help="Provide the simulation scheme name.")

	# net file
	optParser.add_option("-N", "--net-file", 
							dest="netfile",
							 default="map/net4x4.test.net.xml",  # map/single-cross.net.xml
							help="read SUMO network from FILE (mandatory)", 
							metavar="FILE")

	# SUMO configure file, specifying a net file, an additional file that defines loop detectors and a rou file for traffic routing
	optParser.add_option("-c", "--cfg-file",
							dest="cfgfile",
							default="map/net4x4.test.sumocfg", # map/single-cross.sumocfg
							help="read SUMO cfg from FILE (mandatory)",
							metavar="FILE")

	optParser.add_option("-T", 
							type="int", 
							dest="Traffic_Light_Model", 
							default=1, 
							help="Traffic light model (0: periodical, 1: CTR, 2: Actuated) [default: %default]")

	# endTime
	optParser.add_option("-e",
						type="int", 
						dest="endTime",
						default=7200, 
						metavar="NUM",
						help="end time for simulation")

	# simulation mode option
	optParser.add_option("-m",
						type="int",
						dest="mode",
						default=3,
						metavar="NUM",
						help="mode for simulation [default: %default] [0:Dijkstra, 1:CTR, 2:SAINT, 3:SAINT+CTR, 4:Actuated, 5:SAINT+Actuated, 6:Dijkstra+CTR, 7:Dijkstra+Actuated, 8:StaticTL, 9:ActuatedY, 10:new-CTR]")

	optParser.add_option("-l", 
						type="float",
						dest="maxSpeed",
						default=22.22,
						metavar="NUM",
						help="max. speed limit of vehicles (unit : m/s), 80km/h = 22.22m/s [default: %default]")

	# CTR mode
	# -1: turn-off
	# 0: compatible mode, compatible lanes pass
	# 1: maximum mode, maximum lanes pass
	# 2: combimed mode of 0 and 1
	# 3: original CTR in the 2013 paper, group CTT comparison
	optParser.add_option("--CTRMode",
						dest="CTRMode",
						type="int",
						default=2)

	# CTT mode in CTR
	# -1: turn-off
	# 1: phase-based
	# 2: direction-based
	optParser.add_option("--CTTMode",
						dest="CTTMode",
						type="int",
						default=2)

	# CTR Switch Period
	optParser.add_option("--CTRSwitchPeriod",
						dest="CTRSwitchPeriod",
						type="int",
						default=10,
						help='Switching Period When need to swtich TL, including yellow-light')

	# CTR Yellow-light duration
	optParser.add_option("--CTRYLDura",
						dest="CTRYLDura",
						type="int",
						default=2,
						help='Yellow TL duration When need to swtich TL, defaul is 2')
	# vehicle injection mode:
	# 0: no injection
	# 1: inject vehicles with routes defines in rou.xml file, a route only has one edge
	# 2: use default route in route file, reroute later for SAINT
	# 3: inject tic vehicles and traffic flow based on arrival rate
	# 4: inject only tic vehicles, other traffic flow will from .rou file
	optParser.add_option("--InjectMode",
						dest="InjectMode",
						type="int",
						default=4,
						help='Vehicle injection mode: 0, 1, 2, 3, 4')

	# arrival rate of each injection edge
	# the actual information is vehicle arrival interval
	optParser.add_option("--epsilon",
						dest="epsilon",
						type="float",
						default=0.5,
						help='Tolerant value for CTT')

	options, args = optParser.parse_args()
	return options

def headerGenerate(file):
	s1 = "#!/bin/bash"
	s2 = "#$ -cwd"
	s3 = "#$ -j y"
	s4 = "#$ -S /bin/bash"

	print(s1, file)
	print(s2, file)
	print(s3, file)
	print(s4, file)

# this is the main entry point of this script
if __name__ == "__main__":
	options = optionsSet()

	global netFile
	global cfgFile

	global prefix
	global name
	global simEndTime
	global mode
	global maxSpeed
	global CTRMode
	global CTTMode
	global CTRSwitchPeriod
	global CTRYLDura
	global TLMode
	global vehInjectMode

	netFile = options.netfile
	cfgFile = options.cfgfile

	prefix = options.prefix
	name = options.name
	simEndTime = options.endTime
	mode = options.mode
	maxSpeed = options.maxSpeed
	CTRMode = options.CTRMode
	CTTMode = options.CTTMode
	CTRSwitchPeriod = options.CTRSwitchPeriod
	CTRYLDura = options.CTRYLDura
	TLMode = options.Traffic_Light_Model
	vehInjectMode = options.InjectMode

	s1 = "#!/bin/bash"
	s2 = "#$ -cwd"
	s3 = "#$ -j y"
	s4 = "#$ -S /bin/bash"

	savePath = './output/'

	pythonPath ='python2.7'

	simFile = './run-estn.py'

	nogui = '--nogui'
 
	# seed: 0-9
	seed = 1
	# arrival rate: 1, 10, 20, 30, 40, 50
	# arrivalRate = 60
	# arrivalInterval = [1, 3, 5, 7, 9, 11, 13, 15, 20, 30]
	# arrivalInterval = [3, 9, 15, 21, 27, 33, 39, 45, 60, 90]
	arrivalInterval = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

	fileName = ''
	if TLMode == 1:
		fileName = str(prefix)+'-m-'+str(mode)+'-'+str(name)+'-'+str(CTRMode) +'-CTTMode-'+str(CTTMode)
	elif TLMode == 2:
		fileName = str(prefix)+'-m-'+str(mode)+'-'+str(name)+'-'+str(TLMode)
	elif TLMode == 0:
		fileName = str(prefix)+'-m-'+str(mode)+'-'+str(name)+'-'+str(TLMode)
	fullFileName = os.path.join(savePath, fileName)

	# print format:
	# $ python2.7 ./run-estn.py --nogui -e 300 -s 1 ...
	for a in arrivalInterval:
		for s in range(0, seed):
			# create shell script for each parameter
			if a == 0:
				a = 1

			n1 = fullFileName+'-ar-'+str(a)+'-s-'+str(s)+'.sh'

			f = open(n1, 'w')
			print(s1, file=f)
			print(s2, file=f)
			print(s3, file=f)
			print(s4, file=f)
			print(pythonPath, file=f, end=" ")
			print(simFile, file=f, end=" ")
			print(nogui, file=f, end=" ")
			print('-e '+str(simEndTime), file=f, end=" ")
			print('-s '+str(s), file=f, end=" ")
			print('--arrivalRate '+str(a), file=f, end=" ")
			# if TLMode == 1:
			print('--CTRMode '+str(CTRMode), file=f, end=" ")
			print('--CTTMode '+str(CTTMode), file=f, end=" ")
			print('--InjectMode '+str(vehInjectMode), file=f, end=" ")
			print('--CTRSwitchPeriod '+str(CTRSwitchPeriod), file=f, end=" ")
			print('--CTRYLDura '+str(CTRYLDura), file=f, end=" ")

			if vehInjectMode == 0:
				print('-n '+str(netFile), file=f, end=" ")
				print('-c '+str(cfgFile), file=f, end=" ")
			print('-T '+str(TLMode), file=f, end=" ")
			print('-m '+str(mode), file=f)
			f.close()

			# create total submission script
			n2 = fileName+'-ar-'+str(a)+'-s-'+str(s)+'.sh'
			f = open(fullFileName+'.sh', 'a+')
			print('qsub', file=f, end=" ")
			print(n2, file=f)
			f.close()
