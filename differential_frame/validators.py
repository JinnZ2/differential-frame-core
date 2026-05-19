"""
Surface-level validators for quick audits.
Use these when you don't have a full Noun object —
only a text claim or a code snippet to check.
"""
import re
from typing import Optional


# tokens that signal narrative-mode (out-of-frame).
# split by signal strength: heavy tokens assert permanence,
# closure, or universality (genuine frame violations); light
# tokens are copula verbs that appear constantly in
# rate-honest scoped discourse too, so they carry only
# fractional weight.
NARRATIVE_TOKENS_HEAVY = (
    'essence', 'identity', 'nature of',
    'fundamentally', 'inherently', 'simply',
    'always', 'never', 'everyone', 'no one',
)

NARRATIVE_TOKENS_LIGHT = (
    'is', 'are', 'was', 'were',
)

# preserved for callers that imported the original flat tuple
NARRATIVE_TOKENS = NARRATIVE_TOKENS_HEAVY + NARRATIVE_TOKENS_LIGHT

LIGHT_TOKEN_WEIGHT = 0.25

# tokens that signal rate-mode (in-frame)
RATE_TOKENS = (
    'changes', 'shifts', 'flows', 'increases', 'decreases',
    'oscillates', 'cycles', 'drifts', 'relaxes', 'propagates',
    'per ', '/s', '/t', 'd/dt', 'rate of',
)

# tokens that signal scope declaration
SCOPE_TOKENS = (
    'under', 'within', 'bounded by', 'in the regime',
    'at the scale of', 'for ', 'when ',
)


def has_rate_signature(text: str) -> bool:
    t = text.lower()
    return any(tok in t for tok in RATE_TOKENS)

def has_scope_declaration(text: str) -> bool:
    t = text.lower()
    return any(tok in t for tok in SCOPE_TOKENS)

def has_narrative_drift(text: str) -> bool:
    t = text.lower()
    heavy_count = sum(1 for tok in NARRATIVE_TOKENS_HEAVY if tok in t)
    light_count = sum(1 for tok in NARRATIVE_TOKENS_LIGHT if tok in t)
    rate_count  = sum(1 for tok in RATE_TOKENS if tok in t)
    drift_score = heavy_count + (light_count * LIGHT_TOKEN_WEIGHT)
    return drift_score > rate_count and rate_count == 0


def quick_audit(text: str) -> dict:
    """
    Surface-level frame check on a text claim.
    Returns dict with flags and a recommendation.
    """
    rate  = has_rate_signature(text)
    scope = has_scope_declaration(text)
    drift = has_narrative_drift(text)

    in_frame = rate and scope and not drift

    if in_frame:
        rec = 'pass'
    elif drift:
        rec = 'flag: narrative drift — translate to rate'
    elif not rate:
        rec = 'flag: no rate — what is changing?'
    elif not scope:
        rec = 'flag: no scope — under what conditions?'
    else:
        rec = 'flag: unknown failure mode'

    return {
        'in_frame':    in_frame,
        'has_rate':    rate,
        'has_scope':   scope,
        'has_drift':   drift,
        'recommendation': rec,
    }
