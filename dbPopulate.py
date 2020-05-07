from sqlalchemy import MetaData, ForeignKey, Table, Column, Integer, String, LargeBinary, insert, select, update, delete, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.mysql import TINYINT, VARCHAR, TEXT
from flask_sqlalchemy import SQLAlchemy
import csv

alchemy = SQLAlchemy()


DB_NAME = "temp"  # UPDATE THIS if need be
DB_USER = "root"  # UPDATE THIS if need be
DB_PASS = "bkh8hut1HaL6JBLu"  # UPDATE THIS if need be
PORT_NUMBER = "3306"  # UPDATE THIS if need be
DB_SERVER = "127.0.0.1"

engine = alchemy.create_engine(sa_url='mysql+pymysql://{}:{}@{}:{}/{}'.format(DB_USER, DB_PASS, DB_SERVER, PORT_NUMBER, DB_NAME), engine_opts={"echo": True})
Session = sessionmaker(bind=engine)
connection = engine.connect()
meta = MetaData()


# Creating tables in the database
# users table
users = Table(
  'users', meta,
  Column('first_name', VARCHAR(45), nullable=False),
  Column('last_name', VARCHAR(45), nullable=False),
  Column('email', VARCHAR(45), primary_key=True, nullable=False),
  Column('password', TEXT(75), nullable=False),
)

# bookings table
bookings = Table(
  'bookings', meta,
  Column('booking_id', Integer(), primary_key=True, nullable=False, autoincrement=True),
  Column('user_email', VARCHAR(45), ForeignKey('users.email'), nullable=False),
  Column('car_id', Integer(), ForeignKey('cars.car_id'),nullable=False),
  Column('duration', Integer(), nullable=False),
  Column('completed', TINYINT(2), nullable=False)
)

# cars table
cars = Table(
  'cars', meta,
  Column('car_id', Integer(), primary_key=True, nullable=False, autoincrement=True),
  Column('name', VARCHAR(45), nullable=False),
  Column('available', TINYINT(1), nullable=False),
  Column('model_id', Integer(), ForeignKey('car_models.model_id'), nullable=False)
)

# car_models table
car_models = Table(
  'car_models', meta,
  Column('model_id', Integer(), primary_key=True, nullable=False, autoincrement=True),
  Column('make', VARCHAR(45), nullable=False),
  Column('model', VARCHAR(45), nullable=False),
  Column('year', Integer(), nullable=False),
  Column('capacity', Integer(), nullable=False)
)

# encodings table
encodings = Table(
  'encodings', meta,
  Column('image_id', Integer(), primary_key=True, nullable=False, autoincrement=True),
  Column('user_email', VARCHAR(45), ForeignKey('users.email'), nullable=False),
  Column('data', LargeBinary(length=(2**32)-1), nullable=False),
  Column('name', VARCHAR(45), nullable=False),
  Column('type', VARCHAR(45), nullable=False),
  Column('size', VARCHAR(45), nullable=False),
  Column('details', VARCHAR(45), nullable=False),
)

meta.drop_all(engine)
meta.create_all(engine)

# load data
# cars table
with open('test_data/car_models.csv') as csv_file:
  csv_reader = csv.reader(csv_file, delimiter=',')
  line_count = 0
  for row in csv_reader:
    ins = car_models.insert().values(make=row[0], model=row[1], year=row[2], capacity=row[3])
    connection.execute(ins)
    line_count += 1

# users table
with open('test_data/users.csv') as csv_file:
  csv_reader = csv.reader(csv_file, delimiter=',')
  line_count = 0
  for row in csv_reader:
    ins = users.insert().values(first_name=row[0], last_name=row[1], email=row[2], password=row[3])
    connection.execute(ins)
    line_count += 1

# Populate data to tables
session = Session()
session.commit()

connection.close()