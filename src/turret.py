import cv2
import numpy as np
import face_recognition
import serial
import time


height, width = 320, 240
# 640 x 480 is image ratio
# no it is not
vid = cv2.VideoCapture(0)
vid.set(3,height)
vid.set(4,width)
assert vid.isOpened()
face_locations = []

if not vid:
  print("Failed Video Capture!!!")
  sys.exit(1)

#So I can send data to the Arduino
ArduinoSerial = serial.Serial('/dev/ttyACM0',9600,timeout=0.1)
#used to convert x,y coordinates to a string and send to arduino
def convertTuple(tup):
    data = 'X' + str(tup[0]) + 'Y' + str(tup[1])
    return data
while True:
    ret, frame = vid.read()
    #convert to HSV colorspace
    img = frame[:, :, ::-1]
    face_locations = face_recognition.face_locations(img)

    for top, right, bottom, left in face_locations:
        cv2.rectangle(frame, (left, top), (right, bottom), (0,0,255), 2)
        center = (int((left + right) / 2), int(top + bottom)/2)
        #put a dot in the middle of the rectangle
        cv2.circle(frame, (int((left + right) /2), int((top + bottom) /2)), 5, (0,0,255), -1)
        center_ard = convertTuple(center)
        ArduinoSerial.write(center_ard.encode('utf-8'))
    #cv2.rectangle(frame,(320//2-20,240//2-20), (320//2+20,320//2+20), (255,255,255),1)
    cv2.rectangle(frame,(height//2-20,width//2-20), (height//2+20,width//2+20), (255,255,255),1)

    #show the regular feed and the mask
    #cv2.imshow('frame', frame)
    #press q to stop running
    #if cv2.waitKey(1) & 0xFF == ord('q'):
       # break

vid.release()
cv2.destroy()