from distutils.log import error
import cv2
import numpy as np
import RPi.GPIO as GPIO
import os
counter = 0

def _range(x,in_min,in_max,out_min,out_max):
    return int((x-in_min)*(out_max-out_min)/(in_max-in_min)+out_min)

cap = cv2.VideoCapture(0)

prevCircle = None
dist = lambda x1, y1, x2, y2: (x1-x2)**2 + (y1-y2)**2
GPIO.setmode(GPIO.BOARD)

# Set pins 11 & 12 as outputs, and define as PWM servo1 & servo2
GPIO.setup(11,GPIO.OUT)
servo1 = GPIO.PWM(11,50) # pin 11 for servo1
GPIO.setup(12,GPIO.OUT)
servo2 = GPIO.PWM(12,50) # pin 12 for servo2

# Start PWM running on both servos, value of 0 (pulse off)
servo1.start(0)
servo2.start(0)
fps = 30
t = 1/fps
prevError_x = 0
prevError_y = 0
Ix = 0
kP = 9.8
kI = 0.075
kD = 2
#app =  App("A")

while True:

    #Ball 
    ret, frame = cap.read()
    if ret == False:
        break

    grayScaleFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurredFrame = cv2.GaussianBlur(grayScaleFrame, (17,17), 0)
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

        error_x = (chosen[0] - 320)/9
        error_y = (chosen[1] - 240)/9
        
        Px = kP * error_x
        Py = kP * error_y

        Dx = kD * (error_x - prevError_x) / t
        Dy = kD * (error_y - prevError_y) / t

        Ix = Ix + kI* error_x
        Iy = Ix + kI* error_y 
        
        PID_x = Px + Ix+ Dx
        PID_y = Py + Iy+ Dy

        if PID_x < -198:
            PID_x = -198
        elif PID_x>212:
            PID_x=212

        if PID_y < -198:
            PID_y = -198
        elif PID_y>212:
            PID_y= 212

        prevError_x = error_x
        prevError_y = error_y

        #print('X hata %lf' %error_x)
        #print('Y hata %lf\n' %error_y)
        move_x=_range(PID_x,-198,212,2,12)
        move_y=_range(PID_y,-198,212,2,12)
        #print('move X %lf' %move_x)
        #print('move Y %lf\n' %move_y)
        servo1.ChangeDutyCycle(move_x)
        servo2.ChangeDutyCycle(move_y)
        counter = counter + 1
        #_locPrint(error_x, error_y, counter)
        if counter == 12:
            print('\n\n\n\n     X koordinat=  %.2lf' %error_x)
            print('     Y koordinat=  %.2lf\n' %error_y)
        if counter == 24:
            os.system('clear')
            counter = 0
        #print(counter)

    else:
        servo1.ChangeDutyCycle(7)
        servo2.ChangeDutyCycle(7)
    cv2.circle(frame, (320,240), 1, (0,0,0), 2)  #kameranın merkezi  
    cv2.imshow("circle", frame)
    
    

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows() 
servo1.stop()
servo2.stop()
GPIO.cleanup()
