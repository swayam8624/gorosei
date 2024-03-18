import cv2
import mediapipe as mp
import time


class handDetector():
    def __init__(self,mode=False,modelComplexity=1,maxHands=2,detectionCon=1,trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.modelComplexity = modelComplexity
        # Initialize MediaPipe Hands solution
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(self.mode,self.maxHands,self.detectionCon,self.trackCon)
        self.mpdraw = mp.solutions.drawing_utils
        self.tipIds=[4,8,12,16,20]

    def findHands(self,img,draw=True):
        # Convert image to RGB format for MediaPipe
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Process the image with MediaPipe Hands
        self.results = self.hands.process(img_rgb)

        if self.results.multi_hand_landmarks:
            for self.handLlms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpdraw.draw_landmarks(img, self.handLlms, self.mp_hands.HAND_CONNECTIONS)
        return img

    def findPosition(self,img,handno=0,draw=True):

        self.lmlist=[]
        if self.results.multi_hand_landmarks:
            myhand=self.results.multi_hand_landmarks[handno]
            for id, lm in enumerate(self.handLlms.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(id, cx , cy)
                self.lmlist.append([id,cx,cy])
                if draw:
                    cv2.circle(img, (cx, cy), 25, (0, 0, 255), -1)
        return self.lmlist

    def fingersUp(self):
        fingers=[]

        #thumb
        if self.lmlist[self.tipIds[0]][1] < self.lmlist[self.tipIds[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        #4 fingers
        for id in range(1,5):
            if self.lmlist[self.tipIds[id]][2] < self.lmlist[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers

def main():
    ptime = 0
    ctime = 0
    cap = cv2.VideoCapture(0)
    detector=handDetector()
    while True:
        success, img = cap.read()
        img=detector.findHands(img,draw=True)
        lmlist=detector.findPosition(img,handno=0,draw=True)
        if len(lmlist) !=0:
            print(lmlist[4])
        ctime = time.time()
        fps = 1 / (ctime - ptime)
        ptime = ctime
        cv2.putText(img, 'FPS: {:.2f}'.format(fps), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 255), 4)

        # Display the image
        cv2.imshow('img', img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__=="__main__":
    main()


# Release resources

