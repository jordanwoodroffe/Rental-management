from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_bootstrap import Bootstrap
from flask_datepicker import datepicker
from flask_wtf import FlaskForm
from api import api, db, DB_URI, populate
from website import site
from wtforms import StringField, PasswordField, SelectField, IntegerField
from wtforms.validators import InputRequired, Email, Length, NumberRange, ValidationError
from datetime import timedelta
import re


app = Flask(__name__)
app.config['SECRET_KEY'] = 'temp'
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

app.permanent_session_lifetime = timedelta(hours=5)
app.register_blueprint(site)
app.register_blueprint(api)

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

@app.errorhandler(403)
def access_forbidden(error):
    return render_template("403.html"), 403

@app.errorhandler(500)
def internal(error):
    return render_template("500.html"), 500


Bootstrap(app)

db.init_app(app)

if __name__ == '__main__':
    # app.run(debug=True, host='192.168.1.200')  # use IP of MP: as per forums only has to be accessibly locally
    # db.drop_all(app=app)
    db.create_all(app=app)
    app.run(debug=True)

