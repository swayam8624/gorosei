import cv2 as cv
import mediapipe as mp
import pyautogui

cap = cv.VideoCapture(0)

hand_detector = mp.solutions.hands.Hands()
drawing_utiles = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()
index_y = 0

while True:
    success, frame1 = cap.read()
    frame1 = cv.flip(frame1, 1)  # flip on ya axis (1 is for y)
    frame = cv.GaussianBlur(frame1, (5, 5), 0)  # less blurring the the average but more natural
    frame_height, frame_width, _ = frame.shape
    rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    output = hand_detector.process(rgb)
    hands = output.multi_hand_landmarks

    if hands:
        for hand in hands:
            drawing_utiles.draw_landmarks(frame, hand)
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x = int(
                    landmark.x * frame_width)  # will return decimal points we need pixel points so multiply by frame width
                y = int(
                    landmark.y * frame_height)  # will return decimal points we need pixel points so multiply by frame height

                if id == 8:
                    cv.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255), thickness=-1)
                    index_x = screen_width * 1.01 / frame_width * x
                    index_y = screen_height * 1.01 / frame_height * y
                    # step 4 is to move our mouse pointer using index finger
                    pyautogui.moveTo(index_x,
                                     index_y)  # we need to adjust the mouse pointer as per screen (we need to multipy the screen factor)

                if id == 4:
                    cv.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255), thickness=-1)
                    thumb_x = screen_width / frame_width * x
                    thumb_y = screen_height / frame_height * y
                    print('Outside ', index_y - thumb_y)
                    if abs(index_y - thumb_y) < 50:
                        print('Click')
                        pyautogui.click()
                        pyautogui.sleep(1)

                if id == 20:
                    cv.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 0), thickness=-1)
                    pinky_x = screen_width / frame_width * x
                    pinky_y = screen_height / frame_height * y
                    print('Outside ', pinky_y - thumb_y)
                    if abs(pinky_y - thumb_y) < 50:
                        print('Screenshot')
                        counter = 0
                        pyautogui.screenshot(r"C:\Users\Hp\OneDrive\Desktop\OpenCV\screentshot.png")
                        pyautogui.sleep(0.5)

                if id == 16:
                    cv.circle(img=frame, center=(x, y), radius=10, color=(255, 0, 0), thickness=-1)
                    ring_x = screen_width / frame_width * x
                    ring_y = screen_height / frame_height * y
                    if abs(ring_y - thumb_y) < 50:
                        pyautogui.press('volumedown')

                if id == 12:
                    cv.circle(img=frame, center=(x, y), radius=10, color=(255, 0, 0), thickness=-1)
                    middle_x = screen_width / frame_width * x
                    middle_y = screen_height / frame_height * y
                    if abs(middle_y - thumb_y) < 50:
                        pyautogui.press('volumeup')

    cv.imshow('Virtual Mouse', frame)

    if cv.waitKey(15) & 0xFF == ord('q'):  # says if the frame is there for 20 sec or if d is pressed break out of the video
        break

cap.release()  # capture is an instance of the videocapture
cv.destroyAllWindows()