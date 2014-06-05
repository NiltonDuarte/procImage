# -*- coding: utf-8 -*-
from eyeTracking import *
import cv2
import functions
import numpy as np


img = cv2.imread('face.png',0)



eT = eyeTracking((290, 190), (430, 185))
"""
print "EyeTrack"
eT.setImg(img)
eT.eyeTracking()

print "Pontos na imagem como marcador"
print "leftEyeCoord = ", eT.leftEyeCoord, "rightEyeCoord = ", eT.rightEyeCoord
rightCoordTuple = (int(eT.rightEyeCoord[0]), int(eT.rightEyeCoord[1]))
leftCoordTuple = (int(eT.leftEyeCoord[0]), int(eT.leftEyeCoord[1]))
cv2.circle(img, rightCoordTuple, 5,  255, 2, 8, 0 )
cv2.circle(img, leftCoordTuple, 5,  255, 2, 8, 0 )


cv2.imshow('image',img)
k = cv2.waitKey(0)
if k == 27:         # wait for ESC key to exit
    cv2.destroyAllWindows()

"""
cap = cv2.VideoCapture('moving.mov')
ret = True

while(cap.isOpened() and ret):
	ret, frame = cap.read()
	if ret:
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		gray = cv2.GaussianBlur(gray,(7,7),2);

		print "EyeTrack"
		eT.setImg(gray)
		eT.eyeTracking()

		print "Pontos na imagem como marcador"
		print "leftEyeCoord = ", eT.leftEyeCoord, "rightEyeCoord = ", eT.rightEyeCoord
		#rightCoordTuple = eT.rightEyeCoord #(int(eT.rightEyeCoord[0]), int(eT.rightEyeCoord[1]))
		#leftCoordTuple = eT.leftEyeCoord #(int(eT.leftEyeCoord[0]), int(eT.leftEyeCoord[1]))
		#cv2.circle(gray, rightCoordTuple, 5,  255, 2, 8, 0 )
		#cv2.circle(gray, leftCoordTuple, 5,  255, 2, 8, 0 )
		for i in range( len(eT.currImgHarrisTop5)):
			cv2.circle(gray, eT.currImgHarrisTop5[i][1], 5,  255, 2, 8, 0 )
			

		#print eT.rightEyeCurrImgRegion
		cv2.imshow('frame',eT.harrisImg)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break


cap.release()
cv2.destroyAllWindows()

