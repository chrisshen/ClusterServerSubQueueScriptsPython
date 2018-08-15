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
							default="CTR",
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

# this is the main entry point of this script
if __name__ == "__main__":
	options = optionsSet()
	directory = options.directory
	
	if directory[len(directory)-1] != '/':
		directory = directory + '/'

	for root, dirs, files in os.walk(directory):
		# print(root, files)
		for filename in files:
			with open(root+filename, 'r') as f:
				data = json.load(f)
				if data["arrivalRate"] == 50:
					print(data["arrivalRate"], data["meanE2EDelay"])
