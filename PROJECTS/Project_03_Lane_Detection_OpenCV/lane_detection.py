import cv2
import numpy as np

def lanedetection(video_path):
    cap = cv2.VideoCapture(video_path)

    ret, frame = cap.read()

    # Step 1: Select the ROI

    roi = cv2.selectROI("Select Area", frame)

    # Step 2: Crop the area

    frame_copy = frame.copy()
    roi_area = frame_copy[int(roi[1]): int(roi[1] + roi[3]), int(roi[0]): int(roi[0]+roi[2])]

    # Step 3: Perform the Dilation

    kernel = np.ones((3,3), np.uint8)

    dilate = cv2.dilate(roi_area, kernel, iterations=1)

    # Step 4: Convert the Frame into Gray Scale

    gray_scale = cv2.cvtColor(dilate, cv2.COLOR_BGR2GRAY)

    # Step 5: Threshold the Gray Scale Image to detec only White Colors

    threshold = cv2.inRange(gray_scale, 215, 255)

    # Step 6: Applying Bit wise And Operation

    bitwise_and = cv2.bitwise_and(gray_scale, gray_scale, mask = threshold)

    # Step 7: Applying Threshold

    thresh, gray = cv2.threshold(bitwise_and, 150, 255, cv2.THRESH_BINARY)

    # Step 08: Find the Lane Lines using Canny Edge Detector

    canny_edge = cv2.Canny(gray, 0.3*thresh, thresh)

    # Step 09: Apply the Hough Transform

    lane_lines = cv2.HoughLinesP(canny_edge, 2, np.pi/180, 30, minLineLength=15, maxLineGap=40)

    return lane_lines, roi

if __name__ == '__main__':
    video_path = '/Users/swayamsingal/Desktop/Programming/archive/Videos/1.mp4'
    cap = cv2.VideoCapture(video_path)
    lines, r = lanedetection(video_path)
    print(lines)
    print("ROI", r[0])
    while True:
        ret, frame = cap.read()
        if ret:
            if lines is not None:
                for line in lines:
                    x1, y1, x2, y2 = line[0]
                    cv2.line(frame, (x1 + r[0], y1 + r[1]), (x2 + r[0], y2 + r[1]), (0, 255, 0), 3)
            cv2.imshow("Input Video", frame)
            if cv2.waitKey(1) & 0xFF==ord('1'):
                break
        else:
            break