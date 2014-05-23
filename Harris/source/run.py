# -*- coding: utf-8 -*-
from eyeTracking import *
import cv2
import functions

cap = cv2.VideoCapture(0)

if cap.isOpened():
	ret, frame = cap.read()
else:
	cap.open(0)
	ret, frame = cap.read()

print "Criando janela"
winName = "Movement Indicator"
cv2.namedWindow(winName, cv2.CV_WINDOW_AUTOSIZE)

print "Mostrando frame"
cv2.imshow(winName,frame)

eT = eyeTracking()

while(True):	

	# Capture frame-by-frame
	ret, frame = cap.read()
	print "Recuperando frame"

	# Our operations on the frame come here
	print "Escala de cinza"
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	print "EyeTrack"
	eT.setImg(gray)
	eT.eyeTracking()

	print "Pontos na imagem como marcador"
	cv2.circle(frame, eT.leftEyeCoord, 5,  255, 2, 8, 0 )
	cv2.circle(frame, eT.rightEyeCoord, 5,  255, 2, 8, 0 )

	# Display the resulting frame
	cv2.imshow(winName,frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
