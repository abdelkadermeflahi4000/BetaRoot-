# betaroot/core/question_generator.py

from typing import List, Dict, Any


class QuestionGenerator:
    def generate(self, query: Dict[str, Any], facts: List[Dict], causal_paths: List[List[str]]) -> List[str]:
        questions = []

        subject = query.get("subject")
        predicate = query.get("predicate")

        # ----------------------------------
        # 1. No knowledge
        # ----------------------------------
        if not facts:
            questions.append(f"What does '{subject}' {predicate}?")
            return questions

        # ----------------------------------
        # 2. Weak confidence
        # ----------------------------------
        for f in facts:
            if f.get("confidence", 1.0) < 1.0:
                questions.append(
                    f"How certain is it that '{f['subject']}' {f['predicate']} '{f['value']}'?"
                )

        # ----------------------------------
        # 3. Missing causal links
        # ----------------------------------
        for path in causal_paths:
            if len(path) >= 2:
                # مثال: smoking → cancer (لكن missing middle)
                if len(path) == 2:
                    questions.append(
                        f"What intermediate steps connect '{path[0]}' to '{path[1]}'?"
                    )

        # ----------------------------------
        # 4. Deeper reasoning
        # ----------------------------------
        questions.append(
            f"Are there other effects caused by '{subject}'?"
        )

        questions.append(
            f"What happens if '{subject}' is removed?"
        )

        return questions
