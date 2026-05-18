# Differential Frame Core — Specification v1.0

## Contract

Every noun names a state on a curve, not a thing.
Read X as dX/dt under scope.
Carrying a noun outside its bounds is a translation error.

Nothing is certain. Even physical laws are confidence-weighted
across regimes. The frame reflects that: rules return
probabilities, not verdicts.

## Five rules (probability fields)

1. **rate**:    confidence the noun references dX/dt, not X
2. **bounds**:  confidence the bounds are meaningful + scoped
3. **scope**:   confidence the scope is declared + tiered
4. **lawful**:  confidence the rate describes a persistent law
                rather than a perishable state
5. **closure**: confidence the rate equation closes

Each rule returns a float in [0.0, 1.0].
Aggregation produces a FrameField, not a pass/fail.

## Confidence anchors

    → 1.00  asymptotic — evidence accumulating without limit,
            never arrives
    0.97    every test we have ever run passes, across every
            regime we have ever observed — but we have not
            observed every regime
    0.95    physical law, verified in this regime, edge cases
            known
    0.85    well-established mechanism
    0.70    good empirical support
    0.50    ambiguous — structure unclear
    0.30    weak signal, could be artifact
    0.15    narrative drift suspected
    0.00    definitionally out-of-frame

1.00 is not reserved — it is **structurally unreachable**. The
maximum posterior the frame is willing to assign is
`asymptotic_ceiling(n_evidence) = 1 - 0.15/n`, which approaches
1.0 as evidence accumulates but never reaches it.

This makes the differential frame an OPEN probability system:
new regimes can always arrive and revise high-confidence
claims downward. Closed systems verify; open systems receive.

## Confidence bands (for human readers)

    [0.85, 1.00]  STRONG     proceed with high confidence
    [0.70, 0.85)  GOOD       proceed, note weakest rule
    [0.50, 0.70)  AMBIGUOUS  flag for review
    [0.30, 0.50)  WEAK       likely narrative drift
    [0.00, 0.30)  FAIL       out-of-frame

Machines propagate raw floats. Bands are for audit logs.

## Falsifiability

A claim's frame-confidence is the aggregate over five rules.
The weakest rule is reported alongside the aggregate — that
is where the claim is most likely hiding a violation.

A claim does not PASS the frame. It TRAVERSES the field,
accumulating or losing confidence as it moves through.

## Translation rule

When in doubt, translate to:
    energy, rate, or constraint.

Never to:
    identity, category, or essence.
