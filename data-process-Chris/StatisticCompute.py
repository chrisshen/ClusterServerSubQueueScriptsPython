#!/home/chris/anaconda2/bin/python2
# @file    StatisticCompute.py
# @author  Chris Shen
# @date    2020-02-07
# @version $Id$

from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

import os
import sys
# import optparse
# import subprocess
# import random
# import time
import numpy as np 

# pretty printer
import pprint

class StatisticComp:
	"""docstring for StatisticComp"""
	def __init__(self,):
		super(StatisticComp, self).__init__()
		# self.arg = arg

	def cdfMaking(self, inDic, outCDFData):
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

	def meanCompute(self, inputDic, retDic):
		''' Compute mean, return to retDic with list value

		args:
			inputDic (dict): raw data
			retDic (dict): return mean
		return:

		'''	
		for key, valList in inputDic.viewitems():
			if not isinstance(key, str):
				retDic[key] = [sum(valList)/len(valList)]

	def variCompute(self, inDic, inDicMean, retDic):
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

	def confCompute(self, inDic, inVari, retDic):
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

	def mergeMeanAndConfi(self, inDicMean, inDicConf):
		''' Compute confidence interval, return to retDic

		args:
			inDic (dict): raw input data
			inVari (dict): input variance data
			retDic (dict): return confience interval data
		'''	
		for key, val in inDicMean.viewitems():
			if not isinstance(key, str):
				inDicMean[key].append(inDicConf[key])
