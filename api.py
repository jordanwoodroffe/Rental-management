from sqlalchemy import MetaData, Table, Column, Integer, String, insert, select, update, delete
from flask_sqlalchemy import SQLAlchemy

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
PORT_NUMBER = 3305  # UPDATE THIS if need be

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
                sa_url='mysql+pymysql://root@127.0.0.1:{}/{}'.format(PORT_NUMBER, DB_NAME),
                engine_opts={"echo": True}
            )  # UPDATE temp TO THE SQL DATABASE NAME
            self.__db.init_app(app)

    def get_users(self):
        """
        Test method: checking if accessing database as expect
        """
        connection = self.__engine.connect()
        sel = select([users])
        result = connection.execute(sel)
        connection.close()
        return result


# if __name__ == '__main__':
#     alchemy = SQLAlchemy()
#     engine = alchemy.create_engine(sa_url='mysql+pymysql://root@127.0.0.1:3305/temp', engine_opts={"echo": True})
#     connection = engine.connect()
#     # meta = MetaData()
#     #
#     # meta.create_all(engine)
#     # ins = users.insert().values(user_id="2", first_name="don", last_name="uren")
#     # print(ins)
#     # connection.execute(ins)
#     sel = select([users])
#     result = connection.execute(sel)
#     for row in result:
#         print(row)
