#!/home/chris/anaconda2/bin/python2
# @file    readFile.py
# @author  Chris Shen
# @date    2020-02-07
# @version $Id$

from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

import os
import sys

# pretty printer
import pprint

# for CSV file parsing
import csv

DEBUG = False

class ReadFile:
	"""docstring for ReadFile"""
	# def __init__(self):
		# super(ReadFile, self).__init__()
		# self.arg = arg

	def collectData(self, fileDir):
		"""scan the directory to read every data point"""
		# for root, dirs, files in os.walk(directory):
		# 	for filename in files:
		# 		# e.g., EDCA-s1Persis-BGTI-0.010-s-9.csv
		# 		fnSplitList=filename.split('-')

		tDic = {}
		with open(fileDir, 'r') as csvf:
			print('.', end="")

			csvreader=csv.reader(csvf)
			for indRow, row in enumerate(csvreader):
				print(indRow, row)

				# splitedRow = row.split(', ')
				
				for index, value in enumerate(row, start=1):
					self.readData(xAxis=index,
									yAxisDataPoint=value.strip(),
									targetDic=tDic)
					if DEBUG:
						print(index, value.strip())
		return tDic
		
	def readData(self, xAxis, yAxisDataPoint, targetDic):
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

	def readDire(self, fileDir):
		"""scan the directory to read every data point"""
		# for root, dirs, files in os.walk(directory):
		# 	for filename in files:
		# 		# e.g., EDCA-s1Persis-BGTI-0.010-s-9.csv
		# 		fnSplitList=filename.split('-')

		tDic = {}
		with open(fileDir, 'r') as csvf:
			print('.', end="")

			csvreader=csv.reader(csvf)
			for indRow, row in enumerate(csvreader):
				print(indRow, row)

				# splitedRow = row.split(', ')
				
				for index, value in enumerate(row, start=1):
					self.readData(xAxis=index,
									yAxisDataPoint=value.strip(),
									targetDic=tDic)
					if DEBUG:
						print(index, value.strip())
		return tDic