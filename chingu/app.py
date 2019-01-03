import quiz
from db import Database, DB_Interface
import models


db = Database('sqlite', dbname='testdb2.sqlite')

print('\nWelcome to Chingu, your Korean study buddy. ^^\n')

name = input('Enter username (or press enter to continue as guest):  ')
if name == '':
    name = 'guest'

user = models.User(username=name)

setup = quiz.QuizSetup()

quiz_io = setup.create_quiz()

finished_quiz = quiz_io.start_quiz()

db_io = DB_Interface(db, user, finished_quiz)
db_io.commit_quiz()

print('\nThank you for trying Chingu!\n')

quiz_io.print_results()

print('We hope you come back soon!\n')
