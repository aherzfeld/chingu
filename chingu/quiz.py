# Quiz parent class & subject-specific quiz sub-classes
import random
from datetime import datetime
from abc import ABCMeta
from chingu.verb import Verb
from chingu.verblist import verb_dict
from models import Question


class Quiz(object):
    """ Provides general quiz functionality. Instantiated for each quiz.

    Params:
        quiz_type - [category] quiz subtype (param: quiz_type)
        quiz_length - how many questions the quiz will be

    Class Attributes:
        category - Category of child quiz class (i.e. 'verb')
        dictionary - subject specific dict (i.e. verb_dict)
        types - dict of subtypes(keys) with corresponding methods(values)

    Attributes:
        type - category specific subtype (i.e. 'definition')
        type_method - algorithm to generate answer from key based on type
        length - number of questions quiz will test (param: quiz_length)
        key_list - (quiz_length) random keys from dictionary
        question_list - (quiz_length) list of Question objects
        num_correct - number of questions answered correctly
        num_wrong - number of questions answered incorrectly
    """

    __metaclass__ = ABCMeta

    # these will be class variables unique to each [Category]Quiz child class
    category = None
    dictionary = None
    types = None

    def __init__(self, quiz_type=None, quiz_length=10):
        self.type = quiz_type
        self.length = int(quiz_length)
        # add underscore to make private??
        self.type_method = self.types[self.type]
        # add underscore to make private??
        self.key_list = self.make_key_list
        self.question_list = self.make_question_list
        self.num_correct = 0
        self.num_wrong = 0
        # Will be handled by the Model
        # self.date_taken = None

    # can use string formatting for title case
    def __str__(self):
        """ Return quiz_string for printing based on quiz_specs """

        if self.type == 'definition':
            return f'{self.category} {self.type} quiz'
        else:
            return f'{self.type} tense {self.category} quiz'

    @property
    def make_key_list(self):
        """ Returns (quiz_length) random keys from dictionary """
        key_list = list(self.dictionary)
        return random.sample(key_list, self.length)

    # TODO: add question string creation here
    @staticmethod
    def question_string(key, quiz_type):
        """ Receives key & quiz_type, returns formatted question str """

        if quiz_type == 'definition':
            return '\nWhat is the definition of {}?'.format(key)
        else:
            return '\nWhat is the {} tense form of {}?'.format(
                quiz_type, key)

    @property
    def make_question_list(self):
        """ Returns list of Question objects - one for each key in key_list """

        return [Question(k, self.type_method(k), self.dictionary[k],
                self.question_string(k, self.type)) for k in self.key_list]

    ###### THESE WILL ALL BE MOVED TO QUIZ MANAGER ########

    # TODO: this can be removed (replaced by query in QuizManager)
    @property
    def questions_asked(self):
        return self.num_correct + self.num_wrong

    # TODO: this can be removed (replaced by query in QuizManager)
    @property
    def questions_remaining(self):
        return self.length - (self.num_correct + self.num_wrong)

    # TODO: this can be removed (replaced by query in QuizManager)
    @property
    def score_percent(self):
        return round(self.num_correct / self.questions_asked, 2)

    # TODO: this can be removed (replaced by query in QuizManager)
    # can this be better implemented with setters, getters?
    def update_score(self, boolean):
        """ Receives Boolean, updates num_correct(True) / num_wrong(False) """
        if not isinstance(boolean, bool):
            return False
        if boolean:
            self.num_correct += 1
        elif not boolean:
            self.num_wrong += 1
        return True


class VerbQuiz(Quiz, Verb):
    """ Main purpose is to create question_data to pass to QuizInterface

    Params:
        quiz_type - Verb quiz subtype (i.e. 'present')
        quiz_length - how many questions the quiz will be

    Class Attributes:
        category - Category of child quiz class (i.e. 'verb')
        dictionary - subject specific dict (i.e. verb_dict)
        types - dict of subtypes(keys) with corresponding methods(values)

    Attributes:
        type - Verb category quiz subtype (param: quiz_type)
        type_method - algorithm to generate answer from key based on type
        length - number of questions (param: quiz_length)
        key_list - (quiz_length) random keys from dictionary
        question_list - (quiz_length) list of Question objects
    """

    category = 'verb'
    dictionary = verb_dict
    types = {'definition': dictionary.get,
             'present': Verb.conjugate_present,
             'future': 'not yet implemented'}

    def __init__(self, quiz_type='present', quiz_length=10):
        super().__init__(quiz_type, quiz_length)


# TODO: might change to create quiz via static method (without need to instantiate)
class QuizSetup():
    """ Gathers user input to instantiate quiz """

    # NounQuiz not yet implemented
    categories = {'verb': VerbQuiz,
                  'noun': 'NounQuiz'}

    types = {'verb': ('definition', 'present', 'future'),
             'noun': ('demo1', 'demo2')}  # not yet implemented

    def __init__(self, category=None, quiz_type=None, length=None):
        """ Prompts user for input upon initialization """

        self.category = category
        self.type = quiz_type
        self.length = length
        self.quizclass = self.categories[self.category]

    def setup_quiz(self):
        """ Returns quiz object based on init specifications """

        return self.quizclass(self.type, self.length)


class QuizManager():
    """ Statelessly Administer Quiz IO via Flask """

    @staticmethod
    def check(answer, user_answer):
        """ Return True if user input answer is correct """

        # the length check allows for incomplete, but close-enough definitions
        return user_answer in answer and (
            len(user_answer) >= (len(answer) / 3))


# TODO: will become obsolete once QuizManger is complete
class QuizInterface():
    """ Handles User-facing quiz IO and scoretracking

    Params:
        quiz - instantiated Quiz object via QuizSetup
        user - instantiated User object of user taking the quiz
    """

    def __init__(self, quiz):

        self.quiz = quiz

    @staticmethod
    def get_input(question_string):
        """ Prompt user for answer input. Returns user_answer string """

        return input(question_string + '  ')

    # TODO: update to use question object DONE
    def ask_question(self, question):
        """ Returns question object with .correct attribute updated,
            increments quiz.num_correct / num_wrong based on user input

        Param: question - instance of Question
        """

        user_answer = self.get_input(question.question)
        answer_result = question.check(user_answer)
        self.quiz.update_score(answer_result)
        return question

    def feedback(self, question):
        """ Returns feedback string to be printed by print_feedback

        Param:
            question object with updated results via self.ask_question
        """

        meta_data = '{:.0%} correct with {} question{} remaining.'.format(
                    self.quiz.score_percent, self.quiz.questions_remaining,
                    '' if self.quiz.questions_remaining == 1 else 's')

        if question.correct:
            return('\nCorrect! ' + meta_data + '\n')
        else:
            return('\nHmm not quite. The correct answer is {}.\n'.format(
                question.answer) + meta_data + '\n')

    @staticmethod
    def print_feedback(feedback_string):
        print(feedback_string)

    def start_quiz(self):
        """ Loop through quiz.question_list, receiving and giving user IO.
            Returns updated quiz object
        """

        for q in self.quiz.question_list:
            self.print_feedback(self.feedback(self.ask_question(q)))

        self.quiz.date_taken = datetime.utcnow()
        # this returned quiz object could later be passed to db object
        return self.quiz

    def print_results(self):
        """ Prints formatted string summary of post-quiz information"""

        print('You completed a {} on {}.\n\n\
            You got {} question{} correct and {} question{} wrong.\n'.format(
            self.quiz.__str__(), self.quiz.date_taken.strftime('%x'),
            self.quiz.num_correct, '' if self.quiz.num_correct == 1 else 's',
            self.quiz.num_wrong, '' if self.quiz.num_wrong == 1 else 's'))
        return True
