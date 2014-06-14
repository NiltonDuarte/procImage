# -*- coding: utf-8 -*-

from math import *
import copy

def gaussianFunc(dp, d):
	gF = (1.0/(sqrt(2.0*pi)*(dp))) * exp(-(d**2)/(2.0*(dp**2)))
	return gF

def gaussianFilter(img, window=5, dp=2.0):
	width = len(img[0])
	height = len(img)
	
	pixels = copy.deepcopy(img)

	copyPixels = copy.deepcopy(img)
	
	neighbors = window/2
	adjust = 1
	if (window > 3):
		adjust = 0
	for x in range(adjust,width-adjust):
		for y in range(adjust,height-adjust):
			channel = 0
			sumChannel = 0
			for i in range(window):
				for j in range(window):
					if (neighbors-i != 0 or neighbors-j != 0):
						d = sqrt(((neighbors-i)**2)+\
							((neighbors-j)**2))
						w = gaussianFunc(dp,d)
						try:
							channel += pixels[y-(neighbors-j)]\
									[x-(neighbors-i)]*w
						except IndexError:
							channel += pixels[y][x]*w
						sumChannel+=w
			try:
				channel = channel/sumChannel
			except ZeroDivisionError:
				print "Erro: desvio padrão muito pequeno"
				channel = pixel[y][x]
			copyPixels[y][x] = channel
	return copyPixels

def sobel(img):

	"""
		| -1| 0| 1|	| -1| -2|-1|
		| -2| 0| 2|	|  0|  0| 0|
		| -1| 0| 1|	|  1|  2| 1|
	"""

	width = len(img[0])
	height = len(img)
	
	pixels = copy.deepcopy(img)

	copyPixelsX = copy.deepcopy(img)

	copyPixelsY = copy.deepcopy(img)
	
	neighbors = 3/2
	for x in range(1,width-1):
		for y in range(1,height-1):
			channelX = 0
			channelY = 0
			for i in range(3):
				for j in range(3):
					if (neighbors-i != 0 or neighbors-j != 0):
						if (neighbors-i) < 0:
							pairX = -1
						else:
							pairX = 1
						if (neighbors-j) < 0:
							pairY = -1
						else:
							pairY = 1

						if (neighbors-i == 0):
							wY = 2
							wX = 0
						elif (neighbors-j == 0):
							wY = 0
							wX = 2
						else:
							wY = 1
							wX = 1
						
						try:
							channelX += pixels[y-(neighbors-j)]\
									[x-(neighbors-i)]*(pairX*wX)
						except IndexError:
							channelX += pixels[y][x]*(pairX*wX)

						try:
							channelY += pixels[y-(neighbors-j)]\
									[x-(neighbors-i)]*(pairY*wY)
						except IndexError:
							channelY += pixels[y][x]*(pairY*wY)
			copyPixelsX[y][x] = abs(channelX)
			copyPixelsY[y][x] = abs(channelY)	
	return copyPixelsX, copyPixelsY

def imgMul(A, B):
	ret = []
	if type(A) is list and type(B) is list:
		for x in range(len(A)):
			ret.append([])
			for y in range(len(A[0])):
				ret[x].append(A[x][y] * B[x][y])
	elif type(A) is list:
		for x in range(len(A)):
			ret.append([])
			for y in range(len(A[0])):
				ret[x].append(A[x][y] * B)
	elif type(B) is list:
		for x in range(len(B)):
			ret.append([])
			for y in range(len(B[0])):
				ret[x].append(B[x][y] * A)
	else:
		ret = A*B

	return ret

def imgSub(A, B):
	ret = []
	for x in range(len(A)):
		ret.append([])
		for y in range(len(A[0])):
			ret[x].append(A[x][y] - B[x][y])
	return ret

def imgSum(A, B):
	ret = []
	for x in range(len(A)):
		ret.append([])
		for y in range(len(A[0])):
			ret[x].append(A[x][y] + B[x][y])
	return ret

def normalize(imgMatrix):
	ret = []
	maximum = 0
	minimum = 0
	for i in range(len(imgMatrix)):
		for j in range(len(imgMatrix[0])):
			if (imgMatrix[i][j] > maximum):
				maximum = imgMatrix[i][j]
			if (imgMatrix[i][j] < minimum):
				minimum = imgMatrix[i][j]
	for i in range(len(imgMatrix)):
		ret.append([])
		for j in range(len(imgMatrix[0])):
			retAux = 255.0*(imgMatrix[i][j]-minimum)
			ret[i].append(retAux/(maximum-minimum))

	return ret
				
