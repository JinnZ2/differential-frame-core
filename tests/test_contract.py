import math
from differential_frame.contract import (
    Noun, Bounds, Scope, in_frame, ALL_RULES,
)


def make_valid_noun():
    return Noun(
        name='temperature',
        rate=lambda t: -0.1 * math.exp(-t),    # cooling curve
        bounds=Bounds(lo=0.0, hi=100.0, units='s'),
        scope=Scope(tier='physics', domain='room cooling', declared=True),
        closure_check=lambda: True,
    )


def make_invalid_noun():
    # no scope declared, closure fails
    return Noun(
        name='essence_of_truth',
        rate=lambda t: 1.0,
        bounds=Bounds(lo=0, hi=1, units=''),
        scope=Scope(tier='empirical', domain='', declared=False),
        closure_check=lambda: False,
    )


def test_valid_noun_passes_all_rules():
    n = make_valid_noun()
    ok, failures = in_frame(n)
    assert ok
    assert failures == []


def test_invalid_noun_fails_scope_and_closure():
    n = make_invalid_noun()
    ok, failures = in_frame(n)
    assert not ok
    assert 'rule_3_scope_declared' in failures
    assert 'rule_5_closure_or_flag' in failures


def test_each_rule_callable():
    n = make_valid_noun()
    for r in ALL_RULES:
        assert r(n) is True
