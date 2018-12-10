# unittest of the quiz module
import unittest
from chingu.quiz import Quiz


class TestQuizDefaultSetup(unittest.TestCase):
    """ Test base class Quiz functionality """

    def setUp(self):
        """ Instantiate Quiz with default 10 questions """
        self.quiz = Quiz()

    def tearDown(self):
        del self.quiz

    def test_quiz_session(self):
        """ quiz_session function should track questions remaining """
        self.assertEqual(self.quiz.quiz_session, 10)

    def test_quiz_num_correct(self):
        self.assertEqual(self.quiz.num_correct, 0)

    def test_quiz_num_wrong(self):
        self.assertEqual(self.quiz.num_wrong, 0)


if __name__ == '__main__':
    unittest.main()