"""Spelling Corrector in Python 3; see http://norvig.com/spell-correct.html
Copyright (c) 2007-2016 Peter Norvig
MIT license: www.opensource.org/licenses/mit-license.php
"""


################ Spelling Corrector


class SpellCorrector:

    def __init__(self, words):
        self.words = words
        self.N = sum(words.values())

    def correct(self, word):
        "Most probable spelling correction for word."
        return max(self.candidates(word), key=self.P)

    def P(self, word):
        "Probability of `word`."
        return self.words[word] / self.N

    def candidates(self, word):
        "Generate possible spelling corrections for word."
        return self.known([word]) | self.known(self.edits1(word)) | self.known(self.edits2(word)) | {word}

    def known(self, words):
        "The subset of `words` that appear in the dictionary of WORDS."
        return set(w for w in words if w in self.words)

    @staticmethod
    def edits1(word):
        "All edits that are one edit away from `word`."
        letters = 'abcdefghijklmnopqrstuvwxyząęóśłżźćń'
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes = [L + R[1:] for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
        replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
        inserts = [L + c + R for L, R in splits for c in letters]
        return set(deletes + transposes + replaces + inserts)

    @staticmethod
    def edits2(word):
        "All edits that are two edits away from `word`."
        return (e2 for e1 in SpellCorrector.edits1(word) for e2 in SpellCorrector.edits1(e1))
