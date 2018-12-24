# Quiz parent class & subject-specific quiz sub-classes
import random
from datetime import datetime
from abc import ABCMeta, abstractmethod
from chingu.verb import Verb
from chingu.verblist import verb_dict


class Question():
    """ Question object that will be a part of a Quiz's quiz_data

    Param: key_list - (quiz_length) random keys from dictionary

    Attributes:
        key - word/item to be tested from dictionary
        answer - correct answer generated via Quiz.type_method
        definition - word definition
        question - question string for presentation to user
        correct - boolean, True if user answered correctly
    """

    # these param will have to be prepared by Quiz
    def __init__(self, key, answer, definition, quiz_type):
        self.key = key
        self.answer = answer
        self.definition = definition
        self.question = self.question_string(key, quiz_type)
        self.correct = None

    @staticmethod
    def question_string(key, quiz_type):
        """ Receives key & quiz_type, returns formatted question str """

        if quiz_type == 'definition':
            return '\nWhat is the definition of {}?'.format(key)
        else:
            return '\nWhat is the {} tense form of {}?'.format(
                quiz_type, key)

    # currently in QuizInterface
    def check(self, user_answer):
        """ Return True if user input answer is correct """

        # the length check allows for incomplete, but close enough definitions
        self.correct = user_answer in self.answer and (
            len(user_answer) >= (len(self.answer) / 3))
        return self.correct


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

    def __str__(self):
        pass

    @property
    def make_key_list(self):
        """ Returns (quiz_length) random keys from dictionary """
        key_list = list(self.dictionary)
        return random.sample(key_list, self.length)

    # implement this fully here , remove from VerbQuiz
    @property
    def make_question_list(self):
        """ Returns list of Question objects - one for each key in key_list """

        return [Question(k, self.type_method(k), self.dictionary[k], self.type)
                for k in self.key_list]


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


    # DELETE THIS AFTER RUNNING TESTS
    # @property
    # def quiz_data(self):
    #     """ Returns - [(question_key, answer, definition, question_str), ...]]

    #     Utilizes: dictionary - subject specific dictionary {word: definition}
    #               conjugate_present(verb) - method from Verb class
    #               _question_keys - list of keys for dictionary from Quiz
    #               option_method - method corresponding to quiz_option """

    #     return [(q, self.type_method(q), self.dictionary[q],
    #              self._question(q)) for q in self.key_list]


class QuizSetup():
    """ Gathers user input to instantiate quiz """

    # NounQuiz not yet implemented
    categories = {'verb': (VerbQuiz, verb_dict),
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

    def create_quiz(self):
        """ Returns Instantiated QuizInterface object """
        quiz = self.setup_quiz()
        quiz_data = quiz.quiz_data
        quiz_specs = (self.category, self.type)

        return QuizInterface(quiz_data, quiz_specs)


# Maybe score tracking should be broken into its own class
# TODO: inherit from a User object to track persistant quiz history
class QuizInterface():
    """ Handles User-facing quiz IO and scoretracking """

    def __init__(self, quiz_data, quiz_specs=None):
        """ Param: quiz_data - created by [Subject]Quiz object
        (question_key, answer, definition, question_str)

        Param: quiz_type: Quiz.quiz_string"""

        self.quiz_data = quiz_data
        self.quiz_specs = quiz_specs
        self.quiz_length = len(quiz_data)
        self.num_correct = 0
        self.num_wrong = 0

    def start_quiz(self):
        """ Loop through quiz_data and return results tuple.
        return (quiz_type, num_correct, num_wrong, timestamp) """
        for q in self.quiz_data:
            self.print_feedback(self.feedback(self.ask_question(q)))
        # TODO: implement the quiz_type return value
        return (self.quiz_specs, self.num_correct, self.num_wrong,
                datetime.utcnow())

    def ask_question(self, q):
        """ Returns answer_result boolean, increments num_correct / num_wrong
        based on user input

        Param: q = (question_key, answer, definition, question_str) """

        answer = q[1]
        user_answer = self.get_input(q[3])
        answer_result = self.check_answer(q[1], user_answer)
        self.update_score(answer_result)
        return (answer_result, answer)

    def feedback(self, answer_results):
        """ Returns feedback string to be printed by print_feedback
        Param: answer_results tuple
        [0] = True if correct / False if incorrect
        [1] = correct answer """

        meta_data = '{:.0%} correct with {} question{} remaining.'.format(
                    self.score_percent, self.questions_remaining,
                    '' if self.questions_remaining == 1 else 's')
        if answer_results[0]:
            return('\nCorrect! ' + meta_data + '\n')
        else:
            return('\nHmm not quite. The correct answer is {}.\n'.format(
                answer_results[1]) + meta_data + '\n')

    @staticmethod
    def print_feedback(feedback_string):
        print(feedback_string)

    @staticmethod
    def get_input(question_string):
        """ Prompt user for answer input. Returns user_answer string """
        return input(question_string + '  ')

    # implementing in Question , remove from here
    @staticmethod
    def check_answer(answer, user_answer):
        """ Return True if user input answer is correct """
        # this is for definition precision flexibility
        return user_answer in answer and len(user_answer) >= (len(answer) / 3)

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

    @property
    def score_percent(self):
        return round(self.num_correct / self.questions_asked, 2)

    @property
    def questions_asked(self):
        return self.num_correct + self.num_wrong

    @property
    def questions_remaining(self):
        return self.quiz_length - (self.num_correct + self.num_wrong)

    @property
    def quiz_string(self):
        """ Return quiz_string for printing based on quiz_specs """
        if self.quiz_specs[1] == 'definition':
            return f'{self.quiz_specs[0]} {self.quiz_specs[1]} quiz'
        else:
            return f'{self.quiz_specs[1]} tense {self.quiz_specs[0]} quiz'

    def print_results(self, results):
        print('You completed a {} on {}.\n\n\
            You got {} question{} correct and {} question{} wrong.\n'.format(
            self.quiz_string, results[3].strftime('%x'),
            results[1], '' if results[1] == 1 else 's',
            results[2], '' if results[2] == 1 else 's'))
        return True





















