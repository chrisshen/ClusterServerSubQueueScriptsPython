#!/home/chris/anaconda2/bin/python2.7
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
						help="mode for simulation [default: %default] [0:Dijkstra, 1:CTR, 2:SAINT, 3:SAINT+CTR, 4:Actuated, 5:SAINT+Actuated, 6:Dijkstra+CTR, 7:Dijkstra+Actuated]")

	optParser.add_option("-l", 
						type="float",
						dest="maxSpeed",
						default=22.22,
						metavar="NUM",
						help="max. speed limit of vehicles (unit : m/s), 80km/h = 22.22m/s [default: %default]")

	# CTR mode
	# 0: compatible mode, compatible lanes pass
	# 1: maximum mode, maximum lanes pass
	# 2: combimed mode of 0 and 1
	# 3: original CTR in the 2013 paper, group CTT comparison
	optParser.add_option("--CTRMode",
						dest="CTRMode",
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

	global prefix
	global name
	global simEndTime
	global mode
	global maxSpeed
	global CTRMode
	global CTRSwitchPeriod
	global CTRYLDura

	prefix = options.prefix
	name = options.name
	simEndTime = options.endTime
	mode = options.mode
	maxSpeed = options.maxSpeed
	CTRMode = options.CTRMode
	CTRSwitchPeriod = options.CTRSwitchPeriod
	CTRYLDura = options.CTRYLDura

	s1 = "#!/bin/bash"
	s2 = "#$ -cwd"
	s3 = "#$ -j y"
	s4 = "#$ -S /bin/bash"

	savePath = './output/'

	pythonPath ='python2.7'

	simFile = './run-estn.py'

	nogui = '--nogui'
 
	# seed: 0-9
	seed = 10
	# arrival rate: 1, 10, 20, 30, 40, 50
	arrivalRate = 60

	fileName = str(prefix)+'-'+str(name)+'-'+str(CTRMode)

	fullFileName = os.path.join(savePath, fileName)

	# print format:
	# $ python2.7 ./run-estn.py --nogui -e 300 -s 1 ...
	for a in range(0, arrivalRate, 10):
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
			print('--CTRMode '+str(CTRMode), file=f)
			f.close()

			# create total submission script
			n2 = fileName+'-ar-'+str(a)+'-s-'+str(s)+'.sh'
			f = open(fullFileName+'.sh', 'a+')
			print('qsub', file=f, end=" ")
			print(n2, file=f)
			f.close()
