# contains blink detection code
import cv2
import numpy as np
import dlib
from imutils import face_utils
#import time


cap=cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
else:
    print("Camera opened")

detector=dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("E:/Project1/Dot_Dash_Decode/computer_vision/models/shape_predictor_68_face_landmarks.dat")



# initial conditions 

counter=0
pause=0
debounce_counter=0
morse_code=""

# Threshold initialization

EAR_threshold=0.25

# Frames initialization

EAR_dot=5 #frames for a short blink
EAR_dash=15 #frames for a long blink
pause_frames=60 #to detect pause between morse code letters
pause_debounce=10 #to ensure normal opening of eyes is not considered a pause.

# calculation of euclidean distance between the points around the eyes

def distance(pa,pb):
    dist=np.linalg.norm(pa-pb)
    return dist

# calculate EAR (Eye Aspect Ratio)

def eye_aspect_ratio(a,b,c,d,e,f):
    horizontal_dist=distance(b,d)+distance(c,e)
    vertical_dist=distance(a,f)
    ear=horizontal_dist/(2.0*vertical_dist)
    return ear

'''# checking if eye blinked

def blink(ratio):
    if (ratio>0.25):
        return 1
    if (ratio>0.21 and ratio<0.25):
        return 0
    if (ratio<0.21):
        return -1'''
    
status = ""
color = (255, 255, 255)  # Default color (white)
   
while True:
    ret,frame=cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    face_frame=frame.copy()
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    faces=detector(gray)

    for face in faces:
        x1=face.left()
        y1=face.top()
        x2=face.right()
        y2=face.bottom()

        
        cv2.rectangle(face_frame,(x1,y1),(x2,y2),(0,255,0),2)

        landmarks=predictor(gray,face)
        landmarks=face_utils.shape_to_np(landmarks)

        left_blink=eye_aspect_ratio(landmarks[36],landmarks[37],landmarks[38],landmarks[41],landmarks[40],landmarks[39])
        right_blink=eye_aspect_ratio(landmarks[42],landmarks[43],landmarks[44],landmarks[47],landmarks[46],landmarks[45])
        ear=(left_blink+right_blink)/2.0

        #Creating MORSE code

        if(ear<EAR_threshold):
            counter+=1
            pause=0
            debounce_counter=0
        else:
            if EAR_dot<counter<EAR_dash:
                morse_code+="."
                print("Detected:Dot")
            elif counter>EAR_dash:
                morse_code+="-"
                print("Detected:Dash")
            

            # Reset the counter
            counter=0
            pause+=1

            if pause>=pause_frames and debounce_counter==0:
                morse_code+="/"
                print("Detected:pause (new word)")
                pause=0
                debounce_counter=pause_debounce

            if debounce_counter > 0:
                debounce_counter -= 1
        '''if(left_blink==1 and right_blink==1):
            open+=1
            close=0
            if(open>6):
                status="."
                color=(0,0,255)
        elif(left_blink==-1 and right_blink==-1):
            open=0
            close+=1
            if(close>6):
                status="_"
                color=(0,255,0)'''

        cv2.putText(frame,f"EAR:{ear:.2f}",(100,100), cv2.FONT_ITALIC, 1.2, (0,0,255),2)
        cv2.putText(frame,f"Morse:{morse_code}",(50,50),cv2.FONT_HERSHEY_SIMPLEX,1.2,(0,0,255),2)

        for n in range(0,68):
            (x,y)=landmarks[n]
            cv2.circle(face_frame, (x,y), 1, (255,0,0), -1)

    cv2.imshow("Frame",frame)
    cv2.imshow("Result of detector", face_frame)
    key=cv2.waitKey(1)
    if key==27:
        break
cap.release()
cv2.destroyAllWindows()

