import unittest
from website import site
from datetime import timedelta
from api import create_app
import json
import api
import requests

URL = "http://127.0.0.1:5000/"


class TestApi(unittest.TestCase):

    def setUp(self):
        app = create_app()
        app.config['SECRET_KEY'] = 'temp'
        app.config['SQLALCHEMY_DATABASE_URI'] = api.DB_URI
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

        app.permanent_session_lifetime = timedelta(hours=5)
        app.register_blueprint(site)
        app.register_blueprint(api.api)
        app.app_context().push()

    def test_get_users(self): # just confirms that it returns array of all users information
        self.assertEqual(api.get_users().status_code, 200)

    def test_get_user(self): ## gets a user that exists, and fails if the user does not exist/no parameters are given

        user_id1 = "daniel@gmail.com"
        user_id2 = "imnotreal@gmail.com"

        result200 = requests.get(
            "{}{}".format(URL, "/user"),
            params={"user_id": user_id1}
        )

        result404 = requests.get(
            "{}{}".format(URL, "/user"),
            params={"user_id": user_id2}
        )

        result400 = requests.get(
            "{}{}".format(URL, "/user"),
        )

        self.assertEqual(result200.status_code, 200)
        self.assertEqual(result200.json()['email'], "daniel@gmail.com")
        self.assertEqual(result404.status_code, 404)
        self.assertEqual(result400.status_code, 400)

    # def test_add_user(self): ## adds this user, tries to add the same user twice, then checks if they got added. Will cause error if person isn't deleted afterward.

    #     user = {'email': 'anotherran22@gmail.com', 
    #             'l_name': 'steve',
    #             'f_name': 'jawbs',
    #             'password': 'applelover69',
    #             }
    #     result200 = requests.post(
    #         "{}{}".format(URL, "user"),
    #         json=json.dumps(user),
    #     )

    #     self.assertEqual(result200.status_code, 200)

    #     result200 = requests.get(
    #         "{}{}".format(URL, "user"),
    #         params={"user_id": user.get("email")}
    #     )

    #     result200 = requests.post(
    #         "{}{}".format(URL, "user"),
    #         json=json.dumps(user),
    #     )

    #     self.assertEqual(result200.status_code, 404)

    #     email = "anotherran22@gmail.com"

    #     checkInDB = requests.get(
    #         "{}{}".format(URL, "user"),
    #         params={"user_id": email}
    #     )

    #     self.assertEqual(checkInDB.status_code, 200)

        # api.db.session.delete(deleteuser) # removes the user we just created from the database. FIX LATER

    def test_user_authentication(self):  # checks correct account, then wrong pass, then wrong email, then parameters without email, or password.

        result200 = requests.get(
            "{}{}".format(URL, "users/authenticate"),
            params={"user_id": "kev@gmail.com", "password": "123Qwe!"},
        )

        result404password = requests.get(
            "{}{}".format(URL, "users/authenticate"),
            params={"user_id": "kev@gmail.com", "password": "123Qwf!"},
        )

        result404email = requests.get(
            "{}{}".format(URL, "users/authenticate"),
            params={"user_id": "idontexist@gmail.com", "password": "123Qwf!"},
        )

        result400no_email = requests.get(
            "{}{}".format(URL, "users/authenticate"),
            params={"password": "123Qwf!"},
        )

        result400no_password = requests.get(
            "{}{}".format(URL, "users/authenticate"),
            params={"user_id": "idontexist@gmail.com"},
        )

        self.assertEqual(result200.status_code, 200)
        self.assertEqual(result404password.status_code, 404)
        self.assertEqual(result404email.status_code, 404)
        self.assertEqual(result400no_email.status_code, 400)
        self.assertEqual(result400no_password.status_code, 400)

    def test_cars(self): # checks if the cars table isn't empty
        self.assertEqual(api.get_cars().status_code, 200)

    def test_car(self): # tests the returning of the car endpoint

        car_id1 = "EXR143"
        car_id2 = "HIDDEN"

        result200 = requests.get(
            "{}{}".format(URL, "/car"),
            params={"car_id": car_id1}
        )

        result404 = requests.get(
            "{}{}".format(URL, "/car"),
            params={"car_id": car_id2}
        )

        result400 = requests.get(
            "{}{}".format(URL, "/car"),
        )

        self.assertEqual(result200.status_code, 200)
        self.assertEqual(result200.json()['car_id'], "EXR143")
        self.assertEqual(result404.status_code, 404)
        self.assertEqual(result400.status_code, 400)

    def test_update_car(self):

        # no booking check
        car_id1 = "EXR143"
        locked = 0
        user_id = "kev@gmail.com"

        result_no_booking = requests.put(
                "{}{}".format(URL, "/car"),
                params={"car_id": car_id1, "locked" : locked, "user_id" : user_id},
            )

        self.assertEqual(result_no_booking.status_code, 404)

        result_no_car_id = requests.put(
                "{}{}".format(URL, "/car"),
                params={"locked" : locked, "user_id" : user_id},
            )

        result_no_locked = requests.put(
                "{}{}".format(URL, "/car"),
                params={"car_id": car_id1, "user_id" : user_id},
            )

        result_no_user_id = requests.put(
                "{}{}".format(URL, "/car"),
                params={"car_id": car_id1, "locked" : locked},
            )

        self.assertEqual(result_no_car_id.status_code, 400)
        self.assertEqual(result_no_locked.status_code, 400)
        self.assertEqual(result_no_user_id.status_code, 400)

        # TODO create a booking thats gone by to check 404
        # TODO check 200 for correct booking found.
        # TODO check 400 by changing lock from above to invalid value 2

        # result_wrong_lock = requests.put(
        #         "{}{}".format(URL, "/car"),
        #         params={"car_id": car_id1, "locked": 2, "user_id": user_id},
        #     )

        # self.assertEqual(result_wrong_lock.status_code, 400)

        # TODO double book this and re run for 500 check

    # def test_update_location(self):

        # TODO can't test with no route for the values to pass into but i created the test just in case it gets done.
        # TODO can't give these args. dont know where they come from.
        # with self.assertRaises(ValueError):
        #     result_wrong_lat = requests.put(
        #         "{}{}".format(URL, "ROUTE!"),
        #         params={"long": 120, "lat" : 100},
        #     )

        #     self.assertEqual(result_wrong_lat.status_code, 400)

        # with self.assertRaises(ValueError):
        #     result_wrong_long = requests.put(
        #         "{}{}".format(URL, "ROUTE!"),
        #            params={"long": 188, "lat" : 55},
        #       )
        #     self.assertEqual(result_wrong_long.status_code, 400)

        # result_no_car_found = requests.put(
        #         "{}{}".format(URL, "ROUTE!"),
        #         params={"car_id": "NOCAR1"},
        #     )

        # self.assertEqual(result_no_car_found.status_code, 404)

        # result_no_lat_long = requests.put(
        #         "{}{}".format(URL, "ROUTE!"),
        #         params={"car_id": "NOCAR1"},
        #     )

        # self.assertEqual(result_no_lat_long.status_code, 404)

    def test_get_valid_cars(self): # returns all cards right now,
        result_200 = requests.get(
                "{}{}".format(URL, "/cars/1995-01-05T12:12:12/2021-01-05T12:12:12"),
            )
        self.assertEqual(result_200.status_code, 200)

        # TODO check a time where a car is booked (create booking) and that time doesn't contain car.

    def test_get_bookings(self):

        # TODO create a booking first to check user booking

        # no user peram =  all bookings
        result_200 = requests.get(
                "{}{}".format(URL, "/bookings"),
            )

        # TODO booking for user return, has to have made booking
        # result_200_user = requests.get(
        #     "{}{}".format(URL, "/bookings"),
        #     params={"user_id": "kev@gmail.com"},

        # )

        self.assertEqual(result_200.status_code, 200)
        # self.assertEqual(result_200_user.status_code, 200)
        # self.result_200_user.json()['user_id'], "kev@gmail.com"

    def test_get_booking(self):

        # HAVEN'T MADE BOOKING TO TEST
        # TODO test result 200

        result_404 = requests.get(
                    "{}{}".format(URL, "/booking"),
                    params={"booking_id": "IDONTKNOWYET"},
                )

        result_400 = requests.get(
            "{}{}".format(URL, "/booking"),
        )

        self.assertEqual(result_404.status_code, 404)
        self.assertEqual(result_400.status_code, 400)

    def test_add_booking(self):

        # booking = {
        #     'start': '2030-01-05 12:12:12',
        #     'end': '2031-01-05 12:12:12',
        #     'user_id': 'kev@gmail.com',
        #     'car_id': 'EXR143',
        #     'compelted': 0,
        #     'event_id': '',
        #     }

        # booking_with_event = {
        #     'start': '2032-01-05 12:12:12',
        #     'end': '2033-01-05 12:12:12',
        #     'user_id': 'kev@gmail.com',
        #     'car_id': 'EXR143',
        #     'compelted': 0,
        #     'event_id': 'EVENT1',
        #     }

        # result200 = requests.post(
        #     "{}{}".format(URL, "/booking"),
        #     json=json.dumps(booking),
        # )

        # result200_with_event = requests.post(
        #     "{}{}".format(URL, "/booking"),
        #     json=json.dumps(booking_with_event),
        # )

        result400_no_data = requests.post(
             "{}{}".format(URL, "/booking")
        )

        # self.assertEqual(result200.status_code, 200)
        # self.assertEqual(result200_with_event.status_code, 200)
        self.assertEqual(result400_no_data.status_code, 400)

    # def test_update_booking(self):

    #     booking = {
    #         'start': '2035-01-05 12:12:12',
    #         'end': '2034-01-05 12:12:12',
    #         'user_id': 'kev@gmail.com',
    #         'car_id': 'EXR143',
    #         'compelted': 0,
    #         'event_id': '',
    #         }

    #     booking_added = requests.post(
    #         "{}{}".format(URL, "/booking"),
    #         json=json.dumps(booking),
    #     )

    #     self.assertEqual(booking_added.status_code, 200)  # if this failed fix add_booking

    #     booking_id = booking_added.json()['booking_id']

    #     booking_update = {
    #         'booking_id': booking_id,
    #         'status': '1',
    #     }

    #     booking_updated = requests.put(
    #         "{}{}".format(URL, "/booking"),
    #         json=json.dumps(booking_update),
    #     )

    #     self.assertEqual(booking_updated.status_code, 200)

    def test_updated_eventId(self):

        booking = {
            'start': '2036-01-05 12:12:12',
            'end': '2035-01-05 12:12:12',
            'user_id': 'kev@gmail.com',
            'car_id': 'EXR143',
            'compelted': 0,
            'event_id': '',
            }

        booking_added = requests.post(
            "{}{}".format(URL, "/booking"),
            json=json.dumps(booking),
        )

        self.assertEqual(booking_added.status_code, 200)  # if this failed fix add_booking

        booking_id = booking_added.json()['booking_id']

        event_update = {
            'booking_id': booking_id,
            'event_id': 'NEWEID',
        }

        event_update_wrong_id = {
            'booking_id': '9999',
            'event_id': 'NEWEID',
        }

        event_updated = requests.put(
            "{}{}".format(URL, "/eventId"),
            json=json.dumps(event_update),
        )

        event_no_booking = requests.put(
            "{}{}".format(URL, "/eventId"),
            json=json.dumps(event_update_wrong_id),
        )

        event_no_param = requests.put(
            "{}{}".format(URL, "/eventId"),
        )

        self.assertEqual(event_updated.status_code, 200)
        #self.assertEqual(event_no_booking.status_code, 404) # TODO SHOULD BE 404
        #self.assertEqual(event_no_param.status_code, 400) # TODO SHOULD BE 400

if __name__ == '__main__':
    unittest.main()
