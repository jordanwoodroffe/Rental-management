import json
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_wtf import FlaskForm
from flask_datepicker import datepicker
from wtforms import StringField, PasswordField, SelectField, IntegerField, DateTimeField
from wtforms.validators import InputRequired, Email, Length, NumberRange, ValidationError
import re
import requests
from collections import defaultdict

site = Blueprint("site", __name__)

URL = "http://127.0.0.1:5000/"  # TODO: replace with method somewhere/auto-generate


def valid_name(form, field):
    # names must be in ASCII
    if not field.data.isascii():
        raise ValidationError('Please enter valid name')
    # names must not contain number
    if any(char.isdigit() for char in field.data):
        raise ValidationError('Name cannot contain number')


def valid_password(form, field):
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


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message="Invalid email.")])
    password = PasswordField('Password', validators=[InputRequired(), Length(4, 20)])


class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired(), valid_name])
    last_name = StringField('Last Name', validators=[InputRequired(), valid_name])
    email = StringField('Email', validators=[InputRequired(), Email(message="Invalid email.")])
    password = PasswordField('Password', validators=[InputRequired(), Length(6, 12), valid_password])


# replace choices with result of db query
class BookingQueryForm(FlaskForm):
    start = DateTimeField('Start', format="%Y-%m-%d %H:%M", default=datetime.now)
    end = DateTimeField('End', format="%Y-%m-%d %H:%M", default=datetime.now)


class BookingForm(FlaskForm):
    car_id = StringField('Car', render_kw={'readonly': True})


@site.route("/")
def home():
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
        if data['code'] == 'SUCCESS':
            session['user'] = data['user']
            print(session['user'])
        elif data['code'] == 'EMAIL ERROR':
            form.email.errors.append('This email has not been registered')
        elif data['code'] == 'PASSWORD ERROR':
            form.password.errors.append('Incorrect password')
    if 'user' in session:
        return redirect(url_for("site.main"))
    return render_template("login.html", form=form)


@site.route("/register", methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        #  should be using response = requests.get(<DB_API_URL>)
        user = {'id': form.email.data,
                'l_name': form.last_name.data,
                'f_name': form.first_name.data,
                'password': form.password.data,
                }
        result = requests.post(
            "{}{}".format(URL, "user"),
            json=json.dumps(user),
        )
        print(result)
        data = result.json()
        # print(data)
        if data['code'] == 'SUCCESS':
            return redirect(url_for("site.login"))
        elif data['code'] == "USER ERROR":
            form.email.errors.append('This email has been used for register before')
    elif 'user' in session:
        return redirect(url_for("site.main"))
    return render_template("register.html", form=form)


@site.route("/main")
def main():
    if 'user' in session:
        return render_template("main.html", user=session['user'])
    else:
        return redirect(url_for("site.login"))


@site.route("/logout")
def logout():
    session.pop('user', None)
    return redirect(url_for('site.login'))


# def create_booking_choices():
#     form = BookingForm()
#     cars = requests.get(
#         "{}{}".format(URL, "/cars"), params={"available": 1}
#     )  # get a list of available cars to display
#     if cars is not None:
#         choices = [
#             (car['id'], "{} {}, {}".format(car['model']['make'], car['model']['model'], car['model']['year']))
#             for car in cars.json()
#         ]
#         form.car.choices = choices
#         form.car.default = choices[0][0]
#     return form


@site.route("/book", methods=['GET'])
def render_booking_page():
    if 'user' in session:
        start = request.args.get('start')
        end = request.args.get('end')
        form = BookingQueryForm()
        if start is not None and end is not None:
            start_dt = datetime.strptime(start, "%Y-%m-%d %H:%M")
            end_dt = datetime.strptime(end, "%Y-%m-%d %H:%M")
            print(start_dt)
            print(end_dt)
            response = requests.get(
                "{}{}/{}/{}".format(URL, "cars", str(start_dt).replace(" ", "T"), str(end_dt).replace(" ", "T"))
            )
            # booking form - render the car tiles:
            # set datetime to readonly?
            form.start.data = start_dt
            form.end.data = end_dt
            return render_template("booking.html", form=form, cars=response.json(), start=start_dt, end=end_dt)
        return render_template("booking.html", form=form)
    return redirect(url_for('site.login'))


@site.route("/book", methods=['POST'])
def process_booking():
    if 'user' in session:
        completed = 0
        car_id = request.args.get('car_id')
        start = request.args.get('start')
        end = request.args.get('end')
        if None not in (car_id, start, end):
            data = {
                'start': start,
                'end': end,
                'user_id': session['user']['email'],
                'car_id': car_id
            }
            response = requests.post(
                "{}{}".format(URL, "booking"),
                json=json.dumps(data)
            )
            result = response.json()
            print(result)
            completed = 1
        return render_template("booking.html", form=BookingQueryForm(), completed=completed)
    return redirect(url_for('site.login'))


@site.route("/history")
def view_history():
    if 'user' in session:
        print(session['user'])
        bookings = requests.get(
            "{}{}".format(URL, "/bookings"), params={"user_id": session['user']['email']}
        )
        return render_template("history.html", user_bookings=bookings.json())
    return redirect(url_for('site.login'))


@site.route("/list")
def available_cars():
    if 'user' in session:
        cars = requests.get(
            "{}{}".format(URL, "/cars"), params={"available": 1}
        )
        return render_template("list.html", cars=cars.json())
    return redirect(url_for('site.login'))


@site.route("/cancel", methods=['POST', 'GET'])
def cancel_booking():
    if 'user' in session:
        bookings = requests.get(
            "{}{}".format(URL, "/bookings"), params={"user_id": session['user']["email"], "status": 0}
        )
        if request.method == "POST":
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
                result = response.json()
                return str(result)
        return render_template("cancel.html", user_bookings=bookings.json())
    return redirect(url_for('site.login'))


@site.route("/search")
def search_cars():
    if 'user' in session:
        cars = requests.get(
            "{}{}".format(URL, "/cars")
        )
        attributes = defaultdict(set)
        if cars.status_code == 200:
            for car in cars.json():
                attributes['make'].add(car['model']['make'])
                attributes['colour'].add(car['model']['colour'])
                attributes['year'].add(car['model']['year'])
                attributes['capacity'].add(car['model']['capacity'])
            return render_template("search.html", cars=cars.json(), attributes=attributes)

    return redirect(url_for('site.login'))

# @site.route("/<page>", methods=['GET'])
# def generate_page(page):
#     return render_template("{}.html".format(page))
