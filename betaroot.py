import ast
import operator as op
import re

from unary_logic import UnaryLogicEngine


class SafeMathEvaluator:
    """
    Evaluator آمن للعمليات الحسابية الأساسية.
    يدعم:
    + - * / // % **
    """

    ALLOWED_OPERATORS = {
        ast.Add: op.add,
        ast.Sub: op.sub,
        ast.Mult: op.mul,
        ast.Div: op.truediv,
        ast.FloorDiv: op.floordiv,
        ast.Mod: op.mod,
        ast.Pow: op.pow,
        ast.USub: op.neg,
        ast.UAdd: op.pos,
    }

    def evaluate(self, expression: str):
        node = ast.parse(expression, mode="eval").body
        return self._eval(node)

    def _eval(self, node):
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError("Unsupported constant type")

        elif isinstance(node, ast.BinOp):
            left = self._eval(node.left)
            right = self._eval(node.right)
            operator_type = type(node.op)

            if operator_type not in self.ALLOWED_OPERATORS:
                raise ValueError("Unsupported operator")

            return self.ALLOWED_OPERATORS[operator_type](left, right)

        elif isinstance(node, ast.UnaryOp):
            operand = self._eval(node.operand)
            operator_type = type(node.op)

            if operator_type not in self.ALLOWED_OPERATORS:
                raise ValueError("Unsupported unary operator")

            return self.ALLOWED_OPERATORS[operator_type](operand)

        raise ValueError("Invalid expression")


class BetaRoot:
    def __init__(self):
        self.engine = UnaryLogicEngine()
        self.math_evaluator = SafeMathEvaluator()
        self.facts = []

    def add_fact(self, fact: str):
        self.facts.append(fact)
        self.engine.encode(fact)

    def process(self, query: str):
        """
        يدعم:
        - العمليات الحسابية
        - fallback: تخزين/تمثيل نصي
        """
        try:
            math_expr = self._extract_math_expression(query)

            if math_expr:
                result = self.math_evaluator.evaluate(math_expr)

                state = self.engine.encode(result)

                return {
                    "success": True,
                    "type": "math",
                    "query": query,
                    "expression": math_expr,
                    "answer": str(result),
                    "certainty": 1.0,
                    "state": state.representation_id,
                    "natural_explanation": (
                        f"I identified the arithmetic expression '{math_expr}' "
                        f"and evaluated it deterministically."
                    ),
                }

            # fallback
            state = self.engine.encode(query)

            return {
                "success": True,
                "type": "general",
                "query": query,
                "answer": f"Encoded into unary state: {state.representation_id}",
                "certainty": 1.0,
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "recommendation": "Check the syntax of the mathematical expression.",
            }

    def _extract_math_expression(self, text: str):
        """
        يلتقط التعبيرات الحسابية من النص.
        مثال:
        'ما هو 2 + 2؟' -> '2 + 2'
        """
        cleaned = text.replace("؟", "").replace("=", "").strip()

        match = re.search(r"[-+*/%()\d\s\.]+(?:\*\*[-+*/%()\d\s\.]+)?", cleaned)

        if match:
            expr = match.group().strip()
            if any(char.isdigit() for char in expr):
                return expr

        return None


def create_betaroot():
    return BetaRoot()
