import json

from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, IntegerField
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
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    if regex.search(field.data) == None:
        raise ValidationError('Password must contain at least one special character')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message="Invalid email.")])
    password = PasswordField('Password', validators=[InputRequired(), Length(4, 20)])


class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired(), valid_name])
    last_name = StringField('Last Name', validators=[InputRequired(), valid_name])
    email = StringField('Email', validators=[InputRequired(), Email(message="Invalid email.")])
    password = PasswordField('Password', validators=[InputRequired(), Length(4, 20), valid_password])


# replace choices with result of db query
class BookingForm(FlaskForm):
    car = SelectField('Available Cars', choices=[('ABC123', 'car1'), ('car2', 'car2'), ('car3', 'car3')])
    days = StringField('Number of days')


#
# @site.route("/test")
# def test_db():
#     """
#     Endpoint to test db by returning user table
#     """
#     code = "<h1>"
#     code += str(db.get_user_with_email("danieldao@gmail.com"))
#     return code + "</h1>"


@site.route("/")
def home():
    return render_template("index.html")


# @site.route("/<page>", methods=['GET'])
# def generate_page(page):
#     return render_template("{}.html".format(page))


@site.route("/login", methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        # result = db.user_authentication(form.email.data, form.password.data)
        result = requests.get("{}{}/{}/{}".format(URL, "/users/authenticate", form.email.data, form.password.data))
        data = result.json()
        if data['code'] == 'SUCCESS':
            session['user'] = data['user']
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
        if (db.add_users(form.first_name.data, form.last_name.data, form.email.data, form.password.data)):
            result = db.user_authentication(form.email.data, form.password.data)
            user = [result[1], result[2], result[3]]
            session['user'] = user
            return redirect(url_for("site.main"))
        else:
            form.email.errors.append('This email has been used for register before')
    elif ('user' in session):
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


@site.route("/booking", methods=['POST', 'GET'])
def render_booking_page():
    form = BookingForm()
    if form.validate_on_submit():
        return "<h1>" + str(form.car.data) + " " + str(form.days.data) + "</h1>"
    return render_template("booking.html", form=form)


class Booking:
    """
    test class for designing front end
    """

    def __init__(self, id, car_id, start, end):
        self.id = id
        self.car_id = car_id
        self.start = start
        self.end = end


@site.route("/history")
def view_history():
    bookings = [Booking(i, i, i, i) for i in range(0, 6)]
    return render_template("history.html", user_bookings=bookings)


@site.route("/list")
def available_cars():
    bookings = [Booking(i, i, i, i) for i in range(0, 6)]
    return render_template("list.html", cars=bookings)


@site.route("/cancel")
def cancel_booking():
    return render_template("cancel.html")


@site.route("/search")
def search_cars():
    return render_template("search.html")
