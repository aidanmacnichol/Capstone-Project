import cv2
import numpy as np
import face_recognition
import serial
import math
import time
from gpiozero import DistanceSensor
# Our imports
from servo_motors import servo_motors
from temp_sens import temp_sens
from LCD import LCDController

# Aspect ratio of camera
height, width = 320, 240

vid = cv2.VideoCapture(0) #Pi is 0
vid.set(3,height)
vid.set(4,width)
assert vid.isOpened()
face_locations = []

# Create a servo Object
motors = servo_motors()
print("init servos done")

# Create temp sens object
temp_sensor = temp_sens()
print("init temp sens done")

# Create LCD object
lcd = LCDController()
print("init lcd done")

# Initialize distance sensor
dist = DistanceSensor(echo=10, trigger=9, max_distance=300)

# Find forehead given eye coordinates
def findForehead(p1, p2):
     x1 = p1[1][0]
     x2 = p2[1][0]
     y1 = p1[1][1]
     y2 = p2[1][1]
     midpoint = [int(((x1 + x2) / 2)), int(((y1 + y2)/2))]
    # midpoint[1] = midpoint[1] - int(math.dist(p1[0], p2[0]) / 2)

     # Draw dot on forehead ***For Testing***
     #cv2.circle(frame, midpoint ,5,(0,0,255), -1)

     return midpoint    

# array for averaging temp
temp_avg = []
temp_4_bool = False

while True:
    ret, frame = vid.read()

    # convert to HSV colorspace
    img = frame[:, :, ::-1]

    # get facial landmarks
    face_landmarks = face_recognition.face_landmarks(img, model='small')
    
    # Give instructions on LCD
    lcd.cursor(0, 0)
    lcd.display_text('Please face')
    lcd.cursor(0, 1)
    lcd.display_text('the sensor!')


    # Make sure a face is in frame
    if len(face_landmarks) > 0:
        # grab inner eye coordinates for both eyes
        landmark_dict = face_landmarks[0]
        left_eye = landmark_dict["left_eye"]
        right_eye = landmark_dict["right_eye"]

        # Add a dot to frame **FOR TESTING***
        # cv2.circle(frame, right_eye[1],2,(0,0,255), -1)
        # cv2.circle(frame, left_eye[1],2,(0,0,255), -1)

        forehead = findForehead(left_eye, right_eye)
        
        # Move Servos
        motors.moveServos(forehead)
        
        # Print temp data to LCD
        lcd.clear_screen() 
    

        dista = round(dist.distance * 100, 1)

        # dont show anything > 100cm away
        if (dista < 100):
            lcd.clear_screen() 
            lcd.cursor(0, 1)
            lcd.display_text('Dist ~ ' + str(round(dista, 1)) + 'cm')
            
            temp, ptat = temp_sensor.readData()
            
            # '''
            # take temp reading when:
            #     1. distance <= 31cm
            #     2. temp > 36 degrees
            #     3. temp < 36 degrees
            # '''
            if(dista <= 31):
                #print(temp)
                lcd.cursor(0, 0)
                lcd.display_text('Hold Still!')
                if(temp[4] > 36):
                    if(temp[4] < 38): 
                        
                        temp_4_bool = True
                        forehead_temp = temp[4]
                        temp_avg.append(forehead_temp)

                        # wait for 5 readings to average
                        if(len(temp_avg) >= 5):
                            forehead_temp_final = np.mean(temp_avg)
                            #round(forehead_temp_final, 2)  
                            lcd.cursor(0, 0)
                            lcd.display_text('Temp ~ ' + str("%.1f" % forehead_temp_final) + 'C')
                            time.sleep(5)
                            temp_avg = []
                            temp_4_bool = False
                            
                if(temp[5] > 36 and temp_4_bool == False): 
                    if(temp[5] < 38 and temp_4_bool == False):
                        forehead_temp = temp[5]
                        temp_avg.append(forehead_temp)
                        print(temp_avg)

                        # wait for 5 readings to average
                        if(len(temp_avg) >= 3):
                            forehead_temp_final = np.mean(temp_avg)
                            #round(forehead_temp_final, 2)  
                            lcd.cursor(0, 0)
                            lcd.display_text('Temp ~ ' + str("%.1f" % forehead_temp_final) + 'C')
                            time.sleep(5)
                            temp_avg = []
                            
            else:
                lcd.cursor(0, 0)
                lcd.display_text('Move closer!')
                


    # show frame ** *FOR TESTING ***
    # cv2.imshow('frame', frame)
    #press q to stop running
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

vid.release()
cv2.destroy()
