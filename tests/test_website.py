import unittest
import requests
import logging
import api
from datetime import timedelta
from wtforms import StringField, FloatField, IntegerField
from wtforms.validators import ValidationError
from employee_app.website import valid_lat, valid_lng, valid_cph, valid_rego, valid_mac_address, valid_year, \
    valid_capacity, valid_weight, valid_length, valid_load_index, valid_engine_capacity, valid_ground_clearance
from api import create_app
from employee_app.website import site
from employee_app.app import app

IP = "http://127.0.0.1"
PORT = "5000/"
URL = "{}:{}".format(IP, PORT)


class TestFormValidation(unittest.TestCase):

    def test_lat(self):
        field = FloatField()
        field.data = 100
        self.assertRaises(ValidationError, valid_lat, None, field)
        field.data = -100
        self.assertRaises(ValidationError, valid_lat, None, field)

    def test_lng(self):
        field = FloatField()
        field.data = 200
        self.assertRaises(ValidationError, valid_lng, None, field)
        field.data = -200
        self.assertRaises(ValidationError, valid_lng, None, field)

    def test_cph(self):
        field = FloatField()
        field.data = -10
        self.assertRaises(ValidationError, valid_cph, None, field)
        field.data = 200
        self.assertRaises(ValidationError, valid_cph, None, field)

    def test_rego(self):
        field = StringField()
        field.data = "%$123as"
        self.assertRaises(ValidationError, valid_rego, None, field)

    def test_mac_address(self):
        field = StringField()
        field.data = "1234"
        self.assertRaises(ValidationError, valid_mac_address, None, field)
        field.data = "AA:AA:AA:AA:AA"
        self.assertRaises(ValidationError, valid_mac_address, None, field)
        field.data = "AA:AA:AA:GG:11:AA"
        self.assertRaises(ValidationError, valid_mac_address, None, field)
        field.data = "AA:AA:AA:AA:AA:AA:AA"
        self.assertRaises(ValidationError, valid_mac_address, None, field)

    def test_year(self):
        field = IntegerField()
        field.data = 1800
        self.assertRaises(ValidationError, valid_year, None, field)
        field.data = 3000
        self.assertRaises(ValidationError, valid_year, None, field)
        field.data = "asdasdasd"
        self.assertRaises(ValidationError, valid_year, None, field)

    def test_capacity(self):
        field = IntegerField()
        field.data = 1
        self.assertRaises(ValidationError, valid_capacity, None, field)
        field.data = 7
        self.assertRaises(ValidationError, valid_capacity, None, field)
        field.data = "asd&ASD7h"
        self.assertRaises(ValidationError, valid_capacity, None, field)

    def test_weight(self):
        field = FloatField()
        field.data = 900
        self.assertRaises(ValidationError, valid_weight, None, field)
        field.data = 2400
        self.assertRaises(ValidationError, valid_weight, None, field)
        field.data = "asd&ASD7h"
        self.assertRaises(ValidationError, valid_weight, None, field)

    def test_length(self):
        field = FloatField()
        field.data = 2
        self.assertRaises(ValidationError, valid_length, None, field)
        field.data = 6
        self.assertRaises(ValidationError, valid_length, None, field)
        field.data = "asd&ASD7h"
        self.assertRaises(ValidationError, valid_length, None, field)

    def test_load(self):
        field = IntegerField()
        field.data = 70
        self.assertRaises(ValidationError, valid_load_index, None, field)
        field.data = 150
        self.assertRaises(ValidationError, valid_load_index, None, field)
        field.data = "asd&ASD7h"
        self.assertRaises(ValidationError, valid_load_index, None, field)

    def test_engine(self):
        field = FloatField()
        field.data = 0
        self.assertRaises(ValidationError, valid_engine_capacity, None, field)
        field.data = 5
        self.assertRaises(ValidationError, valid_engine_capacity, None, field)
        field.data = "asd&ASD7h"
        self.assertRaises(ValidationError, valid_engine_capacity, None, field)

    def test_clearance(self):
        field = FloatField()
        field.data = 90
        self.assertRaises(ValidationError, valid_ground_clearance, None, field)
        field.data = 300
        self.assertRaises(ValidationError, valid_ground_clearance, None, field)
        field.data = "asd&ASD7h"
        self.assertRaises(ValidationError, valid_ground_clearance, None, field)


class TestWebsite(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app = create_app()
        app.config['SECRET_KEY'] = 'secret_key'
        app.config['SQLALCHEMY_DATABASE_URI'] = api.DB_URI
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

        app.permanent_session_lifetime = timedelta(hours=5)
        app.register_blueprint(site)
        app.register_blueprint(api.api)
        app.app_context().push()

    def test_home(self):
        response = requests.get(
            "{}{}".format(URL, "")
        )

        self.assertEqual(response.url, URL + '')
        self.assertEqual(response.status_code, 200)

    def test_main(self):
        with app.test_client() as c:
            with c.session_transaction() as sess:
                sess['user'] = {
                    'username': 'dandandao',
                    'type': 'ADMIN'
                }
            response = requests.get(
                "{}{}".format(URL, "/main")
            )
            self.assertEqual(response.url, URL + '')
            self.assertEqual(response.status_code, 200)
            rv = requests.post(
                "{}{}".format(URL, "employee/authenticate"),
                params={"employee_id": 'dandandao', "password": '123Qwe!'}
            )
            self.assertEqual(rv.json()['username'], sess['user']['username'])


if __name__ == '__main__':
    logging.getLogger("test_website").setLevel(logging.DEBUG)
    unittest.main()
