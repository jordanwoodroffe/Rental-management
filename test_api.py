import unittest
from website import site
from datetime import timedelta
from api import create_app
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

    def test_get_users(self):
        self.assertEqual(api.get_users().status_code, 200)
        # json = api.UserSchema(many=True, exclude=['password']).dumps(api.User.query.all())
        # print(json)

    def test_get_user(self):
        user_id = "daniel@gmail.com"
        result = requests.get(
            "{}{}".format(URL, "user"),
            params={"user_id": user_id}
        )

        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.json()['email'], "daniel@gmail.com")


        # self.assertEqual(api.get_user(), 200)  ## test if a user comes back that exists

        # self.assertEqual(api.get_user(), 404) ## if user that doesnt exist infact returns nothing

        # self.assertEqual(api.get_user(), 400) ## if the parameter i gave doesnt exist.


if __name__ == '__main__':
    unittest.main()
