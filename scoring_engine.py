# scoring_engine.py
import json
import os

FAILURE_LOG = "failures.json"

class ScoringEngine:
    def __init__(self):
        if not os.path.exists(FAILURE_LOG):
            with open(FAILURE_LOG, "w") as f:
                json.dump([], f)

    def score(self, genome):
        """
        Fake scoring logic for now.
        Later this will be replaced by real ML evaluation.
        """
        # example rule: reject extreme learning rates
        lr = genome.hyperparameters.get("learning_rate", 0.01)

        if lr <= 0 or lr > 1:
            self._log_failure(genome, "Invalid learning rate")
            return None  # rejected pipeline

        # deterministic pseudo-score
        return round(1 / lr, 4)

    def _log_failure(self, genome, reason):
        with open(FAILURE_LOG, "r") as f:
            data = json.load(f)

        data.append({
            "pipeline_hash": genome.generate_hash(),
            "reason": reason
        })

        with open(FAILURE_LOG, "w") as f:
            json.dump(data, f, indent=2)
if __name__ == "__main__":
    ScoringEngine()
