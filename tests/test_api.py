import json
import logging
import unittest
from datetime import timedelta
from datetime import datetime

import requests

import api
from api import create_app
from employee_app.website import site

URL = "http://127.0.0.1:5000/"


class TestApi(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up class - configures app before run

        Returns:

        """
        app = create_app()
        app.config['SECRET_KEY'] = 'secret_key'
        app.config['SQLALCHEMY_DATABASE_URI'] = api.DB_URI
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

        app.permanent_session_lifetime = timedelta(hours=5)
        app.register_blueprint(site)
        app.register_blueprint(api.api)
        app.app_context().push()

    def test_get_employees(self):
        """Test get employees - should always return 200"""
        result200 = requests.get(
            "{}{}".format(URL, "employees")
        )

        self.assertEqual(result200.status_code, 200)

    def test_get_employee(self):
        """Testing getting an employee - incorrect and correct ids"""
        employee_id1 = "johnsmith"
        employee_id2 = "testemp"

        result200 = requests.get(
            "{}{}".format(URL, "employee"),
            params={"employee_id": employee_id1}
        )

        result404 = requests.get(
            "{}{}".format(URL, "employee"),
            params={"employee_id": employee_id2}
        )

        result400 = requests.get(
            "{}{}".format(URL, "employee"),
        )

        self.assertEqual(result200.status_code, 200)
        self.assertEqual(result200.json()['email'], "john@gmail.com")
        self.assertEqual(result404.status_code, 404)
        self.assertEqual(result400.status_code, 400)

    def test_employee_authentication(self):
        """Testing authentication - correct and incorrect user/pass combinations"""
        result200 = requests.get(
            "{}{}".format(URL, "employee/authenticate"),
            params={"employee_id": "johnsmith", "password": "123Qwe!"},
        )

        result404password = requests.get(
            "{}{}".format(URL, "employee/authenticate"),
            params={"employee_id": "johnsmith", "password": "123Qwf!"},
        )

        result404user_id = requests.get(
            "{}{}".format(URL, "employee/authenticate"),
            params={"employee_id": "idontexist", "password": "123Qwf!"},
        )

        result400no_user_id = requests.get(
            "{}{}".format(URL, "employee/authenticate"),
            params={"password": "123Qwf!"},
        )

        result400no_password = requests.get(
            "{}{}".format(URL, "employee/authenticate"),
            params={"employee_id": "idontexist"},
        )

        self.assertEqual(result200.status_code, 200)
        self.assertEqual(result404password.status_code, 404)
        self.assertEqual(result404user_id.status_code, 404)
        self.assertEqual(result400no_user_id.status_code, 400)
        self.assertEqual(result400no_password.status_code, 400)

    def test_create_employee(self):
        """Testing create employee - checking for duplicate username (must not exist in db)"""
        employee = {
            'email': 'test_employee@gmail.com',
            'l_name': 'test',
            'f_name': 'employee',
            'password': 'Applelover69!',
            'username': 'testemployee',
            'type': 'ENGINEER',
            'mac_address': ''
        }

        result200 = requests.post(
            "{}{}".format(URL, "employee"),
            json=json.dumps(employee),
        )

        self.assertEqual(result200.status_code, 200)

        result200 = requests.post(
            "{}{}".format(URL, "employee"),
            json=json.dumps(employee),
        )

        self.assertEqual(result200.status_code, 404)

    def test_update_employee_attributes(self):
        """Testing updating an employee - dupilcate username"""
        employee = {
            'email': 'test_employee@gmail.com',
            'l_name': 'test',
            'f_name': 'employee',
            'password': 'Applelover69!',
            'username': 'testemployee',
            'type': 'ENGINEER',
            'mac_address': ''
        }

        result200 = requests.post(
            "{}{}".format(URL, "employee"),
            json=json.dumps(employee),
        )

        self.assertEqual(result200.status_code, 200)

        result200 = requests.post(
            "{}{}".format(URL, "employee"),
            json=json.dumps(employee),
        )

        self.assertEqual(result200.status_code, 404)

        result200 = requests.delete(
            "{}{}".format(URL, "employee"),
            params={"employee_id": 'testemployee'}
        )

        self.assertEqual(result200.status_code, 200)

    def test_remove_employee(self):
        """Testing remove of employee - must exist before running"""
        result200 = requests.delete(
            "{}{}".format(URL, "employee"),
            params={"employee_id": 'testemployee'}
        )

        self.assertEqual(result200.status_code, 200)

    def test_get_reports(self):
        """Testing get reports - combinations of engineer/resolved/car parameters"""
        result200 = requests.get(
            "{}{}".format(URL, "reports")
        )

        self.assertEqual(result200.status_code, 200)

        result200 = requests.get(
            "{}{}".format(URL, "reports"),
            params={"car_id": 'VSB296', 'resolved': '1', 'engineer_id': 'jwoodroffe'}
        )

        self.assertEqual(result200.status_code, 200)

        result200 = requests.get(
            "{}{}".format(URL, "reports"),
            params={'resolved': '1', 'engineer_id': 'jwoodroffe'}
        )

        self.assertEqual(result200.status_code, 200)

        result200 = requests.get(
            "{}{}".format(URL, "reports"),
            params={"car_id": 'HKF607', 'resolved': '0'}
        )

        self.assertEqual(result200.status_code, 200)

        result200 = requests.get(
            "{}{}".format(URL, "reports"),
            params={"car_id": 'VSB296', 'engineer_id': 'jwoodroffe'}
        )

        self.assertEqual(result200.status_code, 200)

    def test_get_report(self):
        """Testing getting a report - invalid id"""
        result200 = requests.get(
            "{}{}".format(URL, "report"),
            params={"report_id": '2'}
        )
        self.assertEqual(result200.status_code, 200)

        result404 = requests.get(
            "{}{}".format(URL, "report"),
            params={"report_id": '-1'}
        )
        self.assertEqual(result404.status_code, 404)

    def test_create_report(self):
        """Testing create report endpoint - check database for new report"""
        report = {
            'car_id': 'EXR143',
            'details': 'Testing',
            'priority': 'LOW',
            'report_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        result200 = requests.post("{}{}".format(URL, "/report"), json=json.dumps(report))

        self.assertEqual(result200.status_code, 200)

    def test_remove_report(self):
        """Testing report remove operation - run test_Create_report first"""
        data = requests.get(
            "{}{}".format(URL, "reports"),
            params={"car_id": 'EXR143', 'priority': 'LOW'}
        )

        result200 = requests.delete(
            "{}{}".format(URL, "report"),
            params={"report_id": data.json()[0]['report_id']}
        )

        self.assertEqual(result200.status_code, 200)

    def test_update_report(self):
        """Testing updating report - """
        data = requests.get(
            "{}{}".format(URL, "reports"),
            params={"car_id": 'EXR143', 'priority': 'LOW'}
        )

        result200 = requests.put(
            "{}{}".format(URL, "report"),
            params={"report_id": data.json()[0]['report_id'], 'engineer_id': 'jwoodroffe', 'complete_date': '2020-06-19 15:47:38'}
        )

        self.assertEqual(result200.status_code, 200)

        result404 = requests.put(
            "{}{}".format(URL, "report"),
            params={"report_id": "-1"}
        )
        self.assertEqual(result404.status_code, 400)

    def test_update_report_notification(self):
        """testing update notification of report"""
        data = requests.get(
            "{}{}".format(URL, "reports"),
            params={"car_id": 'EXR143', 'priority': 'LOW'}
        )

        result200 = requests.put(
            "{}{}".format(URL, "report_notification"),
            params={"report_id": data.json()[0]['report_id'], 'notification': 1}
        )

        logger = logging.getLogger('TEST LOGGER')
        logger.debug(result200.text)

        self.assertEqual(result200.status_code, 200)

    def test_engineer_unlock(self):
        """Testing engineer unlock functionality - requires a valid engineer and valid car"""
        result = requests.put(
            "{}{}".format(URL, "engineer/unlock_car"),
            params={"car_id": 'EXR143', 'engineer_id': 'jwoodroffe'}
        )  # valid
        self.assertEqual(result.status_code, 200)

        result = requests.put(
            "{}{}".format(URL, "engineer/unlock_car"),
            params={"car_id": 'EXR143', 'engineer_id': 'dootdoot'}
        )  # invalid employee
        self.assertEqual(result.status_code, 404)

        result = requests.put(
            "{}{}".format(URL, "engineer/unlock_car"),
            params={"car_id": 'DOOT12', 'engineer_id': 'jwoodroffe'}
        )  # invalid car
        self.assertEqual(result.status_code, 404)

        result = requests.put(
            "{}{}".format(URL, "engineer/unlock_car"),
            params={"car_id": 'EXR143', 'engineer_id': 'donalduren'}
        )  # invalid employee - wrong type
        self.assertEqual(result.status_code, 404)

        result = requests.put(
            "{}{}".format(URL, "engineer/unlock_car")
        )  # missing parameters
        self.assertEqual(result.status_code, 400)

    def test_get_users(self):
        """confirms that it returns array of all users information"""
        self.assertEqual(api.get_users().status_code, 200)

    def test_get_user(self):
        """gets a user that exists, and fails if the user does not exist/no parameters are given"""
        real_user = "donalduren"
        fake_user = "fakeUser19"

        result200 = requests.get(
            "{}{}".format(URL, "user"),
            params={"user_id": real_user}
        )

        result404 = requests.get(
            "{}{}".format(URL, "user"),
            params={"user_id": fake_user}
        )

        result400 = requests.get(
            "{}{}".format(URL, "user"),
        )

        self.assertEqual(result200.status_code, 200)
        self.assertEqual(result200.json()['email'], "donald@gmail.com")
        self.assertEqual(result404.status_code, 404)
        self.assertEqual(result400.status_code, 400)

    def test_add_user(self):
        """adds this user, tries to add the same user twice, then checks if they got added.
        Will cause error if person isn't deleted afterward.
        """

        user = {
            'email': 'anotherran122@gmail.com',
            'l_name': 'steve',
            'f_name': 'jawbs',
            'password': 'applelover69',
            'username': 'anotherran12'
        }

        result200 = requests.post(
            "{}{}".format(URL, "user"),
            json=json.dumps(user),
        )

        self.assertEqual(result200.status_code, 200)

        result200 = requests.post(
            "{}{}".format(URL, "user"),
            json=json.dumps(user),
        )

        self.assertEqual(result200.status_code, 404)

        user_id = "anotherran12"

        checkInDB = requests.get(
            "{}{}".format(URL, "user"),
            params={"user_id": user_id}
        )

        self.assertEqual(checkInDB.status_code, 200)

    def test_delete_user(self):
        """Test delete user operation"""
        result200 = requests.delete(
            "{}{}".format(URL, "user"),
            params={"user_id": 'anotherran12'}
        )

        self.assertEqual(result200.status_code, 200)

    def test_user_authentication(self):
        """checks correct account, then wrong pass, then wrong username, then parameters without username, or password.
        """

        result200 = requests.get(
            "{}{}".format(URL, "users/authenticate"),
            params={"user_id": "kevmason", "password": "123Qwe!"},
        )

        result404password = requests.get(
            "{}{}".format(URL, "users/authenticate"),
            params={"user_id": "kevmason", "password": "123Qwf!"},
        )

        result404user_id = requests.get(
            "{}{}".format(URL, "users/authenticate"),
            params={"user_id": "idontexist", "password": "123Qwf!"},
        )

        result400no_user_id = requests.get(
            "{}{}".format(URL, "users/authenticate"),
            params={"password": "123Qwf!"},
        )

        result400no_password = requests.get(
            "{}{}".format(URL, "users/authenticate"),
            params={"user_id": "idontexist"},
        )

        self.assertEqual(result200.status_code, 200)
        self.assertEqual(result404password.status_code, 404)
        self.assertEqual(result404user_id.status_code, 404)
        self.assertEqual(result400no_user_id.status_code, 400)
        self.assertEqual(result400no_password.status_code, 400)

    def test_cars(self):
        """checks if the cars table isn't empty"""
        self.assertEqual(api.get_cars().status_code, 200)

    def test_car(self):
        """tests the returning of the car endpoint"""
        car_id1 = "EXR143"
        car_id2 = "HIDDEN"

        result200 = requests.get(
            "{}{}".format(URL, "car"),
            params={"car_id": car_id1}
        )

        result404 = requests.get(
            "{}{}".format(URL, "car"),
            params={"car_id": car_id2}
        )

        result400 = requests.get(
            "{}{}".format(URL, "car"),
        )

        self.assertEqual(result200.status_code, 200)
        self.assertEqual(result200.json()['car_id'], "EXR143")
        self.assertEqual(result404.status_code, 404)
        self.assertEqual(result400.status_code, 400)

    def test_update_car(self):
        """checking update car functionality if no booking exists"""
        car_id1 = "EXR143"
        locked = 0
        user_id = "kevmason"

        result_no_booking = requests.put(
            "{}{}".format(URL, "car"),
            params={"car_id": car_id1, "locked": locked, "user_id": user_id},
        )

        self.assertEqual(result_no_booking.status_code, 404)

        result_no_car_id = requests.put(
            "{}{}".format(URL, "car"),
            params={"locked": locked, "user_id": user_id},
        )

        result_no_locked = requests.put(
            "{}{}".format(URL, "car"),
            params={"car_id": car_id1, "user_id": user_id},
        )

        result_no_user_id = requests.put(
            "{}{}".format(URL, "car"),
            params={"car_id": car_id1, "locked": locked},
        )

        self.assertEqual(result_no_car_id.status_code, 400)
        self.assertEqual(result_no_locked.status_code, 400)
        self.assertEqual(result_no_user_id.status_code, 400)

    def test_update_location(self):
        """Testing updating a vehicles location - invalid id, valid, missing params"""
        result_wrong_lat = requests.put(
            "{}{}".format(URL, "car"),
            params={"long": 120, "lat": 100},
        )

        self.assertEqual(result_wrong_lat.status_code, 400)

        result_wrong_long = requests.put(
            "{}{}".format(URL, "car"),
            params={"long": 188, "lat": 55},
        )
        self.assertEqual(result_wrong_long.status_code, 400)

        result_no_car_found = requests.put(
            "{}{}".format(URL, "car"),
            params={"car_id": "NOCAR1"},
        )

        self.assertEqual(result_no_car_found.status_code, 400)

        result_no_lat_long = requests.put(
            "{}{}".format(URL, "car"),
            params={"car_id": "VB"},
        )

        self.assertEqual(result_no_lat_long.status_code, 400)

    def test_get_valid_cars(self):
        """Testing getting valid cars"""
        result_200 = requests.get(
            "{}{}".format(URL, "cars/1995-01-05T12:12:12/2021-01-05T12:12:12"),
        )
        self.assertEqual(result_200.status_code, 200)

    def test_get_booking(self):
        """Testing get booking"""
        result_404 = requests.get(
            "{}{}".format(URL, "booking"),
            params={"booking_id": "IDONTKNOWYET"},
        )

        result_400 = requests.get(
            "{}{}".format(URL, "booking"),
        )

        self.assertEqual(result_404.status_code, 404)
        self.assertEqual(result_400.status_code, 400)


if __name__ == '__main__':
    unittest.main()
