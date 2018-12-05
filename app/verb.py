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

    def conjugate_present(self):
        pass

    def last_syllable(word):
        """ returns the last syllable (글자), before 다. Useful for verb
        conjugation.

        Param: word - Hangul verb or adjective (다 ending)

        Usage: last_syllable('물어보다') returns '보' """

        return word[-2]

    ###########################################################################
    # Decomposition & Combination
    ###########################################################################

    def _compose(choseong, jungseong, jongseong=''):
        """ Returns a Hangul syllable block composed of its component letters

        Param: choseong (aka initial consonant)
        Param: jungseong (aka medial vowel/diphthong)
        Param (optional): jongseong (aka final consonant)

        Usage: _compose('ㅎ', 'ㅏ', 'ㄴ') returns '한' """

        # seems to not be needed - remove once confirmed
        # if jongseong is None:
        #     jongseong = ''

        try:
            choseong_index = Verb.CHOSEONG.index(choseong)
            jungseong_index = Verb.JUNGSEONG.index(jungseong)
            jongseong_index = Verb.JONGSEONG.index(jongseong)
        except:
            # raise NotHangulException (create custom Exception)
            print('No valid Hangul syllable block can be\
                composed with the given inputs.')

        return chr(Verb.FIRST_HANGUL_UNICODE +
                   (choseong_index * Verb.NUM_JUNGSEONG * Verb.NUM_JONGSEONG) +
                   (jungseong_index * Verb.NUM_JONGSEONG) +
                   jongseong_index)

    def _decompose(syllable_block):
        """ Returns individual letters (자모) by decomposing syllable block

        Param: syllable_block (글자, a Korean "block character")

        Usage: _decompose('한') returns ('ㅎ', 'ㅏ', 'ㄴ') """

        # add exceptions if len(syllable_block) < 1

        code = ord(syllable_block) - Verb.FIRST_HANGUL_UNICODE
        jongseong_index = code % Verb.NUM_JONGSEONG
        code //= Verb.NUM_JONGSEONG
        jungseong_index = code % Verb.NUM_JUNGSEONG
        code //= Verb.NUM_JUNGSEONG
        choseong_index = code

        if Verb.JONGSEONG[jongseong_index] == '':
            return (Verb.CHOSEONG[choseong_index],
                    Verb.JUNGSEONG[jungseong_index])
        else:
            return (Verb.CHOSEONG[choseong_index],
                    Verb.JUNGSEONG[jungseong_index],
                    Verb.JONGSEONG[jongseong_index])





















