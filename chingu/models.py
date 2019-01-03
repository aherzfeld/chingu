from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import (Column, Integer, String, ForeignKey, Boolean)


Base = declarative_base()


class Question(Base):
    __tablename__ = 'questions'

    question_id = Column('id', Integer, primary_key=True)
    key = Column(String)
    answer = Column(String)
    definition = Column(String)
    question = Column(String)
    correct = Column(Boolean)
    quiz_id = Column(Integer, ForeignKey('quizzes.id'))

    quiz = relationship('Quiz', back_populates='questions')

    def __repr__(self):
        return (f"<Question(key='{self.key}', answer='{self.answer}', "
                f"definition='{self.definition}', question='{self.question}', "
                f"correct={self.correct}, quiz_id={self.quiz_id})>")


class Quiz(Base):
    __tablename__ = 'quizzes'

    quiz_id = Column('id', Integer, primary_key=True)
    category = Column(String, nullable=False)
    quiz_type = Column('type', String, nullable=False)
    taken_on = Column(String,
                      default=datetime.utcnow().isoformat(' ', 'seconds'))
    user_id = Column(Integer, ForeignKey('users.id'))

    questions = relationship('Question', order_by=Question.question_id,
                             back_populates='quiz')
    user = relationship('User', back_populates='quizzes')

    def __repr__(self):
        return (f"<Quiz(category='{self.category}', "
                f"quiz_type='{self.quiz_type}', quiz_id={self.quiz_id}, "
                f"taken_on={self.taken_on}>)")


class User(Base):
    __tablename__ = 'users'

    user_id = Column('id', Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    # String because sqlite has no DateTime type isoformat='YYYY-MM-DD'
    created_on = Column(String,
                        default=datetime.utcnow().isoformat(' ', 'seconds'))
    # num_correct , num_wrong

    quizzes = relationship('Quiz', order_by=Quiz.quiz_id,
                           back_populates='user')

    @property
    def num_correct(self):
        pass

    @property
    def num_wrong(self):
        pass

    def __repr__(self):
        return (f"<User(user_id={self.user_id}, username='{self.username}',"
                f" created_on={self.created_on})")
