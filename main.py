import time

import cv2
import mediapipe as mp

WEBCAM_INDEX = 0

webcam = cv2.VideoCapture(WEBCAM_INDEX)

while(True):
    success, img = webcam.read()

    cv2.imshow("Webcam", img)

    cv2.waitKey(1)