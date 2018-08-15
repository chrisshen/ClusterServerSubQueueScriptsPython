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

# pretty printer
import pprint

# for debuging
# import logging

# for JSON parsing
import json

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

	optParser.add_option("-d", "--Directory",
							type=str,
							dest="directory",
							default="/home/chris/usr/CTR_TVT/ESTN/sim/result/test",
							help="Directory to scan")

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

	options, args = optParser.parse_args()
	return options

def collectData(directory):
	for root, dirs, files in os.walk(directory):
		# print(root, files)
		for filename in files:
			with open(root+filename, 'r') as f:
				data = json.load(f)
				
				# E2E delay
				key_ar = data["arrivalRate"]
				valEle_e2e = data["meanE2EDelay"]
				if dicMeanE2EDelay.has_key(key_ar):
					dicMeanE2EDelay[key_ar].append(valEle_e2e)
				else:
					dicMeanE2EDelay[key_ar]=[valEle_e2e]

				# Throughput
				key_ar = data["arrivalRate"]
				valEle_thr = data["throughput"]
				if dicThroughput.has_key(key_ar):
					dicThroughput[key_ar].append(valEle_thr)
				else:
					dicThroughput[key_ar]=[valEle_thr]				
	
	pprint.pprint(dicMeanE2EDelay)
	pprint.pprint(dicThroughput)


# this is the main entry point of this script
if __name__ == "__main__":
	options = optionsSet()
	directory = options.directory

	global dicMeanE2EDelay
	dicMeanE2EDelay = {}
	global dicThroughput
	dicThroughput = {}

	if directory[len(directory)-1] != '/':
		directory = directory + '/'

	collectData(directory)