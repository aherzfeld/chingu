# unittest of the quiz module
import unittest
from chingu.quiz import Quiz
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
        pass
















if __name__ == '__main__':
    unittest.main()