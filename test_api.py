import unittest
import json
import random
from datetime import datetime
import pandas as pd
from json.decoder import JSONDecodeError
import requests
from sqlalchemy import MetaData, Table, Column, DateTime, Integer, Float, String, insert, select, update, delete, \
    ForeignKey, LargeBinary
from flask import Blueprint, jsonify, request, Response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields
from sqlalchemy.orm import sessionmaker
from utils import get_random_alphaNumeric_string, hash_password, verify_password, compare_dates
from sqlalchemy.dialects.mysql import TINYINT, VARCHAR, TEXT
import hashlib
import requests
from environs import Env
from api import api


class TestApi(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        env = Env()
        env.read_env()

        DB_NAME = env("DB_NAME")
        DB_USER = env("DB_USER")
        DB_PASS = env("DB_PASS")
        PORT_NUMBER = env("PORT_NUMBER")
        DB_URI = "mysql+pymysql://{}:{}@127.0.0.1:{}/{}".format(DB_USER, DB_PASS, PORT_NUMBER, DB_NAME)

        api = Blueprint("api", __name__)

        db = SQLAlchemy()
        engine = db.create_engine(
            sa_url=DB_URI,
            engine_opts={"echo": True}
        )
        session = sessionmaker(engine)

        ma = Marshmallow()

        class User(db.Model):
            __tablename__ = "user"
            email = db.Column('email', VARCHAR(45), primary_key=True, nullable=False)
            f_name = db.Column('first_name', VARCHAR(45), nullable=False)
            l_name = db.Column('last_name', VARCHAR(45), nullable=False)
            password = db.Column('password', TEXT(75), nullable=False)

        class Car(db.Model):
            __tablename__ = "car"
            car_id = db.Column('car_id', VARCHAR(6), primary_key=True, nullable=False)
            model_id = db.Column('model_id', Integer(), ForeignKey('car_model.model_id'), nullable=False)
            model = db.relationship("CarModel")
            name = db.Column('name', VARCHAR(45), nullable=False)
            cph = db.Column('cph', Float())
            locked = db.Column('available', TINYINT(1), nullable=False)
            long = db.Column('long', Float())
            lat = db.Column('lat', Float())

        class CarModel(db.Model):
            __tablename__ = "car_model"
            model_id = db.Column('model_id', Integer(), primary_key=True, nullable=False, autoincrement=True)
            make = db.Column('make', VARCHAR(45), nullable=False)
            model = db.Column('model', VARCHAR(45), nullable=False)
            year = db.Column('year', Integer(), nullable=False)
            capacity = db.Column('capacity', Integer(), nullable=False)
            colour = db.Column('colour', VARCHAR(45), nullable=False)

        class Booking(db.Model):
            __tablename__ = "booking"
            booking_id = db.Column('booking_id', Integer(), primary_key=True, nullable=False, autoincrement=True)
            user_id = db.Column('user_email', VARCHAR(45), ForeignKey('user.email'), nullable=False)
            user = db.relationship('User')
            car_id = db.Column('car_id', VARCHAR(6), ForeignKey('car.car_id'), nullable=False)
            car = db.relationship('Car')
            start = db.Column('start', DateTime(), nullable=False)
            end = db.Column('end', DateTime(), nullable=False)
            completed = db.Column('completed', Integer(), nullable=False)
            event_id = db.Column('event_id', VARCHAR(45))

        class Encoding(db.Model):
            __tablename__ = "encoding"
            enc_id = db.Column('image_id', Integer(), primary_key=True, nullable=False, autoincrement=True)
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

            email = ma.auto_field()
            f_name = ma.auto_field()
            l_name = ma.auto_field()

        class CarModelSchema(ma.SQLAlchemyAutoSchema):
            class Meta:
                model = CarModel

            model_id = ma.auto_field()
            make = ma.auto_field()
            model = ma.auto_field()
            year = ma.auto_field()
            capacity = ma.auto_field()
            colour = ma.auto_field()

        class CarSchema(ma.SQLAlchemyAutoSchema):
            class Meta:
                model = Car

            car_id = ma.auto_field()
            name = ma.auto_field()
            model_id = ma.auto_field()
            model = fields.Nested(CarModelSchema)
            locked = ma.auto_field()
            cph = ma.auto_field()
            long = ma.auto_field()
            lat = ma.auto_field()

        class BookingSchema(ma.SQLAlchemyAutoSchema):
            class Meta:
                model = Booking

            booking_id = ma.auto_field()
            user_id = ma.auto_field()
            user = fields.Nested(UserSchema)
            car_id = ma.auto_field()
            car = fields.Nested(CarSchema)
            start = ma.auto_field()
            end = ma.auto_field()
            completed = ma.auto_field()
            event_id = ma.auto_field()

        class EncodingSchema(ma.SQLAlchemyAutoSchema):
            class Meta:
                model = Encoding

            enc_id = ma.auto_field()
            user_id = ma.auto_field()
            user = fields.Nested(UserSchema)
            data = ma.auto_field()
            name = ma.auto_field()
            type = ma.auto_field()
            size = ma.auto_field()
            details = ma.auto_field()

    def test_get_users(self):

        self.assertIsNotNone(api.get_users().users)
        actualResponse = Response(api.get_users())
        expectedResponse = Response(self.UserSchema(many=True, exclude=['password']).dumps(self.users), status=200, mimetype="application/json")

if __name__ == '__main__':
    unittest.main()
