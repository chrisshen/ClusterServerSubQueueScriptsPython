#!/home/chris/anaconda3/bin/python3
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

# from __future__ import absolute_import
# from __future__ import print_function
# from __future__ import division

import os
import sys
import optparse
# import subprocess
# import random
# import time
# import numpy as np 
# import matplotlib.pyplot as plt

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

from ReadFile import ReadFile
from StatisticCompute import StatisticComp

DEBUG = True

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
	optParser.add_option("-x",
						type=str,
						dest="xaxis",
						default="density",
						help="x axis parameter for simulation [default: %default] [density, BGTI]"
						)

	# simulation mode option
	optParser.add_option("-m",
						type="int",
						dest="mode",
						default=3,
						metavar="NUM",
						help="mode for simulation [default: %default] [0:Dijkstra, 1:CTR, 2:SAINT, 3:SAINT+CTR, 4:Actuated, 5:SAINT+Actuated, 6:Dijkstra+CTR, 7:Dijkstra+Actuated, 8:StaticTL]"
						)

	optParser.add_option("--para",
						type=str,
						dest="para",
						default="sigma",
						help="varible for this data set"
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

	# PDR
	outData(inputDicDataRaw=g_dicInputData,
			outputDicMeanData=g_dicMeanData,
			outputCDF=g_cdfData)

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

	if g_dicMeanData:
		# if g_dicMeanData.has_key('filename'):
		filename = prefix0+prefix1
		filename = savePath+filename+'-output'
		saveDataToFile(filename, g_dicMeanData)

if __name__ == "__main__":
	options = optionsSet()
	filePath = options.directory
	outputDir = options.outputDir
	variable = options.para
	# global xaxis;
	# xaxis = options.xaxis

	# if directory[len(directory)-1] != '/':
	# 	directory = directory + '/'

	# print("Scan:", directory)
	
	# raw
	global g_dicData
	g_dicInputData={}

	readFile = ReadFile()
	statComp = StatisticComp()

	g_dicInputData = readFile.readDire(filePath)
	# g_dicInputData = readFile.readDireTimeseries(filePath)

	print(g_dicInputData)
	# if DEBUG:
	# 	pprint.pprint(g_dicInputData)
		# print(len(g_dicInputData['5']))
	# collectData(directory)

	# sys.exit()

	global g_dicMeanData
	g_dicMeanData = {}

	statComp.meanCompute(g_dicInputData, g_dicMeanData)

	pprint.pprint(g_dicMeanData)
	# sys.exit()

	global g_cdfData
	g_cdfData = []

	statComp.outData(g_dicInputData, g_dicMeanData, g_cdfData)

	pprint.pprint(g_dicMeanData)
	# pprint.pprint(g_cdfData)
	schemeName = "ips-box"

	if schemeName:
		# readFile.saveData(prefix1=schemeName, ending=variable,savePath=outputDir, dataToSave=g_dicMeanData)
		# readFile.saveCDFDataToFile(prefix1=schemeName, ending=variable,savePath=outputDir, dataToSave=g_cdfData)
		readFile.saveBoxDataToFile(prefix1=schemeName, ending=variable,savePath=outputDir, dataToSave=g_dicInputData)
	else:
		exit("schemeName is empty!")


	print("Process Finished!")
	print("The data are saved at: " + outputDir)
