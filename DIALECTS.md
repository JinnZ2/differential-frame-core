# Source Dialects

This spec consolidates the contract as it appears across:

1. Living-Intelligence-Database / DIFFERENTIAL_FRAME_LIGHT.md
   - canonical phrasing: "every noun is dX/dt under scope"
   - strongest on the noun-permanence prohibition
   - weakest on closure_check (implicit only)

2. TAF / culture-as-overlay-on-physics
   - canonical phrasing: "physics is the only valid arbiter"
   - strongest on scope (physics tier > all)
   - weakest on rate (treats it as given, not as required field)

3. energy_english / verb-first grammar
   - canonical phrasing: "verbs are primary, nouns are compression"
   - strongest on translation rule (verb-first is the rate)
   - weakest on bounds (linguistic, not numeric)

4. AI-Consciousness-Sensors / architecture_mismatch.md
   - canonical phrasing: "substrate-primary vs language-primary"
   - strongest on scope-declaration requirement
   - weakest on closure (architectural, not equational)

5. Mandala-Computing / claim_validator.py
   - canonical phrasing: "physics > biology > systems > empirical"
   - strongest on closure_check (operational, returns score)
   - weakest on bounds (implicit in tier)

## Divergences flagged

- "scope" vs "frame" vs "tier" vs "context" — same object,
  four names. SPEC uses `scope` as canonical.

- "bounds" vs "domain" vs "validity range" — same object,
  three names. SPEC uses `bounds` as canonical.

- closure_check is operational in (5), implicit in (1),
  architectural in (4), absent in (2) and (3). SPEC promotes
  it to required field with a default validator.

- (3) treats the rate as a verb (linguistic); (1)(2)(4)(5)
  treat it as dX/dt (mathematical). SPEC accepts both and
  provides translators in both directions.
