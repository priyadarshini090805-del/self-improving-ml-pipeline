# governance.py
import json
import os
import time

GOVERNANCE_LOG = "governance_log.json"

class Governance:
    def __init__(self):
        if not os.path.exists(GOVERNANCE_LOG):
            with open(GOVERNANCE_LOG, "w") as f:
                json.dump([], f)

    def record(self, genome, decision, reason):
        with open(GOVERNANCE_LOG, "r") as f:
            data = json.load(f)

        data.append({
            "timestamp": time.time(),
            "pipeline_hash": genome.generate_hash(),
            "decision": decision,
            "reason": reason
        })

        with open(GOVERNANCE_LOG, "w") as f:
            json.dump(data, f, indent=2)
