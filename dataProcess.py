#!/home/chris/anaconda2/bin/python2.7
#
# Data collection and processing.
# Main tasks:
# 1. scan target directory to get file name
# 2. read each json file
# 3. save data to dictionary
# 4. calculate statistic, e.g. mean, variance, confidence intervals, CDF
# 5. save data to file for GNU Plot or matplot
# 
# 
# @file    dataProcess.py
# @author  Chris Shen
# @date    2018-08-15
# @version $Id$

from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

import os
import sys
import optparse
# import subprocess
# import random
# import time
import numpy as np 
import matplotlib.pyplot as plt

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
						default="/home/chris/usr/CTR_TVT/ESTN/sim/result",
						help="Directory to scan"
						)

	# simulation mode option
	optParser.add_option("-m",
						type="int",
						dest="mode",
						default=3,
						metavar="NUM",
						help="mode for simulation [default: %default] [0:Dijkstra, 1:CTR, 2:SAINT, 3:SAINT+CTR, 4:Actuated, 5:SAINT+Actuated, 6:Dijkstra+CTR, 7:Dijkstra+Actuated]"
						)

	optParser.add_option("-l", 
						type="float",
						dest="maxSpeed",
						default=22.22,
						metavar="NUM",
						help="max. speed limit of vehicles (unit : m/s), 80km/h = 22.22m/s [default: %default]"
						)

	# CTR mode
	# 0: compatible mode, compatible lanes pass
	# 1: maximum mode, maximum lanes pass
	# 2: combimed mode of 0 and 1
	# 3: original CTR in the 2013 paper, group CTT comparison
	optParser.add_option("--CTRMode",
						dest="CTRMode",
						type="int",
						default=2
						)

	options, args = optParser.parse_args()
	return options

def cdfMaking(dataList):
	num_bins = 20
	counts, bins = np.histogram(dataList, bins=num_bins, normed=True)
	cdf = np.cumsum(counts)
	print(counts, bins, cdf)
	plt.plot(bins[1:], cdf/cdf[-1])
	plt.show()	


def saveData(xAxis, yAxisDataPoint, targetDic):
	key = xAxis
	valEle = yAxisDataPoint
	if targetDic.has_key(key):
		targetDic[key].append(valEle)
	else:
		targetDic[key]=[valEle]

# def meanCompute(targetDic, retDic):


def collectData(directory):
	# scan the directory to read every data 
	for root, dirs, files in os.walk(directory):
		print(root, files)
		for filename in files:
			with open(root+filename, 'r') as f:
				data = json.load(f)
				
				mode = data["mode"]
				CTRMode = data["CTRMode"]
				if mode == 3:
					if CTRMode == 0:
						dicE2EDelayRaw = {}
						saveData(data["arrivalRate"], 
								data["meanE2EDelay"], 
								dicE2EDelayRaw)

						dicThroughputRaw = {}
						saveData(data["arrivalRate"], 
								data["throughput"], 
								dicThroughputRaw)

						for key, valList in dicE2EDelayRaw.viewitems():
							g_dicMeanE2E_M3CTR0[key] \
								= sum(valList)/len(valList)
						for key, valList in dicThroughputRaw.viewitems():
							g_dicThro_M3CTR0[key] = sum(valList)/len(valList)

					elif CTRMode == 1:
						dicE2EDelayRaw = {}
						saveData(data["arrivalRate"], 
								data["meanE2EDelay"], 
								dicE2EDelayRaw)

						dicThroughputRaw = {}
						saveData(data["arrivalRate"], 
								data["throughput"], 
								dicThroughputRaw)

						for key, valList in dicE2EDelayRaw.viewitems():
							g_dicMeanE2E_M3CTR1[key] = sum(valList)/len(valList)
						for key, valList in dicThroughputRaw.viewitems():
							g_dicThro_M3CTR1[key] = sum(valList)/len(valList)

					elif CTRMode == 2:
						dicE2EDelayRaw = {}
						saveData(data["arrivalRate"], 
								data["meanE2EDelay"], 
								dicE2EDelayRaw)

						dicThroughputRaw = {}
						saveData(data["arrivalRate"], 
								data["throughput"], 
								dicThroughputRaw)

						for key, valList in dicE2EDelayRaw.viewitems():
							g_dicMeanE2E_M3CTR2[key] = sum(valList)/len(valList)
						for key, valList in dicThroughputRaw.viewitems():
							g_dicThro_M3CTR2[key] = sum(valList)/len(valList)

					elif CTRMode == 3:
						dicE2EDelayRaw = {}
						saveData(data["arrivalRate"], 
								data["meanE2EDelay"], 
								dicE2EDelayRaw)

						dicThroughputRaw = {}
						saveData(data["arrivalRate"], 
								data["throughput"], 
								dicThroughputRaw)

						for key, valList in dicE2EDelayRaw.viewitems():
							g_dicMeanE2E_M3CTR3[key] = sum(valList)/len(valList)
						for key, valList in dicThroughputRaw.viewitems():
							g_dicThro_M3CTR3[key] = sum(valList)/len(valList)

				elif mode == 6:
					if CTRMode == 0:
						dicE2EDelayRaw = {}
						saveData(data["arrivalRate"], 
								data["meanE2EDelay"], 
								dicE2EDelayRaw)

						dicThroughputRaw = {}
						saveData(data["arrivalRate"], 
								data["throughput"], 
								dicThroughputRaw)

						for key, valList in dicE2EDelayRaw.viewitems():
							g_dicMeanE2E_M6CTR0[key] = sum(valList)/len(valList)
						for key, valList in dicThroughputRaw.viewitems():
							g_dicThro_M6CTR0[key] = sum(valList)/len(valList)

					elif CTRMode == 1:
						dicE2EDelayRaw = {}
						saveData(data["arrivalRate"], 
								data["meanE2EDelay"], 
								dicE2EDelayRaw)

						dicThroughputRaw = {}
						saveData(data["arrivalRate"], 
								data["throughput"], 
								dicThroughputRaw)

						for key, valList in dicE2EDelayRaw.viewitems():
							g_dicMeanE2E_M6CTR1[key] = sum(valList)/len(valList)
						for key, valList in dicThroughputRaw.viewitems():
							g_dicThro_M6CTR1[key] = sum(valList)/len(valList)

					elif CTRMode == 2:
						dicE2EDelayRaw = {}
						saveData(data["arrivalRate"], 
								data["meanE2EDelay"], 
								dicE2EDelayRaw)

						dicThroughputRaw = {}
						saveData(data["arrivalRate"], 
								data["throughput"], 
								dicThroughputRaw)

						for key, valList in dicE2EDelayRaw.viewitems():
							g_dicMeanE2E_M6CTR2[key] = sum(valList)/len(valList)
						for key, valList in dicThroughputRaw.viewitems():
							g_dicThro_M6CTR2[key] = sum(valList)/len(valList)

					elif CTRMode == 3:
						dicE2EDelayRaw = {}
						saveData(data["arrivalRate"], 
								data["meanE2EDelay"], 
								dicE2EDelayRaw)

						dicThroughputRaw = {}
						saveData(data["arrivalRate"], 
								data["throughput"], 
								dicThroughputRaw)

						for key, valList in dicE2EDelayRaw.viewitems():
							g_dicMeanE2E_M6CTR3[key] = sum(valList)/len(valList)
						for key, valList in dicThroughputRaw.viewitems():
							g_dicThro_M6CTR3[key] = sum(valList)/len(valList)



	print("M3CTR0")
	pprint.pprint(g_dicMeanE2E_M3CTR0)
	pprint.pprint(g_dicThro_M3CTR0)
	print("M3CTR1")
	pprint.pprint(g_dicMeanE2E_M3CTR1)
	pprint.pprint(g_dicThro_M3CTR1)
	print("M3CTR2")
	pprint.pprint(g_dicMeanE2E_M3CTR2)
	pprint.pprint(g_dicThro_M3CTR2)
	print("M3CTR3")
	pprint.pprint(g_dicMeanE2E_M3CTR3)
	pprint.pprint(g_dicThro_M3CTR3)
	print("M6CTR0")
	pprint.pprint(g_dicMeanE2E_M6CTR0)
	pprint.pprint(g_dicThro_M6CTR0)
	print("M6CTR1")
	pprint.pprint(g_dicMeanE2E_M6CTR1)
	pprint.pprint(g_dicThro_M6CTR1)	
	print("M6CTR2")
	pprint.pprint(g_dicMeanE2E_M6CTR2)
	pprint.pprint(g_dicThro_M6CTR2)	
	print("M6CTR3")
	pprint.pprint(g_dicMeanE2E_M6CTR3)
	pprint.pprint(g_dicThro_M6CTR3)

	# dataList = [item for sublist in dicMeanE2EDelayRaw.values() for item in sublist]

	# print(dataList)


# this is the main entry point of this script
if __name__ == "__main__":
	options = optionsSet()
	directory = options.directory

	global g_dicMeanE2E_M3CTR0
	g_dicMeanE2E_M3CTR0 = {}
	global g_dicMeanE2E_M3CTR1
	g_dicMeanE2E_M3CTR1 = {}
	global g_dicMeanE2E_M3CTR2
	g_dicMeanE2E_M3CTR2 = {}
	global g_dicMeanE2E_M3CTR3
	g_dicMeanE2E_M3CTR3 = {}

	global g_dicMeanE2E_M6CTR0
	g_dicMeanE2E_M6CTR0 = {}
	global g_dicMeanE2E_M6CTR1
	g_dicMeanE2E_M6CTR1 = {}
	global g_dicMeanE2E_M6CTR2
	g_dicMeanE2E_M6CTR2 = {}
	global g_dicMeanE2E_M6CTR3
	g_dicMeanE2E_M6CTR3 = {}

	global g_dicThro_M3CTR0
	g_dicThro_M3CTR0 = {}
	global g_dicThro_M3CTR1
	g_dicThro_M3CTR1 = {}
	global g_dicThro_M3CTR2
	g_dicThro_M3CTR2 = {}
	global g_dicThro_M3CTR3
	g_dicThro_M3CTR3 = {}

	global g_dicThro_M6CTR0
	g_dicThro_M6CTR0 = {}
	global g_dicThro_M6CTR1
	g_dicThro_M6CTR1 = {}
	global g_dicThro_M6CTR2
	g_dicThro_M6CTR2 = {}
	global g_dicThro_M6CTR3
	g_dicThro_M6CTR3 = {}

	if directory[len(directory)-1] != '/':
		directory = directory + '/'

	print(directory)
	collectData(directory)