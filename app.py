from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from api import api, db, get_uri
from website import site
from wtforms import StringField, PasswordField, SelectField, IntegerField
from wtforms.validators import InputRequired, Email, Length, NumberRange, ValidationError
from datetime import timedelta
import re


app = Flask(__name__)
app.config['SECRET_KEY'] = 'temp'
app.config['SQLALCHEMY_DATABASE_URI'] = get_uri()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

app.permanent_session_lifetime = timedelta(hours=5)
app.register_blueprint(site)
app.register_blueprint(api)

Bootstrap(app)

if __name__ == '__main__':
    # app.run(debug=True, host='192.168.1.200')  # use IP of MP: as per forums only has to be accessibly locally
    db.init_app(app)
    db.create_all(app=app)
    app.run(debug=True)
