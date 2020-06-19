import unittest
from datetime import datetime
import employee_app.client as client

class TestClient(unittest.TestCase):

    
    def test_qr_code(self): ## Runs the qr login, if login correct and users desired function performs correct, will pass.

        self.assertTrue(client.qrlogin())

    def test_bluetooth(self): ## Runs the bluetooth login, if login correct and users desired function performs correct, will pass.

        self.assertTrue(client.bluelogin())

    def test_scan(self): ## Runs a bluetooth device scan, if it finds a device, will pass.

        self.assertTrue(client.scan())

if __name__ == '__main__':
    unittest.main()