# core/self_rewrite/patch_evaluator.py

class PatchEvaluator:

    def evaluate(self, original, modified):
        score_before = original["energy"]
        score_after = modified["energy"]

        return score_after - score_before
