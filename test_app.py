import unittest
import app
from api import api, DB_URI
from datetime import timedelta
from website import site
import requests

URL = "http://127.0.0.1:5000/"


class TestApp(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        app_run = app.app
        app_run.config['SECRET_KEY'] = 'temp'
        app_run.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
        app_run.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

        app_run.permanent_session_lifetime = timedelta(hours=5)
        app_run.register_blueprint(site)
        app_run.register_blueprint(api)
        app_run.app_context().push()

    def test_page_not_found(self):
        result404 = requests.get(
            "{}{}".format(URL, "anywhereigoyougo")
        )

        self.assertEqual(result404.status_code, 404)
        # TODO check content of response to that of our template file.
        # self.assertEqual(result404.content, '/templates/404.html'.

    # def test_internal(self): unsure how to invoke 500
    # def test_page_not_found(self): unsure how to go to a restricted section without a 302 and redirect


if __name__ == '__main__':
    unittest.main()
