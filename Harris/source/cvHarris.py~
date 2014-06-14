import cv2
import math
import numpy as np
from operator import itemgetter


class cvHarris:
	def __init__(self,leftEyeCoordTuple, rightEyeCoordTuple):
		self.rightEyeCoord = rightEyeCoordTuple
		self.pRightEyeCoord = self.rightEyeCoord

		self.rightEyeCurrImgRegion = None
		
		self.currImgHarrisTop10 = [[0,(0,0)],[0,(0,0)],[0,(0,0)],[0,(0,0)],[0,(0,0)],[0,(0,0)],[0,(0,0)],[0,(0,0)],[0,(0,0)],[0,(0,0)]]
		self.currImg = None
		self.harrisImg = None
		
	def setImg(self, img):
		self.currImg = img
		
	def cvEyeRegion(self,coord):
		
		window = 151
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
	
	def harrisTop5ValuesCoord(self, coord):
		#Detector parameters
		blockSize = 2;
		apertureSize = 3;
		k = 0.04;
		self.currImgHarrisTop10 = [[0,(0,0)],[0,(0,0)],[0,(0,0)],[0,(0,0)],[0,(0,0)],[0,(0,0)],[0,(0,0)],[0,(0,0)],[0,(0,0)],[0,(0,0)]]
		harrisImg = cv2.cornerHarris(self.rightEyeCurrImgRegion, blockSize, apertureSize, k) 
		#normalized = cv2.normalize( harrisImg, 0, 255, cv2.NORM_MINMAX, cv2.CV_32FC1 )
    		#scaled = cv2.convertScaleAbs(dst_norm);
		self.harrisImg = harrisImg

		#print self.harrisImg
		for i in range(len(harrisImg)):
			for j in range(len(harrisImg)):
				if(harrisImg[i][j] > self.currImgHarrisTop10[-1][0]):
					self.currImgHarrisTop10[-1][0] = harrisImg[i][j]
					self.currImgHarrisTop10[-1][1] = (coord[0] + i - (len(harrisImg)-1)/2, coord[1] + j - (len(harrisImg)-1)/2)
					self.currImgHarrisTop10.sort(key = itemgetter(0), reverse=True)
					#print self.currImgHarrisTop5

	def eyeTracking(self):
		self.pRightEyeCoord = self.rightEyeCoord
		self.rightEyeCurrImgRegion = self.cvEyeRegion(self.rightEyeCoord)
		self.harrisTop5ValuesCoord(self.rightEyeCoord)
		#self.rightEyeCoord = self.currImgHarrisTop5[1][1]
		
		
		
		
		
