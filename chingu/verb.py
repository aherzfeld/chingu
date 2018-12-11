# Verb class


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

    POLITE_ENDING = '요'

    def __init__(self, verb):
        self.verb = verb

    @staticmethod
    def conjugate_present(verb):  # sort out doing this with self
        """ Returns a verb/adj in present tense polite form

        Usage: conjugate_present('오다') returns '와요' """

        stable_stem = ''

        if len(verb) >= 3:
            stable_stem = verb[:-2]

        active_stem = Verb.last_syllable(verb)
        # cho = initial consonant, jung = medial vowel, jong = final consonant
        cho, jung, jong = Verb._decompose(active_stem)

        # conjugate 하다 verbs
        if active_stem == '하':
            active_stem = '해'

        # TODO: determine if last vowel is ㅏ (2 cases)
        elif (jung == 'ㅏ' or jung == 'ㅗ') and jong != '':
            active_stem += '아'

        # TODO: determine if last vowel is ㅗ
        elif jung == 'ㅗ':
            jung = 'ㅘ'
            active_stem = Verb._compose(cho, jung, jong)

        # TODO: conjugate verb stem + 어 verbs
        elif (jung != 'ㅏ' or jung != 'ㅗ') and jong != '':
            active_stem += '어'

        # TODO: conjugate verb stem + 어 contraction verbs (ㅜ, ㅡ & no 받침)
        elif jung == 'ㅜ' and jong == '':
            jung = 'ㅝ'
            active_stem = Verb._compose(cho, jung, jong)

        elif jung == 'ㅡ' and jong == '':
            jung = 'ㅓ'
            active_stem = Verb._compose(cho, jung, jong)

        # TODO: conjugate verb stem ㅣ + 여 contraction verbs (no 받침)
        elif jung == 'ㅣ' and jong == '':
            jung = 'ㅕ'
            active_stem = Verb._compose(cho, jung, jong)

        return stable_stem + active_stem + Verb.POLITE_ENDING

    def last_syllable(word):
        """ returns the last syllable (글자) of a verb/adj stem. Useful for verb
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
            print('No valid Hangul syllable block can be composed with the\
             given inputs.')

        return chr(Verb.FIRST_HANGUL_UNICODE +
                   (choseong_index * Verb.NUM_JUNGSEONG * Verb.NUM_JONGSEONG) +
                   (jungseong_index * Verb.NUM_JONGSEONG) +
                   jongseong_index)

    def _decompose(syllable_block):
        """ Returns individual letters (자모) by decomposing syllable block

        Param: syllable_block (글자, a Korean "block character")

        Usage: _decompose('한') returns ('ㅎ', 'ㅏ', 'ㄴ') """

        # add exceptions if len(syllable_block) < 1

        # https://www.unicode.org/versions/Unicode11.0.0/ch03.pdf#G24646
        code = ord(syllable_block) - Verb.FIRST_HANGUL_UNICODE
        jongseong_index = code % Verb.NUM_JONGSEONG
        code //= Verb.NUM_JONGSEONG
        jungseong_index = code % Verb.NUM_JUNGSEONG
        code //= Verb.NUM_JUNGSEONG
        choseong_index = code

        return (Verb.CHOSEONG[choseong_index],
                Verb.JUNGSEONG[jungseong_index],
                Verb.JONGSEONG[jongseong_index])





















