"""
MP Flask Employee Web App

Creates Flask app and registers database :class:`api` and :class:`employee_app.website` endpoints.

"""

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_googlemaps import GoogleMaps
from api import api, db, DB_URI
from employee_app.website import site
from datetime import timedelta

app = Flask(__name__, template_folder="../templates", static_folder='../static')
app.config['SECRET_KEY'] = 'temp'
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["GOOGLEMAPS_KEY"] = "AIzaSyDbaBxoVyou5qJyvH1bhpQQb4aw6tqiGsQ"

app.permanent_session_lifetime = timedelta(hours=5)
app.register_blueprint(api)
app.register_blueprint(site)


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


Bootstrap(app)
db.init_app(app)
GoogleMaps(app)

if __name__ == '__main__':
    """Run the flask application"""
    # db.drop_all(app=app)
    db.create_all(app=app)
    app.run(debug=True, host="0.0.0.0")
