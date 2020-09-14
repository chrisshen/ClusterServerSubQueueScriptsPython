#!/home/chris/anaconda3/bin/python3
import os
import sys
import numpy as np
import math
import time
import argparse
# import statistics
import pprint

import matplotlib.pyplot as plt
from matplotlib.pyplot import figure


lineType = ['-', '--', ':', (0, (3, 1, 1, 1, 1, 1)), '-.', 'dotted']

# lineC = ['blue', 'red', '']

# fillC = ['C0', 'C1', 'C2']

class PlotBase():
	def drawLine(self, x, y, errbar, labelText):
		# ax = plt.axes()
		fig, ax = plt.subplots(1, 1, figsize=(7, 4))
		ax.errorbar(x, y, yerr=errbar, color='blue', capsize=8, label=labelText,
		            linewidth=3, marker='o', markersize=8)
		ax.set_xticks(ticks=x)
		ax.set_xlabel('Sigma (Gaussian Noise)', size=15)
		ax.set_ylabel('Localization Error (m)', size=15)
		# ax.set_title('')
		ax.legend(loc='best', edgecolor='inherit')
		
		fig.tight_layout()
		plt.show()
		fig.savefig(f'/home/chris/Figures/sline-d-{labelText}.eps')

	def drawMultiLine(self, x, y, errbar, labelText):
		# ax = plt.axes()
		fig, ax = plt.subplots(1, 1, figsize=(7, 4))

		for ind in range(len(x)):
			ax.errorbar(x[ind], y[ind], yerr=errbar[ind], capsize=0, label=labelText[ind], linewidth=2, markersize=8)
		
		ax.set_xlim(0, x[0][-1]+1)
		# ax.set_ylim(0.0, 1.01)
		# ax.set_xticks(ticks=x)
		ax.set_xlabel('Time Step', size=15)
		ax.set_ylabel('Localization Error (m)', size=15)
		# ax.set_title('')
		ax.legend(loc='best', fontsize=15, edgecolor='inherit')
		
		fig.tight_layout()
		plt.show()
		fig.savefig(f'/home/chris/Figures/mline-d-{labelText}.eps')

	def drawMultiLineFill(self, x, y, errbar, labelText):
		# ax = plt.axes()
		fig, ax = plt.subplots(1, 1, figsize=(7, 4))

		for ind in range(len(x)):
			y1=np.array(y[ind])
			errbar1=np.array(errbar[ind])
			ax.fill_between(x[ind], y1+errbar1, y1-errbar1, label=labelText[ind], alpha=0.5)
			ax.plot(x[ind], y[ind], ls='--', linewidth=2, markersize=8, color='gray')			
		
		ax.set_xlim(0, x[0][-1]+1)
		# ax.set_ylim(0.0, 1.01)
		# ax.set_xticks(ticks=x)
		ax.set_xlabel('Time Step', size=15)
		ax.set_ylabel('Localization Error (m)', size=15)
		# ax.set_title('')
		ax.legend(loc='best', fontsize=15, edgecolor='inherit')
		
		fig.tight_layout()
		plt.show()
		fig.savefig(f'/home/chris/Figures/mline-d-{labelText}.eps')

	def drawBoxplot(self, x, y, labelText):
		fig, ax = plt.subplots(1, 1, figsize=(7, 4))
		# ax.set_title('Basic Plot')
		ax.boxplot(y, labels=labelText, showmeans=True)
		maxY=max([ele for g1 in y for ele in g1])

		# ax.set_xlim(0, len(x)+1)
		# ax.set_xticks(ticks=x)
		ax.set_yticks(ticks=range(int(maxY+1)))
		# ax.set_yticks(ticks=np.linspace(0,int(maxY)+1, 3))

		# ax.set_xlabel('Number of APs', size=15)
		# ax.set_xlabel('Sigma (Gaussian Noise)', size=15)
		ax.minorticks_on()
		ax.tick_params(labelsize=15)
		ax.set_xlabel('Scheme', size=15)		
		ax.set_ylabel('Localization Error (m)', size=15)
		# ax.legend(loc='best', fontsize=15)
		fig.tight_layout()
		# plt.grid(b=True, axis='y', c='gray', ls='--', which='both')
		plt.grid(b=True, axis='y', c='gray', ls='--')
		# plt.yticks(range(1,int(y[-1])))
		plt.show()
		fig.savefig(f'/home/chris/Figures/boxplot-d-{labelText}.eps')

	def drawCDF(self, x, y, labelText):
		fig, ax = plt.subplots(1, 1, figsize=(7, 4))
		ax.plot(x, y, label=labelText, linewidth=3)
		ax.set_xlim(0.0, 5.7)
		ax.set_ylim(0.0, 1.01)
		ax.set_xlabel('Localization Error (m)', size=15)
		ax.set_ylabel('Empirical CDF', size=15)
		
		ax.legend(loc='best', fontsize=15, edgecolor='inherit')
		fig.tight_layout()
		plt.show()
		fig.savefig(f'/home/chris/Figures/scdf-{labelText}.eps')

	def drawMultiCDF(self, x, y, labelText):
		fig, ax = plt.subplots(1, 1, figsize=(7, 4))

		ax.axhline(0.8, c='black', ls='--', lw=2)
		x80 = []
		for ind in range(len(x)):
			ax.plot(x[ind], y[ind], 
				label=labelText[ind], 
				linewidth=5, 
				linestyle=lineType[ind])
			for ind2 in range(len(x[ind])):
				if round(y[ind][ind2], 2) == 0.80:
					# print(round(y[ind][ind2], 2))
					x80.append(x[ind][ind2])
					break
		# print(x80)
		for ele in x80:
			ax.axvline(ele, ymax=0.79, c='black', ls='--', lw=2)

		maxX=max([ele for g1 in x for ele in g1])

		ax.set_xlim(-0.01, maxX)
		ax.set_ylim(0.0, 1.01)

		# ax.set_xticks()
		ax.set_yticks(ticks=np.linspace(0,1,11))

		ax.minorticks_on()

		ax.set_xlabel('Localization Error (m)', size=15)
		ax.set_ylabel('Empirical CDF', size=15)
		ax.tick_params(labelsize=15)
		ax.legend(loc='best', fontsize=15, edgecolor='inherit', scatterpoints=5)
		fig.tight_layout()
		plt.show()
		fig.savefig(f'/home/chris/Figures/mcdf-{labelText}.eps')

	def extractData(self, filename):
		x = []
		y = []
		errbar = []
		with open(filename, 'r') as f:
			# data=f.readlines()
			data = f.read().splitlines()
			for ele in data:
				eleList = ele.split(' ')
				x.append(float(eleList[0]))
				y.append(float(eleList[1]))
				errbar.append(float(eleList[2]))
				# print(x, y, errbar)
		return x, y, errbar
	
	def extractMultiData(self, filename):
		x = []
		y = []
		errbar = []
		label=[]
		for root, dirs, files in os.walk(folder):
			for file in files:
				splFile=file.split('-')
				label.append(splFile[-2]+'-'+splFile[-1])
				with open(root+file, 'r') as f:
					# data=f.readlines()
					data = f.read().splitlines()
					xEle = []
					yEle = []
					eEle = []
					for ele in data:
						eleList = ele.split(' ')
						xEle.append(float(eleList[0]))
						yEle.append(float(eleList[1]))
						eEle.append(float(eleList[2]))
					x.append(xEle)
					y.append(yEle)
					errbar.append(eEle)
				# print(x, y, errbar)
		# print(label)
		x, y, errbar,label=self.sortData(x, y, errbar, label)
		# print(x, y, errbar, label)
		return x, y, errbar, label

	def extractCDFData(self, filename):
		x = []
		y = []
		label = []
		with open(filename, 'r') as f:
			# data=f.readlines()
			splFile=filename.split('-')
			label.append(splFile[-2]+'-'+splFile[-1])
			data = f.read().splitlines()
			for ele in data:
				eleList = ele.split(' ')
				x.append(float(eleList[0]))
				y.append(float(eleList[1]))
				# print(x, y, errbar)
		return x, y, label

	def extractMultiCDFData(self, folder):
		x = []
		y = []
		label = []
		errbar = []
		for root, dirs, files in os.walk(folder):
			for file in files:
				splFile=file.split('-')
				# label.append(splFile[-3]+'-'+splFile[-2])
				label.append(splFile[-4])

				with open(root+file, 'r') as f:
					# data=f.readlines()
					data = f.read().splitlines()
					xEle = []
					yEle = []
					for ele in data:
						eleList = ele.split(' ')
						xEle.append(float(eleList[0]))
						yEle.append(float(eleList[1]))
					x.append(xEle)
					y.append(yEle)
						# print(x, y, errbar)
		x, y, errbar, label = self.sortData(x=x, y=y, label=label)
		return x, y, label

	def extractBoxplotData(self, filename):
		x = []
		y = []
		label = []
		errbar = []

		splFile=filename.split('-')
		label.append(splFile[-2]+'-'+splFile[-1])
		with open(filename, 'r') as f:
			# data=f.readlines()
			print(filename)
			data = f.read().splitlines()
			# print(len(data))
			# sys.exit()
			for ele in data:
				eleList = ele.split(' ')
				# print(eleList)
				# x.append(float(eleList[0]))
				yEle = []				
				for point in eleList:
					# print(point)
					if point:
						yEle.append(float(point))
				# errbar.append(float(eleList[2]))
				# print(x, y, errbar)
				y.append(yEle)
		# x, y, errbar, label = self.sortData(y=y, label=label)
		return x, y, label

	def extractMultiBoxplotData(self, folder):
		x = []
		y = []
		label = []
		errbar = []
		for root, dirs, files in os.walk(folder):
			for file in files:
				splFile=file.split('-')
				# label.append(splFile[-2]+'-'+splFile[-1])
				label.append(splFile[-3])
				with open(root+file, 'r') as f:
					# data=f.readlines()
					print(file)
					data = f.read().splitlines()
					# print(len(data))
					# sys.exit()
					for ele in data:
						eleList = ele.split(' ')
						# print(eleList)
						# x.append(float(eleList[0]))
						yEle = []				
						for point in eleList:
							# print(point)
							if point:
								yEle.append(float(point))
						# errbar.append(float(eleList[2]))
						# print(x, y, errbar)
						y.append(yEle)
						# print(eleList)
		x, y, errbar, label = self.sortData(y=y, label=label)
		# print(label, y)
		return x, y, label

	def sortData(self, x=[], y=[], errorbar=[], label=[]):
		# print(label, y, x, errorbar)

		# retX =[]
		# retY =[]
		# label=[]
		# errbar=[]

		# if errorbar and x:

		# labelY=zip(label, x, y, errorbar)
		# sDataWLabel=sorted(labelY)
		# # line
		# label = [ele1 for ele1, ele2, ele3, ele4 in sDataWLabel]
		# retX = [ele2 for ele1, ele2, ele3, ele4 in sDataWLabel]
		# retY = [ele3 for ele1, ele2, ele3, ele4 in sDataWLabel]
		# errbar = [ele4 for ele1, ele2, ele3, ele4 in sDataWLabel]

		# elif x:

		# CDF
		labelY=zip(label, y, x)
		sDataWLabel=sorted(labelY)
		label = [ele1 for ele1, ele2, ele3 in sDataWLabel]
		retY = [ele2 for esle1, ele2, ele3 in sDataWLabel]
		retX = [ele3 for ele1, ele2, ele3 in sDataWLabel]
		errbar = []

		# else:

		# boxplot
		# labelY=zip(label, y)
		# sDataWLabel=sorted(labelY)
		# label = [ele1 for ele1, ele2 in sDataWLabel]
		# retY = [ele2 for ele1, ele2 in sDataWLabel]
		# retX = []
		# errbar = []

		if not retY:
			print("ERROR: empty retY.")
			sys.exit()
		# sDataWLabel=sorted(labelY)
		# print(sDataWLabel)

		return retX, retY, errbar, label

def parseArgments():
	parser = argparse.ArgumentParser(description='Specify data to draw.')
	parser.add_argument('--dataFile', type=str, nargs=1, default=[''], 
						help='data file to draw')
	parser.add_argument('--dataFolder', type=str, nargs=1,
	                    default=[''], help='data folder to collect and draw')
	parser.add_argument('--labelText', type=str, nargs='*',
	                    default=[''], help='label for the data shown in legend')
	parser.add_argument('--type', type=str, nargs='*',
	                    default=['line'], help='data type for drawn, sline, mline, mlinefill, scdf, mcdf, sboxplot, mboxplot')
	return parser

if __name__ == "__main__":
	parser = parseArgments()
	para = parser.parse_args()
	filename = para.dataFile[0]
	labelText = para.labelText
	folder = para.dataFolder[0]
	dataType = para.type[0]

	print(labelText)
	draw = PlotBase()

	if dataType == 'sline':
		x,y,errbar,labelText=draw.extractData(filename)
		draw.drawLine(x, y, errbar, labelText)
	elif dataType == 'mline':
		x, y, errbar, labelText=draw.extractMultiData(folder)
		draw.drawMultiLine(x, y, errbar, labelText)
	elif dataType == 'mlinefill':
		x, y, errbar, labelText=draw.extractMultiData(folder)
		draw.drawMultiLineFill(x, y, errbar, labelText)
	elif dataType == 'scdf':
		x, y, labelText = draw.extractCDFData(filename)
	elif dataType == 'mcdf':
		x, y, labelText = draw.extractMultiCDFData(folder)
		draw.drawMultiCDF(x, y, labelText)
	elif dataType == 'sboxplot':
		x, y, labelText = draw.extractBoxplotData(filename)
		draw.drawBoxplot(x=[], y=y, labelText=labelText)
	elif dataType == 'mboxplot':
		x, y, labelText = draw.extractMultiBoxplotData(folder)
		draw.drawBoxplot(x=[], y=y, labelText=labelText)
	# print(x, y, errbar)
