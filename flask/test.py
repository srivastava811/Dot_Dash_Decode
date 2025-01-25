from flask import Flask, render_template, Response
import cv2
import numpy as np
import dlib
from imutils import face_utils
from translation_module import convertMorseToText
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)
# Initialize the webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("E:\Project1\Dot_Dash_Decode\computer_vision\models\shape_predictor_68_face_landmarks.dat")

# Initialize variables for the blink detection
counter = 0
pause = 0
debounce_counter = 0
morse_code = ""
current_word = ""
word_pause_frames = 30
EAR_threshold = 0.25
EAR_dot = 5
EAR_dash = 10
pause_frames = 20
pause_debounce = 3

# Function to calculate Euclidean distance
def distance(pa, pb):
    dist = np.linalg.norm(pa - pb)
    return dist

# Function to calculate EAR (Eye Aspect Ratio)
def eye_aspect_ratio(a, b, c, d, e, f):
    horizontal_dist = distance(b, d) + distance(c, e)
    vertical_dist = distance(a, f)
    ear = horizontal_dist / (2.0 * vertical_dist)
    return ear

@app.route('/')
def index():
    return render_template('index.html')

# Video streaming function
def generate_frames():
    global morse_code, current_word, counter, pause, debounce_counter
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        face_frame = frame.copy()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)

        for face in faces:
            x1 = face.left()
            y1 = face.top()
            x2 = face.right()
            y2 = face.bottom()

            cv2.rectangle(face_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            landmarks = predictor(gray, face)
            landmarks = face_utils.shape_to_np(landmarks)

            left_blink = eye_aspect_ratio(landmarks[36], landmarks[37], landmarks[38], landmarks[41], landmarks[40], landmarks[39])
            right_blink = eye_aspect_ratio(landmarks[42], landmarks[43], landmarks[44], landmarks[47], landmarks[46], landmarks[45])
            ear = (left_blink + right_blink) / 2.0

            # Handling Morse code generation based on blink duration
            if ear < EAR_threshold:
                counter += 1
                pause = 0
                debounce_counter = 0
            else:
                if EAR_dot < counter < EAR_dash:
                    morse_code += "."
                elif counter > EAR_dash:
                    morse_code += "-"

                counter = 0
                pause += 1

                if pause >= pause_frames and debounce_counter == 0:
                    if morse_code:
                        char = convertMorseToText(morse_code)
                        current_word += char
                    morse_code = ""
                    debounce_counter = pause_debounce

                if pause >= word_pause_frames:
                    if current_word:
                        current_word += " "
                    pause = 0

            if debounce_counter > 0:
                debounce_counter -= 1

            cv2.putText(frame, f"EAR: {ear:.2f}", (100, 100), cv2.FONT_ITALIC, 1.2, (0, 0, 255), 2)
            cv2.putText(frame, f"Morse: {morse_code}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 2)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        # Emit the morse code and translated text
        socketio.emit('update', {'morse_code': morse_code, 'translated_text': current_word})
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

'''@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/current_word')
def current_word_view():
    return current_word

if __name__ == '__main__':
    app.run(debug=True)'''
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    socketio.run(app, debug=True)
