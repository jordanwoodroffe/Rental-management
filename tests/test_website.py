import unittest
import requests
import api
from datetime import timedelta
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from api import create_app
from employee_app.website import site
from employee_app.app import app
from unittest import mock


IP = "http://127.0.0.1"
PORT = "5000/"
URL = "{}:{}".format(IP, PORT)


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
        response = requests.get(
            "{}{}".format(URL, "main")
        )

        self.assertEqual(response.url, URL + '')
        self.assertEqual(response.status_code, 200)

        with app.test_client() as c:
            rv = c.post("{}{}".format(URL, "employee/authenticate"),
                        json={"employee_id": 'dandandao', "password": '123Qwe!'}
                        )

            self.assertEqual(rv.json(), session['user'])
            # self.assertEqual(response.status_code, 200)

    def test_history(self):
        pass

    def test_view_cars(self):
        pass

    def test_edit_car(self):
        pass

    def test_create_vehicle(self):
        pass

    def test_remove_car(self):
        pass

    def test_view_reports(self):
        pass

    def test_remove_report(self):
        pass

    def test_report_car(self):
        pass

    def test_alert_report(self):
        pass

    def test_view_users(self):
        pass

    def test_edit_user(self):
        pass

    def test_create_user(self):
        pass

    def test_remove_user(self):
        pass

    def test_view_employees(self):
        pass

    def test_edit_employee(self):
        pass

    def test_create_employee(self):
        pass

    def test_remove_employee(self):
        pass

    def test_manager(self):
        pass

    def test_engineer(self):
        pass

    def test_view_models(self):
        pass

    def test_create_model(self):
        pass

    def test_edit_model(self):
        pass

    def test_logout(self):
        pass


if __name__ == '__main__':
    unittest.main()
