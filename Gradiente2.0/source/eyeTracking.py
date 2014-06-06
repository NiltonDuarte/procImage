# -*- coding: utf-8 -*-


import cv2
import math
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
		self.gradient = None
		self.window = 25
		self.halfWindow = (self.window-1)/2
		
		

	def setImg(self, img):
		if self.currImg == None :
			self.currImg = img
		else:
			self.prevImg = self.currImg
			self.currImg = img

	
	
	def cvEyeRegion(self,coord):
		
		window = 61
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


		
	def gradientCenter(self, coord):

		# white to black, gradiente > 0 
		mx1 = np.array([[1, 0, -1]])
		# black to white, gradiente > 0 
		mx2 = np.array([[-1, 0, 1]])
		
		# white to black, gradiente > 0
		my1 = np.array([[1, 0, -1]]).T
		# black to white, gradiente > 0 
		my2 = np.array([[-1, 0, 1]]).T
		

		gx1 = cv2.filter2D(self.currImg, -1, mx1)
		gx2 = cv2.filter2D(self.currImg, -1, mx2)
		gx = gx2 + gx1
		gy1 = cv2.filter2D(self.currImg, -1, my1)
		gy2 = cv2.filter2D(self.currImg, -1, my2)
		gy = gy1 + gy2	
		gygx = gy + gx
		dummy, img = cv2.threshold(gygx, 20, 255, cv2.THRESH_BINARY)
		self.gradient = img
		
		halfWindow = self.halfWindow
		
		cisVal = np.ndarray(shape=(self.window,self.window), dtype=float)

		#TRATAR ERRO DE RANGE
		for jg in range(coord[0] - halfWindow, coord[0]+ halfWindow+1):
			for ig in range(coord[1] - halfWindow, coord[1]+ halfWindow+1):
				if img[ig,jg] > 0:
					for j in range(coord[0] - halfWindow, coord[0]+ halfWindow+1):
						for i in range(coord[1] - halfWindow, coord[1]+ halfWindow+1):
							if img[i,j] == 0:
								ci = (j,i)

								normaDisti = ((jg - j)**2 + (ig - i)**2 )**0.5 
								disti = ((jg - j)/normaDisti , (ig - i)/normaDisti)

								gxi = int(gx2[ig,jg]) - int(gx1[ig, jg]) 
								gyi = int(gy2[ig,jg]) - int(gy1[ig, jg]) 
								gi = (gxi, gyi)
								disti_dot_gi = (gi[0]*disti[0] + gi[1]*disti[1])
				
								cisVal[j,i] += max(0.0, disti_dot_gi)**2


		aux = np.argmax(cisVal , axis =0)
		aux2 = aux[np.argmax(aux , axis =0)
		ci = (aux[aux2] , aux2)
		
		
		print "ci = ", ci
		return 	ci
			
				
				
		

	
	
	def eyeTracking(self):	
		if (True):#self.prevImg != None):
			self.pRightEyeCoord = self.rightEyeCoord
			
			#self.rightEyePrevImgRegion = np.copy(self.rightEyeCurrImgRegion)
			#self.rightEyeCurrImgRegion = self.cvEyeRegion(self.rightEyeCoord)
			
			self.rightEyeCoord = self.gradientCenter(self.rightEyeCoord)
			self.leftEyeCoord = self.gradientCenter(self.leftEyeCoord)
			
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

		