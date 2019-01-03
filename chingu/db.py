""" Define Database (factory class & DBInterface to handle CRUD  """
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Quiz, Question, Base


class Database():
    """ Create a database engine """
    DB_ENGINE = {
        'sqlite': 'sqlite:///{DB}',
    }

    # Main DB connection reference object
    db_engine = None

    def __init__(self, dbtype, username='', password='', dbname=':memory:'):
        """ Create database engine based on given parameters """
        dbtype = dbtype.lower()
        if dbtype in self.DB_ENGINE.keys():
            engine_url = self.DB_ENGINE[dbtype].format(DB=dbname)
            self.db_engine = create_engine(engine_url)
            print(self.db_engine)
        else:
            print("DBType is not found in DB_ENGINE")

    def create_tables(self):
        try:
            Base.metadata.create_all(self.db_engine)
            print('Tables created.')
        except Exception as e:
            print('An error occurred during table creation.')
            print(e)

    def drop_tables(self):
        try:
            Base.metadata.drop_all(self.db_engine)
            print('Tables dropped.')
        except Exception as e:
            print('An error occurred during table destruction.')
            print(e)

    def print_all_data(self):
        pass


class DB_Interface():
    """ Commit post-quiz data into database  """

    def __init__(self, db, user, quiz=None):
        """ Create a session object and assign objects to be commited """
        self.db = db
        self.session = self.create_session(db.db_engine)
        self.user = None
        self.load_user(user)
        self.quiz = quiz

    # sqlalchemy advises to place the session factory at the global level
    @staticmethod
    def create_session(db_engine):
        """ Return an instantiated session object """
        Session = sessionmaker(bind=db_engine)
        return Session()

    def load_user(self, user):
        """ Load user object from database by username.
            If user does not exist, create user.
        """
        while not self.user:
            self.user = self.session.query(User).filter_by(
                username=user.username).first()
            if self.user is None:
                self.create_user(user)

    def create_user(self, user):
        """ Commit a new user to the database """
        self.session.add(user)
        self.session.commit()
        print(f"New user '{user.username}' added to databse.")

    def commit_quiz(self):
        """ Instantiate quiz row and commit to database """
        quiz = Quiz(category=self.quiz.category, quiz_type=self.quiz.type,
                    questions=self.create_questions(),
                    user_id=self.user.user_id)
        self.session.add(quiz)
        self.session.commit()
        print('A new quiz has been addded to the database.')

    def create_questions(self):
        """ Return list of model.Question objects from quiz.question_list """
        return [Question(key=q.key, answer=q.answer,
                         definition=q.definition, question=q.question,
                         correct=q.correct)
                for q in self.quiz.question_list]















