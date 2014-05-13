# -*- coding: utf-8 -*-

from PIL import Image
from filtros import *
import sys

class MyImg:
	def __init__(self, imgDir):
		self.imgDir = imgDir

		aux = imgDir.split('/')		
		self.outImgName = aux[-1]

		self.img = Image.open(self.imgDir)
                self.isBlackAndWhite = False
		self.width = self.img.size[0]
		self.height = self.img.size[1]

	def getSize(self):
		return self.img.size

	def getMode(self):
		return self.img.mode

	def setOutName(self, imgName):
		self.outImgName = imgName

	def show(self):
		self.img.show()

	def save(self):
		self.img.save("../img/"+self.outImgName)
		
	def setColorGrayScale(self):
	    self.img = self.img.convert("L")
	    self.isBlackAndWhite = True

	def buildPixelsVector(self, window, pixels, x, y):
		neighbors = window/2
		pixelsVector = []
		pixelsVector.append(pixels[x,y])
		for i in range(window):
			for j in range(window):
				if (neighbors-i != 0 or neighbors-j != 0):
					try:
						pixelsVector.append(pixels[x-(neighbors-i),y-(neighbors-j)])
						#print "(",x-neighbors-i,",",y-neighbors-j,") ",
					except IndexError:
						pixelsVector.append(pixelsVector[-1])
		#print ""
		return pixelsVector


	def applySimpleFilter(self, func, extraArgs):
	    
	        if not self.isBlackAndWhite:
			self.setColorBlackAndWhite()
	                print "Image must be set to black and white"
	        
		self.setOutName(func.__name__  +'--'+ self.outImgName)
	
		self.pixels = self.img.load()
		for x in range(self.width):
			for y in range(self.height):
				pixel = self.pixels[x,y]
				self.pixels[x,y] = func(pixel, *extraArgs)

	def applyComplexFilter(self, func, extraArgs, window=3):
	        if not self.isBlackAndWhite:
			self.setColorBlackAndWhite()
	                print "Image must be set to black and white"
	    
		self.setOutName(func.__name__ +'--'+ self.outImgName)
		neighbors = window/2
		self.pixels = self.img.load()
		self.copyImg = self.img.copy()
		self.copyPixels = self.copyImg.load()
		adjust = 1
		if (window > 3):
			adjust = 0
		for x in range(adjust,self.width-adjust):
			for y in range(adjust,self.height-adjust):

				"""
					| i=2 | i=5 | i=4 |
					| i=1 |  0  | i=3 |
					| i=6 | i=7 | i=8 |
				"""

				if (window == 3):
					pixelsVector = [self.pixels[x,y],
							self.pixels[x-1,y], self.pixels[x-1,y-1],
							self.pixels[x+1,y], self.pixels[x+1,y-1],
							self.pixels[x,y-1], self.pixels[x-1,y+1],
							self.pixels[x,y+1], self.pixels[x+1, y+1]]
				else:
					pixelsVector = self.buildPixelsVector(window, self.pixels, x, y)
				
				self.copyPixels[x,y] = func(pixelsVector, *extraArgs)
		self.img = self.copyImg.copy()
		
	def applySimple3ChannelsFilters(self, func, extraArgs):
                self.setOutName(func.__name__  +'--'+ self.outImgName)
	
		self.pixels = self.img.load()
		for x in range(self.width):
			for y in range(self.height):
				pixel = self.pixels[x,y]
				self.pixels[x,y] = func(pixel, *extraArgs)

	def applyComplex3ChannelsFilters(self, func, extraArgs, window=3):
		self.setOutName(func.__name__ +'--'+ self.outImgName)
		self.img = func(self.img, window, *extraArgs).copy()

	def applyComplex3ChannelsFiltersOld(self, func, extraArgs, window=3):	    
		self.setOutName(func.__name__ +'--'+ self.outImgName)
		neighbors = window/2
		self.pixels = self.img.load()
		self.copyImg = self.img.copy()
		self.copyPixels = self.copyImg.load()
		adjust = 1
		if (window > 3):
			adjust = 0
		for x in range(adjust,self.width-adjust):
			for y in range(adjust,self.height-adjust):

				"""
					| i=2 | i=5 | i=4 |
					| i=1 |  0  | i=3 |
					| i=6 | i=7 | i=8 |
				"""

				if (window == 3):
					pixelsVector = [self.pixels[x,y],
							self.pixels[x-1,y], self.pixels[x-1,y-1],
							self.pixels[x+1,y], self.pixels[x+1,y-1],
							self.pixels[x,y-1], self.pixels[x-1,y+1],
							self.pixels[x,y+1], self.pixels[x+1, y+1]]
				else:
					pixelsVector = self.buildPixelsVector(window, self.pixels, x, y)
				
				self.copyPixels[x,y] = func(pixelsVector, *extraArgs)
		self.img = self.copyImg.copy()
			

