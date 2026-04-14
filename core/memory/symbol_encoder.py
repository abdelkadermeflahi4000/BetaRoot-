# core/memory/symbol_encoder.py

import hashlib

class SymbolEncoder:

    def encode(self, concept_name):
        return hashlib.md5(concept_name.encode()).hexdigest()[:6]
