from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from sqlalchemy import MetaData, Table, Column, Integer, String, insert, select, update, delete
from api import DBConnect
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, PasswordField, SelectField, IntegerField
from wtforms.validators import InputRequired, Email, Length, NumberRange, ValidationError
from datetime import timedelta

app = Flask(__name__)
app.permanent_session_lifetime = timedelta(hours=5)
db = DBConnect(app)
Bootstrap(app)

app.config['SECRET_KEY'] = 'temp'


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message="Invalid email.")])
    password = PasswordField('Password', validators=[InputRequired(), Length(4, 20)])


class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email(message="Invalid email.")])
    password = PasswordField('Password', validators=[InputRequired(), Length(4, 20)])


# replace choices with result of db query
class BookingForm(FlaskForm):
    car = SelectField('Available Cars', choices=[('ABC123', 'car1'), ('car2', 'car2'), ('car3', 'car3')])
    days = StringField('Number of days')


@app.route("/test")
def test_db():
    """
    Endpoint to test db by returning user table
    """
    code = "<h1>"
    code += str(db.get_user_with_email("danieldao@gmail.com"))
    return code + "</h1>"


@app.route("/")
def home():
    return render_template("index.html")


# @app.route("/<page>", methods=['GET'])
# def generate_page(page):
#     return render_template("{}.html".format(page))


@app.route("/login", methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        result = db.user_authentication(form.email.data, form.password.data)
        if (result[0] == 'successful'):
            user = [result[1], result[2], result[3]]
            session['user'] = user         
            return redirect(url_for("main"))
        elif (result[0] == 'email error'):
            form.email.errors.append('This email has not been registered')
            return render_template("login.html", form=form)
        elif (result[0] == 'password error'):
            form.password.errors.append('Incorrect password')
            return render_template("login.html", form=form)
    elif 'user' in session:
        return redirect(url_for("main"))
    else:
        return render_template("login.html", form=form)


@app.route("/register", methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        if (db.add_users(form.first_name.data, form.last_name.data, form.email.data, form.password.data)):
            # flash('Thanks for registering')
            return redirect(url_for("login"))
    elif ('user' in session):
        return redirect(url_for("main"))
    else:
        # flash('This email has been registered before, if this is your email, please login!')
        return render_template("register.html", form=form)


@app.route("/main")
def main():
    if 'user' in session:
        user = {
            "first_name": session['user'][0],
            "last_name": session['user'][1],
            "email": session['user'][2],
            "face_id": False
        }
        return render_template("main.html", user=user)
    else:
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


@app.route("/booking", methods=['POST', 'GET'])
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


@app.route("/history")
def view_history():
    bookings = [Booking(i, i, i, i) for i in range(0, 6)]
    return render_template("history.html", user_bookings=bookings)


@app.route("/list")
def available_cars():
    bookings = [Booking(i, i, i, i) for i in range(0, 6)]
    return render_template("list.html", cars=bookings)


@app.route("/cancel")
def cancel_booking():
    return render_template("cancel.html")


@app.route("/search")
def search_cars():
    return render_template("search.html")


if __name__ == '__main__':
    app.run(debug=True, host='192.168.1.200')  # use IP of MP: as per forums only has to be accessibly locally
    # app.run(debug=True)
