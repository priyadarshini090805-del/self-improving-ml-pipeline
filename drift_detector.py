# drift_detector.py
import numpy as np

class DriftDetector:
    def __init__(self, threshold=0.2):
        self.threshold = threshold
        self.reference_mean = None

    def fit_reference(self, X):
        self.reference_mean = np.mean(X, axis=0)

    def detect(self, X_new):
        if self.reference_mean is None:
            return False

        new_mean = np.mean(X_new, axis=0)
        drift = np.abs(new_mean - self.reference_mean)
        return np.any(drift > self.threshold)
