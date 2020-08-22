#!/home/chris/anaconda3/bin/python3
import os
import sys
import numpy as np
import math
import time
import argparse
# import statistics

import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

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
		ax.legend(loc='best')
		
		fig.tight_layout()
		plt.show()
		fig.savefig(f'/home/chris/test-d-{labelText}.eps')

	def drawBoxplot(self):
		pass

	def drawCDF(self, x, y, labelText):
		fig, ax = plt.subplots(1, 1, figsize=(7, 4))
		ax.plot(x, y, label=labelText, linewidth=3)
		ax.set_xlim(0.0, 5.7)
		ax.set_ylim(0.0, 1.01)
		ax.set_xlabel('Localization Error (m)', size=15)
		ax.set_ylabel('CDF', size=15)
		
		ax.legend(loc='best', fontsize=15)
		fig.tight_layout()
		plt.show()
		fig.savefig(f'/home/chris/test-d-{labelText}.eps')

	def drawMultiCDF(self, x, y, labelText):
		fig, ax = plt.subplots(1, 1, figsize=(7, 4))

		ax.axhline(0.8, c='black', ls='--', lw=2)
		x80 = []
		for ind in range(len(x)):
			ax.plot(x[ind], y[ind], label=labelText[ind], linewidth=3)
			for ind2 in range(len(x[ind])):
				if round(y[ind][ind2], 2) == 0.80:
					print(round(y[ind][ind2], 2))
					x80.append(x[ind][ind2])
					break
		print(x80)
		for ele in x80:
			ax.axvline(ele, ymax=0.79, c='black', ls='--', lw=2)

		ax.set_xlim(0.0, x[-1][-1])
		ax.set_ylim(0.0, 1.01)
		ax.set_xlabel('Localization Error (m)', size=15)
		ax.set_ylabel('CDF', size=15)

		ax.legend(loc='best', fontsize=15)
		fig.tight_layout()
		plt.show()
		fig.savefig(f'/home/chris/test-d-{labelText}.eps')

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

	def extractCDFData(self, filename):
		x = []
		y = []
		with open(filename, 'r') as f:
			# data=f.readlines()
			data = f.read().splitlines()
			for ele in data:
				eleList = ele.split(' ')
				x.append(float(eleList[0]))
				y.append(float(eleList[1]))
				# print(x, y, errbar)
		return x, y

	def extractMultiCDFData(self, folder):
		x = []
		y = []
		for root, dirs, files in os.walk(folder):
			for file in files:
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
		return x, y

def parseArgments():
	parser = argparse.ArgumentParser(description='Specify data to draw.')
	parser.add_argument('--dataFile', type=str, nargs=1, default=[''], 
						help='data file to draw')
	parser.add_argument('--dataFolder', type=str, nargs=1,
	                    default=[''], help='data folder to collect and draw')
	parser.add_argument('--labelText', type=str, nargs='*',
	                    default=[''], help='label for the data shown in legend')
	return parser

if __name__ == "__main__":
	parser = parseArgments()
	para = parser.parse_args()
	filename = para.dataFile[0]
	labelText = para.labelText
	folder = para.dataFolder[0]
	print(labelText)
	draw = PlotBase()
	# x,y,errbar=draw.extractData(filename)
	# x, y = draw.extractCDFData(filename)
	x, y = draw.extractMultiCDFData(folder)
	# print(x[1], y[1])
	# sys.exit()
	# draw.drawLine(x, y, errbar, labelText)
	draw.drawMultiCDF(x, y, labelText)
	# print(x, y, errbar)
