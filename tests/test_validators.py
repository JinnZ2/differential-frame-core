from differential_frame.validators import (
    NARRATIVE_TOKENS,
    NARRATIVE_TOKENS_HEAVY,
    NARRATIVE_TOKENS_LIGHT,
    has_narrative_drift,
    has_rate_signature,
    has_scope_declaration,
    quick_audit,
)


# ----------------------------------------------------------------
# has_narrative_drift — weighted token logic
# ----------------------------------------------------------------

def test_heavy_token_with_copula_flags_drift():
    # one heavy token ('fundamentally') + one light ('is'),
    # no rate -> flag
    assert has_narrative_drift("He is fundamentally lazy.")


def test_scoped_rate_speech_with_copula_does_not_flag():
    # '/s' is a rate signal; copula 'is' alone should not
    # outweigh it
    assert not has_narrative_drift(
        "The temperature is decreasing at 0.1 K/s under standard pressure."
    )


def test_rate_verb_with_copula_does_not_flag():
    # 'flows' is a rate token; 'is' alone is below threshold
    assert not has_narrative_drift(
        "Water flows downhill when the slope is positive."
    )


def test_three_heavy_tokens_flag_strongly():
    # 'everyone', 'always', 'inherently' — all heavy, no rate
    assert has_narrative_drift("Everyone always inherently knows the truth.")


def test_pure_rate_speech_does_not_flag():
    # 'drifts' and 'propagates' both rate, no narrative
    assert not has_narrative_drift("The cycle drifts as it propagates.")


# ----------------------------------------------------------------
# token-table invariants
# ----------------------------------------------------------------

def test_narrative_tokens_is_union_for_backward_compat():
    assert set(NARRATIVE_TOKENS) == (
        set(NARRATIVE_TOKENS_HEAVY) | set(NARRATIVE_TOKENS_LIGHT)
    )


def test_heavy_and_light_are_disjoint():
    assert set(NARRATIVE_TOKENS_HEAVY).isdisjoint(NARRATIVE_TOKENS_LIGHT)


# ----------------------------------------------------------------
# surface helpers and quick_audit still behave
# ----------------------------------------------------------------

def test_has_rate_signature_detects_known_tokens():
    assert has_rate_signature("the rate of decay is 0.1 /s")
    assert not has_rate_signature("essence of being")


def test_has_scope_declaration_detects_known_tokens():
    assert has_scope_declaration("valid within the room-temperature regime")
    assert not has_scope_declaration("truth is truth")


def test_quick_audit_passes_scoped_rate_claim():
    result = quick_audit(
        "The temperature decreases at 0.1 K/s under standard pressure."
    )
    assert result['in_frame'] is True
    assert result['recommendation'] == 'pass'


def test_quick_audit_flags_drift_on_heavy_narrative():
    result = quick_audit("He is fundamentally lazy.")
    assert result['in_frame'] is False
    assert result['has_drift'] is True
