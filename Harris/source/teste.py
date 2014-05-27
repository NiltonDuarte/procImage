# -*- coding: utf-8 -*-
from eyeTracking import *
import cv2
import functions

img = cv2.imread('face.png',0)



eT = eyeTracking([300.0, 170.0], [430.0, 165.0])
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

		print "EyeTrack"
		eT.setImg(gray)
		eT.eyeTracking()

		print "Pontos na imagem como marcador"
		print "leftEyeCoord = ", eT.leftEyeCoord, "rightEyeCoord = ", eT.rightEyeCoord
		rightCoordTuple = (int(eT.rightEyeCoord[0]), int(eT.rightEyeCoord[1]))
		leftCoordTuple = (int(eT.leftEyeCoord[0]), int(eT.leftEyeCoord[1]))
		cv2.circle(gray, rightCoordTuple, 5,  255, 2, 8, 0 )
		cv2.circle(gray, leftCoordTuple, 5,  255, 2, 8, 0 )


		cv2.imshow('frame',gray)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break


cap.release()
cv2.destroyAllWindows()

