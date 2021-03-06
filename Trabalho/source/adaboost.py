# -*- coding: utf-8 -*-

from math import *
import copy

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
		
		return abs(dark-light)
		
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
		
		return abs(dark-light)
		
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
		return abs(dark - light)
	
		
class WeakClassifier:
    def __init__(self, set):
		"""@set expects something like a list of tuples [(x,y)]
			x expects features
			y expects 1 or 0 like classification"""
        self.trainingSet = set
		
	def train(self, feature):
		positiveN = 0
		positive = 0
		
		negative = 0
		negativeN = 0
		
		for x in range(len(self.trainingSet)):
			if self.trainingSet[x][1] > 0:
				positiveN += 1
				positive += self.trainingSet[x][0][feature]
			else:
				negativeN += 1
				negative += self.trainingSet[x][0][feature]
		
		self.threshold = 0.5*((negative/negativeN) + (positive/positiveN))
		self.parity = (negative/negativeN) - (positive/positiveN)
		self.parity = copysign(1,self.parity)
		
	def predict(self, x):
		"""@x expects features"""
		if not self.parity or not self.threshold:
			train()
		if (self.parity*x) < (self.parity*self.threshold):
			return 1
		else:
			return -1
    

class AdaBoost():
	"""k - false negative cost k times more than false positives"""
    def __init__(self, P, N, k=2):
		self.k = k
		self.trainingSet = []
		self.d = []
		self.weakClassifier = []
		self.featuresSet=[]
		self.alpha = []
		self.threshold = 0
		
		setTrainingSet(P, N)
		
	def setTrainingSet(self, P, N):
		self.P = P
		self.N = N
		
		for i in range(len(self.P)):
			pair = (self.P[i], 1)
			self.trainingSet.append(pair)
			
		for i in range(len(self.N)):
			pair = (self.N[i], -1)
			self.trainingSet.append(pair) 
		
		self.featuresSet = copy.deepcopy(self.trainingSet)
			
	def setWeights(self):
		for i in range(len(self.trainingSet)):
			di = exp(self.trainingSet[i][1]*log(sqrt(self.k)))
			di = di/len(self.trainingSet)
			self.d.append(di)
			
	def train(self, T):
		setWeights()
		
		for t in range(T):
			epsT = None
			classifierT = None
			featureT = None
			Zt = 0
			e = []
		
			#Normalização dos pesos
			sumD = 0
			for i in range(len(self.d)):
				sumD += self.d[i]
			for i in range(len(self.d)):
				self.d[i] = self.d[i]/sumD
			
			#Obtendo features
			for x in range(len(self.trainingSet)):
				features = []
				haarFeatures = HaarFeatures(self.trainingSet[x][0])
				
				features.append(haarFeatures.edgeFeature())
				features.append(haarFeatures.edgeFeature(self.w-1, self.h/2))
				features.append(haarFeatures.lineFeature())
				features.append(haarFeatures.lineFeature(self.w-1, self.w-1, self.h/3, self.h*2/3)
				features.append(haarFeatures.diagonalFeature())
				
				self.featuresSet[x][0] = copy.deepcopy(features)
			
			#Treinando classificadores fracos pra cada feature
			for feature in range(5):
				currentClassifier = WeakClassifier(self.featuresSet)
				currentClassifier.train(feature)
				eps = 0
				
				for x in range(len(self.featuresSet)):
					h = currentClassifier.predict(self.featuresSet[x][0][feature])
					eps += self.d[x]*abs(h-self.featuresSet[x][1])
					
				#Selecionando classificador de menor erro
				if not epsT:
					epsT = eps
					classifierT = currentClassifier
					featureT = feature
				elif epsT and eps < epsT:
					epsT = eps
					classifierT = currentClassifier
					featureT = feature
			self.weakClassifier.append(classifierT)	
			
			#Atualizando os pesos
			alphaT = 0.5*log((1-epsT)/epsT)
			self.threshold += alphaT
			self.alpha.append(alphaT)
			for i in range(len(self.trainingSet)):
				h = classifierT.predict(self.featuresSet[i][0][featureT])
				self.d[i] = self.d[i]*exp(-alphaT*self.trainingSet[i][1]*h)
		
		self.threshold = self.threshold*0.5
	
	def predict(self, X):
		img = 0
		features = []
		haarFeatures = HaarFeatures(X)
				
		features.append(haarFeatures.edgeFeature())
		features.append(haarFeatures.edgeFeature(self.w-1, self.h/2))
		features.append(haarFeatures.lineFeature())
		features.append(haarFeatures.lineFeature(self.w-1, self.w-1, self.h/3, self.h*2/3)
		features.append(haarFeatures.diagonalFeature())
		
		
		for i in range(len(self.weakClassifier)):
			h = 0
			for feature in features:
				h += self.weakClassifier[i].predict(features[feature])
			img += self.alpha[i]*h	
			
		if img >= self.threshold:
			return 1
		else:
			return 0
