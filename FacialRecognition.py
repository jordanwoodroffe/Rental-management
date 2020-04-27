import sys
import os
import numpy
import cv2  # quit if failed to import

face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
test = face_classifier.load('haarcascade_frontalface_default.xml')
print(test)
video_stream = cv2.VideoCapture(0)

while True:
    _, img = video_stream.read()

    img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    face_objects = face_classifier.detectMultiScale(img_grey, 1.1, 4)

    for (x, y, w, h) in face_objects:
        cv2.rectangle(img, pt1=(x, y), pt2=(x + w, y + h), color=(255, 0, 0), thickness=2)
    cv2.imshow('img', img)

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

video_stream.release()  # release VideoCapture object (finished using)
