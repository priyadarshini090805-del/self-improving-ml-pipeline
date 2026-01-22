# mutation_engine.py
import random
import math
from pipeline_genome import PipelineGenome


class MutationEngine:
    def __init__(self, base_scale=0.5, seed=42, credit_assigner=None):
        self.base_scale = base_scale
        self.credit_assigner = credit_assigner
        random.seed(seed)

    def _diversity(self, population):
        if len(population) <= 1:
            return 0.0
        lrs = [g.hyperparameters.get("learning_rate", 0.1) for g in population]
        mean = sum(lrs) / len(lrs)
        var = sum((x - mean) ** 2 for x in lrs) / len(lrs)
        return var

    def _preferred_direction(self, param):
        if not self.credit_assigner:
            return None
        prefs = self.credit_assigner.best_directions()
        return prefs.get(param, (None, 0.0))[0]

    def mutate(self, genome: PipelineGenome, population=None):
        scale = self.base_scale
        if population is not None:
            scale = self.base_scale * math.exp(-self._diversity(population))

        new_hyperparams = genome.hyperparameters.copy()

        if "learning_rate" in new_hyperparams:
            direction = self._preferred_direction("learning_rate")

            if direction == "up":
                delta = random.uniform(0, scale)
            elif direction == "down":
                delta = -random.uniform(0, scale)
            else:
                delta = random.uniform(-scale, scale)

            new_lr = max(0.0001, new_hyperparams["learning_rate"] * (1 + delta))
            new_hyperparams["learning_rate"] = new_lr

        return PipelineGenome(
            preprocessing=genome.preprocessing,
            model=genome.model,
            hyperparameters=new_hyperparams,
            seed=random.randint(0, 99999)
        )
