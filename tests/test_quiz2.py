# unittest of the quiz module
import unittest
from unittest.mock import patch
import random
import datetime
import chingu.quiz as quiz


class TestQuizSetup(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_setup_quiz_based_on_init_specifications(self):
        pass

    def test_create_quiz_by_returning_instantiated_quiz_interface(self):
        pass


class TestQuestion(unittest.TestCase):
    """ Receive key as arg and has access to subject_dict """

    def setUp(self):
        # Question(key, answer, definition, quiz_type)
        self.question = quiz.Question('오다', '와요', 'to come', 'definition')

    def tearDown(self):
        del self.question

    def test_create_question_string_for_definition_question(self):
        q_string = self.question.question_string('오다', 'definition')
        self.assertEqual(q_string, '\nWhat is the definition of 오다?')

    def test_create_question_string_for_conjugation_question(self):
        q_string = self.question.question_string('오다', 'present')
        self.assertEqual(q_string, '\nWhat is the present tense form of 오다?')

    def test_check_user_answer_for_correctness_on_correct_answer(self):
        self.assertTrue(self.question.check('와요'))

    def test_check_user_answer_for_correctness_on_wrong_answer(self):
        self.assertFalse(self.question.check('와아'))


class TestVerbQuiz(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_population_of_quiz_data(self):
        pass


if __name__ == '__main__':
    unittest.main()
