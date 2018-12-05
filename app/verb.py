# Verb class
import unicodedata


class Verb():
    """ Performs manipulation & checking of korean verbs / adjectives """

    ###########################################################################
    # Hangul Unicode Variables
    ###########################################################################

    CHOSEONG = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ',
                'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

    JUNGSEONG = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ',
                 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']

    JONGSEONG = ['', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ',
                 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ',
                 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

    NUM_CHOSEONG = len(CHOSEONG)  # 19
    NUM_JUNGSEONG = len(JUNGSEONG)  # 21
    NUM_JONGSEONG = len(JONGSEONG)  # 28

    FIRST_HANGUL_UNICODE = 0xAC00  # '가'
    LAST_HANGUL_UNICODE = 0xD7A3  # '힣'

    def __init__(self, verb):
        self.verb = verb

    def conjugate_present_tense(self):
        pass

    def last_syllable(word):
        """ returns the last syllable (글자), before 다 """
        return unicodedata.name(word[-2])

    ###########################################################################
    # Decomposition & Combination
    ###########################################################################

    def _compose(choseong, jungseong, jongseong=''):
        """ Returns a Hangul syllable block composed of its component parts

        Param: choseong (aka initial consonant)
        Param: jungseong (aka medial vowel/diphthong)
        Param (optional): jongseong (aka final consonant) """

        try:
            choseong_index = Verb.CHOSEONG.index(choseong)
            jungseong_index = Verb.JUNGSEONG.index(jungseong)
            jongseong_index = Verb.JONGSEONG.index(jongseong)
        except:
            raise NotHangulException('No valid Hangul syllable block can be\
                composed with the given inputs.')

        return chr(Verb.FIRST_HANGUL_UNICODE +
                   (choseong_index * Verb.NUM_JUNGSEONG * Verb.NUM_JONGSEONG) +
                   (jungseong_index * Verb.NUM_JONGSEONG) +
                   jongseong_index)





















