# -*- coding: utf-8 -*-

import harris
from image import *
import math
from functions import *

class eyeTracking:
	def __init__(self, leftEyeCoordList, rightEyeCoordList):
		self.rightEyeCoord = rightEyeCoordList
		self.pRightEyeCoord = self.rightEyeCoord
		self.leftEyeCoord = leftEyeCoordList
		self.pLeftEyeCoord = self.leftEyeCoord
		self.pTheta = 0
		self.theta = 0
		self.harrisValue = -1
		self.img = None
		self.nextImg = None

	def setImg(self, img):
		if self.nextImg == None :
			self.nextImg = MyImg(img)
			self.nextImg.setColorGrayScale()
		else:
			self.img = self.nextImg
			self.nextImg = MyImg(img)
			self.nextImg.setColorGrayScale()

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
			
			
	
	def eyeTracking(self):
		self.pRightEyeCoord = self.rightEyeCoord
		self.rightEyeCoord = self.harrisCoord(self.rightEyeCoord)
		self.pLeftEyeCoord = self.leftEyeCoord
		self.leftEyeCoord = self.harrisCoord(self.leftEyeCoord)
		prevDistance = ((self.pRightEyeCoord[0] - self.pLeftEyeCoord[0])**2 + (self.pRightEyeCoord[1] - self.pLeftEyeCoord[1])**2)**0.5
		distance = ((self.rightEyeCoord[0] - self.leftEyeCoord[0])**2 + (self.rightEyeCoord[1] - self.leftEyeCoord[1])**2)**0.5
		self.pTheta = self.theta

		self.theta = math.acos(distance/prevDistance if (distance/prevDistance < 1) else prevDistance/distance)
		
