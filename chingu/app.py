import quiz
from db import Database


db = Database('sqlite', dbname='testdb.sqlite')

print('\nWelcome to Chingu, your Korean study buddy. ^^\n')

setup = quiz.QuizSetup()

newquiz = setup.create_quiz()

results = newquiz.start_quiz()

print('\nThank you for trying Chingu!\n')

newquiz.print_results(results)

print('We hope you come back soon!\n')

# TODO: create SQL statements to:


# TODO: update num_correct / num_wrong - user


# TODO: update num_correct / num_wrong, date_taken, user_id - quiz


# TODO: for question in questions, update key, answer, definition, correct, quiz_id
