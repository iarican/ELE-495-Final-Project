import cv2
import numpy as np

cap = cv2.VideoCapture(0)

prevCircle = None
dist = lambda x1, y1, x2, y2: (x1-x2)**2 + (y1-y2)**2

while True:
    ret, frame = cap.read()
    if ret == False:
        break

    grayScaleFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurredFrame = cv2.GaussianBlur(grayScaleFrame, (17,17), 0)
    #binaryFrame = cv2.threshold(grayScaleFrame, 200, 255, cv2.THRESH_BINARY)
    circles = cv2.HoughCircles(blurredFrame, cv2.HOUGH_GRADIENT, 1.2, 100, param1 = 100, param2 = 30, minRadius = 1, maxRadius = 100)

    if circles is not None:
        circles = np.uint16(np.around(circles))
        chosen = None

        for i in circles[0, :]:
            if chosen is None: chosen = i
            if prevCircle is not None:
                if dist(chosen[0], chosen[1], prevCircle[0], prevCircle[1]) <= dist(i[0], i[1], prevCircle[0], prevCircle[1]):
                    chosen = i

        cv2.circle(frame, (chosen[0], chosen[1]), 1, (255, 255, 255), 2)
        cv2.circle(frame, (chosen[0], chosen[1]), chosen[2], (0,90,255), 2)
        
        prevCircle = chosen
        print('x: %d' %chosen[0])
        print('y: %d\n' %chosen[1])
    cv2.circle(frame, (320,240), 1, (0,0,0), 2)  #kameranın merkezi  

    cv2.imshow("circle", frame)
    #cv2.imshow("threshold", binaryFrame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows() 