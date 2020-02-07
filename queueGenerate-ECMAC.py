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
							default="ECMAC",
							help="Provide the prefix for this script for file generation."
							)

	optParser.add_option("-n", "--SchemeName",
							type=str,
							dest="name",
							default="ECMAC",
							help="Provide the simulation scheme name.")

	optParser.add_option("-a", "--Argument",
							type=str,
							dest="parameter",
							default="density", # BgPktInterval, PktInterval
							help="Vary parameter for simulation.")
	optParser.add_option("-t", "--TwoWay",
							dest="twoway",
							default=False,
							# action="store_false", # True: store_true, False: store_false
							help="Twoway scenario")
	options, args = optParser.parse_args()
	return options

def headerGenerate(file):
	s1 = "#!/bin/bash"
	s2 = "#$ -cwd"
	s3 = "#$ -j y"
	s4 = "#$ -S /bin/bash"

	print(s1, file=file)
	print(s2, file=file)
	print(s3, file=file)
	print(s4, file=file)

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

	prefix = options.prefix
	name = options.name
	parameterName = options.parameter
	twoway = options.twoway
	print("twoway", twoway);

	s1 = "#!/bin/bash"
	s2 = "#$ -cwd"
	s3 = "#$ -j y"
	s4 = "#$ -S /bin/bash"

	savePath = './output/'

	# cmd1 = "/home/chris/usr/HCMAC/veins-veins-4.6-EDCA/run -u Cmdenv -f omnetpp_express.ini";
	# cmd1 = "/home/chris/usr/HCMAC/veins_DMMAC/run -u Cmdenv -f omnetpp_express.ini";
	cmd1 = "/home/chris/usr/HCMAC/ECMAC-baseline-DMMAC-UFC/run -u Cmdenv -f omnetpp_express.ini";
 	# cmd1 = "/home/chris/usr/HCMAC/veins_HCMAC/run -u Cmdenv -f omnetpp_express_SCMAC.ini";
 	# cmd1 = "/home/chris/usr/ECMAC-Lte-master/simulte-mec-test/run -u Cmdenv -f omnetpp_TwoCell.ini";

	# seed: 0-9
	seed = 10

	fileName = ''

	fileName = str(prefix)+'-'+name
	fullFileName = os.path.join(savePath, fileName)

	if parameterName == 'density':
		config = 'Density-'

		if twoway:
			config = 'Density2w-'
		# density
		parameter = ['05', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55', '60']
	elif parameterName == 'BgPktInterval':
		config = 'BgPktInterval-'
		# backgroundTrafficInterval
		parameter = ['001', '002', '003', '004', '005', '006', '007', '008', '009', '010']
	elif parameterName == 'PktInterval':
		config = 'PktInterval-'
		# arrival rate: 1, 10, 20, 30, 40, 50
		parameter = ['004', '006', '008', '010', '012']

	# print format:
	# $ python2.7 ./run-estn.py --nogui -e 300 -s 1 ...
	for a in parameter:
		for s in range(0, seed):
			# create shell script for each parameter

			if parameterName == 'density':
				if twoway:
					n1 = fullFileName+'-d-'+str(a)+'-s-'+str(s)+'-tw'+'.sh'
				else:
					n1 = fullFileName+'-d-'+str(a)+'-s-'+str(s)+'.sh'
			elif parameterName == 'BgPktInterval':
				n1 = fullFileName+'-BGTI-'+str(a)+'-s-'+str(s)+'.sh'
			elif parameterName == 'PktInterval':
				n1 = fullFileName+'-PktInterval-'+str(a)+'-s-'+str(s)+'.sh'

			f = open(n1, 'w')

			headerGenerate(f)

			print(cmd1, file=f, end=" ")

			print('-r '+str(s), file=f, end=" ")
			print('-c '+str(config)+str(a), file=f)

			f.close()

			# create total submission script
			if parameterName == 'density':
				if twoway:
					n2 = fileName+'-d-'+str(a)+'-s-'+str(s)+'-tw'+'.sh'
					f = open(fullFileName+'-density'+'-tw'+'.sh', 'a+')
				else:
					n2 = fileName+'-d-'+str(a)+'-s-'+str(s)+'.sh'
					f = open(fullFileName+'-density'+'.sh', 'a+')
			elif parameterName == 'BgPktInterval':
				n2 = fileName+'-BGTI-'+str(a)+'-s-'+str(s)+'.sh'
				f = open(fullFileName+'-BGTI'+'.sh', 'a+')
			elif parameterName == 'PktInterval':
				n2 = fileName+'-PktInterval-'+str(a)+'-s-'+str(s)+'.sh'
				f = open(fullFileName+'-PktInterval'+'.sh', 'a+')

			print('qsub', file=f, end=" ")
			print(n2, file=f)
			f.close()
