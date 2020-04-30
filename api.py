from sqlalchemy import MetaData, Table, Column, Integer, String, insert, select, update, delete
from flask_sqlalchemy import SQLAlchemy

"""
Instructions:
https://cloud.google.com/sql/docs/mysql/connect-external-app#sqlalchemy-tcp

Google Cloud SQL - set up instance, create database

Install the proxy client

Invoke proxy:
    ./cloud_sql_proxy -instances=projectID:region:instanceID=tcp:3306 &
    
should then work

Used MySQLWorkbench/cloud shell
"""

meta = MetaData()
users = Table(
    'users', meta,
    Column('user_id', Integer, primary_key=True),
    Column('first_name', String(16)),
    Column('last_name', String(16)),
)


class DBConnect:
    __connection = None
    __db = None
    __engine = None

    def __init__(self, app):
        if self.__db is None:
            self.__db = SQLAlchemy()
            self.__engine = self.__db.create_engine(
                sa_url='mysql+pymysql://root@127.0.0.1/temp',
                engine_opts={"echo": True}
            )
            self.__db.init_app(app)

    def get_users(self):
        """
        Test method: checking if accessing database as expect
        """
        connection = self.__engine.connect()
        sel = select([users])
        return connection.execute(sel)

# if __name__ == '__main__':
#     alchemy = SQLAlchemy()
# engine = alchemy.create_engine(sa_url='mysql+pymysql://root@127.0.0.1/temp', engine_opts={"echo": True})
# connection = engine.connect()
# meta = MetaData()

# meta.create_all(engine)
# ins = users.insert().values(user_id="2", first_name="don", last_name="uren")
# print(ins)
# connection.execute(ins)
# sel = select([users]).where(users.c.user_id == 2)
# result = connection.execute(sel)
# for row in result:
#     print(row)
