from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length

app = Flask(__name__)
app.config['SECRET_KEY'] = 'temp'
Bootstrap(app)


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message="invalid email.")])
    password = PasswordField('Password', validators=[InputRequired(), Length(4, 20)])


class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email(message="invalid email.")])
    password = PasswordField('Password', validators=[InputRequired(), Length(4, 20)])


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return "<h1>" + form.email.data + " " + form.password.data + "</h1>"
    return render_template("login.html", form=form)


@app.route("/register", methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        return "<h1>" + form.first_name.data + " " + form.last_name.data + \
               " " + form.email.data + " " + form.password.data + "</h1>"
    return render_template("register.html", form=form)


if __name__ == '__main__':
    app.run(debug=True)
