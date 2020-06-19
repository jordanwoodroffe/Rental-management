"""
MP Employee Web App

website.py renders html templates and handles page endpoints.
It handles login functionality and input validation, redirecting each type of employee to the correct website. Data
is retrieved from
"""
from customer_app.website import LoginForm, make_attributes, valid_name, RegistrationForm, CreateReportForm
import json
from json.decoder import JSONDecodeError
from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_wtf import FlaskForm
import re
import requests
from wtforms import StringField, SelectField, HiddenField, FloatField, IntegerField, Field
from wtforms.validators import InputRequired, Length, ValidationError
import datetime
from dateutil.relativedelta import *
from environs import Env

site = Blueprint("site", __name__)

URL = "http://127.0.0.1:5000"

env = Env()
env.read_env()

PUSH_BULLET_TOKEN = env("PUSH_BULLET_TOKEN")  # Pushbullet Access Token: required in order to send a notification
GOOGLE_MAPS_KEY = env("GOOGLE_MAPS_KEY")


# noinspection PyUnusedLocal
def valid_lat(form, field: Field):
    """form validation method for a cars lat value (in range -90 and +90)"""
    if float(field.data) < -90 or float(field.data) > 90:
        raise ValidationError("Latitude value must be between -90 and +90")


# noinspection PyUnusedLocal
def valid_lng(form, field: Field):
    """form validation method for a cars lng value (in range -180 and +180)"""
    if float(field.data) < -180 or float(field.data) > 180:
        raise ValidationError("Longitude value must be between -180 and +180")


# noinspection PyUnusedLocal
def valid_cph(form, field: Field):
    """form validation method for verifying a cars cph value (is > 0)"""
    if float(field.data) <= 0:
        raise ValidationError("Cph value must be > 0")


# noinspection PyUnusedLocal
def valid_rego(form, field: Field):
    """form validation method for verifying a car_id/rego against a regex pattern (alphanumeric)"""
    if not re.match("[A-Za-z0-9]", field.data):
        raise ValidationError("Rego value must be alphanumeric")


# noinspection PyUnusedLocal
def valid_mac_address(form, field: Field):
    """form validation method for verifying a mac address against a regex pattern
    (12 hexadecimal chars separated by : or -)
    """
    if len(field.data) > 0 and not re.match("^([0-9a-fA-F]{2}[:-]){5}([0-9a-fA-F]{2})$", field.data):
        raise ValidationError("Invalid mac address: must be 12 hexadecimal charaters separated by : or -"
                              "<br>for example 98:9E:63:37:A9:8F or 98-9E-63-37-A9-8F")


# noinspection PyUnusedLocal
def valid_make_model(form, field: Field):
    """form validation method for car model make/model attributes: alphanumeric and some special chars"""
    if not re.match("^[0-9A-Za-z ]+-?[0-9A-Za-z ]+$", field.data):
        raise ValidationError("Invalid value - must contain alphanumeric characters")


# noinspection PyUnusedLocal
def valid_year(form, field: Field):
    """form validation method for car model year attribute: 1900 or 2000's only"""
    if not (1900 <= int(field.data) <= 2999):
        raise ValidationError("Year must be within 1900-2999")


# noinspection PyUnusedLocal
def valid_capacity(form, field: Field):
    """form validation method for car model capacity: must be between 2 and 6"""
    if not (2 <= int(field.data) <= 6):
        raise ValidationError("Capcity must be between 2 and 6")


# noinspection PyUnusedLocal
def valid_weight(form, field: Field):
    """form validation method for car model weight: must be between 950 and 2300kg"""
    if not (950 <= int(field.data) <= 2300):
        raise ValidationError("Weight must be between 950 and 2300 kg")


# noinspection PyUnusedLocal
def valid_length(form, field: Field):
    """form validation method for car model length: must be between 3 and 5 metres"""
    if not (3 <= int(field.data) <= 5):
        raise ValidationError("Length must be between 3 and 5 metres")


# noinspection PyUnusedLocal
def valid_load_index(form, field: Field):
    """form validation method for car model load index: must be between 75 and 100"""
    if not (75 <= int(field.data) <= 100):
        raise ValidationError("Load index must be between 75 and 100")


# noinspection PyUnusedLocal
def valid_engine_capacity(form, field: Field):
    """form validation method for car model engine capacity: must be between 1 and 4 litres"""
    if not (1 <= int(field.data) <= 4):
        raise ValidationError("Engine capacity must be between 1 and 4 litres")


# noinspection PyUnusedLocal
def valid_ground_clearance(form, field: Field):
    """form validation method for car model ground clearance: must be between 100 and 250mm"""
    if not (100 <= int(field.data) <= 250):
        raise ValidationError("Ground clearance must be between 100 and 250mm")


class UpdateUserForm(RegistrationForm):
    """UpdateUserForm form to update user details - inherits attributes from :class:`RegistrationForm`"""
    existing_username = HiddenField("Existing Username")


class CreateEmployeeForm(RegistrationForm):
    """Form to create a new employee"""
    type = SelectField('Type', choices=[('ADMIN', 'Admin'), ('ENGINEER', 'Engineer'), ('MANAGER', 'Manager')])
    mac_address = StringField('Mac Address (Bluetooth ID)', validators=[
        Length(0, 17, message="mac address must be 17 characters long"), valid_mac_address
    ], render_kw={"placeholder": "No mac address"})


class UpdateEmployeeForm(CreateEmployeeForm):
    """Form to update employee details - inherits attributes from :class:`CreateEmployeeForm`"""
    existing_username = HiddenField("Existing Username")


class CreateCarForm(FlaskForm):
    """Form for creating a new vehicle"""
    car_id = StringField('Rego', validators=[InputRequired(), Length(6, 6, message="Rego must be 6 characters")])
    name = StringField('Name', validators=[InputRequired(), valid_name])
    cph = FloatField('Cost per hour', validators=[InputRequired(), valid_cph])
    lat = FloatField('Latitude', validators=[InputRequired(), valid_lat])
    lng = FloatField('Longitude', validators=[InputRequired(), valid_lng])
    model_id = SelectField('Model', validators=[InputRequired()], id="model_id", coerce=int)

    def __init__(self, models: [], *args, **kwargs):
        super(CreateCarForm, self).__init__(*args, **kwargs)
        if models is not None:
            self.model_id.choices = [
                (model["model_id"], "{} {} {}".format(model["year"], model["make"], model["model"])) for model in models
            ]


class UpdateCarForm(CreateCarForm):
    """Form for updating a vehicle, inherits attributes from :class:`CreateCarForm`"""
    existing_car_id = HiddenField("Existing CarID")


class CarModelForm(FlaskForm):
    """Form for creating a new vehicle model (car_model) - a car_model instance is a foreign key attribute of car,
    listing mechanical/technical details (make, model, transmission etc)"""
    make = StringField('Make', validators=[InputRequired(), valid_make_model])
    model = StringField('Model', validators=[InputRequired(), valid_make_model])
    year = IntegerField('Year', validators=[InputRequired(), valid_year])
    capacity = IntegerField('Capacity', validators=[InputRequired(), valid_capacity])
    colour = StringField('Colour', validators=[InputRequired()])
    transmission = SelectField('Transmission', validators=[InputRequired()],
                               choices=[('Auto', 'Auto'), ('Manual', 'Manual')])
    weight = IntegerField('Weight', validators=[InputRequired(), valid_weight])
    length = FloatField('Length', validators=[InputRequired(), valid_length])
    load_index = IntegerField('Load index', validators=[InputRequired(), valid_load_index])
    engine_capacity = FloatField('Engine capacity', validators=[InputRequired(), valid_engine_capacity])
    ground_clearance = IntegerField('Ground clearance', validators=[InputRequired(), valid_ground_clearance])


class UpdateCarModelForm(CarModelForm):
    """Form for updating a vehicle, inherits attributes from :class:`CarModelForm` appending the existing model_id"""
    model_id = HiddenField('model_id')


# noinspection DuplicatedCode
@site.route("/", methods=['POST', 'GET'])
def home():
    """Authenticates a user when they log in to the MP employee web app

    Returns:
        redirect site.main or if user successfully authenticated
        or renders login.html on load, with error messages if incorrect login attempt
    """
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
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
    return render_template("login.html", form=form, login_type="Employee")


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
            return redirect(url_for("site.manager_dashboard"))
    return redirect(url_for("site.home"))


@site.route("/history", methods=['GET'])
def rental_history():
    """Renders the rental history page - Admin can browse all bookings

    Returns:
        renders history.html with a list of bookings and search fields (status, user, car)
    """
    if 'user' in session and session['user']['type'] == "ADMIN":
        result = requests.get("{}{}".format(URL, "/bookings"))
        try:
            bookings_data = result.json()
        except JSONDecodeError:
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
            "{}{}".format(URL, "/cars"),
            params={"car_reports": True}
        )  # Retrieve all cars in car table
        reports = requests.get(
            "{}{}".format(URL, "/reports", params={"resolved": 0})
        )
        if cars.status_code == 200:
            try:
                car_data = cars.json()
                reports_data = reports.json()
                append_reports(car_data, reports_data)
            except JSONDecodeError:
                attributes = None
                car_data = None
            else:
                attributes = make_attributes(car_data)  # Get cars's attributes to send to front-end for filter
        else:
            attributes = None
            car_data = None
        messages = session.pop('messages') if 'messages' in session else None
        return render_template("employee/vehicles.html", cars=car_data, attributes=attributes, messages=messages)
    return redirect(url_for('site.home'))


def append_reports(car_data, reports_data):
    """Append repair records to vehicles in order to display repair status to the admin while browsing vehicles.html

    Args:
        car_data: list of cars from cloud database
        reports_data: list of repairs from cloud database

    Returns:
        list: cars matched with corresponding repair status (True if a repair exists for a vehicle)
    """
    for car in car_data:
        for report in reports_data:
            if report['car']['car_id'] == car['car_id'] and int(report['resolved']) == 0:
                car['repairs'] = True
                break


@site.route("/edit_car", methods=['GET', 'POST'])
def render_edit_car():
    """Renders the edit car form - Admin may update any car details, including the model

    Args:
        car_id: id of car to preload form with (attributes are set to existing values)

    Returns:
        renders update_car.html with attributes set to existing values for a vehicle
    """
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
            'model_id': form.model_id.data,
            'name': form.name.data
        }
        result = requests.put("{}{}".format(URL, "/update_car"), json=json.dumps(car))
        if result.status_code == 200:
            session['messages'] = [(
                "success",
                {
                    "message": "Car successfully updated",
                    "data": "Registration number: {}".format(form.car_id.data)
                }
            )]
            return redirect(url_for("site.search_cars"))
        else:
            form.car_id.errors.append(result.text)
            return render_template("employee/update_car.html", form=form, models=models, method="Update")
    if 'user' in session and session['user']['type'] == 'ADMIN':
        car_id = request.args.get("car_id")
        if car_id is not None:
            result = requests.get("{}{}".format(URL, "/car"), params={"car_id": car_id})
            if result.status_code == 200:
                car = result.json()
                form = UpdateCarForm(models=models, model_id=car['model_id'])
                form.existing_car_id.data = car['car_id']
                form.car_id.data = car['car_id']
                form.cph.data = car['cph']
                form.lat.data = car['lat']
                form.lng.data = car['lng']
                form.name.data = car['name']
        return render_template("employee/update_car.html", form=form, models=models, method="Update")
    return redirect(url_for('site.home'))


@site.route("/create_vehicle", methods=['GET', 'POST'])
def render_create_vehicle():
    """Renders the create vehicle form - Admin may create a new vehicle, entering any valid attributes/exsiting model.
    Upon validation, it submits the data to the database :class:`api`

    Returns:
        renders update_car.html form for Admin to create new vehicle
    """
    models = requests.get("{}{}".format(URL, "/car_models"))
    models = models.json()
    form = CreateCarForm(models=models)
    if request.method == 'POST' and form.validate_on_submit():
        car = {
            'car_id': form.car_id.data,
            'cph': form.cph.data,
            'lat': form.lat.data,
            'lng': form.lng.data,
            'model_id': form.model_id.data,
            'name': form.name.data
        }
        result = requests.post(
            "{}{}".format(URL, "/car"),
            json=json.dumps(car),
        )
        if result.status_code == 200:
            session['messages'] = [(
                "success",
                {
                    "message": "Car successfully created",
                    "data": "Registration number: {}".format(form.car_id.data)
                }
            )]
            return redirect(url_for("site.search_cars"))
        else:
            form.car_id.errors.append(result.text)
    if 'user' in session and session['user']['type'] == 'ADMIN':
        return render_template("employee/update_car.html", form=form, models=models, method="Create")
    return redirect(url_for('site.home'))


@site.route("/remove_car", methods=['POST'])
def remove_car():
    """Removes a car from the database: Admin can select 'remove' for any vehicle, and remove from database via
    :class:`api`

    Returns:
        presents alert message for corresponding success/error
    """
    if 'user' in session and session['user']['type'] == 'ADMIN':
        car_id = request.args.get('car_id')
        err = "Missing car_id parameter"
        if car_id is not None:
            result = requests.delete(
                "{}{}".format(URL, "/car"),
                params={"car_id": car_id}
            )
            if result.status_code == 200:
                session['messages'] = [(
                    "success",
                    {
                        "message": "Car successfully removed",
                        "data": "Registration number: {}".format(car_id)
                    }
                )]
                return redirect(url_for("site.search_cars"))
            else:
                err = result.text
        session['messages'] = [(
            "warning",
            {
                "message": "Car unable to be removed",
                "data": "Registration number: {}".format(car_id),
                "error": err
            }
        )]
        return redirect(url_for("site.search_cars"))
    return redirect(url_for('site.home'))


@site.route("/view_reports", methods=['GET'])
def view_reports():
    """Renders a list of repair reports on the Admin MP app

    Returns:
        renders reports.html, displaying a list of repair reports and filters (status, notification, car_id)
    """
    if 'user' in session and session['user']['type'] == 'ADMIN':
        result = requests.get("{}{}".format(URL, "/reports"))
        if result.status_code == 200:
            try:
                reports = result.json()
            except JSONDecodeError:
                reports = None
        else:
            reports = None
        messages = session.pop('messages') if 'messages' in session else None
        return render_template("employee/reports.html", reports=reports, messages=messages)
    return redirect(url_for('site.home'))


@site.route("/remove_report", methods=['GET'])
def remove_report():
    """Allows an Admin user to dismiss a report - upon successful deletion sends notification to engineers

    Returns:
        corresponding success/error message after calling :class:`api` endpoint
    """
    if 'user' in session and session['user']['type'] == 'ADMIN':
        report_id = request.args.get('report_id')
        if report_id is not None:
            result = requests.delete(
                "{}{}".format(URL, "/report"),
                params={"report_id": report_id}
            )
            if result.status_code == 200:
                data = result.json()
                cancel_repair_notification(data)  # send cancellation notifation to engineers
                session['messages'] = [(
                    "success",
                    {
                        "message": "Report for {} successfully removed".format(data['car']['car_id']),
                        "data": "\"{}\"".format(data['details'])
                    }
                )]
            else:
                session['messages'] = [(
                    "warning",
                    {
                        "message": "Car report unable to be removed",
                        "data": "",
                        "error": result.text
                    }
                )]
        return redirect(url_for('site.view_reports'))
    return redirect(url_for('site.home'))


@site.route("/report_car", methods=['GET', 'POST'])
def report_car():
    """Report a car: renders a form for an admin to create a repair request, and upon successful validation submits
    report data to the database via :class:`api`, finally attempts to alert engineers via
    :func:`employee_app.website.send_repair_notification`

    Args:
        car_id: id of selected car (repair request is for this vehicle)

    Returns:
        renders report_car.html with car id/rego preset
    """
    form = CreateReportForm()
    choices = ['High', 'Medium', 'Low']
    if request.method == 'POST' and form.validate_on_submit():
        report = {
            'car_id': form.car_id.data,
            'details': form.details.data,
            'priority': form.priority.data,
            'report_date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        result = requests.post("{}{}".format(URL, "/report"), json=json.dumps(report))
        if result.status_code == 200:
            data = result.json()
            send_repair_notification(data, data['report_id'])
        else:
            session['messages'] = [(
                "danger",
                {
                    "message": "Unable to create report",
                    "data": "Error occurred while attempting to create report",
                    "error": result.text
                }
            )]
        return redirect(url_for('site.view_reports'))
    if 'user' in session and session['user']['type'] == 'ADMIN':
        car_id = request.args.get("car_id")
        if car_id is not None:
            form.car_id.data = car_id
        return render_template("employee/report_car.html", form=form, choices=choices)
    return redirect(url_for('site.home'))


@site.route("/alert_report", methods=['GET'])
def alert_report(param_report_id=None):
    """Sends a Pushbullet notification alert upon a repair being raised. This can be actioned by an Admin user creating
    a new report, or by an Admin user approving/raising a User generated report.
    :func:`employee_app.website.send_repair_notification` carries out the pushbullet functionality

    Args:
        param_report_id: optional parameter when calling functionality by method
        report_id: id of report to notify

    Returns:
        Sends Pushbullet notification, and presents corresponding success/error message on web app
    """
    if 'user' in session and session['user']['type'] == 'ADMIN':
        report_id = request.args.get('report_id')
        if report_id is None:
            report_id = param_report_id
        if report_id is not None:
            result = requests.get(
                "{}{}".format(URL, "/report"),
                params={"report_id": report_id}
            )
            if result.status_code == 200:
                data = result.json()
                send_repair_notification(data, report_id)
            else:
                session['messages'] = [(
                    "danger",
                    {
                        "message": "Unable to retrieve report",
                        "data": "Error occurred while attempting to retrieve report",
                        "error": result.text
                    }
                )]
        return redirect(url_for('site.view_reports'))
    return redirect(url_for('site.home'))


def send_repair_notification(data: [], report_id):
    """Helper function to send Pushbullet notification: used when Admin creates or raises a repair request

    Args:
        report_id: id of report being notified
        data: json data of car repair being raised

    Returns:
        boolean value indicating if report was sent succesfully
    """
    message = "Car: {} - {} {} {}\nReported at: {}\nDetails: {}".format(
        data['car']['car_id'], data['car']['model']['make'], data['car']['model']['model'],
        data['car']['model']['year'], data['report_date'].replace("T", " "), data['details']
    )  # message body - contains description of vehicle and repair required
    data_send = {
        "type": "link",
        "title": "New {} priority repair".format(data['priority']),
        "body": message,
        "url": "https://www.google.com/maps/search/?api=1&query={},{}".format(
            data['car']['lat'], data['car']['lng'])
    }  # message to send - includes title with repair priority, and a link to a google map marking the location
    resp = requests.post(
        'https://api.pushbullet.com/v2/pushes',
        data=json.dumps(data_send),
        headers={
            'Authorization': 'Bearer ' + PUSH_BULLET_TOKEN,
            'Content-Type': 'application/json'
        }
    )
    result = resp.status_code == 200
    if result:  # append success notification to session
        session['messages'] = [(
            "success",
            {
                "message": "Report created and raised for {}".format(data['car']['car_id']),
                "data": "New report created: \"{}\"".format(data['details']),
                "error": "Notification sent to engineers"
            }
        )]
        requests.put("{}{}".format(URL, "/report_notification"), params={"notification": 1, "report_id": report_id})
    else:  # append error notification to session
        session['messages'] = [(
            "warning",
            {
                "message": "Report created for {}".format(data['car']['car_id']),
                "data": "New report created {}".format(data['details']),
                "error": "Unable to send notification"
            }
        )]
    return result


def cancel_repair_notification(data: []):
    """Attempts to send a cancellation notification for a repair (if dismissed by an Admin user). There is no return or
    response handling as this is additional/extra functionality, and amending or deleting actual records occurs
    elsewhere (i.e. this is an optional step in the remove_repair flow)

    Args:
        data: data to be sent (repair/car info)

    Returns:
        None
    """
    message = "Car: {} - {} {} {}\nDetails: {}".format(
        data['car']['car_id'], data['car']['model']['make'], data['car']['model']['model'],
        data['car']['model']['year'], data['details']
    )  # message body contains car information and repair details
    data_send = {
        "type": "note",
        "title": "CANCELLED REPAIR",
        "body": message
    }
    requests.post(
        'https://api.pushbullet.com/v2/pushes',
        data=json.dumps(data_send),
        headers={
            'Authorization': 'Bearer ' + PUSH_BULLET_TOKEN,
            'Content-Type': 'application/json'
        }
    )  # send cancellation message


@site.route("/view_users")
def view_users():
    """Presents a list of customers to the Admin, along with a search field (any customer attributes). Optionally, the
    Admin can select to remove or update a user, or manually create a new user.

    Returns:
        renders users.html (list of customers)
    """
    if 'user' in session and session['user']['type'] == 'ADMIN':
        result = requests.get("{}{}".format(URL, "/users"))
        if result.status_code == 200:
            try:
                users = result.json()
            except JSONDecodeError:  # unable to get user details (none in database)
                users = None
        else:
            users = None
        messages = session.pop('messages') if 'messages' in session else None
        return render_template("employee/users.html", users=users, messages=messages)
    return redirect(url_for('site.home'))


@site.route("/edit_user", methods=['GET', 'POST'])
def render_edit_user():
    """Renders the edit user page - Admin can change any customer attributes

    Args:
        user_id: id of user to edit

    Returns:
        renders update_user.html, with existing attributes
    """
    form = UpdateUserForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = {
            'existing_username': form.existing_username.data,
            'username': form.username.data,
            'email': form.email.data,
            'l_name': form.last_name.data,
            'f_name': form.first_name.data,
            'password': form.password.data,
        }  # get new input values
        result = requests.put(
            "{}{}".format(URL, "/user"),
            json=json.dumps(user),
            params={"update": True}
        )
        if result.status_code == 200:  # add success message to session (display alert)
            session['messages'] = [(
                "success",
                {
                    "message": "Customer successfully updated",
                    "data": "{} {} (@{})".format(form.first_name.data, form.last_name.data, form.username.data)
                }
            )]
        else:  # add error message to session (display alert)
            session['messages'] = [(
                "warning",
                {
                    "message": "Customer unable to be updated",
                    "data": "{} {} (@{})".format(form.first_name.data, form.last_name.data, form.username.data),
                    "error": result.text
                }
            )]
        return redirect(url_for("site.view_users"))
    if 'user' in session and session['user']['type'] == 'ADMIN':
        user_id = request.args.get("user_id")
        if user_id is not None:
            result = requests.get("{}{}".format(URL, "/user"), params={"user_id": user_id})
            if result.status_code == 200:  # append existing values to the form
                user = result.json()
                form.existing_username.data = user['username']
                form.username.data = user['username']
                form.email.data = user['email']
                form.first_name.data = user['f_name']
                form.last_name.data = user['l_name']
        return render_template("employee/update_user.html", form=form, method="Update")
    return redirect(url_for('site.home'))


@site.route("/create_user", methods=['GET', 'POST'])
def create_user():
    """Renders the create user page - Admin can generate a new customer (fallback for A2 Registration - i.e. if errors/
    customer issues when registering)

    Returns:
        renders update_user.html with no prefilled attributes, and submits data to :class:`api` upon validation. After
        response received from API, MP app displays a corresponding alert message (success/error)
    """
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = {
            'username': form.username.data,
            'email': form.email.data,
            'l_name': form.last_name.data,
            'f_name': form.first_name.data,
            'password': form.password.data
        }  # get input values
        result = requests.post(
            "{}{}".format(URL, "/user"),
            json=json.dumps(user),
        )
        if result.status_code == 200:
            session['messages'] = [(
                "success",
                {
                    "message": "Customer successfully updated",
                    "data": "{} {} (@{})".format(form.first_name.data, form.last_name.data, form.username.data)
                }
            )]
            return redirect(url_for("site.view_users"))
        elif result.status_code == 404:
            form.username.errors.append('This username has been used for register before')
        else:
            session['messages'] = [(
                "warning",
                {
                    "message": "Customer unable to be updated",
                    "data": "{} {} (@{})".format(form.first_name.data, form.last_name.data, form.username.data),
                    "error": result.text
                }
            )]
            return redirect(url_for("site.view_users"))
    if 'user' in session and session['user']['type'] == 'ADMIN':
        return render_template("employee/update_user.html", form=form, method="Create")
    return redirect(url_for('site.home'))


@site.route("/remove_user", methods=['POST'])
def remove_user():
    """Allows admin to remove a user

    Args:
        user_id: id of user to remove

    Returns:
        corresponding success/error message after response receveied from :class:`api`
    """
    if 'user' in session and session['user']['type'] == 'ADMIN':
        user_id = request.args.get('user_id')
        err = "Missing user_id parameter"
        if user_id is not None:
            result = requests.delete(
                "{}{}".format(URL, "/user"),
                params={"user_id": user_id}
            )
            if result.status_code == 200:  # add success message to session (display alert)
                session['messages'] = [(
                    "success",
                    {
                        "message": "User successfully removed",
                        "data": "@{}".format(user_id)
                    }
                )]
                return redirect(url_for("site.view_users"))
            else:
                err = result.text
        session['messages'] = [(
            "warning",
            {
                "message": "User unable to be removed",
                "data": "@{}".format(user_id),
                "error": err
            }
        )]  # add error message to session (display alert)
        return redirect(url_for("site.view_users"))
    return redirect(url_for('site.home'))


@site.route("/view_employees", methods=['GET'])
def render_view_employees():
    """Displays a list of employees to the Admin. Optionally, the Admin can select to remove or update an existing
    employee, or generate a new employee.

    Returns:
        renders employees.html (list of employees)
    """
    if 'user' in session and session['user']['type'] == 'ADMIN':
        result = requests.get("{}{}".format(URL, "/employees"))
        if result.status_code == 200:
            try:
                employees = result.json()
            except JSONDecodeError:  # no employees found in database (displays corresponding message in template)
                employees = None
        else:
            employees = None
        messages = session.pop('messages') if 'messages' in session else None
        return render_template("employee/employees.html", employees=employees, messages=messages)
    return redirect(url_for('site.home'))


@site.route("/edit_employee", methods=['GET', 'POST'])
def render_edit_employee():
    """Renders the edit employee page for Admin to update any attributes

    Args:
        employee_id: id of employee to update

    Returns:
        renders update_employee.html with attributes set to existing values
    """
    form = UpdateEmployeeForm()
    if request.method == 'POST' and form.validate_on_submit():
        employee = {
            'existing_username': form.existing_username.data,
            'username': form.username.data,
            'email': form.email.data,
            'l_name': form.last_name.data,
            'f_name': form.first_name.data,
            'password': form.password.data,
            'type': form.type.data,
            'mac_address': form.mac_address.data
        }  # retrieve updated details from form
        result = requests.put(
            "{}{}".format(URL, "/employee"),
            json=json.dumps(employee),
            params={"update": True}
        )
        if result.status_code == 200:  # add success message to session (display alert)
            session['messages'] = [(
                "success",
                {
                    "message": "Employee successfully updated",
                    "data": "{} {} (@{})".format(form.first_name.data, form.last_name.data, form.username.data)
                }
            )]
        else:  # add error message to session (display alert)
            session['messages'] = [(
                "success",
                {
                    "message": "Employee unable to be updated",
                    "data": "{} {} (@{})".format(form.first_name.data, form.last_name.data, form.username.data),
                    "error": result.text
                }
            )]
        return redirect(url_for("site.render_view_employees"))
    if 'user' in session and session['user']['type'] == 'ADMIN':
        employee_id = request.args.get("employee_id")
        if employee_id is not None:
            result = requests.get("{}{}".format(URL, "/employee"), params={"employee_id": employee_id})
            if result.status_code == 200:  # append existing details to form
                employee = result.json()
                form = UpdateEmployeeForm(type=employee['type'])
                form.existing_username.data = employee['username']
                form.username.data = employee['username']
                form.email.data = employee['email']
                form.first_name.data = employee['f_name']
                form.last_name.data = employee['l_name']
                if employee['mac_address'] is not None:
                    form.mac_address.data = employee['mac_address']
        return render_template("employee/update_employee.html", form=form, method="Update")
    return redirect(url_for('site.home'))


@site.route("/create_employee", methods=['GET', 'POST'])
def create_employee():
    """Allows Admin to create a new employee

    Returns:
        renders the update_employee.html page without any attributes set. Upon validaation, submits data to :class:`api`
        and upon api response the web app displays a success/error message
    """
    form = CreateEmployeeForm()
    if request.method == 'POST' and form.validate_on_submit():
        employee = {
            'username': form.username.data,
            'email': form.email.data,
            'l_name': form.last_name.data,
            'f_name': form.first_name.data,
            'password': form.password.data,
            'type': form.type.data,
            'mac_address': form.mac_address.data
        }  # retrieve employee details from form
        result = requests.post(
            "{}{}".format(URL, "/employee"),
            json=json.dumps(employee),
            params={"update": True}
        )
        if result.status_code == 200:  # add success message to session (display alert)
            session['messages'] = [(
                "success",
                {
                    "message": "Employee successfully created",
                    "data": "{} {} (@{})".format(form.first_name.data, form.last_name.data, form.username.data)
                }
            )]
        else:  # add error message to session (display alert)
            session['messages'] = [(
                "warning",
                {
                    "message": "Unable to create new employee",
                    "data": "{} {} (@{})".format(form.first_name.data, form.last_name.data, form.username.data),
                    "error": result.text
                }
            )]
        return redirect(url_for("site.render_view_employees"))
    if 'user' in session and session['user']['type'] == 'ADMIN':
        return render_template("employee/update_employee.html", form=form, method="Create")
    return redirect(url_for('site.home'))


@site.route("/remove_employee", methods=['POST'])
def remove_employee():
    """Allows Admin user to remove employee from the database

    Args:
        employee_id: id of employee to remove

    Returns:
        corresponding success/error message upon response from :class:`api`
    """
    if 'user' in session and session['user']['type'] == 'ADMIN':
        employee_id = request.args.get('employee_id')
        err = "Missing employee_id parameter"
        if employee_id == session['user']['username']:  # an Admin user cannot delete themselves
            err = "{} is unable to delete themselves".format(session['user']['username'])
        elif employee_id is not None:
            result = requests.delete(
                "{}{}".format(URL, "/employee"),
                params={"employee_id": employee_id}
            )
            if result.status_code == 200:  # add success message to session (display alert)
                session['messages'] = [(
                    "success",
                    {
                        "message": "Employee successfully removed",
                        "data": "@{}".format(employee_id)
                    }
                )]
                return redirect(url_for("site.render_view_employees"))
            else:
                err = result.text
        session['messages'] = [(
            "warning",
            {
                "message": "Employee unable to be removed",
                "data": "@{}".format(employee_id),
                "error": err
            }
        )]  # add error message to session (display alert)
        return redirect(url_for("site.render_view_employees"))
    return redirect(url_for('site.home'))


@site.route("/manager")
def manager_dashboard():
    """Renders the Company Manager Visualisations dashboard - displays key business metrics indicating current revenue,
    new users, and status of the vehicle fleet.

    Returns:
        renders manager.html, with updated data fetched via REST api from :class:`api`
    """
    if 'user' in session and session['user']['type'] == 'MANAGER':
        today = datetime.datetime.today()
        # Bookings related queries
        revenue = 0
        last_month_revenue = 0
        bookings_num = 0
        last_bookings_num = 0
        month_revenue = []
        result = requests.get("{}{}".format(URL, "/bookings"))
        try:
            bookings_data = result.json()
        except JSONDecodeError:
            bookings_data = None
        if bookings_data is not None:
            month_revenue = [0 for _ in range(today.day)]
            for booking in bookings_data:
                date = datetime.datetime.strptime(booking["booking_date"], "%Y-%m-%dT%H:%M:%S")
                if date.year == today.year and date.month == today.month:
                    revenue += int(booking["cost"])
                    month_revenue[date.day - 1] += int(booking["cost"])
                    bookings_num += 1
                elif date.year == today.year and (date + relativedelta(months=1)).month == today.month:
                    last_month_revenue += int(booking["cost"])
                    last_bookings_num += 1

        if last_month_revenue is not 0:
            revenue_grow = int((revenue / last_month_revenue) * 100 - 100)
            booking_grow = int((bookings_num / last_bookings_num) * 100 - 100)
        else:
            revenue_grow = 100
            booking_grow = 100

        # Users related queries
        today_year, today_week_num, today_DOW = today.isocalendar()
        last_five_week_users = [0, 0, 0, 0, 0]
        current_month_users = 0
        last_month_users = 0
        result = requests.get("{}{}".format(URL, "/users"))
        try:
            users_data = result.json()
        except JSONDecodeError:
            users_data = None
        if users_data is not None:
            for user in users_data:
                reg_date = datetime.datetime.strptime(user["register_date"], "%Y-%m-%dT%H:%M:%S")
                if reg_date.year == today.year and reg_date.month == today.month:
                    current_month_users += 1
                elif reg_date.year == today.year and (reg_date + relativedelta(months=1)).month == today.month:
                    last_month_users += 1
                year, week_num, DOW = reg_date.isocalendar()
                if year == today_year and week_num == today_week_num:
                    last_five_week_users[4] += 1
                elif year == today_year and week_num == today_week_num - 1:
                    last_five_week_users[3] += 1
                elif year == today_year and week_num == today_week_num - 2:
                    last_five_week_users[2] += 1
                elif year == today_year and week_num == today_week_num - 3:
                    last_five_week_users[1] += 1
                elif year == today_year and week_num == today_week_num - 4:
                    last_five_week_users[0] += 1

        if last_month_users is not 0:
            user_grow = int((current_month_users / last_month_users) * 100 - 100)
        else:
            user_grow = 100
        return render_template("employee/manager.html", user=session['user'], revenue=revenue,
                               month_revenue=month_revenue, revenue_grow=revenue_grow, booking_grow=booking_grow,
                               user_grow=user_grow, last_five_week_users=last_five_week_users)
    return redirect(url_for("site.home"))


@site.route("/engineer")
def engineer_dashboard():
    """Renders the Engineer dashboard - displays a list of current repair requests, and displays repairs pinned to a map

    Returns:
        renders engineer.html with current repairs (as a list and map), and the engineer's details
    """
    if 'user' in session and session['user']['type'] == 'ENGINEER':
        result = requests.get("{}{}".format(URL, "/reports"), params={"resolved": 0})  # get all unresolved reports
        if result.status_code == 200:
            try:
                data = result.json()
            except JSONDecodeError:  # no reports found in database
                data = None
        else:
            data = None
        return render_template("employee/engineer.html", user=session['user'], reports=data, maps_key=GOOGLE_MAPS_KEY)
    return redirect(url_for("site.home"))


@site.route("/view_models", methods=['GET'])
def view_models():
    """Render the vehicle model page - Admin can browse update and create new vehicle models

    Returns:
        renders models.html with a list of models retrieved from the cloud database
    """
    if 'user' in session and session['user']['type'] == 'ADMIN':
        result = requests.get("{}{}".format(URL, "/car_models"))  # get all car_models from database
        if result.status_code == 200:
            try:
                models = result.json()
            except JSONDecodeError:  # no models found in the database
                models = None
        else:
            models = None
        # display messages (success/error on update or create)
        messages = session.pop('messages') if 'messages' in session else None
        return render_template("employee/models.html", models=models, messages=messages)
    return redirect(url_for("site.home"))


@site.route("/create_model", methods=['GET', 'POST'])
def render_create_model():
    """Renders the create vehicle model form - Admin may create a new vehicle model. Upon validation, it submits the
    data to the database :class:`api`

    Returns:
        renders update_model.html form for Admin to create new vehicle
    """
    form = CarModelForm()
    if request.method == 'POST' and form.validate_on_submit():
        model = {
            'make': form.make.data,
            'model': form.model.data,
            'year': form.year.data,
            'capacity': form.capacity.data,
            'colour': form.colour.data,
            'transmission': form.transmission.data,
            'weight': form.weight.data,
            'length': form.length.data,
            'load_index': form.load_index.data,
            'engine_capacity': form.engine_capacity.data,
            'ground_clearance': form.ground_clearance.data
        }  # retrieve model data from form
        result = requests.post("{}{}".format(URL, "/car_model"), json=json.dumps(model))
        if result.status_code == 200:  # add success message to session (display alert)
            session['messages'] = [(
                "success",
                {
                    "message": "Car model successfully created",
                    "data": "{} {} {}".format(form.year.data, form.make.data, form.model.data)
                }
            )]
        else:  # add error message to session (display alert)
            session['messages'] = [(
                "warning",
                {
                    "message": "Car model unable to be created",
                    "data": "{} {} {}".format(form.year.data, form.make.data, form.model.data),
                    "error": result.text
                }
            )]
        return redirect(url_for("site.view_models"))
    if 'user' in session and session['user']['type'] == 'ADMIN':
        return render_template("employee/update_model.html", form=form, method="Create")
    return redirect(url_for('site.home'))


@site.route("/edit_model", methods=['GET', 'POST'])
def edit_model():
    """Renders page for editing a vehicle model - Admin can update any model attributes

    Args:
        model_id: id of model to update

    Returns:
        renders update_model.html with model attributes set to existing values
    """
    form = UpdateCarModelForm()
    if request.method == 'POST' and form.validate_on_submit():
        model = {
            'model_id': form.model_id.data,
            'make': form.make.data,
            'model': form.model.data,
            'year': form.year.data,
            'capacity': form.capacity.data,
            'colour': form.colour.data,
            'transmission': form.transmission.data,
            'weight': form.weight.data,
            'length': form.length.data,
            'load_index': form.load_index.data,
            'engine_capacity': form.engine_capacity.data,
            'ground_clearance': form.ground_clearance.data
        }  # retrieve updated data from form
        result = requests.put("{}{}".format(URL, "/car_model"), json=json.dumps(model))
        if result.status_code == 200:  # add success message to session (display alert)
            session['messages'] = [(
                "success",
                {
                    "message": "Car model successfully updated",
                    "data": "{} {} {}".format(form.year.data, form.make.data, form.model.data)
                }
            )]
        else:  # add error message to session (display alert)
            session['messages'] = [(
                "warning",
                {
                    "message": "Car model unable to be updated",
                    "data": "{} {} {}".format(form.year.data, form.make.data, form.model.data),
                    "error": result.text
                }
            )]
        return redirect(url_for("site.view_models"))
    if 'user' in session and session['user']['type'] == 'ADMIN':
        model_id = request.args.get("model_id")
        if model_id is not None:
            result = requests.get("{}{}".format(URL, "/car_model"), params={"model_id": model_id})
            if result.status_code == 200:  # append existing data to form
                model = result.json()
                form = UpdateCarModelForm(transmission=model['transmission'])
                form.model_id.data = model['model_id']
                form.model.data = model['model']
                form.make.data = model['make']
                form.year.data = model['year']
                form.colour.data = model['colour']
                form.capacity.data = model['capacity']
                form.weight.data = model['weight']
                form.length.data = model['length']
                form.load_index.data = model['load_index']
                form.engine_capacity.data = model['engine_capacity']
                form.ground_clearance.data = model['ground_clearance']
        return render_template("employee/update_model.html", form=form, method="Update")
    return redirect(url_for('site.home'))


@site.route("/logout")
def logout():
    """Logs the user out of MP web app

    Returns:
        redirects to site.home
    """
    session.pop('user', None)  # Remove user from session
    return redirect(url_for('site.home'))
