# -*- coding: utf-8 -*-

import math

class IntegralImg:
	def __init__(self, img):
		self.i = img
		self.h = len(self.i)
		self.w = len(self.i[0])
		self.ii = []
		
	def cumulativeRow(self, x, y):
		if y < 0:
			return 0
		else:
			return cumulativeRow(x,y-1)+self.i[y][x]
	
	def calculateII(self, x, y):
		if x < 0:
			return 0
		else:
			return calculateII(x-1,y)+cumulativeRow(x,y)
			
	def totalIntegralImg(self):
		for y in range(self.h):
			for x in range(self.w):
				self.ii.append(calculateII(x,y))
				
	def getII(self, x ,y):
		return self.ii[y][x]
			
class HaarFeatures:
	"""Dark - light"""
	def __init__(self, img):
		self.i = img
		self.h = len(self.i)
		self.w = len(self.i[0])
		self.integralImg = IntegralImg(img)
		self.integralImg.totalIntegralImg()
		
	def edgeFeature(self, edge=None):
		"""	@edge divides image in two different regions"""
		
		if not edge:
			x = self.w/2
			y = self.h-1
		
		x,y = edge[1]
		light = self.integralImg.getII(x,y)
		
		x,y = self.h-1, self.w-1
		dark = self.integralImg.getII(x,y) - light
		
		return dark-light
		
	def lineFeature(self, edge1=None, edge2=None):
		"""	@edge1 and @edge2 limits dark part of feature"""
		
		if not edge1:
			x0 = self.w/3
			x1 = self.w*2/3
			y0 = self.h-1
			y1 = y0
		
		x0,y0 = edge1[1]
		x1,y1 = edge2[1]
		
		light1 = self.integralImg.getII(x0,y0)
		
		dark = self.integralImg.getII(x1,y1)
		dark -= light1
		
		x,y = len(self.i)-1, len(self.i[0])-1
		light2 = self.integralImg.getII(x,y)
		light2 -= light1 + dark
		
		light = light1 + light2
		
		return dark-light
		
	def diagonalFeature(self):
		x = self.w/2
		y = self.h/2
		light1 = self.integralImg.getII(x,y)
		
		x = self.w-1
		dark1 = self.integralImg.getII(x,y)
		dark1 -= light1
		
		x = self.w/2
		y = self.h-1
		dark2 = self.integralImg.getII(x,y)
		dark2 -= light1
		
		x = self.w-1
		light = self.integralImg.getII(x,y)
		light -= dark1 + dark2
		
		dark = dark1 + dark2
		return dark - light
	
		
class WeakClassifier:
    def __init__(self, set):
	"""@set expects something like a list of tuples [(x,y)]
		x expects features
		y expects 1 or 0 like classification"""
        self.trainingSet = set
		
	def train(self):
		positiveN = 0
		positive = 0
		
		negative = 0
		negativeN = 0
		
		for x in range(len(self.trainingSet)):
			if self.trainingSet[x][1] > 0:
				positiveN += 1
				positive += self.trainingSet[x][0]
			else:
				negativeN += 1
				negative += self.trainingSet[x][0]
		
		self.threshold = 0.5*((negative/negativeN) + (positive/positiveN))
		self.parity = (negative/negativeN) - (positive/positiveN)
		self.parity = math.copysign(1,self.parity)
		
	def classify(self, x):
		"""@x expects features"""
		if not self.parity or not self.threshold:
			train()
		if (self.parity*x) < (self.parity*self.threshold):
			return 1
		else:
			return 0
    

class AdaBoost(Classifier):
    def __init__(self):
        pass
            
