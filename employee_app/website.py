"""
MP Employee Web App

website.py renders html templates and handles page endpoints.
Also handles input validation for login, register, booking, and cancel, along with processing forms.
"""
import json
import re
from json.decoder import JSONDecodeError
from templates import *
import requests
import os
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateTimeField
from wtforms.validators import InputRequired, Email, Length, ValidationError
from collections import defaultdict
from datetime import datetime
from httplib2 import Http
from oauth2client import client
from googleapiclient import discovery
from customer_app.utils import allowed_file, calc_hours
from customer_app.website import LoginForm
from werkzeug.utils import secure_filename

site = Blueprint("site", __name__)

URL = "http://127.0.0.1:5000/"


@site.route("/", methods=['POST', 'GET'])
def home():
    """Authenticates a user when they log in to the MP employee web app

    Returns:
        redirect site.main or if user successfully authenticated
        or renders login.html on load, with error messages if incorrect login attempt
    """
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        # TODO: employee authentication - same process as customer but different table
        result = None  # request result
        data = None  # json data
        session['user'] = {"type": "ADMIN"}  # TODO: replace this tempporary value
        # if result.status_code == 200:
        #     session['user'] = result.json()
        # elif result.status_code == 404:
        #     # If the username is not in the database
        #     if data['error'] == 'USER':
        #         form.username.errors.append('This username has not been registered')  # Form error message
        #     # If the password is incorrect
        #     elif data['error'] == 'PASSWORD':
        #         form.password.errors.append('Incorrect password')  # Form error message
    if 'user' in session:
        employee_type = session['user']['type']
        if employee_type == "ADMIN":  # redirect to ADMIN site
            return redirect(url_for("site.main"))
        elif employee_type == "ENGINEER":  # redirect to ENGINEER dashboard
            return redirect(url_for("site.engineer"))
        elif employee_type == "MANAGER":  # redirect to MANAGER dashboard
            return redirect(url_for("site.manager"))
    return render_template("login.html", form=form)


@site.route("/main", methods=['GET'])
def main():
    """Displays the rental history page - admin can view and search all bookings

    Returns:
        renders history.html with booking data
    """
    if 'user' in session and session['user']['type'] == "ADMIN":
        result = requests.get("{}{}".format(URL, "/bookings"))
        try:
            bookings_data = result.json()
        except JSONDecodeError as je:
            bookings_data = None
        return render_template("employee/history.html", bookings=bookings_data)
    return redirect(url_for("site.home"))


@site.route("/logout")
def logout():
    """Logs the user out of MP web app

    Returns:
        redirects to site.login
    """
    session.pop('user', None)  # Remove user from session
    return redirect(url_for('site.home'))
