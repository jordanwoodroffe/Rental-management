import unittest

testmodules = [
    'test_client',
    'test_server'
    ]

suite = unittest.TestSuite()

for t in testmodules:
    suite.addTest(unittest.defaultTestLoader.loadTestsFromName(t))

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)