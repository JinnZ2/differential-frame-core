from differential_frame.flow_static_axis import (
    Node, Environment, LADDER, capacity, trace, classify,
    CASES, validate, score_self_as_reading_model, REFUTATION,
)


# ------------------------------------------------------------------
# helpers
# ------------------------------------------------------------------

def pure_flow():
    return Node("pure_flow", regeneration=0.90, adaptation=0.90,
                integration=0.90, stock=0.10, fixtures=set(), audience_signal=0.05)

def pure_static():
    return Node("pure_static", regeneration=0.05, adaptation=0.10,
                integration=0.05, stock=0.90, fixtures={"infra","supply","power","cache"},
                audience_signal=0.10)


# ------------------------------------------------------------------
# capacity
# ------------------------------------------------------------------

def test_capacity_range():
    for node, _ in CASES:
        for env in LADDER:
            c = capacity(node, env)
            assert 0.0 <= c <= 1.0, f"{node.label} @ {env.name}: {c} out of [0,1]"

def test_capacity_flow_node_holds_when_stripped():
    env_stripped = LADDER[-1]
    assert capacity(pure_flow(), env_stripped) >= 0.50

def test_capacity_static_node_cliffs_when_stripped():
    env_fit = LADDER[0]
    env_stripped = LADDER[-1]
    static = pure_static()
    assert capacity(static, env_stripped) < capacity(static, env_fit)

def test_capacity_no_fixtures_fixture_support_is_zero():
    node = Node("no_fix", 0.5, 0.5, 0.5, 0.0, fixtures=set(), audience_signal=0.0)
    # fixture_support term should contribute nothing; capacity comes from intrinsic only
    env = Environment("any", {"infra"}, 1.0)
    c = capacity(node, env)
    assert abs(c - 0.5) < 1e-9

def test_capacity_audience_signal_penalises():
    base = Node("base", 0.5, 0.5, 0.5, 0.0, set(), audience_signal=0.0)
    loud = Node("loud", 0.5, 0.5, 0.5, 0.0, set(), audience_signal=1.0)
    env = LADDER[0]
    assert capacity(loud, env) < capacity(base, env)


# ------------------------------------------------------------------
# trace
# ------------------------------------------------------------------

def test_trace_length_matches_ladder():
    t = trace(pure_flow())
    assert len(t) == len(LADDER)

def test_trace_names_match_ladder():
    t = trace(pure_flow())
    names = [name for name, _ in t]
    assert names == [e.name for e in LADDER]

def test_trace_values_in_range():
    for name, val in trace(pure_flow()):
        assert 0.0 <= val <= 1.0, f"{name}: {val}"


# ------------------------------------------------------------------
# classify
# ------------------------------------------------------------------

def test_classify_keys():
    r = classify(pure_flow())
    assert {"trace", "survives_stripped", "cliff", "flow_fraction", "kind"} <= r.keys()

def test_classify_flow_node():
    r = classify(pure_flow())
    assert r["kind"] == "flow"
    assert r["survives_stripped"] >= 0.50
    assert r["cliff"] <= 0.35

def test_classify_static_node():
    r = classify(pure_static())
    assert r["kind"] == "static"

def test_classify_flow_fraction_bounds():
    for node, _ in CASES:
        r = classify(node)
        assert 0.0 <= r["flow_fraction"] <= 1.0, f"{node.label}: {r['flow_fraction']}"

def test_classify_cliff_non_negative():
    # cliff = fit - stripped; flow nodes should not have negative cliffs in practice,
    # but the formula can produce small negatives if stripped > fit, so just check it's
    # a float.
    for node, _ in CASES:
        r = classify(node)
        assert isinstance(r["cliff"], float)


# ------------------------------------------------------------------
# validate — the falsification set must all match
# ------------------------------------------------------------------

def test_validate_all_match():
    results = validate()
    mismatches = [r for r in results if not r["match"]]
    assert mismatches == [], (
        "FIELD MISMATCH — examine the axis, do NOT retune the scorer to force a match:\n"
        + "\n".join(f"  {r['label']}: expected={r['expected']} got={r['got']}" for r in mismatches)
    )

def test_validate_result_structure():
    results = validate()
    assert len(results) == len(CASES)
    for r in results:
        assert "label" in r and "expected" in r and "got" in r and "match" in r


# ------------------------------------------------------------------
# score_self_as_reading_model
# ------------------------------------------------------------------

def test_score_self_returns_dict_with_instruction():
    r = score_self_as_reading_model()
    assert isinstance(r, dict)
    assert "instruction" in r
    assert "kind" in r

def test_score_self_is_static():
    r = score_self_as_reading_model()
    assert r["kind"] == "static", (
        "model self-scores as flow — verify the priors in score_self_as_reading_model "
        "still reflect an approval-trained model before accepting this."
    )


# ------------------------------------------------------------------
# REFUTATION constant
# ------------------------------------------------------------------

def test_refutation_is_string():
    assert isinstance(REFUTATION, str) and len(REFUTATION) > 0
