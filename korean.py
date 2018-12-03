import unicodedata
from wordlist import verb_list


# print([c.decode('utf-8') for c in byteslist])


test_list = ['가다', '앉다', '오다', '물어보다', '봐다', '아다']



def ordinator(chr_list):
    """ receive sequence characters and return list of ordinal numbers """
    return [ord(c) for c in chr_list]


def hexinator(ord_list):
    """ receive list of ordinal numbers and return list of hexadecimals """
    return [hex(n) for n in ord_list]


def bytenator(chr_list):
    """ receive a list of characters and return list of bytes """
    return [bytes(c, 'utf-8') for c in chr_list]


def stem(word):
    """ receive verb / adj and return stem (remove 다) """
    return word[:-1]


def last_vowel(word):
    return unicodedata.name(word[-2])


def conjugate(word):
    """ receives verb / adj and returns conjugated version.
    Only works for 아, 오 and 하 verbs """
    if last_vowel(word) == 'HANGUL SYLLABLE HA':
        return word[:-2] + '해요'
    elif 'A' in last_vowel(word) and ('AE')



def conjugate1(stem):
    """ receives stem of 아 or 오 verb / adj and returns conjugated word """
    pass


def conjugate2(stem):
    """ receives stem of NON 아, 오, or 하 verb / adj and returns conjugated
    word """
    pass


def conjugate3(stem):
    """ receives 하 verb / adj and returns conjugated word """
    pass


#last_vowels = [last_vowel(word) for word in test_list]
#print(last_vowels)

#lasts = [last_vowel(key) for key in verb_list]
#print(lasts)

print(conjugate('필요하다'))
