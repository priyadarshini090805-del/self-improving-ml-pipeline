# multi_objective.py

def dominates(a, b):
    """
    Returns True if solution a dominates solution b
    a and b are dicts with metrics
    """
    better_or_equal = all(a[k] >= b[k] for k in a)
    strictly_better = any(a[k] > b[k] for k in a)
    return better_or_equal and strictly_better


def pareto_front(candidates):
    """
    candidates: list of (genome, metrics_dict)
    returns: non-dominated solutions
    """
    front = []

    for i, (g1, m1) in enumerate(candidates):
        dominated = False
        for j, (g2, m2) in enumerate(candidates):
            if i != j and dominates(m2, m1):
                dominated = True
                break
        if not dominated:
            front.append((g1, m1))

    return front
