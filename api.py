from sqlalchemy import MetaData, Table, Column, Integer, String, insert, select, update, delete
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from utils import get_random_alphaNumeric_string, hash_password, verify_password
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
DB_NAME = "temp"  # UPDATE THIS if need be
DB_USER = "root"  # UPDATE THIS if need be
DB_PASS = "bkh8hut1HaL6JBLu"  # UPDATE THIS if need be
PORT_NUMBER = "3306"  # UPDATE THIS if need be

meta = MetaData()
users = Table(
    'users', meta,
    Column('first_name', String(16), nullable=False),
    Column('last_name', String(16), nullable=False),
    Column('email', String(32), primary_key=True, nullable=False),
    Column('password', String(64), nullable=False),
    Column('salt', String(64), nullable=False),
)


class DBConnect:
    __connection = None
    __db = None
    __engine = None

    def __init__(self, app):
        if self.__db is None:
            self.__db = SQLAlchemy()
            self.__engine = self.__db.create_engine(
                sa_url='mysql+pymysql://' + DB_USER + ':' + DB_PASS + '@127.0.0.1:{}/{}'.format(PORT_NUMBER, DB_NAME),
                engine_opts={"echo": True}
            )  # UPDATE temp TO THE SQL DATABASE NAME
            self.__db.init_app(app)
            self.__Session = sessionmaker(self.__engine)

    def create_users_table(self):
        connection = self.__engine.connect()
        meta = MetaData()
        users = Table(
            'users', meta,
            Column('first_name', String(16), nullable=False),
            Column('last_name', String(16), nullable=False),
            Column('email', String(32), primary_key=True, nullable=False),
            Column('password', String(64), nullable=False),
            Column('salt', String(64), nullable=False),
        )
        meta.create_all(self.__engine)

    def get_users(self):
        """
        Get users: Return all users in the users table
        """
        connection = self.__engine.connect()
        sel = select([users])
        result = connection.execute(sel)
        connection.close()
        return result

    def add_users(self, first_name, last_name, email, password):
        """
        Add method: Add new user to the users table
        """
        connection = self.__engine.connect()
        sess = self.__Session()
        qur = sess.query(users).filter_by(email=email).all()
        if (len(qur) > 0):
            connection.close()
            return False
        else:
            salt = get_random_alphaNumeric_string(10)
            ins = users.insert().values(first_name=first_name, last_name=last_name, email=email, password=hash_password(password, salt), salt=salt)
            print(ins)
            connection.execute(ins)
            connection.close()
            return True

    def get_user_with_email(self, email):
        """
        Check email method: checking if an email is in users table (user is registered)
        """    
        connection = self.__engine.connect()
        sess = self.__Session()
        qur = sess.query(users).filter_by(email=email).all()
        print(qur)
        connection.close()
        return qur

    def user_authentication(self, email, password):
        """
        User authentication method: Allow user to login with correct login information
        """
        connection = self.__engine.connect()
        sess = self.__Session()
        qur = sess.query(users).filter_by(email=email).all()
        if (len(qur) == 0):
            connection.close()
            # This email has not been registered
            return ("email error", None, None, None)
        else:
            salt = qur[0][4]
            key = qur[0][3]
            if verify_password(key, password, salt):
                connection.close()
                # Login successful
                return ("successful", qur[0][0], qur[0][1], qur[0][2])
            else:
                connection.close()
                # Incorrect password
                return ("password error", None, None, None)

            

# if __name__ == '__main__':
#     alchemy = SQLAlchemy()
#     engine = alchemy.create_engine(sa_url='mysql+pymysql://' + DB_USER + ':' + DB_PASS + '@127.0.0.1:' + PORT_NUMBER + '/' + DB_NAME, engine_opts={"echo": True})
#     connection = engine.connect()
#     meta = MetaData()
#     users = Table(
#         'users', meta,
#         Column('first_name', String(16), nullable=False),
#         Column('last_name', String(16), nullable=False),
#         Column('email', String(32), primary_key=True, nullable=False),
#         Column('password', String(64), nullable=False),
#         Column('salt', String(64), nullable=False),
#     )
#     # users.drop(engine)
#     meta.create_all(engine)

#     ins = users.insert().values(first_name="dan", last_name="dao", email = "dan@gmail.com" ,password = "P@ssw0rd")
#     print(ins)
#     connection.execute(ins)
    
#     sel = select([users])
#     result = connection.execute(sel)
#     for row in result:
#         print(row)
