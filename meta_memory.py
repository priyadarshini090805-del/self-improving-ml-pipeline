# meta_memory.py
import json
import os

MEMORY_FILE = "meta_memory.json"

class MetaMemory:
    def __init__(self):
        if not os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, "w") as f:
                json.dump([], f)

    def save(self, genome, score):
        with open(MEMORY_FILE, "r") as f:
            data = json.load(f)

        data.append({
            "pipeline": genome.to_dict(),
            "hash": genome.generate_hash(),
            "score": score
        })

        # keep only top 10 pipelines
        data = sorted(data, key=lambda x: x["score"], reverse=True)[:10]

        with open(MEMORY_FILE, "w") as f:
            json.dump(data, f, indent=2)

    def load_best(self):
        with open(MEMORY_FILE, "r") as f:
            data = json.load(f)

        return data
