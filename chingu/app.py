import quiz


print('\nWelcome to Chingu, your Korean study buddy. ^^\n')

setup = quiz.QuizSetup()

quiz_io = setup.create_quiz()

finished_quiz = quiz_io.start_quiz()

print('\nThank you for trying Chingu!\n')

quiz_io.print_results()

print('We hope you come back soon!\n')
