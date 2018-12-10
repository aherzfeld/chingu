# Quiz parent class
from abc import ABCMeta, abstractmethod


class Quiz(object):
    """ Provides general quiz functionality. Instantiated for each quiz.

    Param: Specific quiz category class to be used (eg: VerbQuiz)
    Param: quiz_length - how many questions the quiz will be """

    __metaclass__ = ABCMeta

    def __init__(self, quiz_length):
        self.quiz_length = quiz_length

    @abstractmethod
    def quiz_type():
        """ Return a string representing what type of quiz this is """
        pass

    # TODO: current quiz score tracking


    # TODO: quiz_session - arg quiz_length, keeps track of current quiz progress

    
    # TODO: get_random_item from provided dict (verbs, phrases etc)
    # Maybe this would be implemented in a Dict class??


