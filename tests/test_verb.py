import unittest
from chingu.verb import Verb


class TestVerb(unittest.TestCase):

    def test_compose(self):
        self.assertEqual(Verb._compose('ㄱ', 'ㅏ'), '가')
        self.assertEqual(Verb._compose('ㅎ', 'ㅏ', 'ㄴ'), '한')
        # checking if separate chars work as jonseong (they don't)
        # self.assertEqual(Verb._compose('ㅇ', 'ㅣ', 'ㄹㄱ'), '읽')
        self.assertEqual(Verb._compose('ㅇ', 'ㅣ', 'ㄺ'), '읽')
        self.assertEqual(Verb._compose('ㅎ', 'ㅐ'), '해')

    def test_decompose(self):
        self.assertEqual(Verb._decompose('가'), ('ㄱ', 'ㅏ', ''))
        self.assertEqual(Verb._decompose('한'), ('ㅎ', 'ㅏ', 'ㄴ'))
        # checking if separate chars work as jonseong (they don't)
        # self.assertEqual(Verb._decompose('읽'), ('ㅇ', 'ㅣ', 'ㄹㄱ'))
        self.assertEqual(Verb._decompose('읽'), ('ㅇ', 'ㅣ', 'ㄺ'))
        self.assertEqual(Verb._decompose('해'), ('ㅎ', 'ㅐ', ''))

    def test_last_syllable(self):
        self.assertEqual(Verb.last_syllable('가다'), '가')
        self.assertEqual(Verb.last_syllable('괜찮다'), '찮')
        self.assertEqual(Verb.last_syllable('힘들다'), '들')
        self.assertEqual(Verb.last_syllable('재미있다'), '있')
        self.assertEqual(Verb.last_syllable('떨어지다'), '지')

    #################################################################
    #  Verb conjugation scenarios
    #################################################################

    # check object instatiation depending on implementation of Verb
    # might need to be Verb([verb]).conjugate_present
    def test_conjugate_present_tense_hada_verbs(self):
        # 하다 verbs (하 + 여 = 해)
        self.assertEqual(Verb.conjugate_present('하다'), '해요')
        self.assertEqual(Verb.conjugate_present('건강하다'), '건강해요')
        self.assertEqual(Verb.conjugate_present('좋아하다'), '좋아해요')
        self.assertEqual(Verb.conjugate_present('궁금하다'), '궁금해요')

    def test_conjugate_present_tense_a_verbs(self):
        # last vowel containing ㅏ with no final consonant (받침) (eg. 가다)
        self.assertEqual(Verb.conjugate_present('가다'), '가요')
        self.assertEqual(Verb.conjugate_present('사다'), '사요')

    def test_conjugate_present_tense_a_with_final_consonant_verbs(self):
        # last vowel containing ㅏ verbs / adjectives with final consonant
        self.assertEqual(Verb.conjugate_present('앉다'), '앉아요')
        self.assertEqual(Verb.conjugate_present('괜찮다'), '괜찮아요')
        self.assertEqual(Verb.conjugate_present('놀다'), '놀아요')
        self.assertEqual(Verb.conjugate_present('맞다'), '맞아요')
        self.assertEqual(Verb.conjugate_present('좋다'), '좋아요')

    def test_conjugate_present_tense_o_verbs(self):
        # last vowel containing ㅗ (오 + 아 = 와)
        self.assertEqual(Verb.conjugate_present('오다'), '와요')
        self.assertEqual(Verb.conjugate_present('보다'), '봐요')
        self.assertEqual(Verb.conjugate_present('물어보다'), '물어봐요')

    def test_conjugate_present_tense_eo_verbs(self):
        # verb stem + 어
        self.assertEqual(Verb.conjugate_present('먹다'), '먹어요')
        self.assertEqual(Verb.conjugate_present('신다'), '신어요')
        self.assertEqual(Verb.conjugate_present('울다'), '울어요')
        self.assertEqual(Verb.conjugate_present('읽다'), '읽어요')
        self.assertEqual(Verb.conjugate_present('힘들다'), '힘들어요')
        self.assertEqual(Verb.conjugate_present('재미있다'), '재미있어요')
        self.assertEqual(Verb.conjugate_present('필요없다'), '필요없어요')

    def test_conjugate_present_tense_no_stem_change(self):
        # verb stems with ㅐ don't change
        self.assertEqual(Verb.conjugate_present('내다'), '내요')

    def test_conjugate_present_tense_eo_verbs_with_contraction(self):
        # verb stem + 어 with contrations (eg. 주다 -> 주어 -> 줘)
        self.assertEqual(Verb.conjugate_present('쓰다'), '써요')
        self.assertEqual(Verb.conjugate_present('주다'), '줘요')
        self.assertEqual(Verb.conjugate_present('크다'), '커요')

    def test_conjugate_present_tense_i_verbs(self):
        # verb stem ending with ㅣ + 어 (all have contractions)
        self.assertEqual(Verb.conjugate_present('내리다'), '내려요')
        self.assertEqual(Verb.conjugate_present('놀리다'), '놀려요')
        self.assertEqual(Verb.conjugate_present('떨어지다'), '떨어져요')
        self.assertEqual(Verb.conjugate_present('먹이다'), '먹여요')
        self.assertEqual(Verb.conjugate_present('웃기다'), '웃겨요')
        self.assertEqual(Verb.conjugate_present('사라지다'), '사라져요')

    # irregular verbs


# allows us to run from command line using: $ python test_app.py
if __name__ == '__main__':
    unittest.main()
