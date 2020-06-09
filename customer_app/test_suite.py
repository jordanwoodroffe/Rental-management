import unittest

testmodules = [
    'test_app',
    'test_utils'
    'test_facial_recognition',
    'test_api'
    'test_website'
    ]

suite = unittest.TestSuite()

for t in testmodules:
    suite.addTest(unittest.defaultTestLoader.loadTestsFromName(t))

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
