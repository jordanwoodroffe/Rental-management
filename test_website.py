import unittest

class TestWebsite(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app = create_app()
        app.config['SECRET_KEY'] = 'temp'
        app.config['SQLALCHEMY_DATABASE_URI'] = api.DB_URI
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

        app.permanent_session_lifetime = timedelta(hours=5)
        app.register_blueprint(site)
        app.register_blueprint(api.api)
        app.app_context().push()


if __name__ == '__main__':
    unittest.main()
