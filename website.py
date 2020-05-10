import json
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_wtf import FlaskForm
from flask_datepicker import datepicker
from wtforms import StringField, PasswordField, SelectField, IntegerField, DateTimeField
from wtforms.validators import InputRequired, Email, Length, NumberRange, ValidationError
import re
import requests

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
class BookingForm(FlaskForm):
    car = SelectField(label='Available Cars', validators=[], choices=[])
    start = DateTimeField('Start', format="%d/%m/%Y %H:%M", default=datetime.now)
    end = DateTimeField('End', format="%d/%m/%Y %H:%M", default=datetime.now)


@site.route("/")
def home():
    response = requests.get(
        "{}{}".format(URL, "/populate")
    )
    return render_template("index.html")


@site.route("/login", methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        # result = db.user_authentication(form.email.data, form.password.data)
        result = requests.get(
            "{}{}".format(URL, "/users/authenticate"),
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
            "{}{}".format(URL, "/user"),
            json = json.dumps(user),
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


def create_booking_choices():
    form = BookingForm()
    cars = requests.get(
        "{}{}".format(URL, "/cars"), params={"available": 1}
    )  # get a list of available cars to display
    if cars is not None:
        choices = [
            (car['id'], "{} {}, {}".format(car['model']['make'], car['model']['model'], car['model']['year']))
            for car in cars.json()
        ]
        form.car.choices = choices
        form.car.default = choices[0][0]
    return form


@site.route("/book", methods=['GET'])
def render_booking_page():
    if 'user' in session:
        form = create_booking_choices()
        car_id = request.args.get('id')  # optional id arg if coming from available cars page
        if car_id is not None:
            form.car.default = str(car_id)
            form.process()
        return render_template("booking.html", form=form, car_id=car_id)
    return redirect(url_for('site.login'))


@site.route("/book", methods=['POST'])
def create_booking():
    if 'user' in session:
        form = create_booking_choices()
        print(str(form.start.data < form.end.data))
        return "<h1>" + str(form.start.data) + " " + str(form.end.data) + " " + "</h1>"
    return redirect(url_for('site.login'))


@site.route("/history")
def view_history():
    if 'user' in session:
        bookings = requests.get(
            "{}{}".format(URL, "/bookings"), params={"user_id": session['user']["id"]}
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


@site.route("/cancel")
def cancel_booking():
    if 'user' in session:
        bookings = requests.get(
            "{}{}".format(URL, "/bookings"), params={"user_id": session['user']["id"], "status": 0}
        )
        return render_template("cancel.html", user_bookings=bookings.json())
    return redirect(url_for('site.login'))


@site.route("/search")
def search_cars():
    if 'user' in session:
        return render_template("search.html")
    return redirect(url_for('site.login'))

# @site.route("/<page>", methods=['GET'])
# def generate_page(page):
#     return render_template("{}.html".format(page))
