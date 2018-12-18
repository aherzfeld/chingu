import quiz


print('\nWelcome to Chingu, your Korean study buddy. ^^\n')


####### TESTING SECTION #########
# TODO: Allow user to configure quiz options
setup = quiz.QuizSetup()

newquiz = setup.create_quiz()

quiz_data = newquiz.quiz_data
quiz_type = newquiz.quiz_string


io = quiz.QuizInterface(quiz_data, quiz_type)

results = io.start_quiz()

print('\nThank you for trying Chingu!\n')

io.print_results(results)

quit()
####### END TESTING SECTION #########

# instantiate default VerbQuiz - quiz_type: present, quiz_length: 10
verbquiz = quiz.VerbQuiz(quiz.verb_list, quiz_length=2)

quiz_data = verbquiz.quiz_data
quiz_type = verbquiz.quiz_string


io = quiz.QuizInterface(quiz_data, quiz_type)

results = io.start_quiz()

print('\nThank you for trying Chingu!\n')

io.print_results(results)

# TODO: add print results method to QuizInterface

print('We hope you come back soon!\n')

# TODO: fix datetime to present current datetime

# TODO: give feedback after each answer
# % correct. num_remaining questions remaining

# TODO: add a \n after each question