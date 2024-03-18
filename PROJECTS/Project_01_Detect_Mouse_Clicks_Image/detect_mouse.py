#in  this code code will able to detect mouse clicks and on 4 corner clicks it will give the warp perspective
import cv2
import numpy as np

img=cv2.imread('/Users/swayamsingal/Desktop/Programming/archive/scan.jpg')
img=cv2.resize(img,(0,0),None,fx=0.75,fy=0.75)
circles=np.zeros((4,2),int)  #to store the coordinates for warp
print(circles)
count=0
def mousepoints(event, x, y, flags, param):
    global count
    if event == cv2.EVENT_LBUTTONDOWN:
        circles[count]=x,y
        print(circles[count])
        count+=1
        print(f'mouse click count: {count}')
while(True):
    if count==4:
        width,height=500,500
        pts1=np.float32([circles[0],circles[1],circles[2],circles[3]])
        pts2=np.float32([[0,0],[width,0],[0,height],[width,height]])
        matrix = cv2.getPerspectiveTransform(pts1,pts2)
        imgout=cv2.warpPerspective(img,matrix,(width,height))
        cv2.imshow('warped image',imgout)
    for x in range(0,4):
        cv2.circle(img,(circles[x][0],circles[x][1]),3,(255,0,0),-1)
    cv2.imshow('original', img)
    cv2.setMouseCallback('original', mousepoints)
    if cv2.waitKey(1) & 0xFF== ord('q'):
        break



