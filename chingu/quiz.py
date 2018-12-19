# Quiz parent class & subject-specific quiz sub-classes
import random
from datetime import datetime
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

    def __init__(self, subject_dict, quiz_type=None, quiz_length=10):
        self.subject_dict = subject_dict
        self.quiz_type = quiz_type
        self.quiz_length = quiz_length

    # Instead of this, create a __str__ method
    # @property
    # @abstractmethod
    # def quiz_type():
    #     """ Return a string representing what type of quiz this is """
    #     pass

    @abstractmethod
    def question_data(self):
        """ Returns (question_key, answer, definition, question_str) """
        pass

    @abstractmethod
    def _question(question_key):
        """ Receives question_key and returns formatted string """
        pass

    @property
    def _question_keys(self):
        """ Returns (quiz_length) random keys from subject_dict """
        key_list = list(self.subject_dict)
        return random.sample(key_list, self.quiz_length)


class VerbQuiz(Quiz, Verb):
    """ Main purpose is to create question_data to pass to QuizInterface

    Param: quiz_length - how many questions the quiz will be
    Param: subject_dict - always verb_dict in the case of VerbQuiz
    """

    def __init__(self, subject_dict, quiz_type='present', quiz_length=10):
        super().__init__(subject_dict, quiz_type, quiz_length)

    # modify to accept option_method as arg
    @property
    def quiz_data(self):
        """ Returns - [(question_key, answer, definition, question_str), ...]] 
        
        Utilizes: subject_dict - subject specific dictionary {word: definition}
                  conjugate_present(verb) - method from Verb class
                  _question_keys - list of keys for subject_dict from Quiz
                  option_method - method corresponding to quiz_option """
        
        return [(q, self.conjugate_present(q), self.subject_dict[q],
                self._question(q)) for q in self._question_keys]

    # modify to accept option_method as arg
    @staticmethod
    def _question(question_key):
        """ Receives question_key, returns formatted question str """
        return '\nWhat is the present tense form of {}?'.format(question_key)

    @property
    def quiz_string(self):
        """ Return quiz_type string to pass to QuizInterface """
        return '{} tense Verb Quiz'.format(self.quiz_type)
    

class QuizSetup():
    """ Gathers user input to instantiate quiz """

    # NounQuiz not yet implemented
    categories = {'verb': (VerbQuiz, verb_list),
                  'noun': ('NounQuiz', 'noun_list')}

    types = {'verb': ('definition', 'present', 'future'),
             'noun': ('demo1', 'demo2')}  # not yet implemented

    def __init__(self):
        """ Prompts user for input upon initialization """

        self.category = None
        while self.category not in QuizSetup.categories:
            self.category = input('Choose a quiz - Options: {}:  '.format(
                [key for key in QuizSetup.categories]))
        self.type = None
        while self.type not in QuizSetup.types[self.category]:
            self.type = input('Choose a category - Options: {}:  '.format(
                [option for option in QuizSetup.types[self.category]]))
        self.length = None
        while self.length not in range(1, 20):
            self.length = int(input('How many questions? (1 - 20):  '))
        self.quizclass = self.categories[self.category][0]
        self.dict = self.categories[self.category][1]

    def setup_quiz(self):
        """ Returns quiz object based on init specifications """

        return self.quizclass(self.dict, self.type, self.length)

    # TODO: create io object
    def create_quiz(self):
        """ Returns Instantiated QuizInterface object """
        quiz = self.setup_quiz()
        quiz_data = quiz.quiz_data
        quiz_type = quiz.quiz_string

        return QuizInterface(quiz_data, quiz_type)


# Maybe score tracking should be broken into its own class
# TODO: inherit from a User object to track persistant quiz history
class QuizInterface():
    """ Handles User-facing quiz IO and scoretracking """

    def __init__(self, quiz_data, quiz_type=None):
        """ Param: quiz_data - created by [Subject]Quiz object 
        (question_key, answer, definition, question_str) 
        Param: quiz_type: Quiz.quiz_string"""

        self.quiz_data = quiz_data
        self.quiz_type = quiz_type
        self.quiz_length = len(quiz_data)
        self.num_correct = 0
        self.num_wrong = 0

    # add quiz_type functionality
    def start_quiz(self):
        """ Loop through quiz_data and return results tuple.
        return (quiz_type, num_correct, num_wrong, timestamp) """
        for q in self.quiz_data:
            self.print_feedback(self.feedback(self.ask_question(q)))
        # TODO: implement the quiz_type return value
        return (self.quiz_type, self.num_correct, self.num_wrong,
                datetime.utcnow())

    # maybe this should return T / F for feedback
    def ask_question(self, q):
        """ Returns answer_result boolean, increments num_correct / num_wrong 
        based on user input
        
        Param: q = (question_key, answer, definition, question_str) """

        user_answer = self.get_input(q[3])
        answer_result = self.check_answer(q[1], user_answer)
        self.update_score(answer_result)
        return answer_result

    # in progress , write test (% might need work)
    def feedback(self, answer_result):
        """ Returns feedback string to be printed by print_feedback
        Param: answer_result - True if correct / False if incorrect"""
        meta_data = '{}% correct with {} questions remaining.'.format(
                self.score_percent * 100, self.questions_remaining)
        if answer_result == True:
            return('\nCorrect! ' + meta_data + '\n')
        else:
            return('\nHmm not quite. ' + meta_data + '\n')

    @staticmethod
    def print_feedback(feedback_string):
        print(feedback_string)

    @staticmethod
    def get_input(question_string):
        """ Prompt user for answer input. Returns user_answer string """
        return input(question_string + '  ')

    @staticmethod
    def check_answer(answer, user_answer):
        """ Return True if user input answer is correct """
        return answer == user_answer

    # can this be better implemented with setters, getters?
    def update_score(self, boolean):
        """ Receives Boolean, updates num_correct(True) / num_wrong(False) """
        if not isinstance(boolean, bool):
            return False
        if boolean == True:
            self.num_correct += 1
        elif boolean == False:
            self.num_wrong += 1
        return True

    @property
    def score_percent(self):
        return round(self.num_correct / self.questions_asked, 2)

    @property
    def questions_asked(self):
        return self.num_correct + self.num_wrong

    @property
    def questions_remaining(self):
        return self.quiz_length - (self.num_correct + self.num_wrong)

    # TODO: print results method
    @staticmethod
    def print_results(results):
        print('You completed a {} on {}.\n\n\
You got {} questions correct and {} questions wrong.\n'.format(results[0],
    results[3].strftime('%x'), results[1], results[2]))
        return True

     



















