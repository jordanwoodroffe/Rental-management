import unittest
from facial_recognition import AbstractFaceDetector, FaceDetector
import pickle
from os import path


class TestFacialRecognition(unittest.TestCase):
    # load test data? should not require db connection to run
    __fr_ref: AbstractFaceDetector = None

    def setUp(self) -> None:
        self.__fr_ref = FaceDetector()

    def test_capture(self):
        images = ["user_data/face_pics/kevmason/img8.jpg", "user_data/face_pics/kevmason/img9.jpg", "user_data/face_pics/kevmason/img2.jpg",\
                   "user_data/face_pics/kevmason/img10.jpg", "user_data/face_pics/kevmason/img11.jpg", "user_data/face_pics/kevmason/img5.jpg",\
                   "user_data/face_pics/kevmason/img6.jpg",]
        detector = FaceDetector()
        encoding = detector.capture_user(images, min_faces=5)
        self.assertIsNotNone(encoding)

    def test_compare(self):

        images = ["user_data/face_pics/kevmason/img4.jpg", "user_data/face_pics/kevmason/img5.jpg","user_data/face_pics/kevmason/img6.jpg",\
                  "user_data/face_pics/kevmason/img7.jpg","user_data/face_pics/kevmason/img9.jpg"]          
        images2 = ["user_data/face_pics/kevmason/img8.jpg", "user_data/face_pics/kevmason/img9.jpg", "user_data/face_pics/kevmason/img2.jpg",\
                   "user_data/face_pics/kevmason/img10.jpg", "user_data/face_pics/kevmason/img11.jpg", "user_data/face_pics/kevmason/img5.jpg",\
                   "user_data/face_pics/kevmason/img6.jpg",]
        detector = FaceDetector()
        encoding = detector.capture_user(images, min_faces=1)
        encoding2 = {}
        encoding2['kev'] = detector.capture_user(images2, min_faces=5)
        data1 = pickle.dumps(encoding)
        data2 = pickle.dumps(encoding2)
        encoding_list1 = pickle.loads(data1)
        encoding_list2 = pickle.loads(data2)
        self.assertGreater(FaceDetector.compare_encodings(FaceDetector, encoding_list1, encoding_list2).score, 3)


if __name__ == '__main__':
    unittest.main()
