# contains blink detection code
import cv2
import numpy as np
import dlib

cap=cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
else:
    print("Camera opened")

detector=dlib.get_frontal_face_detector()
predictor=dlib.shape_predictor("shape_predictor_68__face_landmarks.dat")
