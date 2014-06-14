# -*- coding: utf-8 -*-
from eyeTracking import *
import cv2
import numpy as np




img = cv2.imread('face3.png',0)

img1 = cv2.imread('face3.png')

eT = eyeTracking((288, 207), (382, 203))

height , width , layers =  img1.shape

cap = cv2.VideoCapture('faceNilton.mov')
ret = True

rightPos = []
leftPos = []

fourcc = cv2.cv.CV_FOURCC(*'XVID')
video = cv2.VideoWriter('./videoNilton.avi', fourcc, 25, (width, height), 1)

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
		cv2.circle(frame, eT.rightEyeCoord, 4,  255, 2, 8, 0 )
		cv2.circle(frame, eT.leftEyeCoord, 4,  255, 2, 8, 0 )
		#print "eT.rightEyeCoord = ", eT.rightEyeCoord
		rightPos.append(eT.rightEyeCoord)
		leftPos.append(eT.leftEyeCoord)
		print rightPos
		print leftPos

		video.write(frame)
		cv2.imshow('frame',frame)
		cv2.imshow('gx',eT.gx)
		cv2.imshow('gy',eT.gy)
		cv2.imshow('threshold',eT.threshold)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
		#a = raw_input("da enter")




cap.release()
cv2.destroyAllWindows()

