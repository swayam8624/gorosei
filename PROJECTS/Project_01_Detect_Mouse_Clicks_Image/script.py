import cv2
import numpy as np

image = cv2.imread("../Images/cards2.jpg")
image = cv2.resize(image, (0,0),None, 0.6,0.6)
circles = np.zeros((4,2), int)

print("Empty Matrix", circles)
count = 0

def mousepoints(event, x,y, flags, params):
    global count
    if event == cv2.EVENT_LBUTTONDOWN:
        circles[count] = x,y
        print(f"Mourse Click No: {count}", circles)
        count+=1
        #print(f"Mouse Click No: {count}")

while True:
    if count==4:
        width, height=500,500
        pts1 = np.float32([circles[0], circles[1], circles[2], circles[3]])
        pts2 = np.float32([[0,0], [width, 0], [0, height], [width, height]])
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        imageOutput = cv2.warpPerspective(image, matrix, (width, height))

        cv2.imshow("Final Output Image", imageOutput)
    for x in range(0,4):
        cv2.circle(image, (circles[x][0], circles[x][1]), 3, (0, 255, 244), -1)
    cv2.imshow("Input Image", image)
    cv2.setMouseCallback("Input Image", mousepoints)
    if cv2.waitKey(1) & 0xFF==ord('1'):
        break