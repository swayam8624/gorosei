import cv2
import os
from cvzone.HandTrackingModule import HandDetector

width,height= 1920,1080
cap = cv2.VideoCapture(0)
cap.set(3,width)
cap.set(4,height)

#get the list of images of ppt
folderpath='gorosei'
pathimages=sorted(os.listdir(folderpath))
print(pathimages)

#variables
imgno=0
heigthsmall,widthsmall=180,320
gesturethreshold=300

#hand detector
detector=HandDetector(detectionCon=0.8,maxHands=1)



while(True):

    #import images
    success,img = cap.read()
    img=cv2.flip(img,1)
    pathfullimage=os.path.join(folderpath,pathimages[imgno])
    imgcurrent=cv2.imread(pathfullimage)

    hands,img=detector.findHands(img)
    cv2.line(img,(0,gesturethreshold),(width,gesturethreshold),(0,255,0),5)
    if hands:
        hand= hands[0]
        fingers=detector.fingersUp(hand)
        cx,cy=hand['center']

        if cx <= gesturethreshold:







    #adding webcam image on slides
    imgsmall=cv2.resize(img,(widthsmall,heigthsmall))
    h,w,ch=imgcurrent.shape
    imgcurrent[0:heigthsmall,w-widthsmall:w] = imgsmall  #basic overlay






    if success:
        cv2.imshow('us :D ',img)
        cv2.imshow("slides",imgcurrent)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break