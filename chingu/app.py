import quiz


print('\nWelcome to Chingu, your Korean study buddy. ^^\n')

setup = quiz.QuizSetup()

newquiz = setup.create_quiz()

results = newquiz.start_quiz()

print('\nThank you for trying Chingu!\n')

newquiz.print_results(results)

print('We hope you come back soon!\n')




