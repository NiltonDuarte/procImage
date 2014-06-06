# -*- coding: utf-8 -*-
from eyeTracking import *
import cv2
import numpy as np




img = cv2.imread('face3.png',0)



eT = eyeTracking((287, 166), (397, 170))



cap = cv2.VideoCapture('Face3.mp4')
ret = True

pos = []
#[(397, 170), (392, 170), (386, 170), (382, 170), (377, 170), (373, 171), (365, 170), (361, 170), (356, 171), (351, 171), (347, 173), (341, 173), (337, 175), (333, 176), (330, 177), (326, 177), (323, 178), (321, 179), (318, 179), (317, 179), (317, 179), (318, 179), (319, 180), (324, 177), (324, 182), (328, 182), (333, 183), (337, 183), (344, 184), (351, 185), (358, 186), (364, 187), (372, 187), (380, 187), (387, 187), (395, 187), (406, 162), (416, 187), (419, 162), (430, 187), (433, 162), (443, 187), (445, 162), (454, 187), (458, 188), (465, 186), (473, 187), (482, 187), (490, 185), (497, 185), (504, 185), (511, 184), (517, 185), (524, 184), (530, 184), (536, 185), (542, 185), (548, 186), (553, 186), (558, 184), (563, 185), (566, 185), (568, 185), (569, 185), (570, 185), (571, 185), (571, 185), (569, 185), (567, 186), (561, 185), (557, 185)]


while(cap.isOpened() and ret):
	ret, frame = cap.read()
	#frame = img

	if ret:
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		grayg = cv2.GaussianBlur(gray,(7,7),2);

		print "EyeTrack"
		eT.setImg(grayg)
		eT.eyeTracking()
		
		#print "right eye", eT.rightEyeCoord
		cv2.circle(frame, eT.rightEyeCoord, 3,  255, 2, 8, 0 )
		cv2.circle(frame, eT.leftEyeCoord, 3,  255, 2, 8, 0 )
		#print "eT.rightEyeCoord = ", eT.rightEyeCoord
		pos.append(eT.rightEyeCoord)
		print pos

		cv2.imshow('frame',frame)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
		#a = raw_input("da enter")




cap.release()
cv2.destroyAllWindows()

