# credit_assignment.py
from collections import defaultdict


class CreditAssigner:
    def __init__(self):
        # maps (parameter, direction) -> cumulative credit
        self.credits = defaultdict(float)

    def assign(self, parent, child, metrics_delta):
        """
        metrics_delta: dict of (metric -> improvement)
        """
        for param in parent.hyperparameters:
            p_val = parent.hyperparameters[param]
            c_val = child.hyperparameters.get(param, p_val)

            if c_val == p_val:
                continue

            direction = "up" if c_val > p_val else "down"

            # simple causal signal: accuracy dominates
            credit = metrics_delta.get("accuracy", 0.0)

            self.credits[(param, direction)] += credit

    def best_directions(self):
        """
        Returns preferred mutation directions
        """
        preferences = {}
        for (param, direction), score in self.credits.items():
            if param not in preferences or score > preferences[param][1]:
                preferences[param] = (direction, score)
        return preferences
