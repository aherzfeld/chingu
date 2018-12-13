import quiz


print('\nWelcome to Chingu, your Korean study buddy. ^^\n')

# instantiate default VerbQuiz - quiz_type: present, quiz_length: 10
verbquiz = quiz.VerbQuiz(quiz.verb_list, quiz_length=5)

quiz_data = verbquiz.quiz_data
quiz_type = verbquiz.quiz_type


io = quiz.QuizInterface(quiz_data, quiz_type)

results = io.start_quiz()

print('\nThank you for trying Chingu!\n')

print('You completed a {} tense verb quiz at {}.\n\n\
You got {} questions correct and {} questions wrong.\n'.format(results[0],
    results[3], results[1], results[2]))

print('We hope you come back soon!\n')
