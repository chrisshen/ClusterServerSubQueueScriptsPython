#!/home/chris/anaconda2/bin/python2.7
#
# Data collection and processing.
# Main tasks:
# 1. scan target directory to get file name
# 2. read each JSON file
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

	optParser.add_option("-o", "--Output",
						type=str,
						dest="outputDir",
						default="",
						help="output data to a directory"
						)

	# simulation mode option
	optParser.add_option("-m",
						type="int",
						dest="mode",
						default=3,
						metavar="NUM",
						help="mode for simulation [default: %default] [0:Dijkstra, 1:CTR, 2:SAINT, 3:SAINT+CTR, 4:Actuated, 5:SAINT+Actuated, 6:Dijkstra+CTR, 7:Dijkstra+Actuated]"
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

def cdfMaking(inDic, outCDFData):
	''' Compute CDF, return to cdfData

	args:
		inDic (dict):
	'''
	# if not isinstance(sublist, str): to remove string in the list, which is file name
	dataList = [item for sublist in inDic.values() if not isinstance(sublist, str) for item in sublist]

	# dataList
	dataList = sorted(dataList)

	actFreq = []
	for i in dataList:
		if actFreq:
			actFreq.append( 1.0/len(dataList) + actFreq[len(actFreq)-1])
		else:
			actFreq.append( 1.0/len(dataList) )

	# cdfData = []

	for i in dataList:
		outCDFData.append([i, actFreq[dataList.index(i)]])

	# if inDic.has_key('filename'):
	# 	outCDFData.append(['filename', inDic['filename']])

	# return cdfData

def readData(xAxis, yAxisDataPoint, targetDic):
	''' Save data from each file, save it to the targetDic

	args:
		xAxis (str, int): x axis point
		yAxisDataPoint (float): raw data point
	return:
		targetDic (dict): 
	'''
	key = xAxis
	valEle = yAxisDataPoint
	if targetDic.has_key(key):
		targetDic[key].append(valEle)
	else:
		targetDic[key]=[valEle]



def meanCompute(inputDic, retDic):
	''' Compute mean, return to retDic with list value

	args:
		inputDic (dict): raw data
		retDic (dict): return mean
	return:

	'''	
	for key, valList in inputDic.viewitems():
		if not isinstance(key, str):
			retDic[key] = [sum(valList)/len(valList)]

def variCompute(inDic, inDicMean, retDic):
	''' Compute variance, return to retDic

	args:
		inDic (dict): raw data
		inDicMean (dict): mean data
		retDic (dict): return variance
	'''
	# print(inDic)
	# print(inDicMean)
	for key, valList in inDic.viewitems():
		if not isinstance(key, str):
			sum_var = 0.0
			for value in valList:
				sum_var = sum_var + pow(value-inDicMean.get(key)[0], 2)

			# print(valList)
			vari = sum_var / (len(valList)-1)

			retDic[key] = vari

def confCompute(inDic, inVari, retDic):
	''' Compute confidence interval, return to retDic

	args:
		inDic (dict): raw input data
		inVari (dict): input variance data
		retDic (dict): return confience interval data
	'''	
	for key, val in inVari.viewitems():
		# student t dis., T(10-1, 90%) = 1.833, T(6-1, 90%) = 2.015
		stuT_9 = 1.833
		stuT_5 = 2.015

		retDic[key] = stuT_9 * pow(inVari[key]/len(inDic[key]), 1/2)

def mergeMeanAndConfi(inDicMean, inDicConf):
	''' Compute confidence interval, return to retDic

	args:
		inDic (dict): raw input data
		inVari (dict): input variance data
		retDic (dict): return confience interval data
	'''	
	for key, val in inDicMean.viewitems():
		if not isinstance(key, str):
			inDicMean[key].append(inDicConf[key])


def outData(inputDicDataRaw, outputDicMeanData, outputCDF):
	''' output data, mean and CDF data

	args:
		inputDicDataRaw (dict): input raw data
		outputDicMeanData (dict): output mean and confidence interval data
		outputCDF (list): output CDF data
	'''	
	dicVari = {}
	variCompute(inDic=inputDicDataRaw,
				inDicMean=outputDicMeanData,
				retDic=dicVari)
	dicConf = {}
	confCompute(inDic=inputDicDataRaw,
				inVari=dicVari,
				retDic=dicConf)

	mergeMeanAndConfi(inDicMean=outputDicMeanData,
						inDicConf=dicConf)

	cdfMaking(inDic=inputDicDataRaw,
				outCDFData=outputCDF)

def processData():
	''' Process collected data, generate confidence interval and CDF

	args:
		inDic (dict): raw input data
		inVari (dict): input variance data
		retDic (dict): return confience interval data
	'''	

	# M3CTR0
	# E2E TT
	outData(inputDicDataRaw=g_dicE2EDelayRaw_M3CTR0,
			outputDicMeanData=g_dicMeanE2E_M3CTR0,
			outputCDF=g_cdfE2EDelayRaw_M3CTR0)
	# Throughput
	outData(inputDicDataRaw=g_dicThroRaw_M3CTR0,
			outputDicMeanData=g_dicThro_M3CTR0,
			outputCDF=g_cdfThroRaw_M3CTR0)

	# M3CTR1
	# E2E TT
	outData(inputDicDataRaw=g_dicE2EDelayRaw_M3CTR1,
			outputDicMeanData=g_dicMeanE2E_M3CTR1,
			outputCDF=g_cdfE2EDelayRaw_M3CTR1)
	# Throughput
	outData(inputDicDataRaw=g_dicThroRaw_M3CTR1,
			outputDicMeanData=g_dicThro_M3CTR1,
			outputCDF=g_cdfThroRaw_M3CTR1)

	# M3CTR2
	# E2E TT
	outData(inputDicDataRaw=g_dicE2EDelayRaw_M3CTR2,
			outputDicMeanData=g_dicMeanE2E_M3CTR2,
			outputCDF=g_cdfE2EDelayRaw_M3CTR2)
	# Throughput
	outData(inputDicDataRaw=g_dicThroRaw_M3CTR2,
			outputDicMeanData=g_dicThro_M3CTR2,
			outputCDF=g_cdfThroRaw_M3CTR2)

	# M3CTR3
	# E2E TT
	outData(inputDicDataRaw=g_dicE2EDelayRaw_M3CTR3,
			outputDicMeanData=g_dicMeanE2E_M3CTR3,
			outputCDF=g_cdfE2EDelayRaw_M3CTR3)
	# Throughput
	outData(inputDicDataRaw=g_dicThroRaw_M3CTR3,
			outputDicMeanData=g_dicThro_M3CTR3,
			outputCDF=g_cdfThroRaw_M3CTR3)

	# M6CTR0
	# E2E TT
	outData(inputDicDataRaw=g_dicE2EDelayRaw_M6CTR0,
			outputDicMeanData=g_dicMeanE2E_M6CTR0,
			outputCDF=g_cdfE2EDelayRaw_M6CTR0)
	# Throughput
	outData(inputDicDataRaw=g_dicThroRaw_M6CTR0,
			outputDicMeanData=g_dicThro_M6CTR0,
			outputCDF=g_cdfThroRaw_M6CTR0)

	# M6CTR1
	# E2E TT
	outData(inputDicDataRaw=g_dicE2EDelayRaw_M6CTR1,
			outputDicMeanData=g_dicMeanE2E_M6CTR1,
			outputCDF=g_cdfE2EDelayRaw_M6CTR1)
	# Throughput
	outData(inputDicDataRaw=g_dicThroRaw_M6CTR1,
			outputDicMeanData=g_dicThro_M6CTR1,
			outputCDF=g_cdfThroRaw_M6CTR1)

	# M6CTR2
	# E2E TT
	outData(inputDicDataRaw=g_dicE2EDelayRaw_M6CTR2,
			outputDicMeanData=g_dicMeanE2E_M6CTR2,
			outputCDF=g_cdfE2EDelayRaw_M6CTR2)
	# Throughput
	outData(inputDicDataRaw=g_dicThroRaw_M6CTR2,
			outputDicMeanData=g_dicThro_M6CTR2,
			outputCDF=g_cdfThroRaw_M6CTR2)
	
	# M6CTR3
	# E2E TT
	outData(inputDicDataRaw=g_dicE2EDelayRaw_M6CTR3,
			outputDicMeanData=g_dicMeanE2E_M6CTR3,
			outputCDF=g_cdfE2EDelayRaw_M6CTR3)
	# Throughput
	outData(inputDicDataRaw=g_dicThroRaw_M6CTR3,
			outputDicMeanData=g_dicThro_M6CTR3,
			outputCDF=g_cdfThroRaw_M6CTR3)

	# Actuated
	# E2E TT
	outData(inputDicDataRaw=g_dicE2EDelayRaw_M5ACT,
			outputDicMeanData=g_dicMeanE2E_M5ACT,
			outputCDF=g_cdfE2EDelayRaw_M5ACT)
	# Throughput
	outData(inputDicDataRaw=g_dicThroRaw_M5ACT,
			outputDicMeanData=g_dicThro_M5ACT,
			outputCDF=g_cdfThroRaw_M5ACT)

	# E2E TT
	outData(inputDicDataRaw=g_dicE2EDelayRaw_M7ACT,
			outputDicMeanData=g_dicMeanE2E_M7ACT,
			outputCDF=g_cdfE2EDelayRaw_M7ACT)
	# Throughput
	outData(inputDicDataRaw=g_dicThroRaw_M7ACT,
			outputDicMeanData=g_dicThro_M7ACT,
			outputCDF=g_cdfThroRaw_M7ACT)

	# static TL
	# E2E TT
	outData(inputDicDataRaw=g_dicE2EDelayRaw_M0,
			outputDicMeanData=g_dicMeanE2E_M0,
			outputCDF=g_cdfE2EDelayRaw_M0)
	# Throughput
	outData(inputDicDataRaw=g_dicThroRaw_M0,
			outputDicMeanData=g_dicThro_M0,
			outputCDF=g_cdfThroRaw_M0)

	# E2E TT
	outData(inputDicDataRaw=g_dicE2EDelayRaw_M2,
			outputDicMeanData=g_dicMeanE2E_M2,
			outputCDF=g_cdfE2EDelayRaw_M2)
	# Throughput
	outData(inputDicDataRaw=g_dicThroRaw_M2,
			outputDicMeanData=g_dicThro_M2,
			outputCDF=g_cdfThroRaw_M2)


	# # Print for debug
	# print("M3CTR0")
	# pprint.pprint(g_dicE2EDelayRaw_M3CTR0)
	# pprint.pprint(g_dicMeanE2E_M3CTR0)
	# pprint.pprint(g_dicThroRaw_M3CTR0)
	# pprint.pprint(g_dicThro_M3CTR0)

	# print("CDF")
	# pprint.pprint(g_cdfE2EDelayRaw_M3CTR0)
	# pprint.pprint(g_cdfThroRaw_M3CTR0)

	# print("M3CTR1")
	# pprint.pprint(g_dicMeanE2E_M3CTR1)
	# pprint.pprint(g_dicThro_M3CTR1)

	# print("M3CTR2")
	# pprint.pprint(g_dicMeanE2E_M3CTR2)
	# pprint.pprint(g_dicThro_M3CTR2)

	# print("M3CTR3")
	# pprint.pprint(g_dicMeanE2E_M3CTR3)
	# pprint.pprint(g_dicThro_M3CTR3)

	# print("M6CTR0")
	# pprint.pprint(g_dicMeanE2E_M6CTR0)
	# pprint.pprint(g_dicThro_M6CTR0)

	# print("M6CTR1")
	# pprint.pprint(g_dicMeanE2E_M6CTR1)
	# pprint.pprint(g_dicThro_M6CTR1)

	# print("M6CTR2")
	# pprint.pprint(g_dicMeanE2E_M6CTR2)
	# pprint.pprint(g_dicThro_M6CTR2)

	# print("M6CTR3")
	# pprint.pprint(g_dicMeanE2E_M6CTR3)
	# pprint.pprint(g_dicThro_M6CTR3)

	# print("M5ACT")
	# pprint.pprint(g_dicMeanE2E_M5ACT)
	# pprint.pprint(g_dicThro_M5ACT)

	# print("CDF")
	# pprint.pprint(g_cdfE2EDelayRaw_M5ACT)
	# pprint.pprint(g_cdfThroRaw_M5ACT)

	# print("M7ACT")
	# pprint.pprint(g_dicMeanE2E_M7ACT)
	# pprint.pprint(g_dicThro_M7ACT)

	# print("CDF")
	# pprint.pprint(g_cdfE2EDelayRaw_M7ACT)
	# pprint.pprint(g_cdfThroRaw_M7ACT)

	# print("M0")
	# pprint.pprint(g_dicMeanE2E_M0)
	# pprint.pprint(g_dicThro_M0)

	# print("CDF")
	# pprint.pprint(g_cdfE2EDelayRaw_M0)
	# pprint.pprint(g_cdfThroRaw_M0)

	# print("M2")
	# pprint.pprint(g_dicMeanE2E_M2)
	# pprint.pprint(g_dicThro_M2)

	# print("CDF")
	# pprint.pprint(g_cdfE2EDelayRaw_M2)
	# pprint.pprint(g_cdfThroRaw_M2)

def writeFilename(peType, mode, CTRMode, TLMode, targetDic):
	key = 'filename'
	value = '-'+str(peType)+'-m-'+str(mode)+'-CTR-'+str(CTRMode)+'-TLMode-'+str(TLMode)
	if key not in targetDic:
		targetDic[key] = value

def saveDataToFile(filename, inputDicData):

	inputDataKeySorted = sorted(inputDicData.keys())
	with open(filename, 'w') as f:
		for key in inputDataKeySorted:
			value = inputDicData[key]
			ind = len(value)
			if ind == 2:
				# key: x point, value[0]: y point, value[1]: error bar
				f.write(str(key)+' '+str(value[0])+' '+str(value[1])+'\n')
			elif ind == 1:
				# key: x point, value[0]: y point
				f.write(str(key)+' '+str(value[0])+'\n')

def saveCDFDataToFile(filename, inputCDFData):
	with open(filename, 'w') as f:
		for cdf in inputCDFData:
			# cdf[0]: x point; cdf[1]: y point
			f.write(str(cdf[0])+' '+str(cdf[1])+'\n')

def saveData(prefix1, savePath):
	prefix0 = 'plotData-'
	# prefix1 = scheme name
	if savePath[len(savePath)-1] != '/':
		savePath = savePath + '/'
	
	filename = ''
	
	# for key, value in g_dicAllData.viewitems():
	# 	if 'cdf' not in key and 'Raw' not in key:
	# 		if value.has_key('filename'):
	# 			filename = prefix0+prefix1+value['filename']
	# 		else:
	# 			sys.exit('no filename key')
	# 		filename = savePath+filename
	# 		saveDataToFile(filename, value)
	# 	else:
	# 		if value.has_key('filename'):
	# 			filename = prefix0+prefix1+value['filename']
	# 		else:
	# 			sys.exit('no filename key')	
	# 		filename = savePath+filename
	# 		saveCDFDataToFile(filename, value)

	# CTR, M = 3 and 6
	# E2E
	if g_dicMeanE2E_M3CTR0:
		if g_dicMeanE2E_M3CTR0.has_key('filename'):
			filename = prefix0+prefix1+g_dicMeanE2E_M3CTR0['filename']
		filename = savePath+filename
		saveDataToFile(filename, g_dicMeanE2E_M3CTR0)

	if g_dicMeanE2E_M3CTR1:
		if g_dicMeanE2E_M3CTR1.has_key('filename'):
			filename = prefix0+prefix1+g_dicMeanE2E_M3CTR1['filename']
		filename = savePath+filename
		saveDataToFile(filename, g_dicMeanE2E_M3CTR1)

	if g_dicMeanE2E_M3CTR2:
		if g_dicMeanE2E_M3CTR2.has_key('filename'):
			filename = prefix0+prefix1+g_dicMeanE2E_M3CTR2['filename']
		filename = savePath+filename
		saveDataToFile(filename, g_dicMeanE2E_M3CTR2)

	if g_dicMeanE2E_M3CTR3:
		if g_dicMeanE2E_M3CTR3.has_key('filename'):
			filename = prefix0+prefix1+g_dicMeanE2E_M3CTR3['filename']
		filename = savePath+filename
		saveDataToFile(filename, g_dicMeanE2E_M3CTR3)

	if g_dicMeanE2E_M6CTR0:
		if g_dicMeanE2E_M6CTR0.has_key('filename'):
			filename = prefix0+prefix1+g_dicMeanE2E_M6CTR0['filename']
		filename = savePath+filename
		saveDataToFile(filename, g_dicMeanE2E_M6CTR0)

	if g_dicMeanE2E_M6CTR1:
		if g_dicMeanE2E_M6CTR1.has_key('filename'):
			filename = prefix0+prefix1+g_dicMeanE2E_M6CTR1['filename']
		filename = savePath+filename
		saveDataToFile(filename, g_dicMeanE2E_M6CTR1)

	if g_dicMeanE2E_M6CTR2:
		if g_dicMeanE2E_M6CTR2.has_key('filename'):
			filename = prefix0+prefix1+g_dicMeanE2E_M6CTR2['filename']
		filename = savePath+filename
		saveDataToFile(filename, g_dicMeanE2E_M6CTR2)

	if g_dicMeanE2E_M6CTR3:
		if g_dicMeanE2E_M6CTR3.has_key('filename'):
			filename = prefix0+prefix1+g_dicMeanE2E_M6CTR3['filename']
		filename = savePath+filename
		saveDataToFile(filename, g_dicMeanE2E_M6CTR3)

	# Througput
	if g_dicThro_M3CTR0:
		if g_dicThro_M3CTR0.has_key('filename'):
			filename = prefix0+prefix1+g_dicThro_M3CTR0['filename']
		filename = savePath+filename
		saveDataToFile(filename, g_dicThro_M3CTR0)

	if g_dicThro_M3CTR1:
		if g_dicThro_M3CTR1.has_key('filename'):
			filename = prefix0+prefix1+g_dicThro_M3CTR1['filename']
		filename = savePath+filename
		saveDataToFile(filename, g_dicThro_M3CTR1)

	if g_dicThro_M3CTR2:
		if g_dicThro_M3CTR2.has_key('filename'):
			filename = prefix0+prefix1+g_dicThro_M3CTR2['filename']
		filename = savePath+filename
		saveDataToFile(filename, g_dicThro_M3CTR2)

	if g_dicThro_M3CTR3:
		if g_dicThro_M3CTR3.has_key('filename'):
			filename = prefix0+prefix1+g_dicThro_M3CTR3['filename']
		filename = savePath+filename
		saveDataToFile(filename, g_dicThro_M3CTR3)

	if g_dicThro_M6CTR0:
		if g_dicThro_M6CTR0.has_key('filename'):
			filename = prefix0+prefix1+g_dicThro_M6CTR0['filename']
		filename = savePath+filename
		saveDataToFile(filename, g_dicThro_M6CTR0)

	if g_dicThro_M6CTR1:
		if g_dicThro_M6CTR1.has_key('filename'):
			filename = prefix0+prefix1+g_dicThro_M6CTR1['filename']
		filename = savePath+filename
		saveDataToFile(filename, g_dicThro_M6CTR1)

	if g_dicThro_M6CTR2:
		if g_dicThro_M6CTR2.has_key('filename'):
			filename = prefix0+prefix1+g_dicThro_M6CTR2['filename']
		filename = savePath+filename
		saveDataToFile(filename, g_dicThro_M6CTR2)

	if g_dicThro_M6CTR3:
		if g_dicThro_M6CTR3.has_key('filename'):
			filename = prefix0+prefix1+g_dicThro_M6CTR3['filename']
		filename = savePath+filename
		saveDataToFile(filename, g_dicThro_M6CTR3)

	#cdf E2E 
	if g_cdfE2EDelayRaw_M3CTR0:
		if g_dicE2EDelayRaw_M3CTR0.has_key('filename'):
			filename = prefix0+prefix1+g_dicE2EDelayRaw_M3CTR0['filename']
		filename = savePath+filename
		saveCDFDataToFile(filename, g_cdfE2EDelayRaw_M3CTR0)

	if g_cdfE2EDelayRaw_M3CTR1:
		if g_dicE2EDelayRaw_M3CTR1.has_key('filename'):
			filename = prefix0+prefix1+g_dicE2EDelayRaw_M3CTR1['filename']
		filename = savePath+filename
		saveCDFDataToFile(filename, g_cdfE2EDelayRaw_M3CTR1)

	if g_cdfE2EDelayRaw_M3CTR2:
		if g_dicE2EDelayRaw_M3CTR2.has_key('filename'):
			filename = prefix0+prefix1+g_dicE2EDelayRaw_M3CTR2['filename']
		filename = savePath+filename
		saveCDFDataToFile(filename, g_cdfE2EDelayRaw_M3CTR2)

	if g_cdfE2EDelayRaw_M3CTR3:
		if g_dicE2EDelayRaw_M3CTR3.has_key('filename'):
			filename = prefix0+prefix1+g_dicE2EDelayRaw_M3CTR3['filename']
		filename = savePath+filename
		saveCDFDataToFile(filename, g_cdfE2EDelayRaw_M3CTR3)

	if g_cdfE2EDelayRaw_M6CTR0:
		if g_dicE2EDelayRaw_M6CTR0.has_key('filename'):
			filename = prefix0+prefix1+g_dicE2EDelayRaw_M6CTR0['filename']
		filename = savePath+filename
		saveCDFDataToFile(filename, g_cdfE2EDelayRaw_M6CTR0)

	if g_cdfE2EDelayRaw_M6CTR1:
		if g_dicE2EDelayRaw_M6CTR1.has_key('filename'):
			filename = prefix0+prefix1+g_dicE2EDelayRaw_M6CTR1['filename']
		filename = savePath+filename
		saveCDFDataToFile(filename, g_cdfE2EDelayRaw_M6CTR1)
	
	if g_cdfE2EDelayRaw_M6CTR2:
		if g_dicE2EDelayRaw_M6CTR2.has_key('filename'):
			filename = prefix0+prefix1+g_dicE2EDelayRaw_M6CTR2['filename']
		filename = savePath+filename
		saveCDFDataToFile(filename, g_cdfE2EDelayRaw_M6CTR2)
	
	if g_cdfE2EDelayRaw_M6CTR3:
		if g_dicE2EDelayRaw_M6CTR3.has_key('filename'):
			filename = prefix0+prefix1+g_dicE2EDelayRaw_M6CTR3['filename']
		filename = savePath+filename
		saveCDFDataToFile(filename, g_cdfE2EDelayRaw_M6CTR3)


	# CDF Throughput
	if g_cdfThroRaw_M3CTR0:
		if g_dicThroRaw_M3CTR0.has_key('filename'):
			filename = prefix0+prefix1+g_dicThroRaw_M3CTR0['filename']
		filename = savePath+filename
		saveCDFDataToFile(filename, g_cdfThroRaw_M3CTR0)

	if g_cdfThroRaw_M3CTR1:
		if g_dicThroRaw_M3CTR1.has_key('filename'):
			filename = prefix0+prefix1+g_dicThroRaw_M3CTR1['filename']
		filename = savePath+filename
		saveCDFDataToFile(filename, g_cdfThroRaw_M3CTR1)

	if g_cdfThroRaw_M3CTR2:
		if g_dicThroRaw_M3CTR2.has_key('filename'):
			filename = prefix0+prefix1+g_dicThroRaw_M3CTR2['filename']
		filename = savePath+filename
		saveCDFDataToFile(filename, g_cdfThroRaw_M3CTR2)

	if g_cdfThroRaw_M3CTR3:
		if g_dicThroRaw_M3CTR3.has_key('filename'):
			filename = prefix0+prefix1+g_dicThroRaw_M3CTR3['filename']
		filename = savePath+filename
		saveCDFDataToFile(filename, g_cdfThroRaw_M3CTR3)

	if g_cdfThroRaw_M6CTR0:
		if g_dicThroRaw_M6CTR0.has_key('filename'):
			filename = prefix0+prefix1+g_dicThroRaw_M6CTR0['filename']
		filename = savePath+filename
		saveCDFDataToFile(filename, g_cdfThroRaw_M6CTR0)

	if g_cdfThroRaw_M6CTR1:
		if g_dicThroRaw_M6CTR1.has_key('filename'):
			filename = prefix0+prefix1+g_dicThroRaw_M6CTR1['filename']
		filename = savePath+filename
		saveCDFDataToFile(filename, g_cdfThroRaw_M6CTR1)
	
	if g_cdfThroRaw_M6CTR2:
		if g_dicThroRaw_M6CTR2.has_key('filename'):
			filename = prefix0+prefix1+g_dicThroRaw_M6CTR2['filename']
		filename = savePath+filename
		saveCDFDataToFile(filename, g_cdfThroRaw_M6CTR2)
	
	if g_cdfThroRaw_M6CTR3:
		if g_dicThroRaw_M6CTR3.has_key('filename'):
			filename = prefix0+prefix1+g_dicThroRaw_M6CTR3['filename']
		filename = savePath+filename
		saveCDFDataToFile(filename, g_cdfThroRaw_M6CTR3)

	# Actuated, M = 5 and 7
	if g_dicMeanE2E_M5ACT:
		if g_dicMeanE2E_M5ACT.has_key('filename'):
			filename = prefix0+prefix1+g_dicMeanE2E_M5ACT['filename']
		filename = savePath+filename
		saveDataToFile(filename, g_dicMeanE2E_M5ACT)

	if g_dicMeanE2E_M7ACT:
		if g_dicMeanE2E_M7ACT.has_key('filename'):
			filename = prefix0+prefix1+g_dicMeanE2E_M7ACT['filename']
		filename = savePath+filename	
		saveDataToFile(filename, g_dicMeanE2E_M7ACT)

	if g_dicThro_M5ACT:
		if g_dicThro_M5ACT.has_key('filename'):
			filename = prefix0+prefix1+g_dicThro_M5ACT['filename']
		filename = savePath+filename	
		saveDataToFile(filename, g_dicThro_M5ACT)

	if g_dicThro_M7ACT:
		if g_dicThro_M7ACT.has_key('filename'):
			filename = prefix0+prefix1+g_dicThro_M7ACT['filename']
		filename = savePath+filename
		saveDataToFile(filename, g_dicThro_M7ACT)

	# CDF
	if g_cdfE2EDelayRaw_M5ACT:
		if g_dicE2EDelayRaw_M5ACT.has_key('filename'):
			filename = prefix0+prefix1+g_dicE2EDelayRaw_M5ACT['filename']
		filename = savePath+filename
		saveCDFDataToFile(filename, g_cdfE2EDelayRaw_M5ACT)

	if g_cdfE2EDelayRaw_M7ACT:
		if g_dicE2EDelayRaw_M7ACT.has_key('filename'):
			filename = prefix0+prefix1+g_dicE2EDelayRaw_M7ACT['filename']
		filename = savePath+filename
		saveCDFDataToFile(filename, g_cdfE2EDelayRaw_M7ACT)

	if g_cdfThroRaw_M5ACT:
		if g_dicThroRaw_M5ACT.has_key('filename'):
			filename = prefix0+prefix1+g_dicThroRaw_M5ACT['filename']
		filename = savePath+filename
		saveCDFDataToFile(filename, g_cdfThroRaw_M5ACT)
	
	if g_cdfThroRaw_M7ACT:
		if g_dicThroRaw_M7ACT.has_key('filename'):
			filename = prefix0+prefix1+g_dicThroRaw_M7ACT['filename']
		filename = savePath+filename
		saveCDFDataToFile(filename, g_cdfThroRaw_M7ACT)

	# static TL, M = 0 and 2
	if g_dicMeanE2E_M0:
		if g_dicMeanE2E_M0.has_key('filename'):
			filename = prefix0+prefix1+g_dicMeanE2E_M0['filename']
		filename = savePath+filename
		saveDataToFile(filename, g_dicMeanE2E_M0)

	if g_dicMeanE2E_M2:
		if g_dicMeanE2E_M2.has_key('filename'):
			filename = prefix0+prefix1+g_dicMeanE2E_M2['filename']
		filename = savePath+filename	
		saveDataToFile(filename, g_dicMeanE2E_M2)

	if g_dicThro_M0:
		if g_dicThro_M0.has_key('filename'):
			filename = prefix0+prefix1+g_dicThro_M0['filename']
		filename = savePath+filename	
		saveDataToFile(filename, g_dicThro_M0)

	if g_dicThro_M2:
		if g_dicThro_M2.has_key('filename'):
			filename = prefix0+prefix1+g_dicThro_M2['filename']
		filename = savePath+filename
		saveDataToFile(filename, g_dicThro_M2)

	# CDF
	if g_cdfE2EDelayRaw_M0:
		if g_dicE2EDelayRaw_M0.has_key('filename'):
			filename = prefix0+prefix1+g_dicE2EDelayRaw_M0['filename']
		filename = savePath+filename
		saveCDFDataToFile(filename, g_cdfE2EDelayRaw_M0)

	if g_cdfE2EDelayRaw_M2:
		if g_dicE2EDelayRaw_M2.has_key('filename'):
			filename = prefix0+prefix1+g_dicE2EDelayRaw_M2['filename']
		filename = savePath+filename
		saveCDFDataToFile(filename, g_cdfE2EDelayRaw_M2)

	if g_cdfThroRaw_M0:
		if g_dicThroRaw_M0.has_key('filename'):
			filename = prefix0+prefix1+g_dicThroRaw_M0['filename']
		filename = savePath+filename
		saveCDFDataToFile(filename, g_cdfThroRaw_M0)
	
	if g_cdfThroRaw_M2:
		if g_dicThroRaw_M2.has_key('filename'):
			filename = prefix0+prefix1+g_dicThroRaw_M2['filename']
		filename = savePath+filename
		saveCDFDataToFile(filename, g_cdfThroRaw_M2)

def collectData(directory):
	# scan the directory to read every data point
	for root, dirs, files in os.walk(directory):
		# print(root, files)
		for filename in files:
			with open(root+filename, 'r') as f:
				print('.', end="")
				data = json.load(f)
				
				mode = data["mode"]
				CTRMode = data["CTRMode"]
				TLMode = -1
				if data.has_key('TLMode'):
					TLMode = data["TLMode"]

				if mode == 0:
					# dicE2EDelayRaw = {}
					readData(xAxis=data["arrivalRate"], 
							yAxisDataPoint=data["meanE2EDelay"], 
							targetDic=g_dicE2EDelayRaw_M0)

					writeFilename(peType='cdfE2E', mode=mode, 
									CTRMode=CTRMode, 
									TLMode=TLMode, 
									targetDic=g_dicE2EDelayRaw_M0)

					# dicThroughputRaw = {}
					readData(xAxis=data["arrivalRate"], 
							yAxisDataPoint=data["throughput"], 
							targetDic=g_dicThroRaw_M0)

					writeFilename(peType='cdfThro', mode=mode, 
									CTRMode=CTRMode, 
									TLMode=TLMode, 
									targetDic=g_dicThroRaw_M0)

					meanCompute(inputDic=g_dicE2EDelayRaw_M0, 
								retDic=g_dicMeanE2E_M0)

					writeFilename(peType='meanE2E', mode=mode, 
									CTRMode=CTRMode, 
									TLMode=TLMode, 
									targetDic=g_dicMeanE2E_M0)						
					meanCompute(inputDic=g_dicThroRaw_M0, 
								retDic=g_dicThro_M0)

					writeFilename(peType='meanThro', mode=mode, 
									CTRMode=CTRMode, 
									TLMode=TLMode, 
									targetDic=g_dicThro_M0)
				elif mode == 2:
					# dicE2EDelayRaw = {}
					readData(xAxis=data["arrivalRate"], 
							yAxisDataPoint=data["meanE2EDelay"], 
							targetDic=g_dicE2EDelayRaw_M2)

					writeFilename(peType='cdfE2E', mode=mode, 
									CTRMode=CTRMode, 
									TLMode=TLMode, 
									targetDic=g_dicE2EDelayRaw_M2)

					# dicThroughputRaw = {}
					readData(xAxis=data["arrivalRate"], 
							yAxisDataPoint=data["throughput"], 
							targetDic=g_dicThroRaw_M2)

					writeFilename(peType='cdfThro', mode=mode, 
									CTRMode=CTRMode, 
									TLMode=TLMode, 
									targetDic=g_dicThroRaw_M2)

					meanCompute(inputDic=g_dicE2EDelayRaw_M2, 
								retDic=g_dicMeanE2E_M2)

					writeFilename(peType='meanE2E', mode=mode, 
									CTRMode=CTRMode, 
									TLMode=TLMode, 
									targetDic=g_dicMeanE2E_M2)						
					meanCompute(inputDic=g_dicThroRaw_M2, 
								retDic=g_dicThro_M2)

					writeFilename(peType='meanThro', mode=mode, 
									CTRMode=CTRMode, 
									TLMode=TLMode, 
									targetDic=g_dicThro_M2)
				elif mode == 3:
					if CTRMode == 0:
						# dicE2EDelayRaw = {}
						readData(xAxis=data["arrivalRate"], 
								yAxisDataPoint=data["meanE2EDelay"], 
								targetDic=g_dicE2EDelayRaw_M3CTR0)

						writeFilename(peType='cdfE2E', mode=mode, 
										CTRMode=CTRMode, 
										TLMode=TLMode, 
										targetDic=g_dicE2EDelayRaw_M3CTR0)

						# dicThroughputRaw = {}
						readData(xAxis=data["arrivalRate"], 
								yAxisDataPoint=data["throughput"], 
								targetDic=g_dicThroRaw_M3CTR0)

						writeFilename(peType='cdfThro', mode=mode, 
										CTRMode=CTRMode, 
										TLMode=TLMode, 
										targetDic=g_dicThroRaw_M3CTR0)

						meanCompute(inputDic=g_dicE2EDelayRaw_M3CTR0, 
									retDic=g_dicMeanE2E_M3CTR0)

						writeFilename(peType='meanE2E', mode=mode, 
										CTRMode=CTRMode, 
										TLMode=TLMode, 
										targetDic=g_dicMeanE2E_M3CTR0)						
						meanCompute(inputDic=g_dicThroRaw_M3CTR0, 
									retDic=g_dicThro_M3CTR0)

						writeFilename(peType='meanThro', mode=mode, 
										CTRMode=CTRMode, 
										TLMode=TLMode, 
										targetDic=g_dicThro_M3CTR0)

					elif CTRMode == 1:
						# dicE2EDelayRaw = {}
						readData(xAxis=data["arrivalRate"], 
								yAxisDataPoint=data["meanE2EDelay"], 
								targetDic=g_dicE2EDelayRaw_M3CTR1)

						writeFilename(peType='cdfE2E', mode=mode, 
										CTRMode=CTRMode, 
										TLMode=TLMode, 
										targetDic=g_dicE2EDelayRaw_M3CTR1)

						# dicThroughputRaw = {}
						readData(xAxis=data["arrivalRate"], 
								yAxisDataPoint=data["throughput"], 
								targetDic=g_dicThroRaw_M3CTR1)

						writeFilename(peType='cdfThro', mode=mode, 
										CTRMode=CTRMode, 
										TLMode=TLMode, 
										targetDic=g_dicThroRaw_M3CTR1)

						meanCompute(inputDic=g_dicE2EDelayRaw_M3CTR1, 
									retDic=g_dicMeanE2E_M3CTR1)

						writeFilename(peType='meanE2E', mode=mode, 
										CTRMode=CTRMode, 
										TLMode=TLMode, 
										targetDic=g_dicMeanE2E_M3CTR1)						
						meanCompute(inputDic=g_dicThroRaw_M3CTR1, 
									retDic=g_dicThro_M3CTR1)

						writeFilename(peType='meanThro', 
										mode=mode, CTRMode=CTRMode, 
										TLMode=TLMode, 
										targetDic=g_dicThro_M3CTR1)

					elif CTRMode == 2:					
						# dicE2EDelayRaw = {}
						readData(xAxis=data["arrivalRate"], 
								yAxisDataPoint=data["meanE2EDelay"], 
								targetDic=g_dicE2EDelayRaw_M3CTR2)

						writeFilename(peType='cdfE2E', mode=mode, 
										CTRMode=CTRMode, 
										TLMode=TLMode, 
										targetDic=g_dicE2EDelayRaw_M3CTR2)

						# dicThroughputRaw = {}
						readData(xAxis=data["arrivalRate"], 
								yAxisDataPoint=data["throughput"], 
								targetDic=g_dicThroRaw_M3CTR2)

						writeFilename(peType='cdfThro', 
										mode=mode, CTRMode=CTRMode, 
										TLMode=TLMode, 
										targetDic=g_dicThroRaw_M3CTR2)

						meanCompute(inputDic=g_dicE2EDelayRaw_M3CTR2, 
									retDic=g_dicMeanE2E_M3CTR2)

						writeFilename(peType='meanE2E', 
										mode=mode, CTRMode=CTRMode, 
										TLMode=TLMode, 
										targetDic=g_dicMeanE2E_M3CTR2)						
						meanCompute(inputDic=g_dicThroRaw_M3CTR2, 
									retDic=g_dicThro_M3CTR2)

						writeFilename(peType='meanThro', 
										mode=mode, CTRMode=CTRMode, 
										TLMode=TLMode, 
										targetDic=g_dicThro_M3CTR2)

					elif CTRMode == 3:					
						# dicE2EDelayRaw = {}
						readData(xAxis=data["arrivalRate"], 
								yAxisDataPoint=data["meanE2EDelay"], 
								targetDic=g_dicE2EDelayRaw_M3CTR3)

						writeFilename(peType='cdfE2E', 
										mode=mode, CTRMode=CTRMode, 
										TLMode=TLMode, 
										targetDic=g_dicE2EDelayRaw_M3CTR3)

						# dicThroughputRaw = {}
						readData(xAxis=data["arrivalRate"], 
								yAxisDataPoint=data["throughput"], 
								targetDic=g_dicThroRaw_M3CTR3)

						writeFilename(peType='cdfThro', 
										mode=mode, CTRMode=CTRMode, 
										TLMode=TLMode, 
										targetDic=g_dicThroRaw_M3CTR3)

						meanCompute(inputDic=g_dicE2EDelayRaw_M3CTR3, 
									retDic=g_dicMeanE2E_M3CTR3)

						writeFilename(peType='meanE2E', 
										mode=mode, CTRMode=CTRMode, 
										TLMode=TLMode, 
										targetDic=g_dicMeanE2E_M3CTR3)						
						meanCompute(inputDic=g_dicThroRaw_M3CTR3, 
									retDic=g_dicThro_M3CTR3)

						writeFilename(peType='meanThro', 
										mode=mode, CTRMode=CTRMode, 
										TLMode=TLMode, 
										targetDic=g_dicThro_M3CTR3)
				elif mode == 6:
					if CTRMode == 0:
						# dicE2EDelayRaw = {}
						readData(xAxis=data["arrivalRate"], 
								yAxisDataPoint=data["meanE2EDelay"], 
								targetDic=g_dicE2EDelayRaw_M6CTR0)

						writeFilename(peType='cdfE2E', 
										mode=mode, CTRMode=CTRMode, 
										TLMode=TLMode, 
										targetDic=g_dicE2EDelayRaw_M6CTR0)

						# dicThroughputRaw = {}
						readData(xAxis=data["arrivalRate"], 
								yAxisDataPoint=data["throughput"], 
								targetDic=g_dicThroRaw_M6CTR0)

						writeFilename(peType='cdfThro', 
										mode=mode, CTRMode=CTRMode, 
										TLMode=TLMode, 
										targetDic=g_dicThroRaw_M6CTR0)

						meanCompute(inputDic=g_dicE2EDelayRaw_M6CTR0, 
									retDic=g_dicMeanE2E_M6CTR0)

						writeFilename(peType='meanE2E', 
										mode=mode, CTRMode=CTRMode, 
										TLMode=TLMode, 
										targetDic=g_dicMeanE2E_M6CTR0)						
						meanCompute(inputDic=g_dicThroRaw_M6CTR0, 
									retDic=g_dicThro_M6CTR0)

						writeFilename(peType='meanThro', 
										mode=mode, CTRMode=CTRMode, 
										TLMode=TLMode, 
										targetDic=g_dicThro_M6CTR0)

					elif CTRMode == 1:
						# dicE2EDelayRaw = {}
						readData(xAxis=data["arrivalRate"], 
								yAxisDataPoint=data["meanE2EDelay"], 
								targetDic=g_dicE2EDelayRaw_M6CTR1)

						writeFilename(peType='cdfE2E', 
										mode=mode, CTRMode=CTRMode, 
										TLMode=TLMode, 
										targetDic=g_dicE2EDelayRaw_M6CTR1)

						# dicThroughputRaw = {}
						readData(xAxis=data["arrivalRate"], 
								yAxisDataPoint=data["throughput"], 
								targetDic=g_dicThroRaw_M6CTR1)

						writeFilename(peType='cdfThro', 
										mode=mode, CTRMode=CTRMode, 
										TLMode=TLMode, 
										targetDic=g_dicThroRaw_M6CTR1)

						meanCompute(inputDic=g_dicE2EDelayRaw_M6CTR1, 
									retDic=g_dicMeanE2E_M6CTR1)

						writeFilename(peType='meanE2E', 
										mode=mode, CTRMode=CTRMode, 
										TLMode=TLMode, 
										targetDic=g_dicMeanE2E_M6CTR1)						
						meanCompute(inputDic=g_dicThroRaw_M6CTR1, 
									retDic=g_dicThro_M6CTR1)

						writeFilename(peType='meanThro', 
										mode=mode, CTRMode=CTRMode, 
										TLMode=TLMode, 
										targetDic=g_dicThro_M6CTR1)

					elif CTRMode == 2:
						# dicE2EDelayRaw = {}
						readData(xAxis=data["arrivalRate"], 
								yAxisDataPoint=data["meanE2EDelay"], 
								targetDic=g_dicE2EDelayRaw_M6CTR2)

						writeFilename(peType='cdfE2E', 
										mode=mode, CTRMode=CTRMode, 
										TLMode=TLMode, 
										targetDic=g_dicE2EDelayRaw_M6CTR2)

						# dicThroughputRaw = {}
						readData(xAxis=data["arrivalRate"], 
								yAxisDataPoint=data["throughput"], 
								targetDic=g_dicThroRaw_M6CTR2)

						writeFilename(peType='cdfThro', 
										mode=mode, CTRMode=CTRMode, 
										TLMode=TLMode, 
										targetDic=g_dicThroRaw_M6CTR2)

						meanCompute(inputDic=g_dicE2EDelayRaw_M6CTR2, 
									retDic=g_dicMeanE2E_M6CTR2)

						writeFilename(peType='meanE2E', 
										mode=mode, CTRMode=CTRMode, 
										TLMode=TLMode, 
										targetDic=g_dicMeanE2E_M6CTR2)						
						meanCompute(inputDic=g_dicThroRaw_M6CTR2, 
									retDic=g_dicThro_M6CTR2)

						writeFilename(peType='meanThro', 
										mode=mode, CTRMode=CTRMode, 
										TLMode=TLMode, 
										targetDic=g_dicThro_M6CTR2)

					elif CTRMode == 3:
						# dicE2EDelayRaw = {}
						readData(xAxis=data["arrivalRate"], 
								yAxisDataPoint=data["meanE2EDelay"], 
								targetDic=g_dicE2EDelayRaw_M6CTR3)

						writeFilename(peType='cdfE2E', 
										mode=mode, CTRMode=CTRMode, 
										TLMode=TLMode, 
										targetDic=g_dicE2EDelayRaw_M6CTR3)

						# dicThroughputRaw = {}
						readData(xAxis=data["arrivalRate"], 
								yAxisDataPoint=data["throughput"], 
								targetDic=g_dicThroRaw_M6CTR3)

						writeFilename(peType='cdfThro', 
										mode=mode, CTRMode=CTRMode, 
										TLMode=TLMode, 
										targetDic=g_dicThroRaw_M6CTR3)

						meanCompute(inputDic=g_dicE2EDelayRaw_M6CTR3, 
									retDic=g_dicMeanE2E_M6CTR3)

						writeFilename(peType='meanE2E', 
										mode=mode, CTRMode=CTRMode, 
										TLMode=TLMode, 
										targetDic=g_dicMeanE2E_M6CTR3)						
						meanCompute(inputDic=g_dicThroRaw_M6CTR3, 
									retDic=g_dicThro_M6CTR3)

						writeFilename(peType='meanThro', 
										mode=mode, CTRMode=CTRMode, 
										TLMode=TLMode, 
										targetDic=g_dicThro_M6CTR3)
				elif mode == 5:
					if TLMode == 2:
						# dicE2EDelayRaw = {}
						readData(xAxis=data["arrivalRate"], 
								yAxisDataPoint=data["meanE2EDelay"], 
								targetDic=g_dicE2EDelayRaw_M5ACT)

						writeFilename(peType='cdfE2E', 
										mode=mode, CTRMode=CTRMode, 
										TLMode=TLMode, 
										targetDic=g_dicE2EDelayRaw_M5ACT)

						# dicThroughputRaw = {}
						readData(xAxis=data["arrivalRate"], 
								yAxisDataPoint=data["throughput"], 
								targetDic=g_dicThroRaw_M5ACT)

						writeFilename(peType='cdfThro', 
										mode=mode, CTRMode=CTRMode, 
										TLMode=TLMode, 
										targetDic=g_dicThroRaw_M5ACT)

						meanCompute(inputDic=g_dicE2EDelayRaw_M5ACT, 
									retDic=g_dicMeanE2E_M5ACT)

						writeFilename(peType='meanE2E', 
										mode=mode, CTRMode=CTRMode, 
										TLMode=TLMode, 
										targetDic=g_dicMeanE2E_M5ACT)						
						meanCompute(inputDic=g_dicThroRaw_M5ACT, 
									retDic=g_dicThro_M5ACT)

						writeFilename(peType='meanThro', 
										mode=mode, CTRMode=CTRMode, 
										TLMode=TLMode, 
										targetDic=g_dicThro_M5ACT)

				elif mode == 7:
					if TLMode == 2:
						# dicE2EDelayRaw = {}
						readData(xAxis=data["arrivalRate"], 
								yAxisDataPoint=data["meanE2EDelay"], 
								targetDic=g_dicE2EDelayRaw_M7ACT)

						writeFilename(peType='cdfE2E', 
										mode=mode, CTRMode=CTRMode, 
										TLMode=TLMode, 
										targetDic=g_dicE2EDelayRaw_M7ACT)

						# dicThroughputRaw = {}
						readData(xAxis=data["arrivalRate"], 
								yAxisDataPoint=data["throughput"], 
								targetDic=g_dicThroRaw_M7ACT)

						writeFilename(peType='cdfThro', 
										mode=mode, CTRMode=CTRMode, 
										TLMode=TLMode, 
										targetDic=g_dicThroRaw_M7ACT)

						meanCompute(inputDic=g_dicE2EDelayRaw_M7ACT, 
									retDic=g_dicMeanE2E_M7ACT)

						writeFilename(peType='meanE2E', 
										mode=mode, CTRMode=CTRMode, 
										TLMode=TLMode, 
										targetDic=g_dicMeanE2E_M7ACT)						
						meanCompute(inputDic=g_dicThroRaw_M7ACT, 
									retDic=g_dicThro_M7ACT)

						writeFilename(peType='meanThro', 
										mode=mode, CTRMode=CTRMode, 
										TLMode=TLMode, 
										targetDic=g_dicThro_M7ACT)

# this is the main entry point of this script
if __name__ == "__main__":
	options = optionsSet()
	directory = options.directory
	outputDir = options.outputDir

	global g_dicAllData
	g_dicAllData = {}

	#E2E delay
	#M3
	global g_dicE2EDelayRaw_M3CTR0
	g_dicE2EDelayRaw_M3CTR0={}
	global g_dicMeanE2E_M3CTR0
	g_dicMeanE2E_M3CTR0 = {}

	global g_dicE2EDelayRaw_M3CTR1
	g_dicE2EDelayRaw_M3CTR1={}
	global g_dicMeanE2E_M3CTR1
	g_dicMeanE2E_M3CTR1 = {}

	global g_dicE2EDelayRaw_M3CTR2
	g_dicE2EDelayRaw_M3CTR2={}
	global g_dicMeanE2E_M3CTR2
	g_dicMeanE2E_M3CTR2 = {}

	global g_dicE2EDelayRaw_M3CTR3
	g_dicE2EDelayRaw_M3CTR3={}	
	global g_dicMeanE2E_M3CTR3
	g_dicMeanE2E_M3CTR3 = {}

	#CDF
	global g_cdfE2EDelayRaw_M3CTR0
	g_cdfE2EDelayRaw_M3CTR0 = []
	global g_cdfE2EDelayRaw_M3CTR1
	g_cdfE2EDelayRaw_M3CTR1 = []
	global g_cdfE2EDelayRaw_M3CTR2
	g_cdfE2EDelayRaw_M3CTR2 = []
	global g_cdfE2EDelayRaw_M3CTR3
	g_cdfE2EDelayRaw_M3CTR3 =[]

	# M6
	global g_dicE2EDelayRaw_M6CTR0
	g_dicE2EDelayRaw_M6CTR0={}
	global g_dicMeanE2E_M6CTR0
	g_dicMeanE2E_M6CTR0 = {}

	global g_dicE2EDelayRaw_M6CTR1
	g_dicE2EDelayRaw_M6CTR1={}
	global g_dicMeanE2E_M6CTR1
	g_dicMeanE2E_M6CTR1 = {}

	global g_dicE2EDelayRaw_M6CTR2
	g_dicE2EDelayRaw_M6CTR2={}
	global g_dicMeanE2E_M6CTR2
	g_dicMeanE2E_M6CTR2 = {}

	global g_dicE2EDelayRaw_M6CTR3
	g_dicE2EDelayRaw_M6CTR3={}
	global g_dicMeanE2E_M6CTR3
	g_dicMeanE2E_M6CTR3 = {}

	#CDF
	global g_cdfE2EDelayRaw_M6CTR0
	g_cdfE2EDelayRaw_M6CTR0 = []
	global g_cdfE2EDelayRaw_M6CTR1
	g_cdfE2EDelayRaw_M6CTR1 = []
	global g_cdfE2EDelayRaw_M6CTR2
	g_cdfE2EDelayRaw_M6CTR2 = []
	global g_cdfE2EDelayRaw_M6CTR3
	g_cdfE2EDelayRaw_M6CTR3 = []	

	# Throughput
	global g_dicThroRaw_M3CTR0
	g_dicThroRaw_M3CTR0={}
	global g_dicThro_M3CTR0
	g_dicThro_M3CTR0 = {}
	global g_dicThroRaw_M3CTR1
	g_dicThroRaw_M3CTR1={}	
	global g_dicThro_M3CTR1
	g_dicThro_M3CTR1 = {}
	global g_dicThroRaw_M3CTR2
	g_dicThroRaw_M3CTR2={}
	global g_dicThro_M3CTR2
	g_dicThro_M3CTR2 = {}
	global g_dicThroRaw_M3CTR3
	g_dicThroRaw_M3CTR3={}
	global g_dicThro_M3CTR3
	g_dicThro_M3CTR3 = {}

	# CDF
	global g_cdfThroRaw_M3CTR0
	g_cdfThroRaw_M3CTR0 = []
	global g_cdfThroRaw_M3CTR1
	g_cdfThroRaw_M3CTR1 = []
	global g_cdfThroRaw_M3CTR2
	g_cdfThroRaw_M3CTR2 = []
	global g_cdfThroRaw_M3CTR3
	g_cdfThroRaw_M3CTR3 = []	

	global g_dicThroRaw_M6CTR0
	g_dicThroRaw_M6CTR0={}
	global g_dicThro_M6CTR0
	g_dicThro_M6CTR0 = {}
	global g_dicThroRaw_M6CTR1
	g_dicThroRaw_M6CTR1={}
	global g_dicThro_M6CTR1
	g_dicThro_M6CTR1 = {}
	global g_dicThroRaw_M6CTR2
	g_dicThroRaw_M6CTR2={}
	global g_dicThro_M6CTR2
	g_dicThro_M6CTR2 = {}
	global g_dicThroRaw_M6CTR3
	g_dicThroRaw_M6CTR3={}
	global g_dicThro_M6CTR3
	g_dicThro_M6CTR3 = {}

	# CDF
	global g_cdfThroRaw_M6CTR0
	g_cdfThroRaw_M6CTR0 = []
	global g_cdfThroRaw_M6CTR1
	g_cdfThroRaw_M6CTR1 = []
	global g_cdfThroRaw_M6CTR2
	g_cdfThroRaw_M6CTR2 = []
	global g_cdfThroRaw_M6CTR3
	g_cdfThroRaw_M6CTR3 = []	


	# Actuated
	global g_dicE2EDelayRaw_M5ACT
	g_dicE2EDelayRaw_M5ACT={}
	global g_dicMeanE2E_M5ACT
	g_dicMeanE2E_M5ACT = {}
	global g_dicE2EDelayRaw_M7ACT
	g_dicE2EDelayRaw_M7ACT={}
	global g_dicMeanE2E_M7ACT
	g_dicMeanE2E_M7ACT = {}

	global g_dicThroRaw_M5ACT
	g_dicThroRaw_M5ACT={}
	global g_dicThro_M5ACT
	g_dicThro_M5ACT = {}
	global g_dicThroRaw_M7ACT
	g_dicThroRaw_M7ACT={}
	global g_dicThro_M7ACT
	g_dicThro_M7ACT = {}

	#CDF
	global g_cdfE2EDelayRaw_M5ACT
	g_cdfE2EDelayRaw_M5ACT = []
	global g_cdfE2EDelayRaw_M7ACT
	g_cdfE2EDelayRaw_M7ACT = []
	global g_cdfThroRaw_M5ACT
	g_cdfThroRaw_M5ACT = []
	global g_cdfThroRaw_M7ACT
	g_cdfThroRaw_M7ACT = []


	# Static TL
	# M0, 2
	global g_dicE2EDelayRaw_M0
	g_dicE2EDelayRaw_M0 = {}
	global g_dicMeanE2E_M0
	g_dicMeanE2E_M0 = {}

	global g_dicE2EDelayRaw_M2
	g_dicE2EDelayRaw_M2 = {}
	global g_dicMeanE2E_M2
	g_dicMeanE2E_M2 = {}

	global g_dicThroRaw_M0
	g_dicThroRaw_M0={}
	global g_dicThro_M0
	g_dicThro_M0={}

	global g_dicThroRaw_M2
	g_dicThroRaw_M2 = {}
	global g_dicThro_M2
	g_dicThro_M2 = {}

	# CDF
	global g_cdfE2EDelayRaw_M0
	g_cdfE2EDelayRaw_M0 = []
	global g_cdfE2EDelayRaw_M2
	g_cdfE2EDelayRaw_M2 = []

	global g_cdfThroRaw_M0
	g_cdfThroRaw_M0 = []
	global g_cdfThroRaw_M2
	g_cdfThroRaw_M2 = []


	if directory[len(directory)-1] != '/':
		directory = directory + '/'

	print("Scan:", directory)
	collectData(directory)
	processData()

	saveData(prefix1='ESTN', savePath=outputDir)

	print("Process Finished!")
	print("The data are saved at: " + outputDir)

	# g_dicAllData['g_dicE2EDelayRaw_M3CTR0'] = g_dicE2EDelayRaw_M3CTR0
	# g_dicAllData['g_dicE2EDelayRaw_M3CTR1'] = g_dicE2EDelayRaw_M3CTR1
	# g_dicAllData['g_dicE2EDelayRaw_M3CTR2'] = g_dicE2EDelayRaw_M3CTR2
	# g_dicAllData['g_dicE2EDelayRaw_M3CTR3'] = g_dicE2EDelayRaw_M3CTR3
	# g_dicAllData['g_dicE2EDelayRaw_M6CTR0'] = g_dicE2EDelayRaw_M6CTR0
	# g_dicAllData['g_dicE2EDelayRaw_M6CTR1'] = g_dicE2EDelayRaw_M6CTR1
	# g_dicAllData['g_dicE2EDelayRaw_M6CTR2'] = g_dicE2EDelayRaw_M6CTR2
	# g_dicAllData['g_dicE2EDelayRaw_M6CTR3'] = g_dicE2EDelayRaw_M6CTR3

	# g_dicAllData['g_dicMeanE2E_M3CTR0'] = g_dicMeanE2E_M3CTR0
	# g_dicAllData['g_dicMeanE2E_M3CTR1'] = g_dicMeanE2E_M3CTR1
	# g_dicAllData['g_dicMeanE2E_M3CTR2'] = g_dicMeanE2E_M3CTR2
	# g_dicAllData['g_dicMeanE2E_M3CTR3'] = g_dicMeanE2E_M3CTR3
	# g_dicAllData['g_dicMeanE2E_M6CTR0'] = g_dicMeanE2E_M6CTR0
	# g_dicAllData['g_dicMeanE2E_M6CTR1'] = g_dicMeanE2E_M6CTR1
	# g_dicAllData['g_dicMeanE2E_M6CTR2'] = g_dicMeanE2E_M6CTR2
	# g_dicAllData['g_dicMeanE2E_M6CTR3'] = g_dicMeanE2E_M6CTR3

	# g_dicAllData['g_cdfE2EDelayRaw_M3CTR0'] = g_cdfE2EDelayRaw_M3CTR0
	# g_dicAllData['g_cdfE2EDelayRaw_M3CTR1'] = g_cdfE2EDelayRaw_M3CTR1
	# g_dicAllData['g_cdfE2EDelayRaw_M3CTR2'] = g_cdfE2EDelayRaw_M3CTR2
	# g_dicAllData['g_cdfE2EDelayRaw_M3CTR3'] = g_cdfE2EDelayRaw_M3CTR3
	# g_dicAllData['g_cdfE2EDelayRaw_M6CTR0'] = g_cdfE2EDelayRaw_M6CTR0
	# g_dicAllData['g_cdfE2EDelayRaw_M6CTR1'] = g_cdfE2EDelayRaw_M6CTR1
	# g_dicAllData['g_cdfE2EDelayRaw_M6CTR2'] = g_cdfE2EDelayRaw_M6CTR2
	# g_dicAllData['g_cdfE2EDelayRaw_M6CTR3'] = g_cdfE2EDelayRaw_M6CTR3


	# g_dicAllData['g_dicThroRaw_M3CTR0'] = g_dicThroRaw_M3CTR0
	# g_dicAllData['g_dicThroRaw_M3CTR1'] = g_dicThroRaw_M3CTR1
	# g_dicAllData['g_dicThroRaw_M3CTR2'] = g_dicThroRaw_M3CTR2
	# g_dicAllData['g_dicThroRaw_M3CTR3'] = g_dicThroRaw_M3CTR3
	# g_dicAllData['g_dicThroRaw_M6CTR0'] = g_dicThroRaw_M6CTR0
	# g_dicAllData['g_dicThroRaw_M6CTR1'] = g_dicThroRaw_M6CTR1
	# g_dicAllData['g_dicThroRaw_M6CTR2'] = g_dicThroRaw_M6CTR2
	# g_dicAllData['g_dicThroRaw_M6CTR3'] = g_dicThroRaw_M6CTR3

	# g_dicAllData['g_dicThro_M3CTR0'] = g_dicThro_M3CTR0
	# g_dicAllData['g_dicThro_M3CTR1'] = g_dicThro_M3CTR1
	# g_dicAllData['g_dicThro_M3CTR2'] = g_dicThro_M3CTR2
	# g_dicAllData['g_dicThro_M3CTR3'] = g_dicThro_M3CTR3
	# g_dicAllData['g_dicThro_M6CTR0'] = g_dicThro_M6CTR0
	# g_dicAllData['g_dicThro_M6CTR1'] = g_dicThro_M6CTR1
	# g_dicAllData['g_dicThro_M6CTR2'] = g_dicThro_M6CTR3
	# g_dicAllData['g_dicThro_M6CTR3'] = g_dicThro_M6CTR3

	# g_dicAllData['g_cdfThroRaw_M3CTR0'] = g_cdfThroRaw_M3CTR0
	# g_dicAllData['g_cdfThroRaw_M3CTR1'] = g_cdfThroRaw_M3CTR1
	# g_dicAllData['g_cdfThroRaw_M3CTR2'] = g_cdfThroRaw_M3CTR2
	# g_dicAllData['g_cdfThroRaw_M3CTR3'] = g_cdfThroRaw_M3CTR3
	# g_dicAllData['g_cdfThroRaw_M6CTR0'] = g_cdfThroRaw_M6CTR0
	# g_dicAllData['g_cdfThroRaw_M6CTR1'] = g_cdfThroRaw_M6CTR1
	# g_dicAllData['g_cdfThroRaw_M6CTR2'] = g_cdfThroRaw_M6CTR2
	# g_dicAllData['g_cdfThroRaw_M6CTR3'] = g_cdfThroRaw_M6CTR3


	# g_dicAllData['g_dicE2EDelayRaw_M5ACT'] = g_dicE2EDelayRaw_M5ACT
	# g_dicAllData['g_dicE2EDelayRaw_M7ACT'] = g_dicE2EDelayRaw_M7ACT

	# g_dicAllData['g_dicMeanE2E_M5ACT'] = g_dicMeanE2E_M5ACT
	# g_dicAllData['g_dicMeanE2E_M7ACT'] = g_dicMeanE2E_M7ACT

	# g_dicAllData['g_dicThroRaw_M5ACT'] = g_dicThroRaw_M5ACT
	# g_dicAllData['g_dicThroRaw_M7ACT'] = g_dicThroRaw_M7ACT

	# g_dicAllData['g_dicThro_M5ACT'] = g_dicThro_M5ACT
	# g_dicAllData['g_dicThro_M7ACT'] = g_dicThro_M7ACT

	# g_dicAllData['g_cdfE2EDelayRaw_M5ACT'] = g_cdfE2EDelayRaw_M5ACT
	# g_dicAllData['g_cdfE2EDelayRaw_M7ACT'] = g_cdfE2EDelayRaw_M7ACT
	# g_dicAllData['g_cdfThroRaw_M5ACT'] = g_cdfThroRaw_M5ACT
	# g_dicAllData['g_cdfThroRaw_M7ACT'] = g_cdfThroRaw_M7ACT