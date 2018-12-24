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


# still need to test additional methods (maybe covered in quiz io)
class TestVerbQuiz(unittest.TestCase):

    def setUp(self):
        self.verbquiz = quiz.VerbQuiz(quiz_type='present', quiz_length=15)

    def tearDown(self):
        del self.verbquiz

    def test_quiz_type(self):
        self.assertEqual(self.verbquiz.type, 'present')

    def test_creation_of_key_list_with_proper_length(self):
        key_list = self.verbquiz.make_key_list
        self.assertEqual(len(key_list), 15)

    def test_keys_in_key_list_are_from_verb_dict(self):
        key_list = self.verbquiz.make_key_list
        for key in key_list:
            self.assertIn(key, quiz.verb_dict)

    def test_creation_of_question_list_with_proper_length(self):
        question_list = self.verbquiz.make_question_list
        self.assertEqual(len(question_list), 15)

    def test_creation_of_question_list_with_question_objects(self):
        question_list = self.verbquiz.make_question_list
        for q in question_list:
            self.assertIsInstance(q, quiz.Question)

    def test_proper_instantion_of_question_objects(self):
        question_list = self.verbquiz.make_question_list
        q = question_list[0]
        # check that answer was properly calculated
        self.assertEqual(q.answer, self.verbquiz.type_method(q.key))
        self.assertEqual(q.definition, self.verbquiz.dictionary[q.key])
        self.assertIs(type(q.question), str)
        self.assertEqual(q.correct, None)


class TestQuizInterface(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass






















if __name__ == '__main__':
    unittest.main()
