"""
Surface-level validators for quick audits.
Use these when you don't have a full Noun object —
only a text claim or a code snippet to check.
"""
import re
from typing import Optional


# tokens that signal narrative-mode (out-of-frame)
NARRATIVE_TOKENS = (
    'is',  'are', 'was', 'were',
    'essence', 'identity', 'nature of',
    'fundamentally', 'inherently', 'simply',
    'always', 'never', 'everyone', 'no one',
)

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
    # crude but useful: more narrative tokens than rate tokens
    nar = sum(1 for tok in NARRATIVE_TOKENS if tok in t)
    rat = sum(1 for tok in RATE_TOKENS if tok in t)
    return nar > rat and rat == 0


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
