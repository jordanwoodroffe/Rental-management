import unittest
from datetime import datetime
import utils


class TestUntils(unittest.TestCase):

    def test_get_random_alphaNumeric_string(self):

        random_string = utils.get_random_alphaNumeric_string(5)
        random_string2 = utils.get_random_alphaNumeric_string(5)

        self.assertNotEqual(random_string, random_string2)
        self.assertEqual(len(random_string), 5)
        self.assertIsInstance(random_string, str)

    def test_hash_password(self):

        random_password = utils.hash_password("random", "random")
        same_random_password = utils.hash_password("random", "random")
        different_random_password = utils.hash_password("whatthe", "random")

        self.assertEqual(random_password, same_random_password)
        self.assertNotEqual(random_password, different_random_password)

    def test_verify_password(self):
        salt = "thesalt"
        hashed_password = utils.hash_password("mypassword", salt)

        self.assertTrue(utils.verify_password(hashed_password, "mypassword", salt))
        self.assertFalse(utils.verify_password(hashed_password, "notmypassword", salt))

    def test_compare_dates(self):

        start = datetime(2020, 11, 11, 10, 00, 00)
        end = datetime(2020, 11, 11, 12, 00, 00)
        b_start = datetime(2020, 11, 11, 11, 00, 00)
        b_end = datetime(2020, 11, 11, 11, 30, 00)

        self.assertTrue(utils.compare_dates(start, end, b_start, b_end))

        start = datetime(2020, 11, 11, 11, 1, 00)
        self.assertTrue(utils.compare_dates(start, end, b_start, b_end))

        start = datetime(2021, 11, 11, 10, 00, 00)
        end = datetime(2021, 11, 11, 12, 00, 00)
        self.assertFalse(utils.compare_dates(start, end, b_start, b_end))


if __name__ == '__main__':
    unittest.main()
