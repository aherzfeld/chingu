# Verb class
import unicodedata


class Verb():
    """ Performs manipulation & checking of korean verbs / adjectives """

    def __init__(self, verb):
        self.verb = verb

    def conjugate_present_tense(self):
        pass

    def last_vowel(word):
        return unicodedata.name(word[-2])
