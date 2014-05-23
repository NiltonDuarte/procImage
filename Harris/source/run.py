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

winName = "Movement Indicator"
cv2.namedWindow(winName, cv2.CV_WINDOW_AUTOSIZE)


eT = eyeTracking()

while(True):
	cv2.imshow(winName,frame)	

	# Capture frame-by-frame
	ret, frame = cap.read()
	

	# Our operations on the frame come here
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	eT.setImg(gray)
	eT.eyeTracking()

	cv2.circle(gray, eT.leftEyeCoord, 5,  cv2.Scalar(255), 2, 8, 0 )
	cv2.circle(gray, eT.rightEyeCoord, 5,  cv2.Scalar(255), 2, 8, 0 )

	# Display the resulting frame
	cv2.imshow('frame',gray)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
