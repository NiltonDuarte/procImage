# -*- coding: utf-8 -*-

from harris import *
from image import *
import math

class eyeTracking:
	def __init__(self):
		self.rightEyeCoord = [570.0,264.0]
		self.pRightEyeCoord = [570.0,264.0]
		self.leftEyeCoord = [744.0,261.0]
		self.pLeftEyeCoord = [744.0,261.0]
		self.pTheta = 0
		self.theta = 0

	def setImg(img):
		self.img = MyImg(img)
		self.img.setColorGrayScale()
	
	def harrisGreatestValueCoord(self, coord):
		harrisImg = harrisImg(coord[0], coord[1], self.img.img)
		maxHarris = 0;
		harrisCoord = [0,0]
		for i in range(len(harrisImg)):
			for j in range(len(harrisImg[0])):
				if(harrisImg > maxHarris):
					maxHarris = harrisImg
					harrisCoord = [i,j]
		globalCoord = [coord[0] + harrisCoord[0] - 25, coord[1] + harrisCoord[1] - 25]
		return globalCoord	
	
	def eyeTracking():
		self.pRightEyeCoord = self.eyeCoord
		self.rightEyeCoord = harrisGreatestValueCoord(self.rightEyeCoord)
		self.pLeftEyeCoord = self.leftEyeCoord
		self.leftEyeCoord = harrisGreatestValueCoord(self.leftEyeCoord)
		prevDistance = ((self.pRightEyeCoord[0] - self.pLeftEyeCoord[0])**2 + (self.pRightEyeCoord[1] - self.pLeftEyeCoord[1])**2)**0.5
		distance = ((self.rightEyeCoord[0] - self.leftEyeCoord[0])**2 + (self.rightEyeCoord[1] - self.leftEyeCoord[1])**2)**0.5
		self.pTheta = self.theta
		self.theta = math.acos(distance/prevDistance)
		
