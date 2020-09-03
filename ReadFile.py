#!/home/chris/anaconda3/bin/python3
# @file    readFile.py
# @author  Chris Shen
# @date    2020-02-07
# @version $Id$

# from __future__ import absolute_import
# from __future__ import print_function
# from __future__ import division

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

		# rss
		for root, dirs, files in os.walk(fileDir):
			for folder in dirs:
				for root2, dirs2, files2 in os.walk(root+folder):
					currPath=root2+'/'
					# print(currPath)
					# for folder in dirs:
					for filename in files2:
						temp = []
						with open(currPath+filename, 'r') as csvf:
							print('.', end="")

							csvreader=csv.reader(csvf)
							for indRow, row in enumerate(csvreader):
								# print(indRow, row)
								temp.append(row)

						for ele in temp:
							if ele[0] == 'ap':
								lastEle = temp[-1]
								# print(lastEle)
								# alter here to get different data
								if float(ele[1]) == 4.0:
									if float(ele[1]) in tDic:
										tDic[float(ele[1])].append(float(lastEle[3]))
									else:
										tDic[float(ele[1])]=[float(lastEle[3])]
									break
		return tDic

	def readSDire(self, fileDir):
		"""scan the directory to read every data point"""
		# for root, dirs, files in os.walk(directory):
		# 	for filename in files:
		# 		# e.g., EDCA-s1Persis-BGTI-0.010-s-9.csv
		# 		fnSplitList=filename.split('-')
		tDic = {}

		# rss
		for root, dirs, files in os.walk(fileDir):
			# print(currPath)
			# for folder in dirs:
			for filename in files:
				temp = []
				with open(root+filename, 'r') as csvf:
					print('.', end="")

					csvreader=csv.reader(csvf)
					for indRow, row in enumerate(csvreader):
						# print(indRow, row)
						temp.append(row)

				for ele in temp:
					if ele[0] == 'ap':
						lastEle = temp[-1]
						# print(lastEle)
						# alter here to get different data
						if float(ele[1]) == 6.0:
							if float(ele[1]) in tDic:
								tDic[float(ele[1])].append(float(lastEle[3]))
							else:
								tDic[float(ele[1])]=[float(lastEle[3])]
							break
		return tDic


	def readDireTimeseries(self, fileDir):
		"""scan the directory to read every data point"""
		# for root, dirs, files in os.walk(directory):
		# 	for filename in files:
		# 		# e.g., EDCA-s1Persis-BGTI-0.010-s-9.csv
		# 		fnSplitList=filename.split('-')
		tDic = {}
		for root, dirs, files in os.walk(fileDir):
			for filename in files:
				temp = []
				with open(root+filename, 'r') as csvf:
					print('.', end="")

					csvreader=csv.reader(csvf)
					for indRow, row in enumerate(csvreader):
						# print(indRow, row)
						temp.append(row)
				# print(temp)
				timeStep = 1.0
				for ele in temp:
					if len(ele) > 2 and ele[2] == 'error':
						if timeStep in tDic:
							tDic[timeStep].append(float(ele[3]))
						else:
							tDic[timeStep]=[float(ele[3])]
						timeStep += 1
		return tDic

	def readDataIPStoDict(self, key, yAxisDataPoint, targetDic):
		''' Save data from each file, save it to the targetDic

		args:
			xAxis (str, int): x axis point
			yAxisDataPoint (float): raw data point
		return:
			targetDic (dict): 
		'''
		# key = xAxis
		valEle = 0
		# if yAxisDataPoint:
		# 	valEle = float(yAxisDataPoint)
		if key == 1:
			if targetDic.has_key(yAxisDataPoint):
				if valEle:
					targetDic[key].append(valEle)
			else:
				if valEle:
					targetDic[key]=[valEle]

	def saveData(self, prefix1, ending, savePath, dataToSave):
		prefix0 = 'plotData-'
		# prefix1 = scheme name
		if savePath[len(savePath)-1] != '/':
			savePath = savePath + '/'
		
		filename = ''

		if dataToSave:
			# if g_dicMeanData.has_key('filename'):
			filename = prefix0+prefix1
			filename = savePath+filename+'-'+ending
			self.saveDataToFile(filename, dataToSave)

	def saveDataToFile(self, filename, inputDicData):

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

	def saveCDFDataToFile(self, prefix1, ending, savePath, dataToSave):
		prefix0 = 'plotData-'
		# prefix1 = scheme name
		if savePath[len(savePath)-1] != '/':
			savePath = savePath + '/'
		
		filename = ''

		if dataToSave:
			# if g_dicMeanData.has_key('filename'):
			filename = prefix0+prefix1
			filename = savePath+filename+'-'+ending+'-cdf'
			
			with open(filename, 'w') as f:
				for cdf in dataToSave:
					# cdf[0]: x point; cdf[1]: y point
					f.write(str(cdf[0])+' '+str(cdf[1])+'\n')

	def saveBoxDataToFile(self, prefix1, ending, savePath, dataToSave):
		prefix0 = 'plotData-'
		# prefix1 = scheme name
		if savePath[len(savePath)-1] != '/':
			savePath = savePath + '/'
		
		filename = ''

		if dataToSave:
			# if g_dicMeanData.has_key('filename'):
			filename = prefix0+prefix1
			filename = savePath+filename+'-'+ending
			
			with open(filename, 'w') as f:
				for key, value in dataToSave.items():
					# cdf[0]: x point; cdf[1]: y point
					for ele in value:
						f.write(str(ele)+' ')
					f.write('\n')