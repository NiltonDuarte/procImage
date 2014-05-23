

class eyeTracking:


	def __init__(self):
		self.eyeCoord = [0,0]
		self.pEyeCoord = [0,0]
	
	def harrisGreatestValueCoord(self)
		img = None;
		harrisImg = harrisImg(eyeCoord[0], eyeCoord[1], img);
		maxHarris = 0;
		harrisCoord = [0,0]
		for i in range(len(harrisImg)):
			for j in range(len(harrisImg[0])):
				if(harrisImg > maxHarris)
					maxHarris = harrisImg
					harrisCoord = [i,j]
		globalCoord = [eyeCoord[0] + harrisCoord[0] - 25, eyeCoord[1] + harrisCoord[1] - 25]
		return globalCoord	
	
	def eyeTracking():
		pEyeCoord = eyeCoord
		eyeCoord = harrisGreatestValueCoord()