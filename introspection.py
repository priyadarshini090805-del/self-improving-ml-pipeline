# introspection.py
from collections import defaultdict

class Introspector:
    def __init__(self, credit_assigner):
        self.credit_assigner = credit_assigner

    def summarize(self, top_k=5):
        """
        Returns a ranked explanation of influential mutations.
        """
        agg = defaultdict(float)
        for (param, direction), score in self.credit_assigner.credits.items():
            agg[(param, direction)] += score

        ranked = sorted(agg.items(), key=lambda x: x[1], reverse=True)
        return ranked[:top_k]

    def explain(self):
        summary = self.summarize()
        if not summary:
            return "No sufficient evidence to explain evolution yet."

        lines = ["Evolutionary Explanation:"]
        for (param, direction), score in summary:
            lines.append(
                f"- Increasing '{param}' tended to improve outcomes"
                if direction == "up"
                else f"- Decreasing '{param}' tended to improve outcomes"
            )
        return "\n".join(lines)
