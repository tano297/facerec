#!/usr/bin/python
import numpy as np
import cv2

#video cap
cap = cv2.VideoCapture(0)

#pretrained cascade filters
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

while(cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()

    if not ret:
      print("No video! Exiting...")
      exit()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #search for faces' bounding boxes
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    #for each one, draw the rectangle and search for eyes
    for (x,y,w,h) in faces:
      #rect for face
      cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
      roi_gray = gray[y:y+h, x:x+w]
      roi_color = frame[y:y+h, x:x+w]
      eyes = eye_cascade.detectMultiScale(roi_gray)
      for (ex,ey,ew,eh) in eyes:
        cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()