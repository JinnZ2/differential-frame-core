import math
from differential_frame.contract import (
    Noun, Bounds, Scope, FrameField, in_frame, ALL_RULES, band_for,
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
    # constant rate (no dX/dt structure), no scope declared,
    # no units on bounds, closure fails.
    return Noun(
        name='essence_of_truth',
        rate=lambda t: 1.0,
        bounds=Bounds(lo=0, hi=1, units=''),
        scope=Scope(tier='empirical', domain='', declared=False),
        closure_check=lambda: False,
    )


def test_in_frame_returns_frame_field():
    f = in_frame(make_valid_noun())
    assert isinstance(f, FrameField)
    assert set(f.per_rule.keys()) == set(ALL_RULES.keys())
    assert 0.0 <= f.aggregate <= 1.0


def test_valid_noun_is_propagatable():
    f = in_frame(make_valid_noun())
    assert f.is_propagatable()
    assert f.confidence_band in ('STRONG', 'GOOD')


def test_invalid_noun_collapses_aggregate():
    f = in_frame(make_invalid_noun())
    assert not f.is_propagatable()
    # scope.declared=False forces rule_3_scope to 0.0,
    # which makes it the weakest rule and drives the
    # harmonic mean to 0.0.
    assert f.per_rule['scope'] == 0.0
    assert f.weakest_rule == 'scope'
    assert f.aggregate == 0.0
    assert f.confidence_band == 'FAIL'


def test_each_rule_returns_unit_interval_float():
    n = make_valid_noun()
    for name, fn in ALL_RULES.items():
        score = fn(n)
        assert isinstance(score, float), f'{name} did not return float'
        assert 0.0 <= score <= 1.0, f'{name} out of [0,1]: {score}'


def test_band_for_anchors():
    assert band_for(0.95) == 'STRONG'
    assert band_for(0.75) == 'GOOD'
    assert band_for(0.55) == 'AMBIGUOUS'
    assert band_for(0.35) == 'WEAK'
    assert band_for(0.10) == 'FAIL'
