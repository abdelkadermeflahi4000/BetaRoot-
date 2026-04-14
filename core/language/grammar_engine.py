# core/language/grammar_engine.py

class GrammarEngine:

    def generate(self, symbols):
        if len(symbols) < 2:
            return None

        return f"{symbols[0]} -> {symbols[1]}"
