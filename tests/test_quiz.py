# unittest of the quiz module
import unittest
import random
from chingu.quiz import Quiz, VerbQuiz
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

    def test_questions_remaining(self):
        """ quiz_session function should track questions remaining """
        self.assertEqual(self.quiz.questions_remaining, 10)

    def test_quiz_num_correct(self):
        self.assertEqual(self.quiz.num_correct, 0)

    def test_quiz_num_wrong(self):
        self.assertEqual(self.quiz.num_wrong, 0)

class TestQuizCustomSetup(unittest.TestCase):
    """ Test base class Quiz functionality """

    def setUp(self):
        """ Instantiate Quiz with 20 questions """
        self.quiz = Quiz(verb_list, 20)
        self.quiz.num_correct = 10
        self.quiz.num_wrong = 5

    def tearDown(self):
        del self.quiz

    def test_question_key_list_generation(self):
        self.assertTrue(len(self.quiz._question_keys), 20)
        for key in self.quiz._question_keys:
            self.assertIs(type(key), str)

    def test_questions_remaining(self):
        """ quiz_session function should track questions remaining """
        self.assertEqual(self.quiz.questions_remaining, 5)

    def test_questions_asked(self):
        self.assertEqual(self.quiz.questions_asked, 15)

    def test_quiz_num_correct(self):
        self.assertEqual(self.quiz.num_correct, 10)

    def test_quiz_num_wrong(self):
        self.assertEqual(self.quiz.num_wrong, 5)

    def test_quiz_score_percent(self):
        self.assertEqual(self.quiz.score_percent, 0.67)

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












if __name__ == '__main__':
    unittest.main()