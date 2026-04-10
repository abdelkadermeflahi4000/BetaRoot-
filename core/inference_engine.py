class InferenceEngine:
    def __init__(self, memory_store):
        self.memory = memory_store

    def answer_query(self, subject, target_property):
        """
        مثال:
        facts:
        أرسطو بشر

        rules:
        البشر -> فانون

        query:
        هل أرسطو فان؟
        """

        facts = self.memory.get_facts()
        rules = self.memory.get_rules()

        # ابحث عن فئة الشخص
        subject_category = None

        for fact in facts:
            if fact.subject == subject:
                subject_category = fact.object
                break

        if not subject_category:
            return {
                "success": False,
                "answer": "لا توجد معرفة كافية.",
                "certainty": 0.0,
                "reasoning": []
            }

        reasoning = []

        reasoning.append(f"{subject} ينتمي إلى: {subject_category}")

        # ابحث عن قاعدة تربط الفئة بالخاصية
        for rule in rules:
            if rule.category == subject_category:
                reasoning.append(
                    f"كل {rule.category} {rule.consequence}"
                )

                if rule.consequence == target_property:
                    reasoning.append(
                        f"إذن {subject} {target_property}"
                    )

                    return {
                        "success": True,
                        "answer": f"نعم، {subject} {target_property}",
                        "certainty": 1.0,
                        "reasoning": reasoning
                    }

        return {
            "success": False,
            "answer": "لا يمكن الاستنتاج.",
            "certainty": 0.0,
            "reasoning": reasoning
        }
