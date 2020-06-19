import unittest
import employee_app.server as server

class TestServer(unittest.TestCase):

    def test_unlockCar(self):
        self.assertTrue(server.unlockCar("Message from Client:b'_unloCarVSB296_user_jwoodroffe'"))

    def test_lockCar(self):
        self.assertTrue(server.lockCar("Message from Client:b'_lockedCarVSB296_user_jwoodroffe'"))

if __name__ == '__main__':
    unittest.main()