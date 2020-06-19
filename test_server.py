import unittest
import server

class TestServer(unittest.TestCase):

    def test_unlockCar(self):
        self.assertTrue(server.unlockCar("_unloCar" + "VSB296" + "_user_" + "jwoodroffe"))

    def test_lockCar(self):
        self.assertTrue(server.lockCar("_unloCar" + "VSB296" + "_user_" + "jwoodroffe"))

if __name__ == '__main__':
    unittest.main()