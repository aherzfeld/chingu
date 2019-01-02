# SQLAlchemy core database implementation
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy import (Table, Column, Integer, String, MetaData, ForeignKey,
                        DateTime, Boolean)


class Database():
    # http://docs.sqlalchemy.org/en/latest/core/engines.html
    DB_ENGINE = {
        'sqlite': 'sqlite:///{DB}'
    }

    # Main DB connection reference object
    db_engine = None

    def __init__(self, dbtype, username='', password='', dbname=''):
        dbtype = dbtype.lower()
        if dbtype in self.DB_ENGINE.keys():
            engine_url = self.DB_ENGINE[dbtype].format(DB=dbname)
            self.db_engine = create_engine(engine_url)
            print(self.db_engine)
        else:
            print("DBType is not found in DB_ENGINE")

    def create_db_tables(self):
        metadata = MetaData()

        # when switching to ORM add Column('quizzes', ),
        # maybe just query for num_correct / wrong
        user = Table('user', metadata,
                     Column('id', Integer, primary_key=True),
                     Column('username', String, nullable=False),
                     Column('date_created', String))
                     # Column('num_correct', Integer),
                     # Column('num_wrong', Integer))
        # when switching to ORM add Column('questions', ),
        quiz = Table('quiz', metadata,
                     Column('id', Integer, primary_key=True),
                     Column('category', String, nullable=False),
                     Column('type', String, nullable=False),
                     # These can be retrieved via queries
                     # Column('num_correct', Integer),
                     # Column('num_wrong', Integer),
                     Column('date_taken', DateTime),
                     Column('user_id', Integer, ForeignKey('user.id')))
        question = Table('question', metadata,
                         Column('id', Integer, primary_key=True),
                         Column('key', String),
                         Column('answer', String),
                         Column('definition', String),
                         Column('correct', Boolean),
                         Column('quiz_id', Integer, ForeignKey('quiz.id')))
        try:
            metadata.create_all(self.db_engine)
            print('Tables created.')
        except Exception as e:
            print('An error occurred during table creation.')
            print(e)

    # Insert, Update, Delete
    def execute_query(self, query=''):
        """ Performs provided SQL query """
        if query == '':
            return
        print(query)
        with self.db_engine.connect() as connection:
            try:
                connection.execute(query)
            except Exception as e:
                print(e)

    def drop_table(self, table):
        self.execute_query("DROP TABLE {};".format(table))
        print('Dropped {} table.'.format(table))

    def print_all_data(self, table='', query=''):
        """ Prints all data from given table or executes optional query """
        if query != '':
            query = query
        else:
            query = "SELECT * FROM '{}';".format(table)
        print(query)
        with self.db_engine.connect() as connection:
            try:
                result = connection.execute(query)
            except Exception as e:
                print(e)
            else:
                for row in result:
                    print(row)
                result.close()
        print('\n')


# figuring out if I should load user/quiz ids upon instatiation
class DB_Interface():
    """ Instantiate with Database, User & Quiz objects to update data """

    def __init__(self, db, user, quiz):
        self.db = db
        self.user = user
        self.quiz = quiz

    @property
    def user_id(self):
        return self.db.execute_query(f"SELECT id FROM user WHERE \
username={self.user.username});")

    @property
    def quiz_id(self):
        return self.db.execute_query(f"SELECT id FROM quiz WHERE \
date_taken={self.quiz.date_taken});")

    def add_user(self):
        self.db.execute_query("INSERT INTO user (username, date_created)\
VALUES ('{}', '{}');".format(self.user.username, datetime.utcnow()))

    # is this even needed?? might be reverse to pull data from db in User
    def update_user(self):
        """ Use to update user data after completing quiz """
        pass

    def update_quiz(self):
        """ Use to update quiz data after completing quiz """
        self.execute_query(f"INSERT INTO quiz (category, type, date_taken,\
user_id) VALUES(\
{self.quiz.category} {self.quiz.type} {self.quiz.date_taken} {self.user_id});")

    def update_question(self):
        """ Use to update question data after completing quiz """
        pass












