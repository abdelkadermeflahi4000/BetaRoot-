class ExplorerAgent:
    def explore(self, query, kb):
        """
        يبحث عن علاقات جديدة
        """

        results = []

        for fact in kb.get_all_facts():
            if fact["subject"] == query["subject"]:
                results.append(fact)

        return results
