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
		fig, ax = plt.subplots(1, 1, figsize=(7, 5))
		ax.errorbar(x, y, yerr=errbar, capsize=8, label=labelText,
		            linewidth=3, marker='o', markersize=10)
		ax.set_xticks(ticks=x)
		ax.set_xlabel('Sigma (Gaussian Noise)')
		ax.set_ylabel('Localization Error (m)')
		# ax.set_title('')
		ax.legend(loc='best')
		
		fig.tight_layout()
		plt.show()
		fig.savefig(f'/home/chris/test-d-{labelText}.eps')

	def drawBoxplot(self):
		pass

	def drawCDF(self, x, y, labelText):
		fig, ax = plt.subplots(1, 1, figsize=(7, 5))
		ax.plot(x, y, label=labelText, linewidth=3)
		ax.set_ylim(0.0, 1.01)
		ax.set_xlabel('Localization Error (m)')
		ax.set_ylabel('CDF')
		
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

def parseArgments():
	parser = argparse.ArgumentParser(description='Specify data to draw.')
	parser.add_argument('--dataFile', type=str, nargs=1, help='data file to draw')
	parser.add_argument('--labelText', type=str, nargs=1, help='label for the data shown in legend')
	return parser

if __name__ == "__main__":
	parser = parseArgments()
	para = parser.parse_args()
	filename = para.dataFile[0]
	labelText = para.labelText[0]

	draw = PlotBase()
	# x,y,errbar=draw.extractData(filename)
	x, y = draw.extractCDFData(filename)

	# draw.drawLine(x, y, errbar, labelText)
	draw.drawCDF(x, y, labelText)
	# print(x, y, errbar)
