import unittest
from tests.test_website import TestFormValidation, TestWebsite
from tests.test_api import TestApi
from tests.test_app import TestApp

if __name__ == '__main__':
    suite1 = unittest.TestLoader().loadTestsFromTestCase(TestFormValidation)
    suite2 = unittest.TestLoader().loadTestsFromTestCase(TestWebsite)
    suite3 = unittest.TestLoader().loadTestsFromTestCase(TestApi)
    suite4 = unittest.TestLoader().loadTestsFromTestCase(TestApp)
    unittest.TestSuite([suite1, suite2, suite3, suite4]).run()
