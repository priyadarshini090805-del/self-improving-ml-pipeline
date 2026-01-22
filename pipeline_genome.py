# pipeline_genome.py
import hashlib
import json

class PipelineGenome:
    def __init__(self, preprocessing, model, hyperparameters, seed):
        self.preprocessing = preprocessing
        self.model = model
        self.hyperparameters = hyperparameters
        self.seed = seed

    def to_dict(self):
        return {
            "preprocessing": self.preprocessing,
            "model": self.model,
            "hyperparameters": self.hyperparameters,
            "seed": self.seed
        }

    def generate_hash(self):
        data = json.dumps(self.to_dict(), sort_keys=True)
        return hashlib.sha256(data.encode()).hexdigest()
