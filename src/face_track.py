import cv2
import numpy as np
import face_recognition
import serial
import math
'''
Done by Aidan MacNichol
'''


height, width = 320, 240
# 640 x 480 is image ratio
# no it is not
vid = cv2.VideoCapture(1) #Pi is 1
vid.set(3,height)
vid.set(4,width)
assert vid.isOpened()
face_locations = []


# So I can send data to the Arduino ()
# Windows PC: 'COM4'
# raspberry Pi '/dev/ttyACM0' 
ArduinoSerial = serial.Serial('COM4',9600,timeout=0.1)

# Used to convert x,y coordinates to a string and send to arduino
def convertTuple(tup):
    data = 'X' + str(tup[0]) + 'Y' + str(tup[1])
    return data

# Find forehead given eye coordinates
def findForehead(p1, p2):
     x1 = p1[1][0]
     x2 = p2[1][0]
     y1 = p1[1][1]
     y2 = p2[1][1]
     midpoint = [int(((x1 + x2) / 2)), int(((y1 + y2)/2))]
     midpoint[1] = midpoint[1] - int(math.dist(p1[0], p2[0]) / 2)

     # Draw dot on forehead ***For Testing***
     #cv2.circle(frame, midpoint ,5,(0,0,255), -1)

     return midpoint    




while True:
    ret, frame = vid.read()

    #convert to HSV colorspace
    img = frame[:, :, ::-1]

    face_landmarks = face_recognition.face_landmarks(img, model='small')



    # Make sure a face is in frame
    if len(face_landmarks) > 0:
        # grab inner eye coordinates for both eyes
        landmark_dict = face_landmarks[0]
        left_eye = landmark_dict["left_eye"]
        right_eye = landmark_dict["right_eye"]

        # Add a dot to frame **FOR TESTING***
        #cv2.circle(frame, right_eye[1],2,(0,0,255), -1)
        #cv2.circle(frame, left_eye[1],2,(0,0,255), -1)

        forehead = findForehead(left_eye, right_eye)


        # Format data for arduino 
        center_ard = convertTuple(forehead)

        # Send location to arduino (replace with python implementation)
        ArduinoSerial.write(center_ard.encode('utf-8'))

    # Need to add face_recognition.face_locations() if want to use this
    # cv2.rectangle(frame,(height//2-20,width//2-20), (height//2+20,width//2+20), (255,255,255),1)

    #show the regular feed and the mask
    #cv2.imshow('frame', frame)
    #press q to stop running
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

vid.release()
cv2.destroy()