

class eyeTracking:


	def __init__(self):
		self.rightEyeCoord = [0,0]
		self.pRightEyeCoord = [0,0]
		self.leftEyeCoord = [0,0]
		self.pLeftEyeCoord = [0,0]
	
	def harrisGreatestValueCoord(self, coord)
		img = None;
		harrisImg = harrisImg(coord[0], coord[1], img);
		maxHarris = 0;
		harrisCoord = [0,0]
		for i in range(len(harrisImg)):
			for j in range(len(harrisImg[0])):
				if(harrisImg > maxHarris):
					maxHarris = harrisImg
					harrisCoord = [i,j]
		globalCoord = [eyeCoord[0] + harrisCoord[0] - 25, eyeCoord[1] + harrisCoord[1] - 25]
		return globalCoord	
	
	def eyeTracking():
		pRightEyeCoord = eyeCoord
		rightEyeCoord = harrisGreatestValueCoord(rightEyeCoord)
		pLeftEyeCoord = leftEyeCoord
		leftEyeCoord = harrisGreatestValueCoord(leftEyeCoord)
		prevDistance = ((pRightEyeCoord[0] - pLeftEyeCoord[0])**2 + (pRightEyeCoord[1] - pLeftEyeCoord[1])**2)**0.5