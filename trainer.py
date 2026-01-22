# trainer.py
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


class Trainer:
    def train_and_evaluate(self, genome):
        np.random.seed(genome.seed)

        # Synthetic data (leakage-safe)
        X = np.random.randn(500, 5)
        y = (X.sum(axis=1) > 0).astype(int)

        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=0.3, random_state=genome.seed
        )

        lr = genome.hyperparameters.get("learning_rate", 0.1)

        model = LogisticRegression(
            C=1 / lr,
            max_iter=200
        )

        model.fit(X_train, y_train)
        preds = model.predict(X_val)

        # --- Multi-objective metrics ---
        accuracy = accuracy_score(y_val, preds)

        training_cost = X_train.shape[0] * X_train.shape[1]  # proxy for cost
        simplicity = 1 / lr  # higher = simpler model

        return {
            "accuracy": accuracy,
            "training_cost": -training_cost,  # negate because we maximize
            "simplicity": simplicity
        }
