import cv2
import numpy as np
import time
import os
import handtrackingmodule as htm

fingers=[]
brushthickness=10
eraserthickness=60
folderpath='Untitled design'
my_list=sorted(os.listdir(folderpath))
print(my_list)
overlaylist=[]
for impath in my_list:
    image=cv2.imread(f'{folderpath}/{impath}')
    overlaylist.append(image)
header=overlaylist[1]
print(header.shape)
header=cv2.resize(header,(1280,125))
drawcolor=(255,0,255)
cap=cv2.VideoCapture(0)
print(len(overlaylist))

cap.set(3,1280)
cap.set(4,720)
detector=htm.handDetector(detectionCon=1)
xp,yp=0,0
imgcanvas=np.zeros((720,1280,3),dtype=np.uint8)
while True:
    # 1. import the image
    success, frame=cap.read()
    frame=cv2.flip(frame,1) #along y axis
    frame[0:125, 0:1280] = header  # overlaying the header image


    #2. find the landmarks
    frame=detector.findHands(frame)
    lmlist=detector.findPosition(frame,draw=False)

    if(len(lmlist)!=0):

        # print(lmlist)
        #tip of index and middle finger
        x1,y1 =lmlist[8][1:]
        x2,y2 =lmlist[12][1:]


        #3. checking which fingers are up

        fingers=detector.fingersUp()

        #4. if selection mode - two fingers are up then we have to select
        if fingers[1] and fingers[2]:

            xp, yp = 0, 0
            print("selection mode")
            #checking for the click
            if y1<125:
                if 250<x1<450:
                    header=overlaylist[2]
                    drawcolor=(0,0,255)
                elif 550<x1<750:
                    header=overlaylist[3]
                    drawcolor=(255,26,0)
                elif 800<x1<950:
                    header=overlaylist[4]
                    drawcolor=(255,0,143)
                elif 1050<x1<1200:
                    header=overlaylist[5]
                    drawcolor=(0,0,0)
            cv2.rectangle(frame, (x1, y1 - 20), (x2, y2 + 20), drawcolor, -1)



        #5. if on drawing mode - index finger is up
        if fingers[1] and fingers[2]==False:
            cv2.circle(frame,(x1,y1),15,drawcolor,-1)
            print("drawing mode")
            if xp==0 and yp==0:
                xp,yp=x1,y1
            if drawcolor==(0,0,0):
                cv2.line(frame, (xp, yp), (x1, y1), drawcolor, eraserthickness)
                cv2.line(imgcanvas, (xp, yp), (x1, y1), drawcolor, eraserthickness)
            else:
                cv2.line(frame, (xp, yp), (x1, y1), drawcolor, brushthickness)
                cv2.line(imgcanvas,(xp,yp),(x1,y1),drawcolor,brushthickness)
            xp,yp=x1,y1

    imggray = cv2.cvtColor(imgcanvas, cv2.COLOR_BGR2GRAY)
    _,imginv=cv2.threshold(imggray,50,255,cv2.THRESH_BINARY_INV)
    imginv=cv2.cvtColor(imginv, cv2.COLOR_GRAY2BGR)
    frame=cv2.bitwise_and(frame , imginv)
    frame=cv2.bitwise_or(frame, imgcanvas)


    if success:
        # frame = cv2.addWeighted(frame, 0.5, imgcanvas, 0.5, 0)
        cv2.imshow('frame',frame)
        # cv2.imshow('inv', imginv)
        if cv2.waitKey(1) and fingers==[1,1,0,0,1]:
            break
    else:
        break









