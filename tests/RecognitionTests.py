import unittest
from FacialRecognition import AbstractFaceDetector, FaceDetector


class RecognitionTests(unittest.TestCase):
    # load test data? should not require db connection to run
    __fr_ref: AbstractFaceDetector = None

    def setUp(self) -> None:
        self.__fr_ref = FaceDetector()

    def test_login(self):
        pass

    def test_register(self):
        pass
