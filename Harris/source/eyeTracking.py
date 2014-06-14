# -*- coding: utf-8 -*-

import harris
#from image import *
import cv2
import math
from functions import *
import numpy as np
from operator import itemgetter


class eyeTracking:
	def __init__(self, leftEyeCoordTuple, rightEyeCoordTuple):
		self.rightEyeCoord = rightEyeCoordTuple
		self.pRightEyeCoord = self.rightEyeCoord
		self.leftEyeCoord = leftEyeCoordTuple
		self.pLeftEyeCoord = self.leftEyeCoord
		self.pTheta = 0
		self.theta = 0
		#self.harrisValue = -1
		self.currImg = None
		self.prevImg = None
		#lista com o valos do harris, e aposicao dele
		self.harrisImg = None
		self.currImgHarrisTop5 = [[0,(0,0)],[0,(0,0)],[0,(0,0)],[0,(0,0)],[0,(0,0)]]
		self.prevImgHarrisTop5 = [[0,(0,0)],[0,(0,0)],[0,(0,0)],[0,(0,0)],[0,(0,0)]]
		self.rightEyePrevImgRegion = None
		self.rightEyeCurrImgRegion = None
		self.leftEyePrevImgRegion = None
		self.leftEyeCurrImgRegion = None
		
		

	def setImg(self, img):
		if self.currImg == None :
			self.currImg = img
		else:
			self.prevImg = self.currImg
			self.currImg = img

	

	"""
	def harrisGreatestValueCoord(self, coord):
		harrisImg = harris.harrisImg(coord[0], coord[1], self.img.img)
		maxHarris = 0;
		harrisCoord = [0,0]
		for i in range(len(harrisImg)):
			for j in range(len(harrisImg[0])):
				if(harrisImg[i][j] > maxHarris):
					maxHarris = harrisImg[i][j]
					#print int(maxHarris)
					harrisCoord = [i,j]
		globalCoord = [coord[0] + harrisCoord[0] - (len(harrisImg)-1)/2, coord[1] + harrisCoord[1] - (len(harrisImg)-1)/2]
		self.harrisValue = maxHarris
		return globalCoord

	def harrisCoordValue(self, coord):
		harrisImg = harris.harrisImg(coord[0], coord[1], self.img.img)
		self.harrisValue = harrisImg[0][0]
		return coord
	
	def harrisNearestValueCoord(self,coord):
		harrisImg = harris.harrisImg(coord[0], coord[1], self.img.img)
		harrisCoord = [0,0]
		smallerValueDistance = 8000
		for i in range(len(harrisImg)):
			for j in range(len(harrisImg[0])):
				#distance pro coord to the point being compared
				coordDistance = ( (i - (len(harrisImg)-1)/2)**2 + (j - (len(harrisImg)-1)/2)**2)**0.5
				#print 	coordDistance,
				value = (1 + coordDistance) * (abs(harrisImg[i][j] - self.harrisValue))
				
				if( value < smallerValueDistance):
					#print "value = ", value
					smallerValueDistance = value
					harrisAuxValue = harrisImg[i][j]
					harrisCoord = [i,j]
		globalCoord = [coord[0] + harrisCoord[0] - (len(harrisImg)-1)/2, coord[1] + harrisCoord[1] - (len(harrisImg)-1)/2]
		#print "value = ", value
		self.harrisValue = harrisAuxValue
		return globalCoord
	
	def harrisCoord(self, coord):
		if self.harrisValue == -1:
			 return self.harrisCoordValue(coord)
		else:
			return self.harrisNearestValueCoord(coord)
			
	
	def minSSD(self, prevRegion, currRegion, coord):
		#tamanho do template em pixels x pixels
		template = 7
		halfTemplate = (template-1)/2
		#pixelInputValue = self.img.img[coord[0]][coord[1]]
		#pixelInputSSD = 0
		minSSD = 999999999
		#minSSDCoord = (0,0)
		regionLen = len(currRegion)

		
		for x in range(halfTemplate,regionLen-halfTemplate):
			for y in range(halfTemplate,regionLen-halfTemplate):
				currSSD = 0
				aux = 0
				for templateX in range(-halfTemplate, halfTemplate+1):
					for templateY in range(-halfTemplate, halfTemplate+1):
						aux += 1

						SD = (currRegion[x+templateX,y+templateY] \
							- prevRegion[(regionLen-1)/2 + templateX,(regionLen-1)/2 + templateY])**2
						#print SD
						currSSD += SD
						#print (regionLen-1)/2 + templateX
						
				if (currSSD < minSSD):
					minSSD = currSSD
					minSSDRegionCoord = (x,y)
					#print minSSD, aux
							
		
		#globalCoord = [coord[0] + harrisCoord[0] - (len(harrisImg)-1)/2, coord[1] + harrisCoord[1] - (len(harrisImg)-1)/2]
		minSSDCoord = (coord[0] + minSSDRegionCoord[0] - (regionLen-1)/2, coord[1] + minSSDRegionCoord[1] - (regionLen-1)/2)

		return minSSDCoord
		
	def maxCC(self, prevRegion, currRegion, coord):
		#tamanho do template em pixels x pixels
		template = 15
		halfTemplate = (template-1)/2
		maxCC = 0
		regionLen = len(currRegion)
		
		for x in range(halfTemplate,regionLen-halfTemplate-1):
			for y in range(halfTemplate,regionLen-halfTemplate-1):
				currCCnum = 0
				currCCdenom = 0
				aux = 0
				for templateX in range(-halfTemplate, halfTemplate+1):
					for templateY in range(-halfTemplate, halfTemplate+1):
						aux += 1
						# CC = G*F / F^2 http://liris.cnrs.fr/Documents/Liris-4190.pdf pg 130
						
						currCCnum += float(prevRegion[(regionLen-1)/2 + templateX,(regionLen-1)/2 + templateY])* \
							float(currRegion[x+templateX,y+templateY])
						currCCdenom +=  (float(prevRegion[(regionLen-1)/2 + templateX,(regionLen-1)/2 + templateY]))**2

				CC = 	currCCnum / (currCCdenom**0.5)
				#print CC	
				if (maxCC < CC):
					maxCC = CC
					maxCCRegionCoord = (x,y)
					#print minSSD, aux
							
		
		#globalCoord = [coord[0] + harrisCoord[0] - (len(harrisImg)-1)/2, coord[1] + harrisCoord[1] - (len(harrisImg)-1)/2]
		maxCCCoord = (coord[0] + maxCCRegionCoord[0] - (regionLen-1)/2, coord[1] + maxCCRegionCoord[1] - (regionLen-1)/2)

		return maxCCCoord
		
	"""
	def harrisTop5ValuesCoord(self, coord, img):
		self.prevImgHarrisTop5 = copy.deepcopy(self.currImgHarrisTop5)
		self.currImgHarrisTop5 = [[0,(0,0)],[0,(0,0)],[0,(0,0)],[0,(0,0)],[0,(0,0)]]
		harrisImg = (harris.harrisImg(coord[0], coord[1], img))
		self.harrisImg = harrisImg
		print self.harrisImg
		for i in range(len(harrisImg)):
			for j in range(len(harrisImg)):
				if(harrisImg[i][j] > self.currImgHarrisTop5[-1][0]):
					self.currImgHarrisTop5[-1][0] = harrisImg[i][j]
					self.currImgHarrisTop5[-1][1] = (coord[0] + i - (len(harrisImg)-1)/2, coord[1] + j - (len(harrisImg)-1)/2)
					self.currImgHarrisTop5.sort(key = itemgetter(0), reverse=True)
					#print self.currImgHarrisTop5
		

	def harrisTracking(self, img ,coord):
		self.harrisTop5ValuesCoord(coord, img)

	

	
	def cvEyeRegion(self,coord):
		
		window = 71
		halfWindow = (window-1)/2
		
		"""
		startY and endY coordinates, followed by the startX and endX 
		If (x1,y1) top left and (x2,y2) bottom right are the two opposite vertices of plate you obtained, then simply use function:

		roi = gray[y1:y2, x1:x2]
		"""
		x1 = coord[0]-halfWindow
		y1 = coord[1]-halfWindow
		x2 = coord[0]+halfWindow+1
		y2 = coord[1]+halfWindow+1
		
		
		
		eye = self.currImg[y1:y2, x1:x2]
		#gaussianEye = cv2.GaussianBlur(eye,(5,5),2);
		return eye


		
						
		

	
	
	def eyeTracking(self):	
		if (True):#self.prevImg != None):
			self.pRightEyeCoord = self.rightEyeCoord
			
			self.rightEyePrevImgRegion = np.copy(self.rightEyeCurrImgRegion)
			self.rightEyeCurrImgRegion = self.cvEyeRegion(self.rightEyeCoord)
			
			self.harrisTracking(self.rightEyeCurrImgRegion.tolist(), self.rightEyeCoord)
			
			"""
			self.rightEyeCoord = self.maxCC(self.rightEyePrevImgRegion, self.rightEyeCurrImgRegion, self.rightEyeCoord)
			print (self.rightEyeCoord[0] - self.pRightEyeCoord[0] , self.rightEyeCoord[1] - self.pRightEyeCoord[1])
			
			self.pLeftEyeCoord = self.leftEyeCoord

			self.leftEyePrevImgRegion = np.copy(self.leftEyeCurrImgRegion)
			self.leftEyeCurrImgRegion = self.cvEyeRegion(self.leftEyeCoord)
			#region = self.coordRegion(self.leftEyeCoord)
			#self.leftEyeCurrImgRegion = gaussianFilter(region)
			
			self.leftEyeCoord = self.minSSD(self.leftEyePrevImgRegion, self.leftEyeCurrImgRegion, self.leftEyeCoord)
			"""
		else: #inicializacao de next img
			#region = self.coordRegion(self.rightEyeCoord)
			self.rightEyeCurrImgRegion = self.cvEyeRegion(self.rightEyeCoord)

			#region = self.coordRegion(self.leftEyeCoord)
			self.leftEyeCurrImgRegion = self.cvEyeRegion(self.leftEyeCoord)	
			
		

	"""
		if (self.img != None):
			self.pRightEyeCoord = self.rightEyeCoord
			self.rightEyeCoord = self.harrisCoord(self.rightEyeCoord)
			self.pLeftEyeCoord = self.leftEyeCoord
			self.leftEyeCoord = self.harrisCoord(self.leftEyeCoord)
	"""

		
