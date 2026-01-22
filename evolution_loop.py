import numpy as np

from pipeline_genome import PipelineGenome
from mutation_engine import MutationEngine
from scoring_engine import ScoringEngine
from trainer import Trainer
from meta_memory import MetaMemory
from drift_detector import DriftDetector
from governance import Governance
from multi_objective import pareto_front
from credit_assignment import CreditAssigner
from counterfactual import CounterfactualEvaluator
from introspection import Introspector


class Species:
    def __init__(self, name, base_genome):
        self.name = name
        self.population = [base_genome]


class EvolutionLoop:
    def __init__(self, max_failures=5):
        # Learning & explanation modules
        self.credit = CreditAssigner()
        self.counterfactual = CounterfactualEvaluator()
        self.introspector = Introspector(self.credit)

        self.mutator = MutationEngine(credit_assigner=self.credit)

        # Infrastructure
        self.scorer = ScoringEngine()
        self.trainer = Trainer()
        self.memory = MetaMemory()
        self.drift = DriftDetector()
        self.gov = Governance()

        # Safety
        self.max_failures = max_failures
        self.failure_count = 0

        # Co-evolution
        self.species = []

    def seed_species(self):
        self.species = [
            Species(
                "conservative",
                PipelineGenome(
                    preprocessing=["scale"],
                    model="linear_model",
                    hyperparameters={"learning_rate": 0.05},
                    seed=1,
                ),
            ),
            Species(
                "aggressive",
                PipelineGenome(
                    preprocessing=["scale"],
                    model="linear_model",
                    hyperparameters={"learning_rate": 0.3},
                    seed=2,
                ),
            ),
            Species(
                "balanced",
                PipelineGenome(
                    preprocessing=["scale"],
                    model="linear_model",
                    hyperparameters={"learning_rate": 0.1},
                    seed=3,
                ),
            ),
        ]

        for s in self.species:
            self.gov.record(
                s.population[0],
                "seeded",
                f"Species={s.name}"
            )

    def evolve_species(self, species, generations=3, children_per_gen=3):
        for gen in range(generations):
            candidates = []

            for parent in species.population:
                parent_metrics = self.trainer.train_and_evaluate(parent)

                for _ in range(children_per_gen):
                    if self.failure_count >= self.max_failures:
                        print("KILL-SWITCH ACTIVATED")
                        return

                    child = self.mutator.mutate(parent, species.population)

                    try:
                        child_metrics = self.trainer.train_and_evaluate(child)

                        if self.drift.reference_mean is None:
                            X_ref = np.random.randn(500, 5)
                            self.drift.fit_reference(X_ref)

                        # Counterfactual causal credit
                        delta = self.counterfactual.evaluate(
                            parent_metrics, child_metrics
                        )
                        self.credit.assign(parent, child, delta)

                        candidates.append((child, child_metrics))
                        self.gov.record(child, "accepted", str(child_metrics))

                    except Exception:
                        self.failure_count += 1
                        self.scorer._log_failure(child, "Training failure")
                        self.gov.record(child, "rejected", "Training failure")

            if candidates:
                front = pareto_front(candidates)
                species.population = [g for g, _ in front]

    def inter_species_competition(self):
        all_candidates = []

        for s in self.species:
            for g in s.population:
                metrics = self.trainer.train_and_evaluate(g)
                all_candidates.append((g, metrics))

        global_front = pareto_front(all_candidates)
        survivors = [g for g, _ in global_front]

        for i, s in enumerate(self.species):
            if survivors:
                s.population = [survivors[i % len(survivors)]]

    def monitor_and_adapt(self):
        X_new = np.random.randn(500, 5) + np.random.choice([0, 0.5])

        if self.drift.detect(X_new):
            print("Drift detected — re-evolving")
            self.gov.record(
                self.species[0].population[0],
                "drift",
                "Auto re-evolution triggered"
            )
            self.run()
        else:
            print("No drift detected — stable")

    def run(self):
        self.seed_species()

        for s in self.species:
            print(f"Evolving species: {s.name}")
            self.evolve_species(s)

        print("Inter-species competition")
        self.inter_species_competition()

        print("Final surviving pipelines:")
        for s in self.species:
            for g in s.population:
                print(s.name, g.generate_hash())

        # 🔍 Evolutionary Introspection
        print("\n" + self.introspector.explain())


if __name__ == "__main__":
    loop = EvolutionLoop()
    loop.run()
    loop.monitor_and_adapt()
