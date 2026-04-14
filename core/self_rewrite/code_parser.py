# core/self_rewrite/code_parser.py

import ast

class CodeParser:

    def parse(self, code_str):
        tree = ast.parse(code_str)
        return tree
