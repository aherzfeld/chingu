# unittest of the quiz module
import unittest
import random
from chingu.quiz import Quiz, VerbQuiz, QuizInterface
from chingu.verblist import verb_list


class TestQuizDefaultSetup(unittest.TestCase):
    """ Test base class Quiz functionality """

    def setUp(self):
        """ Instantiate Quiz with default 10 questions """
        self.quiz = Quiz(verb_list)

    def tearDown(self):
        del self.quiz

    def test_question_key_list_generation(self):
        self.assertTrue(len(self.quiz._question_keys), 10)


class TestQuizCustomSetup(unittest.TestCase):
    """ Test base class Quiz functionality """

    def setUp(self):
        """ Instantiate Quiz with 20 questions """
        self.quiz = Quiz(verb_list, 20)

    def tearDown(self):
        del self.quiz

    def test_question_key_list_generation(self):
        self.assertTrue(len(self.quiz._question_keys), 20)
        for key in self.quiz._question_keys:
            self.assertIs(type(key), str)


class TestVerbQuiz(unittest.TestCase):

    def setUp(self):
        self.verbquiz = VerbQuiz(verb_list, 20)

    def tearDown(self):
        del self.verbquiz

    def test_question_keys_is_list(self):
        self.assertIs(type(self.verbquiz._question_keys), list)

    def test_question_key_list_generation(self):
        self.assertTrue(len(self.verbquiz._question_keys), 20)

    def test_create_questions(self):
        self.assertEqual(self.verbquiz._question('하다'),
            'What is the present tense form of 하다?')

    def test_population_of_question_data(self):
        data = self.verbquiz.question_data
        self.assertTrue(len(data), 20)
        
    def test_population_of_question_data_verbs_in_subject_dict(self):
        data = self.verbquiz.question_data
        for item in data:
            self.assertIn(item[0], self.verbquiz.subject_dict)
        
    def test_population_of_question_data_definitions(self):
        data = self.verbquiz.question_data
        for item in data:
            # ensure definitions are correct
            self.assertEqual(item[2], self.verbquiz.subject_dict[item[0]])
            
    def test_population_of_question_data_conjugations(self):
        data = self.verbquiz.question_data
        for item in data:    
            # ensure conjugations are correct
            self.assertEqual(item[1], self.verbquiz.conjugate_present(item[0]))

    def test_population_of_question_data_questions(self):
        data = self.verbquiz.question_data
        for item in data:
            # ensure question strings are properly formed
            self.assertIn(item[0], item[3])


class TestQuizInterfaceDefaultSetup(unittest.TestCase):

    def test_default_setup(self):
        self.quiz = VerbQuiz(verb_list)  # no quiz_length param
        data = self.quiz.question_data
        self.interface = QuizInterface(data)
        self.assertEqual(self.interface.quiz_length, 10)


class TestQuizInterfaceCustomSetup(unittest.TestCase):

    def test_custom_setup(self):
        self.quiz = VerbQuiz(verb_list, 20)
        data = self.quiz.question_data
        self.interface = QuizInterface(data)
        self.assertEqual(self.interface.quiz_length, 20)


class TestQuizInterfaceQuestionTracking(unittest.TestCase):

    def setUp(self):
        self.quiz = VerbQuiz(verb_list, 20)
        data = self.quiz.question_data
        self.interface = QuizInterface(data)
        self.interface.num_correct = 10
        self.interface.num_wrong = 5

    def tearDown(self):
        del self.quiz
        del self.interface

    def test_quiz_length(self):
        self.assertEqual(self.interface.quiz_length, 20)

    def test_questions_remaining(self):
        self.assertEqual(self.interface.questions_remaining, 5)

    def test_questions_asked(self):
        self.assertEqual(self.interface.questions_asked, 15)

    def test_num_correct(self):
        self.assertEqual(self.interface.num_correct, 10)

    def test_num_wrong(self):
        self.assertEqual(self.interface.num_wrong, 5)

    def test_score_percent(self):
        self.assertEqual(self.interface.score_percent, 0.67)


class TestQuizInterfaceStartQuiz(unittest.TestCase):

    def setUp(self):
        self.quiz = VerbQuiz(verb_list, 20)
        data = self.quiz.question_data
        self.interface = QuizInterface(data)    

    def tearDown(self):
        del self.quiz
        del self.interface

    def test_ask_question(self):
        # need to simulate user input here
        answer = self.interface.ask_question("Test question")
        self.assertIs(answer, str)

    def test_check_answer(self):
        self.assertTrue(self.interface.check_answer('해요', '해요'))
        self.assertFalse(self.interface.check_answer('해요', '해'))

    def test_update_score(self):
        initial_num_correct = self.interface.num_correct
        self.interface.update_score(True)
        updated_num_correct = self.interface.num_correct
        self.assertEqual(initial_num_correct, updated_num_correct)
        initial_num_wrong = self.interface.num_wrong
        self.interface.update_score(False)
        updated_num_wrong = self.interface.num_wrong
        self.assertEqual(initial_num_wrong, updated_num_wrong)

    def test_start_quiz(self):
        # need to simulate user input
        results = self.interface.start_quiz()
        self.assertIs(results[0], str)
        # add assertEqual to quiz type once implemented
        self.assertIs(results[1], int)
        self.assertEqual(results[1], self.interface.num_correct)
        self.assertIs(results[2], int)
        self.assertEqual(results[2], self.interface.num_wrong)
        self.assertIs(results[3], #timestamp)
        self.assertEqual(self.interface.quiz_length,
                         self.interface.questions_asked)





if __name__ == '__main__':
    unittest.main()