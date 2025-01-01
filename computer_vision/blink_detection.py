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

# initial conditions 

open=0
closed=0

# calculation of euclidean distance between the points around the eyes

def distance(pa,pb):
    dist=np.linalg.norm(pa,pb)
    return dist

# calculate EAR (Eye Aspect Ratio)

def eye_aspect_ratio(a,b,c,d,e,f):
    horizontal_dist=distance(b,d)+distance(c,e)
    vertical_dist=distance(a,f)
    ear=horizontal_dist/(2.0*vertical_dist)