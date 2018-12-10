# Quiz parent class
from abc import ABCMeta, abstractmethod


class Quiz(object):
    """ Provides general quiz functionality. Instantiated for each quiz.

    Param: quiz_length - how many questions the quiz will be 

    Attributes:
        quiz_length: number of questions quiz will test
        num_correct: number of questions answered correctly
        num_wrong: number of questions answered incorrectly
    """

    __metaclass__ = ABCMeta

    def __init__(self, quiz_length=10):
        self.quiz_length = quiz_length
        self.num_correct = 0
        self.num_wrong = 0

    @abstractmethod
    def quiz_type():
        """ Return a string representing what type of quiz this is """
        pass

    # TODO: current quiz score tracking


    # TODO: quiz_session - returns num_questions remaining
    @property
    def questions_remaining(self):
        return self.quiz_length - (self.num_correct + self.num_wrong)

    # TODO: get_random_item from provided dict (verbs, phrases etc)
    # Maybe this would be implemented in a Dict class??


