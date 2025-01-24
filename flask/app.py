from flask import Flask, render_template, Response
import cv2
import dlib
from imutils import face_utils
import numpy as np
from translation_module import convertMorseToText

app = Flask(__name__)
cap=cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
else:
    print("Camera opened")
# Load dlib face detector and shape predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("E:/Project1/Dot_Dash_Decode/computer_vision/models/shape_predictor_68_face_landmarks.dat")

# Initialize variables for blink detection
EAR_THRESHOLD = 0.25
EAR_DOT_FRAMES = 5
EAR_DASH_FRAMES = 10
PAUSE_FRAMES = 15
PAUSE_DEBOUNCE = 5

counter, pause, debounce_counter, morse_code = 0, 0, 0, ""

# Calculate Euclidean distance between two points
def distance(pa, pb):
    return np.linalg.norm(pa - pb)

# Calculate the Eye Aspect Ratio (EAR)
def eye_aspect_ratio(a, b, c, d, e, f):
    horizontal_dist = distance(b, d) + distance(c, e)
    vertical_dist = distance(a, f)
    return horizontal_dist / (2.0 * vertical_dist)

def process_faces(faces, gray, frame):
    """Process detected faces to calculate EAR and detect blinks."""
    global counter, pause, debounce_counter, morse_code

    for face in faces:
        landmarks = predictor(gray, face)
        landmarks = face_utils.shape_to_np(landmarks)

        # Calculate EAR for both eyes
        ear = calculate_ear(landmarks)

        # Handle blink detection and Morse code
        handle_blink_detection(ear)

        # Display EAR and Morse code on the frame
        cv2.putText(frame, f"EAR: {ear:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f"Morse: {morse_code}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

def calculate_ear(landmarks):
    """Calculate the average Eye Aspect Ratio (EAR) for both eyes."""
    left_eye = landmarks[36:42]
    right_eye = landmarks[42:48]
    left_ear = eye_aspect_ratio(*left_eye)
    right_ear = eye_aspect_ratio(*right_eye)
    return (left_ear + right_ear) / 2.0

def handle_blink_detection(ear):
    """Handle blink detection and Morse code generation."""
    global counter, pause, debounce_counter, morse_code

    if ear < EAR_THRESHOLD:
        handle_eye_closure()
    else:
        handle_eye_opening()

def handle_eye_closure():
    """Handle logic when eyes are closed."""
    global counter, pause, debounce_counter
    counter += 1
    pause = 0
    debounce_counter = 0

def handle_eye_opening():
    """Handle logic when eyes are open."""
    global counter, pause, debounce_counter, morse_code

    if EAR_DOT_FRAMES < counter < EAR_DASH_FRAMES:
        morse_code += "."
        print("Detected: Dot")
    elif counter >= EAR_DASH_FRAMES:
        morse_code += "-"
        print("Detected: Dash")

    # Reset counter
    counter = 0
    pause += 1

    if pause >= PAUSE_FRAMES and debounce_counter == 0:
        morse_code += "/"
        print("Detected: Pause (new word)")
        pause = 0
        debounce_counter = PAUSE_DEBOUNCE

    if "/" in morse_code:
        translate_and_reset_morse_code()

    if debounce_counter > 0:
        debounce_counter -= 1

def translate_and_reset_morse_code():
    """Translate Morse code to text and reset."""
    global morse_code
    translated_text = convertMorseToText(morse_code.strip("/"))
    print("Translated Text:", translated_text)
    morse_code = ""

def generate_video_stream():
    """Generate frames for the video stream."""
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Cannot open webcam.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)
        process_faces(faces, gray, frame)

        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

@app.route('/')
def index():
    """Render the main video page."""
    return render_template('video_page.html')

@app.route('/video_feed')
def video_feed():
    """Video streaming route."""
    return Response(generate_video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)
