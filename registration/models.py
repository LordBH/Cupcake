from flask_login import UserMixin
import psycopg2


class User(UserMixin):
    user_id = None

    def __init__(self, username, user_id=None):
        self.username = username

        if user_id is None:
            extra = SqlQuery()
            user_id = extra.execute("""SELECT * FROM user_table as u WHERE u.username='%s';""" % (username,))

        self.user_id = user_id

    def get_id(self):
        if self.user_id is not None:
            return self.user_id
        return None

    def __repr__(self):
        return self.username


class SqlQuery:
    db_name = 'keks_db'
    user_db = 'maxx'

    def connect(self, db_name=None, user_db=None):
        if db_name is not None:
            User.db_name = db_name
        if user_db is not None:
            User.user = user_db
        connection = psycopg2.connect("dbname=%s user=%s" % (self.db_name, self.user_db))
        cursor = connection.cursor()
        return cursor, connection

    def execute(self, sql, q=1):
        cursor, connection = self.connect()
        cursor.execute(sql)

        sql = sql.lower()
        if sql.startswith('select'):
            resp = SqlQuery.response(cursor, q)
        else:
            resp = None

        SqlQuery.close_connection(cursor, connection)

        return resp

    @staticmethod
    def close_connection(cursor, connection):

        connection.commit()
        cursor.close()
        connection.close()

    @staticmethod
    def response(cursor, q):

        if q == 1:
            resp = cursor.fetchone()
        elif q > 1:
            resp = cursor.fetchmany(q)
        else:
            resp = cursor.fetchall()

        return resp
