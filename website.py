import json
import re
from json.decoder import JSONDecodeError

import requests
import os
from api import LOCAL_IP
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, Response
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, IntegerField, DateTimeField
from wtforms.validators import InputRequired, Email, Length, NumberRange, ValidationError
from collections import defaultdict
from datetime import datetime, timedelta
from httplib2 import Http
from oauth2client import client
from googleapiclient import discovery
from utils import allowed_file, calc_hours
from werkzeug.utils import secure_filename

site = Blueprint("site", __name__)

URL = "http://127.0.0.1:5000/"


def valid_name(form, field):
    """
    Form validation method for name fields - checks to ensure all chars are ascii and are not digits
    Args:
        form: FlaskForm to check
        field: fields to validate
    Raises:
        ValidationError: if name is invalid (not ascii or contains digit)
    """
    # names must be in ASCII
    if not field.data.isascii():
        raise ValidationError('Please enter valid name')
    # names must not contain number
    if any(char.isdigit() for char in field.data):
        raise ValidationError('Name cannot contain number')


def valid_password(form, field):
    """
    Form validation method to ensure password is correct format
    Args:
        form: FlaskForm to validate
        field: field to check

    Raises:
        ValidationError: if password is invalid (no number, no upper/lowercase, no special char)

    """
    # password must contain at least one number
    if not any(char.isdigit() for char in field.data):
        raise ValidationError('Password must contain at least one number')
    # password must contain at least one uppercase letter
    if not any(char.isupper() for char in field.data):
        raise ValidationError('Password must contain at least one uppercase letter')
    # password must contain at least one lowercase letter
    if not any(char.islower() for char in field.data):
        raise ValidationError('Password must contain at least one lowercase letter')
    # password must contain at least one special character
    regex = re.compile('[@_!#$%^&*()<>?/|}{~:]')
    if regex.search(field.data) is None:
        raise ValidationError('Password must contain at least one special character')


def validate_date(form, field):
    """
    Form validation method for date fields
    Args:
        form: FlaskForm to validate
        field: field to check

    Raises:
        ValidationError: if invalid date entry (incorrect format, or <= current datetime)

    """
    try:
        dt = datetime.strptime(field.data, "%Y-%m-%d %H:%M")
    except Exception:
        raise ValidationError('Incorrect input format. Please input as YYYY-mm-dd  HH:MM')
    else:
        if dt < datetime.now():
            raise ValidationError('Date must be later than current date')


class LoginForm(FlaskForm):
    """
    Login form to capture existing user details - rendered on login.html
    """
    email = StringField('Email', validators=[InputRequired(), Email(message="Invalid email.")])
    password = PasswordField('Password', validators=[InputRequired()])


class RegistrationForm(FlaskForm):
    """
    Registration form to capture new user details - rendered on register.html
    """
    first_name = StringField('First Name', validators=[InputRequired(), valid_name])
    last_name = StringField('Last Name', validators=[InputRequired(), valid_name])
    email = StringField('Email', validators=[InputRequired(), Email(message="Invalid email.")])
    password = PasswordField('Password', validators=[InputRequired(), Length(6, 12), valid_password])


class BookingQueryForm(FlaskForm):
    """
    Booking form to capture new booking date range information - rendered on booking.html
    """
    start = DateTimeField('Start', format="%Y-%m-%d %H:%M", validators=[InputRequired(), validate_date],
                          default=datetime.now)
    end = DateTimeField('End', format="%Y-%m-%d %H:%M", validators=[InputRequired(), validate_date],
                        default=datetime.now)


@site.route("/")
def home():
    """
    Index page for site - user can choose to login or register
    Returns:
        renders main.html if user has logged in
        renders index.html if user has not logged in
    """
    response = requests.get(
        "{}{}".format(URL, "populate")
    )
    if 'user' in session:
        return redirect(url_for("site.main"))
    return render_template("index.html")


@site.route("/login", methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        # result = db.user_authentication(form.email.data, form.password.data)
        result = requests.get(
            "{}{}".format(URL, "users/authenticate"),
            params={"user_id": form.email.data, "password": form.password.data},
        )
        data = result.json()
        if result.status_code == 200:
            session['user'] = result.json()
        elif result.status_code == 404:
            if data['error'] == 'EMAIL':
                form.email.errors.append('This email has not been registered')
            elif data['error'] == 'PASSWORD':
                form.password.errors.append('Incorrect password')
    if 'user' in session:
        return redirect(url_for("site.main"))
    return render_template("login.html", form=form)


@site.route("/register", methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        #  should be using response = requests.get(<DB_API_URL>)
        user = {'email': form.email.data,
                'l_name': form.last_name.data,
                'f_name': form.first_name.data,
                'password': form.password.data,
                }
        result = requests.post(
            "{}{}".format(URL, "user"),
            json=json.dumps(user),
        )
        if result.status_code == 200:
            return redirect(url_for("site.login"))
        elif result.status_code == 404:
            form.email.errors.append('This email has been used for register before')
    elif 'user' in session:
        return redirect(url_for("site.main"))
    return render_template("register.html", form=form)


@site.route("/main")
def main():
    if 'user' in session:
        result = requests.get("{}{}".format(URL, "/cars"), params={})
        test = result.json()
        return render_template("main.html", user=session['user'], points=json.dumps(test))
    return redirect(url_for("site.home"))


@site.route("/capture_user", methods=['POST', 'GET'])
def capture_user():
    if 'user' in session:
        if request.method == 'POST':
            # check if the post request has the file
            files = request.files.getlist("image")
            if len(files) < 5:
                flash('You need at least 5 photos to register')
                return redirect(url_for("site.main"))
            elif len(files) >= 10:
                flash('Maxium of 10 photos are accepted')
                return redirect(url_for("site.main"))
            for file in files:
                if not allowed_file(file.filename):
                    flash('Only images of extensions: txt, pdf, png, jpg, jpeg, gif are allowed')
                    return redirect(url_for("site.main"))
            directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'user_data/face_pics',
                                     session['user']['email'])
            if not os.path.exists(directory):
                os.makedirs(directory)
            for file in files:
                filename = secure_filename(file.filename)
                file.save(os.path.join(directory, filename))
            result = requests.post(
                "{}{}".format(URL, "/encode_user"),
                params={"user_id": session['user']['email'], "directory": directory}
            )
            if result.status_code == 200:
                result = requests.put(
                    "{}{}".format(URL, "/user"),
                    params={"user_id": session['user']['email'], "face_id": 1}
                )
                if result.status_code == 200:
                    try:
                        new_user = result.json()
                    except JSONDecodeError as je:
                        session['user']['face_id'] = True
                    else:
                        session['user'] = new_user
            return redirect(url_for("site.main"))
        return redirect(url_for("site.main"))
    return redirect(url_for("site.home"))


@site.route("/logout")
def logout():
    session.pop('user', None)
    return redirect(url_for('site.login'))


@site.route("/book", methods=['GET'])
def render_booking_page():
    if 'user' in session:
        start = request.args.get('start')
        end = request.args.get('end')
        form = BookingQueryForm()
        attributes = defaultdict(set)
        if start is not None and end is not None:
            try:
                start_dt = datetime.strptime(start, "%Y-%m-%d %H:%M")
                end_dt = datetime.strptime(end, "%Y-%m-%d %H:%M")
                if start_dt > end_dt:
                    raise DateException("Start date cannot be after end date")
                elif start_dt < datetime.now() or end_dt < datetime.now():
                    raise DateException("Start and end date must be after current time")
            except DateException as de:
                form.start.errors = [str(de)]
            except ValueError as ve:
                form.start.errors = ['Incorrect format', 'expected YYYY-mm-dd HH:MM']
            else:
                response = requests.get(
                    "{}{}/{}/{}".format(URL, "cars", str(start_dt).replace(" ", "T"), str(end_dt).replace(" ", "T"))
                )
                # if cars.status_code == 200:
                #     try:
                #         car_data = cars.json()
                #     except JSONDecodeError as je:
                #         attributes = None
                #         car_data = None
                #     else:
                #         for car in car_data:
                #             attributes['make'].add(car['model']['make'])
                #             attributes['colour'].add(car['model']['colour'])
                #             attributes['year'].add(car['model']['year'])
                #             attributes['capacity'].add(car['model']['capacity'])
                #             attributes['cost'].add(car['cph'])
                try:
                    cars = response.json()
                    for car in cars:
                        cph = car['cph']
                        attributes['make'].add(car['model']['make'])
                        attributes['colour'].add(car['model']['colour'])
                        attributes['year'].add(car['model']['year'])
                        attributes['capacity'].add(car['model']['capacity'])
                        attributes['cost'].add(car['cph'])
                        try:
                            amount = float(cph)
                            car['total_cost'] = float("{:.2f}".format(amount * calc_hours(d1=start_dt, d2=end_dt)))
                        except ValueError:
                            car['total_cost'] = None
                except JSONDecodeError as je:
                    cars = None
                form.start.data = start_dt
                form.end.data = end_dt
                return render_template("booking.html", form=form, cars=cars, start=start_dt, end=end_dt, attributes=attributes)
        return render_template("booking.html", form=form, attributes=attributes)
    return redirect(url_for('site.home'))


@site.route("/book", methods=['POST'])
def process_booking():
    if 'user' in session:
        car_id = request.args.get('car_id')
        start = request.args.get('start')
        end = request.args.get('end')
        messages = None
        if None not in (car_id, start, end):
            response = requests.get(
                "{}{}".format(URL, "car"), params={"car_id": car_id}
            )
            car = response.json()
            amount = float(car['cph'])
            data = {
                'start': start,
                'end': end,
                'user_id': session['user']['email'],
                'car_id': car_id,
                'event_id': None,
                'cph': amount
            }
            response = requests.post(
                "{}{}".format(URL, "booking"),
                json=json.dumps(data)
            )
            if response.status_code == 200:
                try:
                    data = response.json()
                    booking_id = data['booking_id']
                except JSONDecodeError:
                    booking_id = "JSON Decode Error"
                messages = [(
                    "success",
                    {
                        "message": "Booking successfully created!",
                        "data": "With {}\n{} - {}".format(
                            car_id, start, end
                        ),
                        "car_id": car_id,
                        "start": start,
                        "end": end,
                        "booking_id": booking_id
                    }
                )]
            else:
                messages = [(
                    "warning",
                    {
                        "message": "Booking unsuccessful",
                        "data": "Unable to create booking",
                        "error": response.text
                    }
                )]
        return render_template("booking.html", form=BookingQueryForm(), messages=messages)
    return redirect(url_for('site.home'))


@site.route("/cancel", methods=['GET'])
def render_cancel_page():
    if 'user' in session:
        bookings = requests.get(
            "{}{}".format(URL, "/bookings"), params={"user_id": session['user']["email"], "status": 0}
        )
        try:
            bookings_data = bookings.json()
        except JSONDecodeError as je:
            bookings_data = None
        messages = request.args.get('messages')
        if messages is not None:
            try:
                message_data = json.loads(messages)
            except JSONDecodeError as je:
                message_data = None
        else:
            message_data = None
        return render_template("cancel.html", user_bookings=bookings_data, messages=message_data)
    return redirect(url_for('site.home'))


@site.route("/cancel", methods=['POST'])
def cancel_booking():
    """
    TODO: separate get and post into different methods -- easier to follow logic
    TODO: api will use response objects
    Returns:

    """
    if 'user' in session:
        messages = []
        booking_id = request.args.get('booking_id')
        status = request.args.get('status')
        if None not in (booking_id, status):
            data = {
                "booking_id": booking_id,
                "status": status
            }
            response = requests.put(
                "{}{}".format(URL, "booking"),
                json=json.dumps(data)
            )
            if response.status_code == 200:
                if booking_id is not None:
                    session['cancel'] = booking_id

                if 'credentials' not in session:
                    return redirect(url_for('site.oauth2callback'))
                credentials = client.OAuth2Credentials.from_json(session['credentials'])
                if credentials.access_token_expired:
                    return redirect(url_for('site.oauth2callback'))
                else:
                    http_auth = credentials.authorize(Http())
                    service = discovery.build('calendar', 'v3', http=http_auth)

                if 'cancel' in session:
                    booking_id = session['cancel']
                    session.pop('cancel', None)
                    booking = requests.get(
                        "{}{}".format(URL, "/booking"), params={"booking_id": booking_id}
                    )
                    event_id = booking.json()['event_id']
                    if event_id is not None:
                        delete_event = service.events().delete(calendarId="primary", eventId=event_id,
                                                               sendUpdates="all").execute()
                try:
                    booking = response.json()
                    data = "With {}\n{} - {}".format(booking['car_id'], booking['start'], booking['end'])
                except JSONDecodeError:
                    data = "server error - invalid json"
                messages.append((
                    "success",
                    {
                        "message": "Booking successfully cancelled!",
                        "data": data
                    }
                ))
            else:
                messages.append((
                    "warning",
                    {
                        "message": "Unable to cancel booking",
                        "data": response.text
                    }
                ))
        return redirect(url_for('site.render_cancel_page', messages=json.dumps(messages)))
    return redirect(url_for('site.home'))


@site.route("/history")
def view_history():
    if 'user' in session:
        bookings = requests.get(
            "{}{}".format(URL, "/bookings"), params={"user_id": session['user']['email']}
        )
        try:
            bookings_data = bookings.json()
        except JSONDecodeError as je:
            bookings_data = None
        return render_template("history.html", user_bookings=bookings_data)
    return redirect(url_for('site.home'))


@site.route("/list")
def available_cars():
    """
    Lists available cars
    NOTE - currently removed from nav as this functionality is covered by site.render_booking_page
    Returns:
        list.html if user in session, otherwise index.html
    """
    if 'user' in session:
        cars = requests.get(
            "{}{}".format(URL, "/cars"), params={"available": 1}
        )
        attributes = defaultdict(set)
        if cars.status_code == 200:
            try:
                car_data = cars.json()
                for car in car_data:
                    attributes['make'].add(car['model']['make'])
                    attributes['colour'].add(car['model']['colour'])
                    attributes['year'].add(car['model']['year'])
                    attributes['capacity'].add(car['model']['capacity'])
                    attributes['cost'].add(car['cph'])
            except JSONDecodeError as je:
                attributes = None
                car_data = None
        else:
            car_data = None
            attributes = None
        return render_template("list.html", cars=car_data, attributes=attributes)
    return redirect(url_for('site.home'))


@site.route("/map", methods=['POST', 'GET'])
def render_map():
    """
    Map page - displays car locations
    Returns:
        renders map.html if user logged in, otherwise redirects to index.html
    """
    if 'user' in session:
        result = requests.get("{}{}".format(URL, "/cars"), params={})
        test = result.json()
        return render_template('map.html', points=json.dumps(test))
    return redirect(url_for("site.home"))


@site.route("/search")
def search_cars():
    """
    Search cars by attributes
    NOTE - functionality also available on booking.html
    Returns:
        search.html if user logged in, otherwise index.html
    """
    if 'user' in session:
        cars = requests.get(
            "{}{}".format(URL, "/cars")
        )
        attributes = defaultdict(set)
        if cars.status_code == 200:
            try:
                car_data = cars.json()
            except JSONDecodeError as je:
                attributes = None
                car_data = None
            else:
                for car in car_data:
                    attributes['make'].add(car['model']['make'])
                    attributes['colour'].add(car['model']['colour'])
                    attributes['year'].add(car['model']['year'])
                    attributes['capacity'].add(car['model']['capacity'])
                    attributes['cost'].add(car['cph'])
            return render_template("search.html", cars=car_data, attributes=attributes)
    return redirect(url_for('site.home'))


@site.route("/addevent")
def add_event():
    """

    Returns:

    """
    if 'user' in session:
        car_id = request.args.get('car_id')
        start = request.args.get('time_start')
        end = request.args.get('time_end')
        booking_id = request.args.get('booking_id')
        if None not in (start, end, booking_id, car_id):
            time_start = start.replace(" ", "T") + "+10:00"
            time_end = end.replace(" ", "T") + "+10:00"
            session['booking'] = {
                "car_id": car_id,
                "booking_id": booking_id,
                "time_start": time_start,
                "time_end": time_end
            }

        if 'credentials' not in session:
            return redirect(url_for('site.oauth2callback'))
        credentials = client.OAuth2Credentials.from_json(session['credentials'])
        if credentials.access_token_expired:
            return redirect(url_for('site.oauth2callback'))
        else:
            http_auth = credentials.authorize(Http())
            service = discovery.build('calendar', 'v3', http=http_auth)

        if 'booking' in session:
            time_start = session['booking']['time_start']
            time_end = session['booking']['time_end']
            booking_id = session['booking']['booking_id']
            car_id = session['booking']['car_id']
            session.pop('booking', None)
            event = {
                "summary": "Booking car number: " + car_id + " for " + session['user']['f_name'] + " " +
                           session['user']['l_name'],
                "start": {
                    "dateTime": time_start,
                    "timeZone": "Australia/Melbourne",
                },
                "end": {
                    "dateTime": time_end,
                    "timeZone": "Australia/Melbourne",
                },
                "attendees": [
                    {"email": session['user']['email']},
                ],
                "reminders": {
                    "useDefault": False,
                    "overrides": [
                        {"method": "email", "minutes": 5},
                        {"method": "popup", "minutes": 10},
                    ],
                }
            }
            add_event = service.events().insert(calendarId="primary", body=event).execute()
            data = {
                'booking_id': booking_id,
                'event_id': add_event.get("id")
            }
            response = requests.put(
                "{}{}".format(URL, "eventId"),
                json=json.dumps(data)
            )
            return redirect(url_for('site.render_booking_page'))
    return redirect(url_for('site.home'))


# @site.route("/cancelevent")
# def cancel_event():
#     booking_id = request.args.get('booking_id')
#
#     if booking_id is not None:
#         session['cancel'] = booking_id
#
#     if 'credentials' not in session:
#         return redirect(url_for('site.oauth2callback'))
#     credentials = client.OAuth2Credentials.from_json(session['credentials'])
#     if credentials.access_token_expired:
#         return redirect(url_for('site.oauth2callback'))
#     else:
#         http_auth = credentials.authorize(Http())
#         service = discovery.build('calendar', 'v3', http=http_auth)
#
#     if 'cancel' in session:
#         booking_id = session['cancel']
#         session.pop('cancel', None)
#         booking = requests.get(
#             "{}{}".format(URL, "/booking"), params={"booking_id": booking_id}
#         )
#         event_id = booking.json()['event_id']
#         print("event id" + event_id)
#         if event_id is not None:
#             delete_event = service.events().delete(calendarId="primary", eventId=event_id,
#                                                    sendUpdates="all").execute()
#             print(delete_event)
#             return Response(status=200)
#     return Response("Missing booking_id in session", status=404)


@site.route('/oauth2callback')
def oauth2callback():
    flow = client.flow_from_clientsecrets(
        'credentials.json',
        scope='https://www.googleapis.com/auth/calendar',
        redirect_uri=url_for('site.oauth2callback', _external=True))
    if 'code' not in request.args:
        auth_uri = flow.step1_get_authorize_url()
        return redirect(auth_uri)
    else:
        auth_code = request.args.get('code')
        credentials = flow.step2_exchange(auth_code)
        session['credentials'] = credentials.to_json()
    return redirect(url_for('site.add_event'))


class DateException(ValueError):
    pass
