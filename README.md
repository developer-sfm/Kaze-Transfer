# 🗃️ Kaze-Transfer
A gesture based file transfer system that allows users to capture screenshot by "Closing" their hand and transfer it using an  "Open" hand gesture.
No clicks. No cables. Just gestures.

## 📋 Features
- Gesture detection
- Cross-device transfer
- Real-time communication
- Background execution support

## 🎯 Use Case
- Touchless file transfer
- Quick screenshot sharing between devices
- Useful in presentations or hands-free environments

## 🛠️ Tech Stack
- Python
- Flask
- Flask-SocketIO
- OpenCV
- Mediapipe
- PyAutoGUI
- Pygame
- HTML, CSS, JavaScript

## ⚠️ Limitations
- Needs a webcam to work
- Requires a graphical environment (will not work on headless systems)
- Depends on PyAutoGUI for screenshot capture
- The Server(PC) can ONLY capture screenshot
- The client(Web) can ONLY recieve screenshot
- Works locally (not for server deployment)
- Both devices must be on the same network


## 📂 Project Structure
```bash
Kaze-Transfer-main/
├── KazeTransfer.py
├── HandTrack.py      
├── requirements.txt
├── README.md
├── templates/
│   ├── home.html
│   ├── index.html
│   ├── about.html
│   ├── features.html
│   └── updates.html     
└── static/
    ├── css/
    │   ├── start.css
    │   └── style.css
    └── media/
        ├── darkMode.png
        ├── lightMode.png
        ├── click.mp3
        ├── pop.mp3
        ├── shutter.mp3
```


## 🖥️ Setup

**1. Clone Repository**
```bash
git clone https://github.com/developer-sfm/KazeTransfer.git
```


**2. Go Into The Folder**
```bash
cd Kaze-Transfer-main
```


**3. Install Dependencies**
```bash
pip install -r requirements.txt
```


**4. Run The App**
```bash
python KazeTransfer.py
```


**5. Access the web interface on another device**
Open your browser and go to:
```bash
http://{YOUR_IPV4_ADDRESS}:5000
```


## ⚙️ How It Works
- MediaPipe detects hand gestures via OpenCV on the server
- A closed hand gesture triggers screenshot capture
- An open hand gesture triggers transfer to the client
- The client receives and displays the image in real time

## 📌 Note
All video and screenshot data is transferred directly between your devices over your local network. No data is sent to any external server. Not even the Kaze Transfer developer can access your screenshots or camera feed.


## 📄 License
This project is licensed under the MIT License. See the LICENSE file for details.
