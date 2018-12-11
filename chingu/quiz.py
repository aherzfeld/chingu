# Quiz parent class & subject-specific quiz sub-classes
import random
from abc import ABCMeta, abstractmethod
from chingu.verb import Verb
from chingu.verblist import verb_list


class Quiz(object):
    """ Provides general quiz functionality. Instantiated for each quiz.

    Param: quiz_length - how many questions the quiz will be 

    Attributes:
        quiz_length: number of questions quiz will test
        num_correct: number of questions answered correctly
        num_wrong: number of questions answered incorrectly
    """

    __metaclass__ = ABCMeta

    def __init__(self, subject_dict, quiz_length=10):
        self.subject_dict = subject_dict
        self.quiz_length = quiz_length
        self.num_correct = 0
        self.num_wrong = 0

    @property
    @abstractmethod
    def quiz_type():
        """ Return a string representing what type of quiz this is """
        pass

    @abstractmethod
    def load_questions(subject_dict):
        """ Returns n(quiz_length) questions/answers as list of tuples """
        pass

    @abstractmethod
    def create_question(question_answer_tuple):
        """ Receives question/answer tuple and returns formatted string """
        pass

    @property
    def _question_keys(self):
        """ Returns (quiz_length) random keys from subject_dict """
        key_list = list(self.subject_dict)
        return random.sample(key_list, self.quiz_length)
        # return self._question_keys
    
    @property
    def score_percent(self):
        return round(self.num_correct / self.questions_asked, 2)

    @property
    def questions_asked(self):
        return self.num_correct + self.num_wrong

    @property
    def questions_remaining(self):
        return self.quiz_length - (self.num_correct + self.num_wrong)

    # TODO: get_random_item from provided dict (verbs, phrases etc)
    # Maybe this would be implemented in a Dict class??

    #TODO: start_quiz - loop through questions until done


class VerbQuiz(Quiz, Verb):
    """ Builds verb quiz logic on top of Quiz parent class

    Param: quiz_length - how many questions the quiz will be
    Param: subject_dict - always verb_dict in the case of VerbQuiz
    """

    def __init__(self, subject_dict, quiz_length=10):
        super().__init__(subject_dict, quiz_length=10)
        # create list of question/answer tuples
        # specific to present tense for now - add other options later
        # Turn this into a method that is passed tense methods as args
        # self.question_answers = [
        #     (q, self.conjugate_present(q), subject_dict[q])
        #     for q in self._question_keys]

    @property
    def question_data(self):
        """ Returns (question_key, answer, definition, question_str) 
        
        Params: subject_dict - subject specific dictionary {word: definition}
                option_method - method corresponding to quiz_option """
        
        return [(q, self.conjugate_present(q), self.subject_dict[q], self._question(q)) for q in self._question_keys]

    @staticmethod
    def _question(question_key):
        """ Receives question_answer tuple, returns formatted question str """
        return 'What is the present tense form of {}?'.format(question_key)

    # this functionality might be better incoporated into question_answers
    def question_list(self):
        pass























