import cv2
import mediapipe as mp
import time  # to check framerate
import math  # for distance calculation


# import numpy as np


class handDetector:
    def __init__(self, mode=False, maxHands=1, detectionCon=0.5, trackCon=0.5, model_complexity=1):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.model_complexity = model_complexity

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.model_complexity,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)  # Processes an RGB image and returns the hand landmarks
        # print(self.results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:  # to draw
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)

        return img

    def findPosition(self, img, handNo=0, draw=True):
        xList = []  # pixel x lm  points
        yList = []  # y lm points pixels
        bbox = []  # bounding box for palm
        self.lmList = []  # contains id and pixel of each lm
        if self.results.multi_hand_landmarks:  # if landmarks in results means palm in front of cam
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                # print(id, lm)#landmarks are in decimals
                h, w, _ = img.shape  # convert lm values to pixels img height width
                cx, cy = int(lm.x * w), int(lm.y * h)  # lm x and y
                xList.append(cx)
                yList.append(cy)
                # print(id, cx, cy)
                self.lmList.append([id, cx, cy])
                if draw:  # draw pink dot for all lms
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

            xmin, xmax = min(xList), max(xList)  # extract min and max values from both lists
            ymin, ymax = min(yList), max(yList)
            bbox = xmin, ymin, xmax, ymax

            if draw:
                cv2.rectangle(img, (xmin - 20, ymin - 20), (xmax + 20, ymax + 20),
                              (0, 255, 0), 2)

        return self.lmList, bbox

    def fingersUp(self):
        fingers = []

        # Thumb tip 0 is 4 id 1 means xpixel
        if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]:  # lmlist [id x y]
            fingers.append(1)

        else:
            fingers.append(0)

        # Fingers
        for id in range(1, 5):

            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        # totalFingers = fingers.count(1)

        return fingers

    def findDistance(self, p1, p2, img, draw=True, r=15, t=3):  # p1-8 p2-12 tip ids, r radius ,t thickness
        x1, y1 = self.lmList[p1][1:]  # pixels coordinates
        x2, y2 = self.lmList[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2  # the circle in between the fingers

        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)  # line between fingers
            cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED)  # x1 y1 pixels,index finger circle
            cv2.circle(img, (x2, y2), r, (255, 0, 255), cv2.FILLED)  # middle finger circle
            cv2.circle(img, (cx, cy), r, (0, 0, 255), cv2.FILLED)  # circle in between fingers
        length = math.hypot(x2 - x1, y2 - y1)  # distance formula (hypotenus)

        return length, img, [x1, y1, x2, y2, cx, cy]


def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    while True:
        success, img = cap.read()  # that will give us frame being captured
        img = detector.findHands(img)
        lmList, bbox = detector.findPosition(img)
        #if len(lmList) != 0:
            #print(lmList[4])

        #cTime = time.time()
        #fps = 1 / (cTime - pTime)
        #pTime = cTime

        # to display fps on the screen
        # cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,(255, 0, 255), 3)

        # to run a web cam
        cv2.imshow("Image",
                   cv2.flip(img, 1))  # to display it to us continous while, flip to camera to overcome mirror image
        cv2.waitKey(1)  # 1 millisecond frame capture
    # end to running a webcam


if __name__ == "__main__":
    main()
