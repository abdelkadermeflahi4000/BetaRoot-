# core/language/internal_language.py

class InternalLanguage:

    def __init__(self):
        self.dictionary = {}

    def register(self, concept, symbol):
        self.dictionary[symbol] = concept

    def express(self):
        return " ".join(self.dictionary.keys())
