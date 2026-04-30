import cv2 as cv
import mediapipe as mp
import math

mp_hands = mp.solutions.hands
pcHands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
webHands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
# mp_draw = mp.solutions.drawing_utils


def status(hands, frame):
    img = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    results = hands.process(img)

    

    if not results.multi_hand_landmarks:
        return None
        
    for handLms in results.multi_hand_landmarks:
        lmList = []
        for id, lm in enumerate(handLms.landmark):
            lmList.append([lm.x, lm.y])
        
        if len(lmList) != 0:
            wrist = lmList[0]
            middleMCP = lmList[9]
            palm = math.dist(wrist, middleMCP)

            fingers = 0
            tips = [8, 12, 16, 20]
            mcpS = [5, 9, 13, 17]
            # I added two "tab" and got for loop inside this loop

            for i in range(4):
                tip = lmList[tips[i]]
                mcp = lmList[mcpS[i]]
                fingerDist = math.dist(tip, mcp)

                if fingerDist > (palm * 0.6):
                    fingers += 1

    return "open" if fingers else "close"


def pcStatus(frame):
    return status(hands=pcHands, frame=frame)

def webStatus(frame):
    return status(hands=webHands, frame=frame)