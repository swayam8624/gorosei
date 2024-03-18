import cv2
import os
from cvzone.HandTrackingModule import HandDetector
import pyautogui
import numpy as np

width,height= 1920,1080
cap = cv2.VideoCapture(0)
cap.set(3,width)
cap.set(4,height)
#get the list of images of ppt
folderpath='/Users/swayamsingal/Desktop/Programming/gorosei/PROJECTS/indivisualProjects/gorosei_resources'
pathimages=sorted(os.listdir(folderpath))
print(pathimages)
#variables
imgno=1
heigthsmall,widthsmall=180,320
gesturethreshold=600
annotations=[[]]
annotation_no=-1
annotationstart=False
#hand detector
detector=HandDetector(detectionCon=0.8,maxHands=1)
while(True):
    #import images
    success,img = cap.read()
    img=cv2.flip(img,1)
    pathfullimage=os.path.join(folderpath,pathimages[imgno])
    imgcurrent=cv2.imread(pathfullimage)
    print(imgno)
    hands,img=detector.findHands(img)
    cv2.line(img,(0,gesturethreshold),(width,gesturethreshold),(0,255,0),5)
    if hands:
        hand= hands[0]
        fingers=detector.fingersUp(hand)
        cx,cy=hand['center']
        lmlist=hand['lmList']
        indexfinger=lmlist[8][0],lmlist[8][1]
        xVal=int(np.interp(lmlist[8][0],[width//2,w],[0,width]))
        yVal = int(np.interp(lmlist[8][1], [150,height-150], [0, height]))
        indexfinger=xVal,yVal
        if cx >= gesturethreshold:
            #gesture 1 - left
            if fingers==[1,0,0,0,0]:
                print("left")
                pyautogui.sleep(0.42)
                annotations = [[]]
                annotation_no = -1
                annotationstart = False
                if imgno>1:
                    imgno=imgno-1
            # gesture 2 - right
            if fingers == [0, 0, 0, 0,1]:
                print("right")
                pyautogui.sleep(0.42)
                annotations = [[]]
                annotation_no = -1
                annotationstart = False
                if imgno<len(pathimages)-1:
                    imgno = imgno +1
            #gesture 3 - show pointers
            if fingers==[0,1,1,0,0]:
                cv2.circle(imgcurrent,indexfinger,12,(0,0,255),-1)
            #gesture 4: draw
            if fingers==[0,1,0,0,0]:
                if annotationstart==False:
                    annotationstart=True
                    annotation_no+=1
                    annotations.append([])
                cv2.circle(imgcurrent, indexfinger, 12, (0, 0, 255), -1)
                annotations[annotation_no].append(indexfinger)
            else:
                annotationstart=False
        for i in range(len(annotations)):
            for j in range(len(annotations[i])):
                if j!=0:
                    cv2.line(imgcurrent, annotations[i][j-1],annotations[i][j],(0,0,200),12)
    #adding webcam image on slides
    imgsmall=cv2.resize(img,(widthsmall,heigthsmall))
    h,w,_=imgcurrent.shape
    imgcurrent[0:heigthsmall,w-widthsmall:w] = imgsmall  #basic overlay
    if success:
        cv2.imshow('us :D ',img)
        cv2.imshow("slides",imgcurrent)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break