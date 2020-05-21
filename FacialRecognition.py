"""
FacialRecognition.py

Note - can raise a MemoryError when installing packages onto RPI due to limited cache size/memory.
Solved by using:
    pip --no-cache-dir install <package_name>
"""
from collections import namedtuple
import numpy as np
import cv2  # facilitates face recognition: detects faces, does not recognise face landmarks (i.e. recognition)
import face_recognition  # recognise and encode user faces
import pickle
from abc import ABC, abstractmethod


class AbstractFaceDetector(ABC):
    Match = namedtuple("max_match", "user_id score")  # simple data-structure to house encoding comparison results

    @abstractmethod
    def capture_user(self) -> list:
        """
        Captures a user and encodes face: used for storing in database, or for sending to MP for login/authentication
        Returns:
            a list containing the users login authentication
        """

    @abstractmethod
    def compare_encodings(self, login: list, users: {str: list}):
        """
        Args:
            login: encoded face of user attempting to login
            users: a dictionary of user_ids to their saved encodings
        Returns:
            a string for matched user_id, or None if no match was found
        """


class FaceDetector(AbstractFaceDetector):
    """
    TODO: add requirements for install etc. and check imports
    TODO: add option to check by video upload (no usb camera on rpi) - add some sort of file flag
    """
    __haar_model = 'haarcascade_frontalface_default.xml'
    __min_faces = 5  # minimum required faces for a valid detection - set to 5 for efficiency on RPI

    def __init__(self):
        self.__classifier = cv2.CascadeClassifier(self.__haar_model)
        try:
            test = self.__classifier.load(self.__haar_model)
            if test is False:
                raise ImportError("Unable to load classifier xml. Check file path before proceeding.")
        except ImportError as ie:
            print(ie)

    def capture_user(self, images: [str] = None, min_faces: int = None) -> list:
        min_faces = self.__min_faces if min_faces is None else min_faces
        faces = self.__capture_face(min_faces=min_faces, images=images)
        if faces is not None and len(faces) > 0:
            return self.__encode_face(faces)
        return []  # unable to encode/capture faces

    def compare_encodings(self, login_encs: list, saved_encs: {str: list}) -> AbstractFaceDetector.Match:
        max_match = self.Match(None, 0)
        if len(login_encs) > 0:
            for encoding in login_encs:
                for user_id in saved_encs.keys():
                    user_encs = saved_encs.get(user_id)
                    result = sum(face_recognition.compare_faces(user_encs, encoding))
                    max_match = self.Match(user_id, result) if result > max_match.score else max_match
        return max_match

    def __capture_face(self, min_faces, images: [str] = None):
        """
        Captures a users face from an image or video stream
        TODO: replace/add image upload - filepath to directory with images, load/capture faces until self.__min_faces
        TODO: add validation/exceptions for image upload etc.
        Returns:
            a list of faces capture from images or video-stream
        """

        if images is not None and len(images) < min_faces:
            return None

        video_stream = None
        faces = []
        i = 0
        print(images)

        while len(faces) < min_faces:
            if images is None:
                if video_stream is None:
                    video_stream = cv2.VideoCapture(0)
                _, img = video_stream.read()
            else:
                img = cv2.imread(images[i])
                i += 1

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

            # for (x, y, w, h) in face_objects:
            #     cv2.rectangle(img, pt1=(x, y), pt2=(x + w, y + h), color=(255, 0, 0), thickness=2)
            # cv2.imshow('img', img)
        if video_stream is not None:
            video_stream.release()
        return faces

    @staticmethod
    def __encode_face(faces) -> list:
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
                frames = face_recognition.face_locations(face_img, model='hog')
                face_encodings = face_recognition.face_encodings(face_img, frames)
                if len(face_encodings) > 0:
                    encodings.append(face_encodings[0])
        return encodings


if __name__ == "__main__":
    # capture registration faces
    reg_encs = {}
    detector = FaceDetector()
    # images = ["user_data/face_pics/donald@gmail.com/img1.jpg"]
    images = ["user_data/face_pics/donald@gmail.com/img{}.jpg".format(i) for i in range(1, 6)]
    # images = None
    don = detector.capture_user(images=images)
    temp = pickle.dumps(don)
    reg_encs['don'] = pickle.loads(temp)

    # capture login face & compare with reg
    login = detector.capture_user(images=["user_data/face_pics/donald@gmail.com/img1.jpg"], min_faces=1)
    match = detector.compare_encodings(login, reg_encs)
    print(match)
