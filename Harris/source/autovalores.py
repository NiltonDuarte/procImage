
import numpy as np 


def eigenvalues (matrix):
#matrix = {A, B}
#		  {B, C}
#lambda_1 = 1/2 (-sqrt(A^2-2 A C+4 B^2+C^2)+A+C)
#lambda_2 = 1/2 (sqrt(A^2-2 A C+4 B^2+C^2)+A+C)
#return [lambda_1, lambda_2]
	A = matrix[0][0]
	B = matrix[0][1]
	C = matrix[1][1]
	lambda_1 = (1/2.0)*(- ((A**2 - 2*A*C + 4*B**2 + C**2)**0.5) + A + C)
	lambda_2 = (1/2.0)*((A**2 - 2*A*C + 4*B**2 + C**2)**0.5 + A + C)
	
	return [lambda_1, lambda_2]
	
def harrisValue (x2g_derivative ,y2g_derivative, xyg_derivative) :
	# A = x2g_derivative  B = xyg_derivative  C = y2g_derivative
	# M = [[A, B] , [B, C]]
	# value = det(M) - a * trace(M)^2
	# det(M) = A*C - B^2 = x2y2 - xy2
	# trace(M) = A + C = x2g_derivative + y2g_derivative
	a = 0.06
	x2y2 = imgMul(x2g_derivative, y2g_derivative)
	xy2 = imgMul(xyg_derivative, xyg_derivative)
	detM = imgSub(x2y2, xy2)
	traceM = imgSumx2g_derivative, y2g_derivative)
	traceM2 = imgMul(traceM, traceM)
	value = imgSub(detM , imgMul(a, traceM2))
	return value
	
def harrisImagesDerivatives (gray_image):
	#partial derivatives
	x_derivative , y_derivative = sobel(gray_image)
	
	#autocorrelation matrix values
	x2_derivative = imgMul(x_derivative, x_derivative)
	y2_derivative = imgMul(y_derivative, y_derivative)
	xy_derivative = imgMul(x_derivative, y_derivative)
	
	#gaussian of the autocorrelation matrix values
	x2g_derivative = gaussianFilter(x2_derivative,7)
	y2g_derivative = gaussianFilter(y2_derivative,7)
	xyg_derivative = gaussianFilter(xy_derivative,7
	return x2g_derivative, y2g_derivative, xyg_derivative
	
	
def coodRegion(coordX, coordY, inputImg):
	#takes a region 50x50 pixels centered in coord
	window = 51
	half_window = window-1/2.0
	pixels = inputImg.load()
	region = [[0]*50]*50
	for i in range(window):
		for j in range(window):
			region[i][j] = pixels[i - half_window, j - half_window]
	
	return region
	
def harrisImg(coordX, coordY, inputImg):
	region = coodRegion(coordX, coordY, inputImg)
	x2g_derivative, y2g_derivative, xyg_derivative = harrisImagesDerivatives(region)
	harrisImg = harrisValue (x2g_derivative ,y2g_derivative, xyg_derivative)
	return harrisImg
	
	