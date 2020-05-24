import unittest
import app
from api import api, DB_URI
from datetime import timedelta
from website import site
import pickle
import requests
import facial_recognition

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

    
    def test_encode_user(self):
        result200 = requests.post(
                "{}{}".format(URL, "/encode_user"),
                params={"user_id": "kevmason", "directory": "user_data/face_pics/"}
            )
        self.assertEquals(result200.status_code, 200)

    def test_get_encoding(self):
        result200 = requests.get(
            "{}{}".format(URL, "/get_encoding"),
            params={"user_id": "kevmason"}
        )
        self.assertIsNotNone(result200.content)

if __name__ == '__main__':
    unittest.main()
