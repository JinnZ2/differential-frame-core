"""
Aggregators for combining the five rule scores into a single
frame-confidence.

Three options are provided. They make different assumptions
about rule independence and about how weak rules should be
penalized.

The default is harmonic_mean because it matches the sovereignty
model's pack-scoring and because the five rules are NOT
independent — a noun missing scope tends to also fail closure,
so we want a penalty that compounds weakness rather than
averaging it away.
"""
from typing import Dict


def harmonic_mean(scores: Dict[str, float]) -> float:
    """
    Harmonic mean penalizes weak rules disproportionately.
    A single 0.0 rule drives the aggregate to 0.0.
    Matches sovereignty model's pack-resilience scoring.

    Use when: rules are not independent, and a single failure
    should not be averaged away by other strong rules.
    """
    vals = list(scores.values())
    if not vals:
        return 0.0
    if any(v <= 0.0 for v in vals):
        return 0.0
    n = len(vals)
    return n / sum(1.0 / v for v in vals)


def arithmetic_mean(scores: Dict[str, float]) -> float:
    """
    Simple average. Treats rules as independent and equally
    weighted. Tolerant of single weak rules.

    Use when: the audit is informational, not gating.
    """
    vals = list(scores.values())
    return sum(vals) / len(vals) if vals else 0.0


def bayesian_update(
    scores: Dict[str, float],
    prior: float = 0.5,
    correlation: float = 0.6,
) -> float:
    """
    Bayesian-style update treating each rule's score as evidence
    for frame-validity. Accounts for non-independence via the
    correlation parameter (0.0 = independent, 1.0 = redundant).

    The five rules are correlated: scope, bounds, and closure
    tend to fail together (narrative-mode claims usually lack
    all three). correlation=0.6 reflects this empirically.

    Use when: you want a posterior probability over frame-
    validity that honestly accounts for the rules being
    partially redundant.
    """
    if not scores:
        return prior

    posterior = prior
    vals = list(scores.values())

    # discount factor reduces each rule's evidential weight
    # to account for shared information with other rules
    discount = 1.0 - correlation * (1.0 - 1.0 / len(vals))

    for score in vals:
        # likelihood ratio: how much more likely is this score
        # under "in-frame" than "out-of-frame"?
        # we model in-frame likelihood as score, out-of-frame
        # as (1 - score), then discount the update.
        lr = (score / max(1.0 - score, 1e-9)) ** discount
        odds_prior = posterior / max(1.0 - posterior, 1e-9)
        odds_post = odds_prior * lr
        posterior = odds_post / (1.0 + odds_post)

    return max(0.0, min(0.97, posterior))   # never claim certainty
