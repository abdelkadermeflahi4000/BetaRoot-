# core/conflict_engine.py

class ConflictEngine:

    def resolve(self, decisions):
        if not decisions:
            return None

        # نحسب القوة لكل قرار
        scored = []

        for d in decisions:
            score = d["confidence"] * d["energy"]
            scored.append((score, d))

        # نختار الأعلى
        scored.sort(key=lambda x: x[0], reverse=True)

        winner = scored[0][1]

        print(f"[CONFLICT] Winner: {winner['agent']}")

        return winner
