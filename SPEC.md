# Differential Frame Core — Specification v1.0

## Contract

Every noun names a state on a curve, not a thing.
Read X as dX/dt under scope.
Carrying a noun outside its bounds is a translation error.

## Five rules

1. No noun is permanent. Every noun is dX/dt.
2. No claim travels without its bounds.
3. Scope is the claim, not a limitation on it.
4. Cycles persist; states do not.
5. If the equation does not close, flag — do not infer.

## Formal type

A valid noun in this frame is the tuple:

    Noun = (name, rate, bounds, scope, closure_check)

where:
    name           : str        — the label (compression artifact)
    rate           : dX/dt      — the actual referent
    bounds         : (lo, hi)   — the domain over which rate holds
    scope          : Context    — the frame in which the claim is valid
    closure_check  : bool       — does the rate equation close?

A noun missing any field is not a noun. It is a narrative.

## Translation rule

When in doubt, translate to:
    energy, rate, or constraint.

Never to:
    identity, category, or essence.

## Falsifiability

A claim is in-frame iff:
    1. its noun has a rate
    2. its rate has bounds
    3. its bounds have scope
    4. its scope is declared
    5. its closure check passes

A claim failing any of these is OUT-OF-FRAME and must be
flagged before being passed downstream.
