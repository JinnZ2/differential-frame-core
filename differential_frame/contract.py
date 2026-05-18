"""
Differential Frame Core — formal contract as code.
Probability-field semantics. Stdlib only. CC0.
"""
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Optional, Tuple


# ------------------------------------------------------------
# core types
# ------------------------------------------------------------

@dataclass(frozen=True)
class Scope:
    tier: str                         # 'physics' | 'biology' | 'systems' | 'empirical'
    domain: str                       # human-readable scope
    declared: bool = True


@dataclass(frozen=True)
class Bounds:
    lo: float
    hi: float
    units: str

    def contains(self, x: float) -> bool:
        return self.lo <= x <= self.hi

    def span(self) -> float:
        return self.hi - self.lo


@dataclass(frozen=True)
class Noun:
    name: str
    rate: Callable[[float], float]
    bounds: Bounds
    scope: Scope
    closure_check: Callable[[], Any]


@dataclass(frozen=True)
class FrameField:
    """The probability field a noun occupies across the five rules."""
    per_rule: Dict[str, float]
    aggregate: float
    weakest_rule: str
    weakest_score: float
    confidence_band: str

    def is_strong(self) -> bool:
        return self.aggregate >= 0.85

    def is_propagatable(self) -> bool:
        return self.aggregate >= 0.70


# ------------------------------------------------------------
# helpers — sampling, structure detection
# ------------------------------------------------------------

KNOWN_PHYSICAL_UNITS = frozenset({
    's', 'ms', 'us', 'ns',
    'm', 'km', 'cm', 'mm',
    'kg', 'g',
    'K', 'C',
    'J', 'eV', 'W',
    'Hz', 'rad/s',
    'Pa', 'bar',
    'mol',
    'A', 'V', 'ohm',
    'N', 'N*m',
})

TIER_WEIGHTS = {
    'physics':   0.95,
    'biology':   0.80,
    'systems':   0.65,
    'empirical': 0.50,
}


def _sample_rate(noun: Noun, n: int = 16) -> list:
    """Sample the rate function across its bounds. Returns []
    if the function can't be evaluated safely."""
    lo, hi = noun.bounds.lo, noun.bounds.hi
    if hi <= lo:
        return []
    step = (hi - lo) / max(n - 1, 1)
    samples = []
    for i in range(n):
        try:
            v = noun.rate(lo + i * step)
            samples.append(float(v))
        except Exception:
            return []
    return samples


def _all_equal(samples: list, tol: float = 1e-9) -> bool:
    if not samples:
        return False
    a = samples[0]
    return all(abs(s - a) < tol for s in samples)


def _monotonic(samples: list) -> bool:
    if len(samples) < 2:
        return False
    incs = [b - a for a, b in zip(samples, samples[1:])]
    return all(d >= 0 for d in incs) or all(d <= 0 for d in incs)


def _bounded(samples: list, factor: float = 100.0) -> bool:
    """True if the sample range is finite and not explosive."""
    if not samples:
        return False
    rng = max(samples) - min(samples)
    base = max(abs(min(samples)), abs(max(samples)), 1e-9)
    return rng < factor * base


def _revisits(samples: list, tol_frac: float = 0.05) -> bool:
    """True if the trajectory revisits values (suggests cycle)."""
    if len(samples) < 4:
        return False
    rng = max(samples) - min(samples)
    if rng < 1e-12:
        return False
    tol = tol_frac * rng
    # check for any non-adjacent revisit
    for i in range(len(samples)):
        for j in range(i + 2, len(samples)):
            if abs(samples[i] - samples[j]) < tol:
                return True
    return False


def _converges(samples: list) -> bool:
    """True if successive differences shrink (suggests attractor)."""
    if len(samples) < 4:
        return False
    diffs = [abs(b - a) for a, b in zip(samples, samples[1:])]
    early = sum(diffs[:len(diffs)//2])
    late  = sum(diffs[len(diffs)//2:])
    return late < 0.5 * early and early > 1e-9


# ------------------------------------------------------------
# the five rules as probability fields
# ------------------------------------------------------------

def rule_1_rate(noun: Noun) -> float:
    """Confidence the noun references dX/dt, not X."""
    if not callable(noun.rate):
        return 0.0
    samples = _sample_rate(noun, n=8)
    if not samples:
        return 0.05
    if _all_equal(samples):
        return 0.20
    if _monotonic(samples):
        return 0.65
    if _bounded(samples):
        return 0.85
    return 0.50


def rule_2_bounds(noun: Noun) -> float:
    """Confidence the bounds are meaningful, not just present."""
    if not isinstance(noun.bounds, Bounds):
        return 0.0
    if noun.bounds.span() <= 0:
        return 0.10
    if noun.bounds.units == '':
        return 0.40
    if noun.bounds.units in KNOWN_PHYSICAL_UNITS:
        return 0.90
    return 0.60


def rule_3_scope(noun: Noun) -> float:
    """Confidence the scope is declared and tier-anchored."""
    if not noun.scope.declared:
        return 0.0
    base = TIER_WEIGHTS.get(noun.scope.tier, 0.30)
    if noun.scope.domain == '':
        base *= 0.5
    return base


def rule_4_lawful(noun: Noun) -> float:
    """Confidence the rate describes a LAW (persistent),
    not a STATE (perishable)."""
    samples = _sample_rate(noun, n=16)
    if not samples:
        return 0.0
    if _all_equal(samples):
        return 0.10

    score = 0.0
    if not _all_equal(samples):    score += 0.30   # sensitive to input
    if _bounded(samples):          score += 0.20
    if _revisits(samples):         score += 0.30
    if _converges(samples):        score += 0.20
    return min(score, 0.95)


def rule_5_closure(noun: Noun) -> float:
    """Confidence the rate equation closes."""
    try:
        result = noun.closure_check()
    except Exception:
        return 0.0
    if isinstance(result, bool):
        return 0.90 if result else 0.10
    if isinstance(result, (int, float)):
        return max(0.0, min(1.0, float(result)))
    return 0.40


ALL_RULES = {
    'rate':    rule_1_rate,
    'bounds':  rule_2_bounds,
    'scope':   rule_3_scope,
    'lawful':  rule_4_lawful,
    'closure': rule_5_closure,
}


# ------------------------------------------------------------
# bands
# ------------------------------------------------------------

def band_for(score: float) -> str:
    if score >= 0.85: return 'STRONG'
    if score >= 0.70: return 'GOOD'
    if score >= 0.50: return 'AMBIGUOUS'
    if score >= 0.30: return 'WEAK'
    return 'FAIL'


# ------------------------------------------------------------
# main entry point
# ------------------------------------------------------------

def in_frame(noun: Noun, aggregator: Optional[Callable] = None) -> FrameField:
    """
    Run all five rules against the noun and return a FrameField.
    Pass a custom aggregator from differential_frame.aggregation
    to override the default (harmonic mean).
    """
    from .aggregation import harmonic_mean   # default
    agg = aggregator or harmonic_mean

    scores = {name: fn(noun) for name, fn in ALL_RULES.items()}
    aggregate = agg(scores)
    weakest_name, weakest_val = min(scores.items(), key=lambda kv: kv[1])

    return FrameField(
        per_rule=scores,
        aggregate=aggregate,
        weakest_rule=weakest_name,
        weakest_score=weakest_val,
        confidence_band=band_for(aggregate),
    )
