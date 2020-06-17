"""
MP Customer Web App

website.py renders html templates and handles page endpoints.
Also handles input validation for login, register, booking, and cancel, along with processing forms.
"""
import json
import re
from json.decoder import JSONDecodeError
import requests
import os
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateTimeField, SelectField
from wtforms.validators import InputRequired, Email, Length, ValidationError
from collections import defaultdict
from datetime import datetime
from httplib2 import Http
from oauth2client import client
from googleapiclient import discovery
from customer_app.utils import allowed_file, calc_hours
from werkzeug.utils import secure_filename

site = Blueprint("site", __name__)

IP = "http://127.0.0.1"
PORT = "5000/"
URL = "{}:{}".format(IP, PORT)


def valid_name(form, field):
    """Form validation method for name fields - checks to ensure all chars are ascii and are not digits

    Args:
        form: FlaskForm to check
        field: fields to validate

    Raises:
        ValidationError: if name is invalid (not ascii or contains digit)
    """
    # names must be in ASCII
    if not re.match("[A-Za-z]", field.data):
        raise ValidationError('Please enter valid name')
    # names must not contain number
    if any(char.isdigit() for char in field.data):
        raise ValidationError('Name cannot contain number')


def valid_password(form, field):
    """Form validation method to ensure password is correct format

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


def valid_username(form, field):
    """Form Validation method to ensure username is in correct format

    Args:
        form: form to validate
        field: field to check

    Raises:
        ValidationError: if username is invalid
    """
    # Username must contain characters or digits
    if not re.match("[a-zA-Z0-9]+", field.data):
        raise ValidationError("Invalid username: must contain characters or digits")
    # Username must be between 6 and 12 characters long
    if not 6 <= len(field.data) <= 12:
        raise ValidationError("Invalid username: be between 6 and 12 characters long")


def validate_date(form, field):
    """Form validation method for date fields

    Args:
        form: FlaskForm to validate
        field: field to check

    Raises:
        ValidationError: if invalid date entry (incorrect format, or <= current datetime)

    """
    try:
        dt = datetime.strptime(field.data, "%Y-%m-%d %H:%M")  # Get datetime data from the form field
    except Exception:
        raise ValidationError('Incorrect input format. Please input as YYYY-mm-dd  HH:MM')
    else:
        # Datetime must be later than current datetime
        if dt < datetime.now():
            raise ValidationError('Date must be later than current date')


class LoginForm(FlaskForm):
    """Login form to capture existing user details - rendered on login.html"""
    # email = StringField('Email', validators=[InputRequired(), Email(message="Invalid email.")])
    username = StringField('Username', validators=[InputRequired(), Length(6, 12), valid_username])
    password = PasswordField('Password', validators=[InputRequired(), valid_password])


class RegistrationForm(FlaskForm):
    """Registration form to capture new user details - rendered on register.html"""
    first_name = StringField('First Name', validators=[InputRequired(), valid_name])
    last_name = StringField('Last Name', validators=[InputRequired(), valid_name])
    username = StringField('Username', validators=[InputRequired(), Length(6, 12), valid_username])
    email = StringField('Email', validators=[InputRequired(), Email(message="Invalid email.")])
    password = PasswordField('Password', validators=[InputRequired(), Length(6, 12), valid_password])


class BookingQueryForm(FlaskForm):
    """Booking form to capture new booking date range information - rendered on booking.html"""
    start = DateTimeField('Start', format="%Y-%m-%d %H:%M", validators=[InputRequired(), validate_date],
                          default=datetime.now)
    end = DateTimeField('End', format="%Y-%m-%d %H:%M", validators=[InputRequired(), validate_date],
                        default=datetime.now)


class CreateReportForm(FlaskForm):
    car_id = StringField('Rego', validators=[InputRequired(), Length(6, 6, message="Rego must be 6 characters")])
    details = StringField('Details', validators=[InputRequired(), valid_name])
    priority = SelectField('Priority', choices=[('HIGH', 'High'), ('MEDIUM', 'Medium'), ('LOW', 'Low')])


@site.route("/")
def home():
    """Index page for site - user can choose to login or register

    Returns:
        renders main.html if user has logged in
        or renders index.html if user has not logged in
    """
    response = requests.get(
        "{}{}".format(URL, "populate")  # Populate database if it's empty
    )
    # If user is logged in, go to main page
    if 'user' in session:
        return redirect(url_for("site.main"))
    # Else, go to home page
    return render_template("customer/index.html")


@site.route("/login", methods=['POST', 'GET'])
def login():
    """Authenticates a user when they log in to the MP web app

    Returns:
        redirect site.main or if user successfully authenticated
        or renders login.html on load, with error messages if incorrect login attempt
    """
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        result = requests.get(
            "{}{}".format(URL, "users/authenticate"),
            params={"user_id": form.username.data, "password": form.password.data},
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
    return render_template("login.html", form=form, login_type="Customer")


@site.route("/register", methods=['POST', 'GET'])
def register():
    """Registers a user: captures details from form and attempts to append to User table

    Returns:
        redirect site.login if successful or renders register.html on load, with errors if incorrect register attempt
    """
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        #  should be using response = requests.get(<DB_API_URL>)
        user = {
            'username': form.username.data,
            'email': form.email.data,
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
            form.username.errors.append('This username has been used for register before')
    elif 'user' in session:
        return redirect(url_for("site.main"))
    return render_template("customer/register.html", form=form)


@site.route("/main")
def main():
    """Renders the home page for MP web app

    Returns:
        renders main.html if user logged in or site.home if user not logged in
    """
    if 'user' in session:  # If user is logged in, go to main page and display cars's location
        result = requests.get("{}{}".format(URL, "/cars"), params={})
        try:
            test = result.json()
        except JSONDecodeError:
            test = []  # error - unable to load cars
        messages = session.pop('messages') if 'messages' in session else None
        return render_template("customer/main.html", user=session['user'], points=json.dumps(test), messages=messages)
    return redirect(url_for("site.home"))  # Else go to home page


@site.route("/capture_user", methods=['POST', 'GET'])
def capture_user():
    """Captures/encodes a user for face recognition login

    Returns:
        redirect site.main if successful or site.home if user not logged in
    """
    if 'user' in session:
        if request.method == 'POST':
            files = request.files.getlist("image")  # check if the post request has the file
            if len(files) < 5:
                flash('You need at least 5 photos to register')
                return redirect(url_for("site.main"))
            elif len(files) >= 10:
                flash('Maximum of 10 photos are accepted')
                return redirect(url_for("site.main"))
            for file in files:
                if not allowed_file(file.filename):
                    flash('Only images of extensions: txt, pdf, png, jpg, jpeg, gif are allowed')
                    return redirect(url_for("site.main"))
            directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'user_data/face_pics',
                                     session['user']['username'])
            if not os.path.exists(directory):
                os.makedirs(directory)
            for file in files:
                filename = secure_filename(file.filename)
                file.save(os.path.join(directory, filename))  # Add user photos to user_data/face_pics/user_name folder
            result = requests.post(
                "{}{}".format(URL, "/encode_user"),
                params={"user_id": session['user']['username'], "directory": directory}
            )  # Encode user photos
            if result.status_code == 200:  # If encode successful, add facial login option to user object in user table
                result = requests.put(
                    "{}{}".format(URL, "/user"),
                    params={"user_id": session['user']['username'], "face_id": 1}
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
    """Logs the user out of MP web app

    Returns:
        redirects to site.login
    """
    session.pop('user', None)  # Remove user from session
    return redirect(url_for('site.login'))


@site.route("/book", methods=['GET'])
def render_booking_page():
    """Renders the booking page - loads cars if start/end dates are valid

    Returns:
        renders booking.html with cars if applicable or site.home if user not logged in
    """
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
                )  # get all cars available during the time frame
                try:
                    cars = response.json()
                    attributes = make_attributes(cars)  # Send cars's attributes to the front end
                    for car in cars:
                        cph = car['cph']
                        try:
                            amount = float(cph)
                            car['total_cost'] = float("{:.2f}".format(amount * calc_hours(d1=start_dt, d2=end_dt)))
                        except ValueError:
                            car['total_cost'] = None
                except JSONDecodeError as je:
                    cars = None
                form.start.data = start_dt
                form.end.data = end_dt
                return render_template("customer/booking.html", form=form, cars=cars, start=start_dt, end=end_dt,
                                       attributes=attributes)
        return render_template("customer/booking.html", form=form, attributes=attributes)
    return redirect(url_for('site.home'))


@site.route("/book", methods=['POST'])
def process_booking():
    """Sends new booking request to database api

    Returns:
        renders booking.html with confirmation/error messages
    """
    if 'user' in session:  # Check is user is logged in
        car_id = request.args.get('car_id')
        start = request.args.get('start')
        end = request.args.get('end')
        messages = None
        if None not in (car_id, start, end):  # Check if car_id, start and end time are provided
            response = requests.get(
                "{}{}".format(URL, "car"), params={"car_id": car_id}
            )
            car = response.json()
            amount = float(car['cph'])
            data = {
                'start': start,
                'end': end,
                'user_id': session['user']['username'],
                'car_id': car_id,
                'event_id': None,
                'cph': amount
            }
            response = requests.post(
                "{}{}".format(URL, "booking"),
                json=json.dumps(data)
            )  # Add booking to booking table
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
                )]  # create success message - displayed as bootstrap alerts
            else:
                messages = [(
                    "warning",
                    {
                        "message": "Booking unsuccessful",
                        "data": "Unable to create booking",
                        "error": response.text
                    }
                )]  # append error message - displayed as bootstrap alerts
        return render_template("customer/booking.html", form=BookingQueryForm(), messages=messages)
    return redirect(url_for('site.home'))


@site.route("/cancel", methods=['GET'])
def render_cancel_page():
    """Renders the booking cancellation page, with booked bookings for a user

    Returns:
        renders cancel.html if logged in, otherwise redirects to site.login
    """
    if 'user' in session:  # Check if user is logged in
        bookings = requests.get(
            "{}{}".format(URL, "/bookings"), params={"user_id": session['user']['username'], "status": 0}
        )  # Get all booking of user with username
        try:
            bookings_data = get_valid_bookings(bookings.json())
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
        return render_template("customer/cancel.html", user_bookings=bookings_data, messages=message_data)
    return redirect(url_for('site.home'))


def get_valid_bookings(bookings: []) -> []:
    """Extracts valid bookings to display for cancellation: user can only cancel an upcoming booking

    Args:
        bookings: list of bookings

    Returns:
        valid_bookings: list of bookings that end after the current time

    """
    valid_bookings = []
    for booking in bookings:
        if datetime.strptime(booking['end'], "%Y-%m-%d %H:%M:%S") >= datetime.now():
            valid_bookings.append(booking)
    return valid_bookings


@site.route("/cancel", methods=['POST'])
def cancel_booking():
    """Attempts to cancel a booking/bookings for a user

    Returns:
        redirects to site.render_cancel_page with confirmation/error messages
    """
    if 'user' in session:
        bookings = request.form.getlist('cancel')
        messages = []
        for booking in bookings:
            booking_id = int(booking)
            status = 2
            result = requests.get(
                "{}{}".format(URL, "booking"), params={"booking_id": booking_id}
            )  # get the booking and determine if booking id was valid
            if result.status_code == 200:
                data = result.json()
                if data['user_id'] != session['user']['username']:
                    messages.append(("warning", {"message": "Booking is not for current user"}))
                    return redirect(url_for('site.render_cancel_page', messages=json.dumps(messages)))
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

                if 'credentials' not in session:  # Check if user is logged in to google or not
                    return redirect(url_for('site.oauth2callback'))  # If not, get credential
                credentials = client.OAuth2Credentials.from_json(session['credentials'])
                if credentials.access_token_expired:  # If token is expired, get a new one
                    return redirect(url_for('site.oauth2callback'))
                else:
                    http_auth = credentials.authorize(Http())
                    service = discovery.build('calendar', 'v3', http=http_auth)

                if 'cancel' in session:  # reload cancelaation info after google authentication
                    booking_id = session['cancel']
                    session.pop('cancel', None)
                    booking = requests.get(
                        "{}{}".format(URL, "/booking"), params={"booking_id": booking_id}
                    )
                    event_id = booking.json()['event_id']
                    if event_id is not None:  # Remove event from google calendar if possible
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
                ))  # append success message
            else:
                messages.append((
                    "warning",
                    {
                        "message": "Unable to cancel booking",
                        "data": response.text
                    }
                ))  # append error message
        return redirect(url_for('site.render_cancel_page', messages=json.dumps(messages)))
    return redirect(url_for('site.home'))


@site.route("/history")
def view_history():
    """Renders booking history for a user - view cars previously/currently booked, and filter by status or car rego

    Returns:
        renders history.html with booking data
    """
    if 'user' in session:  # Check if user is logged in
        bookings = requests.get(
            "{}{}".format(URL, "/bookings"), params={"user_id": session['user']['username']}
        )  # Get all booking for user with username
        try:
            bookings_data = bookings.json()
        except JSONDecodeError as je:
            bookings_data = None
        return render_template("customer/history.html", user_bookings=bookings_data)
    return redirect(url_for('site.home'))


@site.route("/list")
def available_cars():
    """Lists available cars
    NOTE - currently removed from nav as this functionality is covered by site.render_booking_page

    Returns:
        list.html if user in session, otherwise index.html
    """
    if 'user' in session:  # Check if user is logged in
        cars = requests.get(
            "{}{}".format(URL, "/cars"), params={"available": 1}
        )  # Get all available cars in the database
        if cars.status_code == 200:
            try:
                car_data = cars.json()
                attributes = make_attributes(car_data)
            except JSONDecodeError as je:
                attributes = None
                car_data = None
        else:
            car_data = None
            attributes = None
        return render_template("customer/list.html", cars=car_data, attributes=attributes)
    return redirect(url_for('site.home'))


@site.route("/map", methods=['POST', 'GET'])
def render_map():
    """Map page - displays car locations

    Returns:
        renders map.html if user logged in, otherwise redirects to index.html
    """
    if 'user' in session:  # Check if user is logged in
        result = requests.get("{}{}".format(URL, "/cars"), params={})  # Get all cars in the database for cars's
        # location
        test = result.json()
        return render_template('customer/map.html', points=json.dumps(test))
    return redirect(url_for("site.home"))


@site.route("/search")
def search_cars():
    """Search cars by attributes

    NOTE - functionality also available on booking.html

    Returns:
        vehicles.html if user logged in, otherwise index.html
    """
    if 'user' in session:  # Check if user is logged in
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
            return render_template("customer/search.html", cars=car_data, attributes=attributes)
    return redirect(url_for('site.home'))


def make_attributes(car_data: []) -> {set}:
    """Creates a list of attributes for displaying on search & booking page

    Args:
        car_data:

    Returns:
        car_attributes: list of data to display
    """
    attributes = defaultdict(set)
    for car in car_data:
        attributes['make'].add(car['model']['make'])
        attributes['colour'].add(car['model']['colour'])
        attributes['year'].add(car['model']['year'])
        attributes['capacity'].add(car['model']['capacity'])
        attributes['cost'].add(car['cph'])
        attributes['transmission'].add(car['model']['transmission'])
        attributes['weight'].add(car['model']['weight'])
        attributes['length'].add(car['model']['length'])
        attributes['load_index'].add(car['model']['load_index'])
        attributes['engine_capacity'].add(car['model']['engine_capacity'])
        attributes['ground_clearance'].add(car['model']['ground_clearance'])
    return attributes


@site.route("/report_car", methods=['GET', 'POST'])
def report_car():
    form = CreateReportForm()
    choices = ['High', 'Medium', 'Low']
    if request.method == 'POST' and form.validate_on_submit():
        report = {
            'car_id': form.car_id.data,
            'details': form.details.data,
            'priority': form.priority.data,
            'report_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        result = requests.post("{}{}".format(URL, "/report"), json=json.dumps(report))
        if result.status_code == 200:
            session['messages'] = [(
                "success",
                {
                    "message": "Report successfully created",
                    "data": "Registration number: {}".format(form.car_id.data)
                }
            )]
            return redirect(url_for("site.home"))
        else:
            form.car_id.errors.append(result.text)
            return render_template("employee/report_car.html", form=form, choices=choices)
    if 'user' in session:
        car_id = request.args.get("car_id")
        if car_id is not None:
            form.car_id.data = car_id
        return render_template("employee/report_car.html", form=form, choices=choices)
    return redirect(url_for('site.home'))


@site.route("/addevent")
def add_event():
    """Adds an event for a booking to the users Google Calendar

    Returns:
        redirects to the booking page after attempting to add/authenticate
    """
    if 'user' in session:  # Check if user is logged in
        car_id = request.args.get('car_id')
        start = request.args.get('time_start')
        end = request.args.get('time_end')
        booking_id = request.args.get('booking_id')
        if None not in (start, end, booking_id, car_id):  # create booking object and add booking data to session
            time_start = start.replace(" ", "T") + "+10:00"
            time_end = end.replace(" ", "T") + "+10:00"
            session['booking'] = {
                "car_id": car_id,
                "booking_id": booking_id,
                "time_start": time_start,
                "time_end": time_end
            }  # save booking information in session while redirect to google authentication

        if 'credentials' not in session:  # Check for google credential
            return redirect(url_for('site.oauth2callback'))  # If not, get one
        credentials = client.OAuth2Credentials.from_json(session['credentials'])
        if credentials.access_token_expired:  # Get new credential if the current one is expired
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
            }  # Create new event object
            new_event = service.events().insert(calendarId="primary", body=event).execute()  # Add new event to
            # google calendar
            data = {
                'booking_id': booking_id,
                'event_id': new_event.get("id")
            }
            response = requests.put(
                "{}{}".format(URL, "eventId"),
                json=json.dumps(data)
            )  # Add event_id to booking table
            return redirect(url_for('site.render_booking_page'))
    return redirect(url_for('site.home'))


@site.route('/oauth2callback')
def oauth2callback():
    """Callback function for Google Calendar Integration

    Returns:
        redirects to add_event if successful
    """
    flow = client.flow_from_clientsecrets(
        '../credentials.json',
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
    """Used to raise incorrect date exceptions when validating a FlaskForm"""
    pass
