# SQLAlchemy core database implementation

from sqlalchemy import create_engine
from sqlalchemy import (Table, Column, Integer, String, MetaData, ForeignKey,
                        DateTime, Boolean)

# Global variables
SQLITE = 'sqlite'

# Table names
USER = 'user'
QUIZ = 'quiz'
QUESTION = 'question'


class Database():
    # http://docs.sqlalchemy.org/en/latest/core/engines.html
    DB_ENGINE = {
        SQLITE: 'sqlite:///{DB}'
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
        user = Table(USER, metadata,
                     Column('id', Integer, primary_key=True),
                     Column('num_correct', Integer),
                     Column('num_wrong', Integer))
        # when switching to ORM add Column('questions', ),
        quiz = Table(QUIZ, metadata,
                     Column('id', Integer, primary_key=True),
                     Column('num_correct', Integer),
                     Column('num_wrong', Integer),
                     Column('date_taken', DateTime),
                     Column('user_id', Integer, ForeignKey('user.id')))
        question = Table(QUESTION, metadata,
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
