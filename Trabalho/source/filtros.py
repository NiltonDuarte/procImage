# -*- coding: utf-8 -*-

from PIL import Image
from common_functions import *
from math import *

def RGBtoYCbCr(RGB):
	Y = 16 + (0.257*RGB[0] + 0.504*RGB[1] + 0.098*RGB[2]);
	Cb = 128 + (-0.148*RGB[0] - 0.291*RGB[1] + 0.439*RGB[2]);
	Cr = 128 + (0.439*RGB[0] - 0.368*RGB[1] - 0.071*RGB[2]);
	YCbCr = (Y, Cb, Cr)
	return YCbCr

class SimpleFilters:
	def negative(self, x):
		ret = (1.0-(x/255.0)) * 255.0
		return ret

	def cubic(self, x, factor=1, zero=0):
		ret = ((factor*x/255.0)**3 - zero**3) * 255.0
		return ret

	def quadratic(self, x, factor=1, zero=0):
		ret = ((factor*x/255.0)**2 - zero**2) * 255.0
		return ret
		

class Simple3ChannelsFilters:
        def skin(self, RGB):
                #Y = 16 + (0.257*RGB[0] + 0.504*RGB[1] + 0.098*RGB[2]);
		#Cb = 128 + (-0.148*RGB[0] - 0.291*RGB[1] + 0.439*RGB[2]);
		#Cr = 128 + (0.439*RGB[0] - 0.368*RGB[1] - 0.071*RGB[2]);
		YCbCr = RGBtoYCbCr(RGB)
		#if ( (80 <= YCbCr[0]) and (YCbCr[0] <= 230) and (77 <= YCbCr[1]) and (YCbCr[1]  <= 127) and (133 <= YCbCr[2]) and (YCbCr[2] <=173) ):
		if ( (80 <= YCbCr[0]) and (YCbCr[0] <= 230) and (77 <= YCbCr[1]) and (YCbCr[1]  <= 145) and (120 <= YCbCr[2]) and (YCbCr[2] <=173) ):
		    return RGB
		else:
		    return (0,0,0)
		    
	def eyeMapC(self, RGB):
	"""EyeMapC = 1/3 ( (Cb**2)' + ((1-Cr)**2)' + (Cb/Cr)')  todos os termos precisam ser normalizado para [0,1]
		(Cb**2)' = Cb**2/255**2
		((1-Cr)**2)' = (1-Cr)**2/255*2
		(Cb/Cr)' = Cb/(255*Cr)"""
		YCbCr = RGBtoYCbCr(RGB)
		Cb = YCbCr[1]
		Cr = YCbCr[2]
		Cb2n = Cb**2/255**2
		Cr2n = (1-Cr)**2/255*2
		CbDivCr = Cb/(255*Cr)
		EyeMapC = 1/3 ( Cb2n + Cr2n + CbDivCr)  
		return (EyeMapC,EyeMapC,EyeMapC)
		
	def eyeMapC_PrimeiraComponente (self,RGB):
		YCbCr = RGBtoYCbCr(RGB)
		Cb = YCbCr[1]
		Cb2n = Cb**2/255**2
		return (Cb2n,Cb2n,Cb2n)
		
	def eyeMapC_SegundaComponente (self,RGB):
		YCbCr = RGBtoYCbCr(RGB)
		Cr = YCbCr[2]
		Cr2n = (1-Cr)**2/255*2
		return (Cr2n,Cr2n,Cr2n)
		
	def eyeMapC_TerceiraComponente (self,RGB):
		YCbCr = RGBtoYCbCr(RGB)
		Cb = YCbCr[1]
		Cr = YCbCr[2]
		CbDivCr = Cb/(255*Cr)
		return (CbDivCr,CbDivCr,CbDivCr)

class Complex3ChannelsFilters:
	def gaussianRGB(self, img, window=5, dp=2.0):
		width = img.size[0]
		height = img.size[1]
		
		pixels = img.load()
		copyImg = img.copy()
		copyPixels = copyImg.load()
		
		neighbors = window/2
		adjust = 1
		if (window > 3):
			adjust = 0
		for x in range(adjust,width-adjust):
			for y in range(adjust,height-adjust):
				channels = [0,0,0]
				channelR = 0
				channelG = 0
				channelB = 0
				sumChannel = 0
				for i in range(window):
					for j in range(window):
						if (neighbors-i != 0 or neighbors-j != 0):
							d = sqrt(((neighbors-i)**2)+\
								((neighbors-j)**2))
							w = gaussianFunc(dp,d)
							try:
								channelR += pixels[x-(neighbors-i),\
										y-(neighbors-j)][0]*w
								channelG += pixels[x-(neighbors-i),\
										y-(neighbors-j)][1]*w
								channelB += pixels[x-(neighbors-i),\
										y-(neighbors-j)][2]*w
							except IndexError:
								channelR += pixels[x,y][0]*w
								channelG += pixels[x,y][0]*w
								channelB += pixels[x,y][0]*w
							sumChannel+=w
				try:
					channelR = channelR/sumChannel
				except ZeroDivisionError:
					print "Erro: desvio padrão muito pequeno"
					channelR = pixel[x,y][0]
				try:
					channelG = channelG/sumChannel
				except ZeroDivisionError:
					print "Erro: desvio padrão muito pequeno"
					channelG = pixel[x,y][1]
				try:
					channelB = channelB/sumChannel
				except ZeroDivisionError:
					print "Erro: desvio padrão muito pequeno"
					channelB = pixel[x,y][2]
				channels[0] = int(round(channelR))
				channels[1] = int(round(channelG))
				channels[2] = int(round(channelB))
				copyPixels[x,y] = tuple(channels)
		return copyImg	

class ComplexFilters:
	"""
		| i=2 (-1)| i=5 (0)| i=4 (1)|
		| i=1 (-2)| i=0 (0)| i=3 (2)|
		| i=6 (-1)| i=7 (0)| i=8 (1)|
	"""
	def __init__(self):
		self.pixelsDict = {1:-2, 2:-1, 3:2, 4:1, 5:0, 6:-1, 7:0, 8:1}

	def gradient1D(self, pixels):
		ret = pixels[1]-pixels[3]
		return abs(ret)

	def gradient4D(self, pixels):
		grad1 = abs(pixels[1]-pixels[3])
		grad2 = abs(pixels[5]-pixels[7])
		grad3 = abs(pixels[2]-pixels[8])
		grad4 = abs(pixels[6]-pixels[4])

		ret = (grad1 + grad2 + grad3 + grad4)/4.0
		return ret
	
	def gaussian(self, pixels, dp=1.5):
		ret = 0
		sumRet = 0
		for i in range(1, len(pixels)):
			if (i%2==0):
				d = 1
			else:
				d = 1 
			#d = (pixels[i]-pixels[0])/255.0
			w = gaussianFunc(dp, d)
			ret += pixels[i]*w
			sumRet += w
		try:
			ret = ret / sumRet
		except ZeroDivisionError:
			print "Erro: desvio padrão muito pequeno"
			ret = pixels[0]
		return ret

	def median(self, pixels):
		sortPixels = pixels[:]
		sortPixels.sort()
		print sortPixels
		length = len(sortPixels)

		if (length%2 == 0):
			ret = pixels[(length/2) - 1] + pixels[length/2]
			ret = ret/2.0
		else:
			ret = pixels[length/2+1]

		return ret

	def radiationIntensity(self, pixels):
		sumI = 0
		area = 4*pi
		for i in range(1, len(pixels)):
			if ((i+1)%2 == 0):
				area *= 2.0
			else:
				area *= 1.0
			intensity = ((pixels[i]/255.0) / area)*255.0
			sumI += intensity
		ret = pixels[0] + (sumI * 1.0)
		return ret

	def eletricPotentialEnergy(self, pixels):
		"""
			E = kqQ/d
		"""

		k = 9*(10**9)
		d = 1.0
		sumEnergy = 0
		energy = 0

		for i in range(1, len(pixels)):
			if ((i+1)%2 == 0):
				d = sqrt(2)
			else:
				d = 1.0
			localEnergy = (k * (pixels[0]/255.0) * (pixels[i]/255.0))
			energy += (localEnergy/d)
			sumEnergy += 1
		ret = (energy / sumEnergy)
		return ret
	
	def sobel(self, pixels):
		"""
			| i=2 (-1)| i=5 (0)| i=4 (1)|
			| i=1 (-2)| i=0 (0)| i=3 (2)|
			| i=6 (-1)| i=7 (0)| i=8 (1)|
		"""
		self.pixelsDict = {1:-2, 2:-1, 3:2, 4:1, 5:0, 6:-1, 7:0, 8:1}
		x = 0.0
		for i in range(1, len(pixels)):
			#peso * valor
			x += self.pixelsDict[i] * pixels[i]


		"""
			| i=2 (-1)| i=5 (-2)| i=4 (-1)|
			| i=1 (0) | i=0 (0) | i=3 (0) |
			| i=6 (1) | i=7 (2) | i=8 (1) |
		"""
		self.pixelsDict = {1:0, 2:-1, 3:0, 4:-1, 5:-2, 6:1, 7:2, 8:1}
		y = 0.0
		for i in range(1, len(pixels)):
			y += self.pixelsDict[i] * pixels[i]

		ret = sqrt((x**2)+(y**2))
		return ret

	def changeRange(self, pixels, indice):
		"""
			| i=2 (-1)| i=5 (0)| i=4 (1)|
			| i=1 (-2)| i=0 (0)| i=3 (2)|
			| i=6 (-1)| i=7 (0)| i=8 (1)|
		"""
		self.pixelsDict = {1:-2, 2:-1, 3:2, 4:1, 5:0, 6:-1, 7:0, 8:1}
		rangeList = [x for x in range(1, len(pixels)) if x != indice]
		x = 0.0

		for i in rangeList:
			#peso * valor
			x += self.pixelsDict[i] * pixels[i]


		"""
			| i=2 (-1)| i=5 (-2)| i=4 (-1)|
			| i=1 (0) | i=0 (0) | i=3 (0) |
			| i=6 (1) | i=7 (2) | i=8 (1) |
		"""
		self.pixelsDict = {1:0, 2:-1, 3:0, 4:-1, 5:-2, 6:1, 7:2, 8:1}
		y = 0.0
		for i in rangeList:
			y += self.pixelsDict[i] * pixels[i]

		ret = sqrt((x**2)+(y**2))
		return ret
		
	def EyeMapL (self, pixels):
	"""nao faço ideia de como fazer"""
		return
		

