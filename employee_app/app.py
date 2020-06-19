"""
MP Flask Employee Web App

Creates Flask app and registers database :class:`api` and :class:`employee_app.website` endpoints.

"""
from environs import Env
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from api import api, db, DB_URI
from employee_app.website import site
from datetime import timedelta

env = Env()
env.read_env()

GOOGLE_MAPS_KEY = env("GOOGLE_MAPS_KEY")
SECRET_KEY = env('SECRET_KEY')

app = Flask(__name__, template_folder="../templates", static_folder='../static')
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["GOOGLEMAPS_KEY"] = GOOGLE_MAPS_KEY

app.permanent_session_lifetime = timedelta(hours=5)
app.register_blueprint(api)
app.register_blueprint(site)
Bootstrap(app)
db.init_app(app)


@app.errorhandler(404)
def page_not_found(error):
    """Renders when page is not found"""
    return render_template("404.html"), 404


@app.errorhandler(403)
def access_forbidden(error):
    """Renders when user attempts to access forbidden page"""
    return render_template("403.html"), 403


@app.errorhandler(500)
def internal(error):
    """Renders when server error occurs"""
    return render_template("500.html"), 500


if __name__ == '__main__':
    """Run the flask application"""
    # db.drop_all(app=app)  # optional: uncomment to drop all data from tables
    db.create_all(app=app)
    app.run(debug=True, host="0.0.0.0")
