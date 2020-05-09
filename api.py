import json

from marshmallow import fields
from sqlalchemy import MetaData, Table, Column, Integer, Float, String, insert, select, update, delete, ForeignKey, \
    LargeBinary
from flask import Blueprint, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import sessionmaker
from utils import get_random_alphaNumeric_string, hash_password, verify_password
from sqlalchemy.dialects.mysql import TINYINT, VARCHAR, TEXT
import hashlib

"""
Instructions:
https://cloud.google.com/sql/docs/mysql/connect-external-app

Enable Cloud SQL Admin API for the project.

Create a new Google Cloud SQL Instance, then create a database.

    Copy the INSTANCE_CONNECTION_NAME from overview screen

Install the proxy client (as per google doc instructions), make it executable 

Invoke proxy:
    ./cloud_sql_proxy -instances=<INSTANCE_CONNECTION_NAME>=tcp:<PORT> &
    
And update the below/db code to use the right port number, database name, etc.
"""

DB_NAME = "IOTA2"  # UPDATE THIS if need be
DB_USER = "root"  # UPDATE THIS if need be
DB_PASS = "3o6IsbqJKPedMGsr"  # UPDATE THIS if need be
PORT_NUMBER = "3306"  # UPDATE THIS if need be


def get_uri():
    return "mysql+pymysql://{}:{}@127.0.0.1:{}/{}".format(DB_USER, DB_PASS, PORT_NUMBER, DB_NAME)


api = Blueprint("api", __name__)

db = SQLAlchemy()  # use to define models/tables for database
engine = db.create_engine(
    sa_url=get_uri(),
    engine_opts={"echo": True}
)  # UPDATE temp TO THE SQL DATABASE NAME
session = sessionmaker(engine)

ma = Marshmallow()  # use to define schema/API output


#
# meta = MetaData()
# users = Table(
#     'users', meta,
#     Column('first_name', VARCHAR(45), nullable=False),
#     Column('last_name', VARCHAR(45), nullable=False),
#     Column('email', VARCHAR(45), primary_key=True, nullable=False),
#     Column('password', TEXT(75), nullable=False),
# )


class User(db.Model):
    __tablename__ = "user"
    id = db.Column('email', VARCHAR(45), primary_key=True, nullable=False)
    f_name = db.Column('first_name', VARCHAR(45), nullable=False)
    l_name = db.Column('last_name', VARCHAR(45), nullable=False)
    password = db.Column('password', TEXT(75), nullable=False)

    def __init__(self, id, f_name, l_name, password):
        self.id = id
        self.f_name = f_name
        self.l_name = l_name
        self.password = password


class Car(db.Model):
    __tablename__ = "car"
    id = db.Column('car_id', Integer(), primary_key=True, nullable=False, autoincrement=True)
    model_id = db.Column('model_id', Integer(), ForeignKey('car_model.model_id'), nullable=False)
    model = db.relationship("CarModel")
    name = db.Column('name', VARCHAR(45), nullable=False)
    cph = db.Column('cph', Float())
    available = db.Column('available', TINYINT(1), nullable=False)


class CarModel(db.Model):
    __tablename__ = "car_model"
    id = db.Column('model_id', Integer(), primary_key=True, nullable=False, autoincrement=True)
    make = db.Column('make', VARCHAR(45), nullable=False)
    model = db.Column('model', VARCHAR(45), nullable=False)
    year = db.Column('year', Integer(), nullable=False)
    capacity = db.Column('capacity', Integer(), nullable=False)


class Booking(db.Model):
    __tablename__ = "booking"
    id = db.Column('booking_id', Integer(), primary_key=True, nullable=False, autoincrement=True)
    user_id = db.Column('user_email', VARCHAR(45), ForeignKey('user.email'), nullable=False)
    user = db.relationship('User')
    car_id = db.Column('car_id', Integer(), ForeignKey('car.car_id'), nullable=False)
    car = db.relationship('Car')
    duration = db.Column('duration', Integer(), nullable=False)
    completed = db.Column('completed', TINYINT(2), nullable=False)


class Encoding(db.Model):
    __tablename__ = "encoding"
    id = db.Column('image_id', Integer(), primary_key=True, nullable=False, autoincrement=True)
    user_id = db.Column('user_email', VARCHAR(45), ForeignKey('user.email'), nullable=False)
    user = db.relationship('User')
    data = db.Column('data', LargeBinary(length=(2 ** 32) - 1), nullable=False)
    name = db.Column('name', VARCHAR(45), nullable=False)
    type = db.Column('type', VARCHAR(45), nullable=False)
    size = db.Column('size', VARCHAR(45), nullable=False)
    details = db.Column('details', VARCHAR(45), nullable=False)


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

    id = ma.auto_field()
    f_name = ma.auto_field()
    l_name = ma.auto_field()


class CarModelSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CarModel

    id = ma.auto_field()
    make = ma.auto_field()
    model = ma.auto_field()
    year = ma.auto_field()
    capacity = ma.auto_field()


class CarSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Car

    id = ma.auto_field()
    name = ma.auto_field()
    model_id = ma.auto_field()
    model = fields.Nested(CarModelSchema)
    available = ma.auto_field()
    cph = ma.auto_field()


class BookingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Booking

    id = ma.auto_field()
    user_id = ma.auto_field()
    user = fields.Nested(UserSchema)
    car_id = ma.auto_field()
    car = fields.Nested(CarSchema)
    duration = ma.auto_field()
    completed = ma.auto_field()


class EncodingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Encoding

    id = ma.auto_field()
    user_id = ma.auto_field()
    user = fields.Nested(UserSchema)
    data = ma.auto_field()
    name = ma.auto_field()
    type = ma.auto_field()
    size = ma.auto_field()
    details = ma.auto_field()


@api.route("/users", methods=['GET'])
def get_users():
    """
    endpoint to return all users in DB
    """
    users = User.query.all()
    return jsonify(UserSchema(many=True, exclude=['password']).dumps(users))


@api.route("/user/<user_id>", methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    return UserSchema(exclude=['password']).dump(user)


@api.route("/users/authenticate/<user_id>/<password>")
def user_authentication(user_id, password):
    """
    User authentication method: Allow user to login with correct login information
    """
    user = User.query.get(user_id)
    response = {}
    if user is not None:
        if user.password == password:
            response['code'] = 'SUCCESS'
            response['user'] = UserSchema(exclude=['password']).dump(user)
        else:
            response['code'] = 'PASSWORD ERROR'
    else:
        response['code'] = 'EMAIL ERROR'
    return json.dumps(response)
    # connection = self.__engine.connect()
    # sess = self.__Session()
    # qur = sess.query(users).filter_by(email=email).all()
    # print(qur)
    # if (len(qur) == 0):
    #     connection.close()
    #     # This email has not been registered
    #     return ("email error", None, None, None)
    # else:
    #     salt = qur[0][3].split(':')[1]
    #     key = qur[0][3].split(':')[0]
    #     if verify_password(key, password, salt):
    #         connection.close()
    #         # Login successful
    #         return ("successful", qur[0][0], qur[0][1], qur[0][2])
    #     else:
    #         connection.close()
    #         # Incorrect password
    #         return ("password error", None, None, None)


@api.route("/cars", methods=['GET'])
def get_cars():
    cars = Car.query.all()
    return CarSchema(many=True).dumps(cars)


@api.route("/car/<car_id>", methods=['GET'])
def get_car(car_id):
    car = Car.query.get(car_id)
    return CarSchema().dump(car)

#
# class DBConnect:
#     db = SQLAlchemy()
#     ma = Marshmallow()
#     __engine = None
#
#     def __init__(self, app):
#         if self.__engine is None:
#             self.__engine = self.db.create_engine(
#                 sa_url='mysql+pymysql://' + DB_USER + ':' + DB_PASS + '@127.0.0.1:{}/{}'.format(PORT_NUMBER, DB_NAME),
#                 engine_opts={"echo": True}
#             )  # UPDATE temp TO THE SQL DATABASE NAME
#             self.db.init_app(app)
#             self.__Session = sessionmaker(self.__engine)
#
#     def get_users(self):
#         """
#         Get users: Return all users in the users table
#         """
#         connection = self.__engine.connect()
#         sel = select([users])
#         result = connection.execute(sel)
#         connection.close()
#         return result
#
#     def add_users(self, first_name, last_name, email, password):
#         """
#         Add method: Add new user to the users table
#         """
#         connection = self.__engine.connect()
#         sess = self.__Session()
#         qur = sess.query(users).filter_by(email=email).all()
#         if (len(qur) > 0):
#             connection.close()
#             return False
#         else:
#             salt = get_random_alphaNumeric_string(10)
#             ins = users.insert().values(first_name=first_name, last_name=last_name, email=email,
#                                         password=hash_password(password, salt) + ':' + salt)
#             print(ins)
#             connection.execute(ins)
#             connection.close()
#             return True
#
#     def get_user_with_email(self, email):
#         """
#         Check email method: checking if an email is in users table (user is registered)
#         """
#         connection = self.__engine.connect()
#         sess = self.__Session()
#         qur = sess.query(users).filter_by(email=email).all()
#         print(qur)
#         connection.close()
#         return qur
#


#

