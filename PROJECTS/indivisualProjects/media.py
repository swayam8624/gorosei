import cv2 as cv
import mediapipe as mp
import pyautogui
import subprocess
import os
# from AppKit import NSWorkspace

# def play_pause():
#     workspace = NSWorkspace.sharedWorkspace()
#     workspace.performAction_forKey_to(`AXPress`, `AXPress`, `playpause`)  # Replace with appropriate accessibility key codes
# def open_spotify():
#     subprocess.call(["open", "/Applications/Apple.app"])
#
# open_spotify()

cap = cv.VideoCapture(0)

hand_detector = mp.solutions.hands.Hands()
drawing_utiles = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()
def increase_volume():
    os.system("osascript -e 'set Volume 2 of application \"System Events\" to (output volume of (get applications whose name is \"System Events\") + 2)'")

def decrease_volume():
    os.system("osascript -e 'set Volume 2 of application \"System Events\" to (output volume of (get applications whose name is \"System Events\") - 2)'")

index_y_l = 0
index_y_r = 0
middle_y_r = 0
middle_y_l = 0
thumb_y_l = 0
thumb_y_r = 0
ring_y_r = 0
ring_x_r = 0

while True:
    success, frame = cap.read()
    print(success)
    frame = cv.flip(frame, 1)  # flip on ya axis (1 is for y)
    # frame = cv.GaussianBlur(frame1, (7,7), 0)          # less blurring the the average but more natural
    frame_height, frame_width, _ = frame.shape
    rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    output = hand_detector.process(rgb)
    hands = output.multi_hand_landmarks
    multi_handedness = output.multi_handedness
    if multi_handedness is not None:
        for hand_landmarks, handedness in zip(hands, multi_handedness):
            classification = handedness.classification[0].label
            # print(classification)
    else:
        pass

    if hands:
        for hand in hands:
            drawing_utiles.draw_landmarks(frame, hand)
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x = int(
                    landmark.x * frame_width)  # will return decimal points we need pixel points so multiply by frame width
                y = int(
                    landmark.y * frame_height)  # will return decimal points we need pixel points so multiply by frame height

                if id == 8 and classification == "Right":
                    cv.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255), thickness=-1)
                    index_x_r = screen_width * 1.01 / frame_width * x
                    index_y_r = screen_height * 1.01 / frame_height * y
                # step 4 is to move our mouse pointer using index finger
                # pyautogui.moveTo(index_x_r,index_y_r)       # we need to adjust the mouse pointer as per screen (we need to multipy the screen factor)

                # if id==8 and classification=="Left" or classification=="None":
                #     continue

                if id == 4 and classification == "Right":
                    cv.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255), thickness=-1)
                    thumb_x_r = screen_width / frame_width * x
                    thumb_y_r = screen_height / frame_height * y
                    if abs(index_y_r - thumb_y_r) < 50:
                        # Example usage
                        # play_pause()
                        # print("Play/Pause toggled")
                        pyautogui.sleep(1)

                if id == 4 and classification == "Left":
                    cv.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255), thickness=-1)
                    thumb_x_l = screen_width / frame_width * x
                    thumb_y_l = screen_height / frame_height * y
                    # if abs(index_y_l-thumb_y_l) < 50:
                    #     continue
                    # print('Play / Pause')
                    # pyautogui.press('playpause')
                    # pyautogui.sleep(1)

                if id == 12 and classification == "Right":
                    cv.circle(img=frame, center=(x, y), radius=10, color=(255, 0, 0), thickness=-1)
                    middle_x_r = screen_width / frame_width * x
                    middle_y_r = screen_height / frame_height * y
                    if abs(middle_y_r - thumb_y_r) < 50:
                        increase_volume()
                        print("Volume increased")

                if id == 12 and classification == "Left":
                    cv.circle(img=frame, center=(x, y), radius=10, color=(255, 0, 0), thickness=-1)
                    middle_x_l = screen_width / frame_width * x
                    middle_y_l = screen_height / frame_height * y
                    if abs(middle_y_l - thumb_y_l) < 50:
                        decrease_volume()
                        print("Volume decreased")

                # if id==20:
                #     cv.circle(img=frame,center=(x,y),radius=10,color=(0,255,0),thickness=-1)
                #     pinky_x=screen_width/frame_width*x
                #     pinky_y=screen_height/frame_height*y
                #     if abs(pinky_y-thumb_y) < 50:
                #         print('Going to Next Track')
                #         pyautogui.press('nexttrack')
                #         pyautogui.sleep(1)

                if id == 16 and classification == "Left":
                    cv.circle(img=frame, center=(x, y), radius=10, color=(255, 0, 0), thickness=-1)
                    ring_x_l = screen_width / frame_width * x
                    ring_y_l = screen_height / frame_height * y
                    if abs(ring_y_l - thumb_y_l) < 50:
                        print("Going to previous Track")
                        pyautogui.press('prevtrack')
                        pyautogui.sleep(1)

                if id == 16 and classification == "Right":
                    cv.circle(img=frame, center=(x, y), radius=10, color=(255, 0, 0), thickness=-1)
                    ring_x_r = screen_width / frame_width * x
                    ring_y_r = screen_height / frame_height * y
                    if abs(ring_y_r - thumb_y_r) < 50:
                        print("Going to Next Track")
                        pyautogui.press('nexttrack')
                        pyautogui.sleep(1)

    cv.imshow('Virtual Media Player', frame)

    if cv.waitKey(15) & 0xFF == ord(
            'q'):  # says if the frame is there for 15 sec or if d is pressed break out of the video
        break

cap.release()  # capture is an instance of the videocapture
cv.destroyAllWindows()