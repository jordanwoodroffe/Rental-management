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
from flask_googlemaps import Map
from wtforms import StringField, PasswordField, SelectField, HiddenField, FloatField, BooleanField
from wtforms.validators import InputRequired, Email, Length, ValidationError
from collections import defaultdict
from datetime import datetime
from httplib2 import Http
from oauth2client import client
from googleapiclient import discovery
from customer_app.utils import allowed_file, calc_hours
from customer_app.website import LoginForm, make_attributes, RegistrationForm, valid_name, valid_username, \
    valid_password
from werkzeug.utils import secure_filename

site = Blueprint("site", __name__)

URL = "http://127.0.0.1:5000"


class UpdateUserForm(FlaskForm):
    """UpdateUserForm form to update user details"""
    first_name = StringField('First Name', validators=[InputRequired(), valid_name])
    last_name = StringField('Last Name', validators=[InputRequired(), valid_name])
    existing_username = HiddenField("Existing Username")
    username = StringField('Username', validators=[InputRequired(), Length(6, 12), valid_username])
    email = StringField('Email', validators=[InputRequired(), Email(message="Invalid email.")])
    password = PasswordField('Password', validators=[InputRequired(), Length(6, 12), valid_password])


class UpdateEmployeeForm(FlaskForm):
    """UpdateEmployeeForm form to update employee details"""
    first_name = StringField('First Name', validators=[InputRequired(), valid_name])
    last_name = StringField('Last Name', validators=[InputRequired(), valid_name])
    existing_username = HiddenField("Existing Username")
    username = StringField('Username', validators=[InputRequired(), Length(6, 12), valid_username])
    email = StringField('Email', validators=[InputRequired(), Email(message="Invalid email.")])
    password = PasswordField('Password', validators=[InputRequired(), Length(6, 12), valid_password])
    type = SelectField('Type', choices=[('ADMIN', 'Admin'), ('ENGINEER', 'Engineer'), ('MANAGER', 'Manager')])


class UpdateCarForm(FlaskForm):
    existing_car_id = HiddenField("Existing CarID")
    car_id = StringField('Rego', validators=[InputRequired(), Length(6, 6, message="Rego must be 6 characters")])
    cph = FloatField('Cost per hour', validators=[InputRequired()])
    lat = FloatField('Latitude', validators=[InputRequired()])
    lng = FloatField('Longitude', validators=[InputRequired()])
    model = SelectField('Model', validators=[InputRequired()], id="model_id")

    def __init__(self, models: [], *args, **kwargs):
        super(UpdateCarForm, self).__init__(*args, **kwargs)
        self.model.choices = [
            (model["model_id"], "{} {} {}".format(model["year"], model["make"], model["model"])) for model in models
        ]


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
        result = requests.get(
            "{}{}".format(URL, "/employee/authenticate"),
            params={"employee_id": form.username.data, "password": form.password.data}
        )
        data = result.json()
        if result.status_code == 200:
            session['user'] = result.json()
        elif result.status_code == 404:
            # If the username is not in the database
            if data['error'] == 'USER':
                form.username.errors.append('This username has not been registered')  # Form error message
            # If the password is incorrect
            elif data['error'] == 'PASSWORD':
                form.password.errors.append('Incorrect password')  # Form error message
    if 'user' in session:
        return redirect(url_for("site.main"))
    return render_template("login.html", form=form)


@site.route("/main", methods=['GET'])
def main():
    """Displays the rental history page - admin can view and search all bookings

    Returns:
        renders history.html with booking data
    """
    if 'user' in session:
        employee_type = session['user']['type']
        if employee_type == "ADMIN":  # redirect to ADMIN site
            return redirect(url_for("site.rental_history"))
        elif employee_type == "ENGINEER":  # redirect to ENGINEER dashboard
            return redirect(url_for("site.engineer_dashboard"))
        elif employee_type == "MANAGER":  # redirect to MANAGER dashboard
            return redirect(url_for("site.manager"))
    return redirect(url_for("site.home"))


@site.route("/history", methods=['GET'])
def rental_history():
    if 'user' in session and session['user']['type'] == "ADMIN":
        result = requests.get("{}{}".format(URL, "/bookings"))
        try:
            bookings_data = result.json()
        except JSONDecodeError as je:
            bookings_data = None
        return render_template("employee/history.html", bookings=bookings_data)
    return redirect(url_for("site.home"))


@site.route("/view_cars", methods=['GET'])
def search_cars():
    """Search cars by attributes

    NOTE - functionality also available on booking.html

    Returns:
        vehicles.html if user logged in, otherwise index.html
    """
    if 'user' in session and session['user']['type'] == 'ADMIN':  # Check if user is logged in & is an admin
        cars = requests.get(
            "{}{}".format(URL, "/cars")
        )  # Retrieve all cars in car table
        if cars.status_code == 200:
            try:
                car_data = cars.json()
            except JSONDecodeError as je:
                attributes = None
                car_data = None
            else:
                attributes = make_attributes(car_data)  # Get cars's attributes to send to front-end for filter
        else:
            attributes = None
            car_data = None
        return render_template("employee/vehicles.html", cars=car_data, attributes=attributes)
    return redirect(url_for('site.home'))


@site.route("/edit_car", methods=['GET', 'POST'])
def render_edit_car():
    models = requests.get("{}{}".format(URL, "/car_models"))
    models = models.json()
    form = UpdateCarForm(models=models)
    if request.method == 'POST' and form.validate_on_submit():
        car = {
            'existing_car_id': form.existing_car_id.data,
            'car_id': form.car_id.data,
            'cph': form.cph.data,
            'lat': form.lat.data,
            'lng': form.lng.data,
            'model': form.model_id.data,
        }
    if 'user' in session and session['user']['type'] == 'ADMIN':
        car_id = request.args.get("car_id")
        if car_id is not None:
            result = requests.get("{}{}".format(URL, "/car"), params={"car_id": car_id})
            car = result.json()
            form = UpdateCarForm(models=models, model=car['model_id'])
            form.existing_car_id.data = car['car_id']
            form.car_id.data = car['car_id']
            form.cph.data = car['cph']
            form.lat.data = car['lat']
            form.lng.data = car['lng']
        else:
            user = None
        return render_template("employee/update_car.html", form=form, models=models)
    return redirect(url_for('site.home'))


@site.route("/view_users")
def view_users():
    if 'user' in session and session['user']['type'] == 'ADMIN':
        result = requests.get("{}{}".format(URL, "/users"))
        if result.status_code == 200:
            try:
                users = result.json()
            except JSONDecodeError as je:
                users = None
        else:
            users = None
        return render_template("employee/users.html", users=users)
    return redirect(url_for('site.home'))


@site.route("/edit_user", methods=['GET', 'POST'])
def render_edit_user():
    form = UpdateUserForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = {
            'existing_username': form.existing_username.data,
            'username': form.username.data,
            'email': form.email.data,
            'l_name': form.last_name.data,
            'f_name': form.first_name.data,
            'password': form.password.data,
        }
        result = requests.put(
            "{}{}".format(URL, "/user"),
            json=json.dumps(user),
            params={"update": True}
        )
        print(result)
        if result.status_code == 200:
            return redirect(url_for("site.view_users"))
    if 'user' in session and session['user']['type'] == 'ADMIN':
        user_id = request.args.get("user_id")
        if user_id is not None:
            result = requests.get("{}{}".format(URL, "/user"), params={"user_id": user_id})
            user = result.json()
            form.existing_username.data = user['username']
            form.username.data = user['username']
            form.email.data = user['email']
            form.first_name.data = user['f_name']
            form.last_name.data = user['l_name']
        else:
            user = None
        print(user)
        return render_template("employee/update_user.html", form=form)
    return redirect(url_for('site.home'))


@site.route("/view_employees", methods=['GET'])
def render_view_employees():
    if 'user' in session and session['user']['type'] == 'ADMIN':
        result = requests.get("{}{}".format(URL, "/employees"))
        if result.status_code == 200:
            try:
                employees = result.json()
            except JSONDecodeError as je:
                employees = None
        else:
            employees = None
        return render_template("employee/employees.html", employees=employees)
    return redirect(url_for('site.home'))


@site.route("/edit_employee", methods=['GET', 'POST'])
def render_edit_employee():
    form = UpdateEmployeeForm()
    if request.method == 'POST' and form.validate_on_submit():
        employee = {
            'existing_username': form.existing_username.data,
            'username': form.username.data,
            'email': form.email.data,
            'l_name': form.last_name.data,
            'f_name': form.first_name.data,
            'password': form.password.data,
            'type': form.type.data
        }
        result = requests.put(
            "{}{}".format(URL, "/employee"),
            json=json.dumps(employee),
            params={"update": True}
        )
        print(result)
        if result.status_code == 200:
            return redirect(url_for("site.render_view_employees"))
    if 'user' in session and session['user']['type'] == 'ADMIN':
        employee_id = request.args.get("employee_id")
        if employee_id is not None:
            result = requests.get("{}{}".format(URL, "/employee"), params={"employee_id": employee_id})
            employee = result.json()
            form = UpdateEmployeeForm(type=employee['type'])
            form.existing_username.data = employee['username']
            form.username.data = employee['username']
            form.email.data = employee['email']
            form.first_name.data = employee['f_name']
            form.last_name.data = employee['l_name']
        else:
            employee = None
        print(employee)
        return render_template("employee/update_employee.html", form=form)
    return redirect(url_for('site.home'))


@site.route("/engineer")
def engineer_dashboard():
    if 'user' in session and session['user']['type'] == 'ENGINEER':
        result = requests.get("{}{}".format(URL, "/reports"), params={"resolved": 0})
        if result.status_code == 200:
            try:
                data = result.json()
                markers = []
                for i in range(len(data)):
                    item = data[i]
                    markers.append(
                        {
                            "infobox": "<h5>{}:</h5><p>{} {} {}<br>"
                                       "<small class='text-muted'>Details: {}</small></p>".format(
                                item['car_id'], item['car']['model']['year'], item['car']['model']['make'],
                                item['car']['model']['model'], item['details']),
                            "lat": item['car']['lat'],
                            "lng": item['car']['lng']
                        }
                    )
            except JSONDecodeError as je:
                markers = []
                data = None
        else:
            markers = []
            data = None
        car_map = Map(
            identifier="view-side",
            lat=-37.781255,
            lng=145.135217,
            zoom=9,
            style="height:600px;width:100%;margin:0;padding:0;",
            markers=markers
        )
        return render_template("employee/engineer.html", user=session['user'], reports=data, map=car_map)
    return redirect(url_for("site.home"))


@site.route("/logout")
def logout():
    """Logs the user out of MP web app

    Returns:
        redirects to site.login
    """
    session.pop('user', None)  # Remove user from session
    return redirect(url_for('site.home'))
