import sys
import os
from collections import namedtuple

import numpy as np
import cv2  # facilitates face recognition: detects faces, does not recognise face landmarks (i.e. recognition)
import face_recognition  # recognise and encode user faces
from abc import ABC, abstractmethod


class AbstractFaceDetector(ABC):
    @abstractmethod
    def register_user(self, user_id: str) -> bool:
        """
        Capture a users face and save under their id for login on AP.
        Args:
            user_id - a users id, will be associated with captured face encoding
        Returns:
            a boolean value indicating if a user was successfully captured
        """

    @abstractmethod
    def login_user(self):
        """
        Authenticate user by comparing captured encoding to saved encodings.
        Args:

        Returns:
            a boolean value indicating whether a successful scan occurred.
        """


class FaceDetector(AbstractFaceDetector):
    """
    TODO: add requirements for install etc. and check imports
    TODO: add option to check by video upload (no usb camera on rpi) - add some sort of file flag
    """

    __encodings = {}  # temp (store in cloud), hold encodings matched to a face/user id
    __haar_model = 'haarcascade_frontalface_default.xml'

    def __init__(self):
        self.__classifier = cv2.CascadeClassifier(self.__haar_model)
        try:
            test = self.__classifier.load(self.__haar_model)
            if test is False:
                raise ImportError("Unable to load xml. Check file path.")
        except ImportError as ie:
            print(ie)

    def register_user(self, user_id: str) -> bool:
        faces = self.__capture_face()
        if len(faces) > 0:
            encodings = self.__encode_face(faces)
            if len(encodings) > 0:
                self.__encodings[user_id] = encodings
                return True
        return False

    def login_user(self):
        Match = namedtuple("max_match", "id score")
        faces = self.__capture_face()
        if len(faces) > 0:
            max_match = Match(None, 0)
            encodings = self.__encode_face(faces)
            for encoding in encodings:
                for user_id in self.__encodings.keys():
                    user_encodings = self.__encodings.get(user_id)
                    result = sum(face_recognition.compare_faces(user_encodings, encoding))
                    max_match = Match(user_id, result) if result > max_match.score else max_match
            print(max_match)

    def __capture_face(self):
        video_stream = cv2.VideoCapture(0)
        faces = []

        while True:
            _, img = video_stream.read()

            img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            face_objects = self.__classifier.detectMultiScale(img_grey, scaleFactor=1.2, minNeighbors=5)
            if len(face_objects) > 1:
                print("one at a time!")
            elif len(face_objects) <= 0:
                print("no faces found :(")
            else:
                print("found ya")
                for x, y, w, h in face_objects:
                    faces.append(img[y: y + h, x: x + w])

            for (x, y, w, h) in face_objects:
                cv2.rectangle(img, pt1=(x, y), pt2=(x + w, y + h), color=(255, 0, 0), thickness=2)
            cv2.imshow('img', img)

            k = cv2.waitKey(30) & 0xff
            if k == 27:
                break

        video_stream.release()
        return faces

    def __encode_face(self, faces) -> list:
        """
        encode faces
        Args:
            faces: list of faces captured by camera/from video to encode
        """
        encodings = []
        for face in faces:
            if np.shape(face) == ():
                continue
            else:
                face_img = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
                frames = face_recognition.face_locations(face_img, model='cnn')
                face_encodings = face_recognition.face_encodings(face_img, frames)
                if len(face_encodings) > 0:
                    encodings.append(face_encodings[0])
        return encodings

    def get_encoding(self, user_id: str):
        return self.__encodings.get(user_id)


if __name__ == "__main__":
    detector = FaceDetector()
    if not detector.register_user(user_id="temp-user"):
        print("unable to read face :(")
    else:
        detector.login_user()
