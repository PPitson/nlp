import re

import nltk
from bs4 import BeautifulSoup


def clear_text(text: str):
    return re.sub('-\n', '', BeautifulSoup(text).get_text())


def tokenize_and_filter(text):
    yield from filter(is_word, map(str.lower, nltk.word_tokenize(text, language='polish')))


def is_vowel(letter):
    return letter in ('a', 'ą', 'e', 'ę', 'i', 'o', 'ó', 'u', 'y')


def is_word(word: str):
    return len(word) > 1 and word.isalpha() and any(is_vowel(letter) for letter in word)
