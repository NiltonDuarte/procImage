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
