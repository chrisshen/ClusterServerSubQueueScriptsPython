#!/home/chris/anaconda2/bin/python2
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
# import json

# for CSV file parsing
import csv

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
						help="mode for simulation [default: %default] [0:Dijkstra, 1:CTR, 2:SAINT, 3:SAINT+CTR, 4:Actuated, 5:SAINT+Actuated, 6:Dijkstra+CTR, 7:Dijkstra+Actuated, 8:StaticTL]"
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
	# print("dataList: ", dataList)

	actFreq = []
	for i in dataList:
		if actFreq:
			actFreq.append( 1.0/len(dataList) + actFreq[len(actFreq)-1])
		else:
			actFreq.append( 1.0/len(dataList) )

	# print("actFreq: ", actFreq)
	# cdfData = []

	for ind, i in enumerate(dataList):
		# print(actFreq[dataList.index(i)])
		outCDFData.append([i, round(actFreq[ind], 6)])

	# print("outCDFData: ", outCDFData)

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
	valEle = 0
	if yAxisDataPoint:
		valEle = float(yAxisDataPoint)
	if targetDic.has_key(key):
		if valEle:
			targetDic[key].append(valEle)
	else:
		if valEle:
			targetDic[key]=[valEle]


def readRawData(xAxis, yAxisDataPoint, targetDic):
	''' Save data from each file, save it to the targetDic

	args:
		xAxis (str, int): x axis point
		yAxisDataPoint (float): raw data point
	return:
		targetDic (dict): 
	'''
	key = xAxis
	valEle = float(yAxisDataPoint)
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

			if len(valList) > 1:
				# print(valList)
				vari = sum_var / (len(valList)-1)
			else:
				vari = 0
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
	# PDR
	outData(inputDicDataRaw=g_dicPDRRaw_BGTI,
			outputDicMeanData=g_dicMeanPDR_BGTI,
			outputCDF=g_cdfPDR_BGTI)
	# mean
	outData(inputDicDataRaw=g_dicMeanE2ERaw_BGTI,
			outputDicMeanData=g_dicMeanE2E_BGTI,
			outputCDF=g_cdfMeanE2E_BGTI)
	# max
	outData(inputDicDataRaw=g_dicMaxE2ERaw_BGTI,
			outputDicMeanData=g_dicMeanMaxE2E_BGTI,
			outputCDF=g_cdfMaxE2E_BGTI)

	# # Print for debug
	# print("M3CTR0")
	# pprint.pprint(g_dicMeanPDR_BGTI)
	# pprint.pprint(g_dicMeanE2E_BGTI)
	# pprint.pprint(g_dicMeanMaxE2E_BGTI)
	# pprint.pprint(g_cdfPDR_BGTI)
	# pprint.pprint(g_cdfMeanE2E_BGTI)
	# pprint.pprint(g_cdfMaxE2E_BGTI)

def writeFilename(peType, mode, targetDic):
	key = 'filename'
	value = '-'+str(peType)+'-m-'+str(mode)
	if key not in targetDic:
		targetDic[key] = value

def saveDataToFile(filename, inputDicData):

	inputDataKeySorted = sorted(inputDicData.keys())

	print(filename)
	with open(filename, 'w') as f:
		for key in inputDataKeySorted:
			value = inputDicData[key]
			length = len(value)
			if length == 2:
				# key: x point, value[0]: y point, value[1]: error bar
				f.write(str(key)+' '+str(value[0])+' '+str(value[1])+'\n')
			elif length == 1:
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
	
	# CTR, M = 3 and 6
	# E2E

	if g_dicMeanPDR_BGTI:
		if g_dicMeanPDR_BGTI.has_key('filename'):
			filename = prefix0+prefix1+g_dicMeanPDR_BGTI['filename']
		filename = savePath+filename
		saveDataToFile(filename, g_dicMeanPDR_BGTI)

	if g_dicMeanE2E_BGTI:
		if g_dicMeanE2E_BGTI.has_key('filename'):
			filename = prefix0+prefix1+g_dicMeanE2E_BGTI['filename']
		filename = savePath+filename
		saveDataToFile(filename, g_dicMeanE2E_BGTI)

	if g_dicMeanMaxE2E_BGTI:
		if g_dicMeanMaxE2E_BGTI.has_key('filename'):
			filename = prefix0+prefix1+g_dicMeanMaxE2E_BGTI['filename']
		filename = savePath+filename
		saveDataToFile(filename, g_dicMeanMaxE2E_BGTI)
			
	#cdf E2E 
	if g_cdfPDR_BGTI:
		if g_dicPDRRaw_BGTI.has_key('filename'):
			filename = prefix0+prefix1+g_dicPDRRaw_BGTI['filename']
		filename = savePath+filename
		saveCDFDataToFile(filename, g_cdfPDR_BGTI)

	if g_cdfMeanE2E_BGTI:
		if g_dicMeanE2ERaw_BGTI.has_key('filename'):
			filename = prefix0+prefix1+g_dicMeanE2ERaw_BGTI['filename']
		filename = savePath+filename
		saveCDFDataToFile(filename, g_cdfMeanE2E_BGTI)

	if g_cdfMaxE2E_BGTI:
		if g_dicMaxE2ERaw_BGTI.has_key('filename'):
			filename = prefix0+prefix1+g_dicMaxE2ERaw_BGTI['filename']
		filename = savePath+filename
		saveCDFDataToFile(filename, g_cdfMaxE2E_BGTI)

def collectData(directory):

	mode = ''
	global schemeName
	# scan the directory to read every data point
	for root, dirs, files in os.walk(directory):
		# print(root, files)
		for filename in files:
			# e.g., EDCA-s1Persis-BGTI-0.010-s-9.csv
			fnSplitList=filename.split('-')

			with open(root+filename, 'r') as csvf:
				print('.', end="")

				# bBGTI=False
				xAxisValue=0.0
				seed=-1
				# density=0.0
				# preprocess of prefix and parameters by file name
				# e.g., EDCA-s1Persis-BGTI-0.010-s-9.csv
				# ['EDCA', 's1Persis', 'BGTI', '0.020', 's', '2.csv']
				schemeName = fnSplitList[1]
				mode = fnSplitList[2]
				xAxisValue = float(fnSplitList[3])
				seed = int(fnSplitList[5].split('.')[0])
				print(schemeName, mode, xAxisValue, seed)

				delayDataRowInd = -1
				delayDataRow = []
				csvreader=csv.reader(csvf)
				for indRow, row in enumerate(csvreader):
					print(row)
					for ind, ele in enumerate(row):
						# prefix discovery 
						if ele == 'scheme':
							schemeName = row[ind+1]
						elif ele == 'seed':
							seed = int(row[ind+1])

						if ele == 'BGTI' and float(row[ind+1]):
							# bBGTI = True
							mode = ele
							xAxisValue = float(row[ind+1])
							
						elif ele == 'density' and float(row[ind+1]):
							mode = ele
							xAxisValue = float(row[ind+1]) * 0.01

						# elif ele == 'pktSendInterval':
						# 	mode = ele
						# 	xAxisValue = float(row[ind+1])

						# Data collection
						# elif ele == 'SuccessfulRatio': # PDR
						elif ele == 'PDR': # PDR

							readData(xAxis=xAxisValue, 
									yAxisDataPoint=row[ind+1], 
									targetDic=g_dicPDRRaw_BGTI)

						elif ele == 'maxE2EDelay': 

							readData(xAxis=xAxisValue, 
									yAxisDataPoint=row[ind+1], 
									targetDic=g_dicMaxE2ERaw_BGTI)

						# elif ele == 'meanE2EDelay': 

						# 	readData(xAxis=xAxisValue, 
						# 			yAxisDataPoint=row[ind+1], 
						# 			targetDic=g_dicMeanE2ERaw_BGTI)

					if row[0] == "E2E Delay":
						delayDataRowInd = indRow+1
					if delayDataRowInd != -1:
						delayDataRow = row

				if delayDataRowInd != -1:
					for ind, ele in enumerate(delayDataRow):
						readData(xAxis=xAxisValue, 
								yAxisDataPoint=ele, 
								targetDic=g_dicMeanE2ERaw_BGTI)

	meanCompute(inputDic=g_dicPDRRaw_BGTI, 
				retDic=g_dicMeanPDR_BGTI)
	meanCompute(inputDic=g_dicMaxE2ERaw_BGTI, 
				retDic=g_dicMeanMaxE2E_BGTI)
	meanCompute(inputDic=g_dicMeanE2ERaw_BGTI, 
				retDic=g_dicMeanE2E_BGTI)

	writeFilename(peType='MeanPDR', mode=mode, 
				targetDic=g_dicMeanPDR_BGTI)
	writeFilename(peType='MeanMaxE2E', mode=mode, 
			targetDic=g_dicMeanMaxE2E_BGTI)
	writeFilename(peType='MeanE2E', mode=mode, 
			targetDic=g_dicMeanE2E_BGTI)

	writeFilename(peType='cdfPDR', mode=mode, 
				targetDic=g_dicPDRRaw_BGTI)
	writeFilename(peType='cdfMaxE2E', mode=mode, 
			targetDic=g_dicMaxE2ERaw_BGTI)
	writeFilename(peType='cdfMeanE2E', mode=mode, 
			targetDic=g_dicMeanE2ERaw_BGTI)

	pprint.pprint(g_dicPDRRaw_BGTI)
	pprint.pprint(g_dicMaxE2ERaw_BGTI)
	pprint.pprint(g_dicMeanE2ERaw_BGTI)

	pprint.pprint(g_dicMeanPDR_BGTI)
	pprint.pprint(g_dicMeanMaxE2E_BGTI)
	pprint.pprint(g_dicMeanE2E_BGTI)

	pprint.pprint(g_cdfPDR_BGTI)
	pprint.pprint(g_cdfMeanE2E_BGTI)
	pprint.pprint(g_cdfMaxE2E_BGTI)

if __name__ == "__main__":
	options = optionsSet()
	directory = options.directory
	outputDir = options.outputDir

	global schemeName
	schemeName = ''

	# raw
	global g_dicPDRRaw_BGTI
	g_dicPDRRaw_BGTI={}
	global g_dicMeanE2ERaw_BGTI
	g_dicMeanE2ERaw_BGTI={}
	global g_dicMaxE2ERaw_BGTI
	g_dicMaxE2ERaw_BGTI={}

	# mean
	global g_dicMeanPDR_BGTI
	g_dicMeanPDR_BGTI={}
	global g_dicMeanE2E_BGTI
	g_dicMeanE2E_BGTI={}
	global g_dicMeanMaxE2E_BGTI
	g_dicMeanMaxE2E_BGTI={}

	# CDF
	global g_cdfPDRRaw_BGTI
	g_cdfPDRRaw_BGTI = []
	global g_cdfMeanE2ERaw_BGTI
	g_cdfMeanE2ERaw_BGTI = []
	global g_cdfMaxE2ERaw_BGTI
	g_cdfMaxE2ERaw_BGTI = []

	global g_cdfPDR_BGTI
	g_cdfPDR_BGTI = []
	global g_cdfMeanE2E_BGTI
	g_cdfMeanE2E_BGTI = []
	global g_cdfMaxE2E_BGTI
	g_cdfMaxE2E_BGTI = []


	if directory[len(directory)-1] != '/':
		directory = directory + '/'

	print("Scan:", directory)
	collectData(directory)
	processData()

	if schemeName:
		saveData(prefix1=schemeName, savePath=outputDir)
	else:
		exit("schemeName is empty!")


	print("Process Finished!")
	print("The data are saved at: " + outputDir)
