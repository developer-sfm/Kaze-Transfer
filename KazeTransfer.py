import cv2 as cv
import numpy as np
import base64
import pyautogui
import secrets
from pathlib import Path
from flask import Flask, render_template
from flask_socketio import SocketIO
import HandTrack as HandTrack
import importlib
import pygame
import os



# initializing varaibles

psState = ""
pwState = ""

# Flask set-up
app = Flask(__name__)
app.config["SECRET_KEY"] = secrets.token_hex(16)
socketio = SocketIO(app, async_mode="threading")

# defining paths

SCR_PATH = Path(app.root_path) / "static" / "screenshots" / "pic.jpg"
SCR_PATH.parent.mkdir(parents=True, exist_ok=True)


pygame.mixer.init()
SHUTTER_SOUND = Path(app.root_path) / "static" / "media" / "shutter.mp3"
shutterSound = pygame.mixer.Sound(str(SHUTTER_SOUND))




# Making sure even FLASK deleted its cache
@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


@app.route('/')
def home():
    return render_template("home.html")

@app.route("/features")
def features():
    return render_template("features.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/updates")
def updates():
    return render_template("updates.html")

@app.route("/transfer")
def transfer():
    return render_template("index.html")


# Processing FeedBack
@socketio.on("Feedback")
def feedback(feed):
    # print("Function is WORKING!!!")

    FEEDBACK_PATH = Path(app.root_path) / "static" / "feedback.txt"
    FEEDBACK_PATH.touch(exist_ok=True)
    

    rating = feed.get("rating")
    feedText = feed.get("feedB")

    if FEEDBACK_PATH.exists():
        # print("It Exists!")
        with open(FEEDBACK_PATH, "a") as feedbFile:
            feedbFile.write(f'Rating: {rating}/5\nFeedback: "{feedText}"\n')



# Server(PC) side processing

def capture():
    global psState

    # deleting old screenshot if its present still

    if SCR_PATH.exists():
        os.remove(SCR_PATH)


    cap = cv.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Camera Not Found! (In Use With Another App??)")
            break

        try:
            state = HandTrack.pcStatus(frame)
            # cv.imshow("Image", frame)

        except Exception as e:
            importlib.reload(HandTrack)
            # print(f"Mediapipe Error [{e}]")
            continue

        if state != psState:
            if state == "close":
                # print("SERVER: Hand Closed")
                try:
                    pic = pyautogui.screenshot()
                    pic.save(SCR_PATH)
                    

                    # Sending signal for audio to be played
                
                    shutterSound.play()


                except Exception as e:
                    print(f"Cannot Capture/Save screenshot. Probably no GUI environment. [{e}]")
            psState = state


        if cv.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv.destroyAllWindows()


#client(Web) side processing
@socketio.on("clientCam")
def release(data):
    
    global pwState

    if not data or "," not in data:
        return

    try:
        decodedData = data.split(",")[1]
        nparr = np.frombuffer(base64.b64decode(decodedData), np.uint8)
        frame = cv.imdecode(nparr, cv.IMREAD_COLOR)
        # print("Recieved Frames from web")
        
        if frame is None:
            return
        
    except Exception as e:
        print(f"Error Decoding Frame [{e}]")
        return

    try:
        state = HandTrack.webStatus(frame)
        # print("Processed Web Frames")

    except Exception as e:
        importlib.reload(HandTrack)
        # print(f"Mediapipe TimeStamp Error [{e}]")
        return
    

    if state != pwState:
        if state == "open":
            # print("CLIENT: Hand Open")
            if SCR_PATH.exists():
                try:
                    with open(SCR_PATH, "rb") as image:
                        encodedData = base64.b64encode(image.read()).decode("utf-8")
                        # print("Process??..")
                    socketio.emit("encodedImg", {"image": encodedData})
                
                except Exception as e:
                    print(f"Error Reading Image [{e}]")

        pwState = state

if __name__ == "__main__":
    socketio.start_background_task(capture)
    socketio.run(app, host="0.0.0.0", port=5000, debug=False)