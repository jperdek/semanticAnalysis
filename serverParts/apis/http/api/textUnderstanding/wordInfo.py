
class WordInfo:
    def __init__(self, word: str):
        self.pos = ''
        self.word = word

    def as_verb(self, lemma_word: str):
        self.pos = 'v'
        self.word = lemma_word

    def as_adj(self, lemma_word: str):
        self.pos = 'a'
        self.word = lemma_word

    def as_noun(self, word: str):
        self.pos = 'n'
        self.word = word
