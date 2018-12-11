# Quiz parent class & subject-specific quiz sub-classes
import random
from abc import ABCMeta, abstractmethod
from chingu.verb import Verb
from chingu.verblist import verb_list


class Quiz(object):
    """ Provides general quiz functionality. Instantiated for each quiz.

    Params: quiz_length - how many questions the quiz will be
            subject_dict - subject specific dict (e.i. verb_list)

    Attributes:
        quiz_length: number of questions quiz will test
        num_correct: number of questions answered correctly
        num_wrong: number of questions answered incorrectly """

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

    #TODO: start_quiz - loop through questions until done
    # This will be implemented in IO_Manager class


class VerbQuiz(Quiz, Verb):
    """ Main purpose is to create question_data to pass to IO Manager Object

    Param: quiz_length - how many questions the quiz will be
    Param: subject_dict - always verb_dict in the case of VerbQuiz
    """

    def __init__(self, subject_dict, quiz_length=10):
        super().__init__(subject_dict, quiz_length=10)

    # modify to accept option_method as arg
    @property
    def question_data(self):
        """ Returns (question_key, answer, definition, question_str) 
        
        Utilizes: subject_dict - subject specific dictionary {word: definition}
                  conjugate_present(verb) - method from Verb class
                  _question_keys - list of keys for subject_dict from Quiz
                  option_method - method corresponding to quiz_option """
        
        return [(q, self.conjugate_present(q), self.subject_dict[q],
                self._question(q)) for q in self._question_keys]

    # modify to accept option_method as arg
    @staticmethod
    def _question(question_key):
        """ Receives question_answer tuple, returns formatted question str """
        return 'What is the present tense form of {}?'.format(question_key)
























