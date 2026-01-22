# counterfactual.py

class CounterfactualEvaluator:
    def evaluate(self, parent_metrics, child_metrics):
        """
        Returns causal improvement signal.
        Positive → mutation helped
        Negative → mutation hurt
        """
        return {
            "accuracy": child_metrics["accuracy"] - parent_metrics["accuracy"]
        }
