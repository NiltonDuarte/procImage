# -*- coding: utf-8 -*-

from PIL import Image
from filtros import *

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
