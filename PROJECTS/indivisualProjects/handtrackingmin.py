import cv2
import mediapipe as mp
import time

# Initialize video capture
cap = cv2.VideoCapture(0)

# Initialize MediaPipe Hands solution
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=2,  # Optional: Set maximum number of hands to track
    min_detection_confidence=0.5,  # Adjust as needed
    min_tracking_confidence=0.5  # Adjust as needed
)
mpdraw = mp.solutions.drawing_utils

ptime=0
ctime=0

while True:
    success, img = cap.read()

    # Convert image to RGB format for MediaPipe
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Process the image with MediaPipe Hands
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks :
        for handLlms in results.multi_hand_landmarks :
            for id, lm in enumerate(handLlms.landmark) :
                # print(id, lm)
                h, w,c = img.shape
                cx,cy = int(lm.x*w), int(lm.y*h)
                # print(id, cx , cy)
                if id==0:
                    cv2.circle(img,(cx,cy),25,(0,0,255),-1)
            mpdraw.draw_landmarks(img,handLlms,mp_hands.HAND_CONNECTIONS)




    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime
    cv2.putText(img, 'FPS: {:.2f}'.format(fps), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 255), 4)


    # Display the image
    cv2.imshow('img', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
