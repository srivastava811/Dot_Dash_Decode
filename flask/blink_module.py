from flask import Flask, render_template, Response
import cv2
import dlib
from imutils import face_utils
import numpy as np

app = Flask(__name__)

# Load dlib face detector and shape predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("E:\Project1\Dot_Dash_Decode\computer_vision\models\shape_predictor_68_face_landmarks.dat")

# Initialize variables for blink detection
EAR_THRESHOLD = 0.25
EAR_DOT_FRAMES = 5
EAR_DASH_FRAMES = 10
PAUSE_FRAMES = 15

counter, pause, morse_code = 0, 0, ""

def eye_aspect_ratio(eye):
    """Calculate the Eye Aspect Ratio (EAR)."""
    A = np.linalg.norm(eye[1] - eye[5])
    B = np.linalg.norm(eye[2] - eye[4])
    C = np.linalg.norm(eye[0] - eye[3])
    return (A + B) / (2.0 * C)

def generate_video_stream():
    """Stream video with blink detection and Morse code processing."""
    global counter, pause, morse_code
    cap = cv2.VideoCapture(0)

    while True:
        frame = capture_frame(cap)
        if frame is None:
            break

        process_frame(frame)

        # Encode and stream the frame
        yield encode_frame_for_streaming(frame)

def capture_frame(cap):
    """Capture a frame from the video stream."""
    ret, frame = cap.read()
    return frame if ret else None

def process_frame(frame):
    """Process the frame for blink detection and Morse code."""
    global counter, pause, morse_code
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    for face in faces:
        landmarks = get_landmarks(gray, face)
        ear = calculate_ear(landmarks)
        update_blink_and_morse(ear)
        display_feedback(frame, ear, morse_code)

def get_landmarks(gray, face):
    """Get facial landmarks for a detected face."""
    landmarks = predictor(gray, face)
    return face_utils.shape_to_np(landmarks)

def calculate_ear(landmarks):
    """Calculate the Eye Aspect Ratio (EAR) for both eyes."""
    left_eye = landmarks[36:42]
    right_eye = landmarks[42:48]
    return (eye_aspect_ratio(left_eye) + eye_aspect_ratio(right_eye)) / 2.0

from translation_module import convertMorseToText

def update_blink_and_morse(ear):
    """Update blink detection and Morse code logic."""
    global counter, pause, morse_code

    if ear < EAR_THRESHOLD:
        counter += 1
        pause = 0
    else:
        add_to_morse_code(counter)
        counter = 0
        pause += 1
        if pause >= PAUSE_FRAMES:
            morse_code += " / "
            pause = 0

            # Translate Morse code to text when a pause is detected
            translated_text = convertMorseToText(morse_code.strip())
            print(f"Translated Text: {translated_text}")  # Debug output or display


def add_to_morse_code(counter):
    """Add dots or dashes to Morse code based on the counter."""
    global morse_code
    if EAR_DOT_FRAMES <= counter < EAR_DASH_FRAMES:
        morse_code += "."
    elif counter >= EAR_DASH_FRAMES:
        morse_code += "-"

def display_feedback(frame, ear, morse_code):
    """Display EAR and Morse code on the frame."""
    cv2.putText(frame, f"EAR: {ear:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(frame, f"Morse: {morse_code}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

def encode_frame_for_streaming(frame):
    """Encode the frame for streaming."""
    _, buffer = cv2.imencode('.jpg', frame)
    return (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

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

def convert_morse_to_text(morse_code):
    """Convert Morse code to readable text."""
    morse_dict = {
        '.-': 'a', '-...': 'b', '-.-.': 'c', '-..': 'd',
        '.': 'e', '..-.': 'f', '--.': 'g', '....': 'h',
        '..': 'i', '.---': 'j', '-.-': 'k', '.-..': 'l',
        '--': 'm', '-.': 'n', '---': 'o', '.--.': 'p',
        '--.-': 'q', '.-.': 'r', '...': 's', '-': 't',
        '..-': 'u', '...-': 'v', '.--': 'w', '-..-': 'x',
        '-.--': 'y', '--..': 'z', '/': ' '
    }

    words = morse_code.strip().split(' / ')
    return ' '.join(''.join(morse_dict.get(char, '?') for char in word.split()) for word in words)
