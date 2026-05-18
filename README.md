# differential-frame-core

The shared contract that says: every noun is dX/dt under scope.

## What this is

Five repos in the ecosystem each independently derive the same
contract in their own dialect. This repo consolidates them into
one canonical, importable, testable spec.

## Why it exists

Dialect drift was becoming the dominant failure mode.
One source of truth = every downstream audit becomes
cross-comparable.

## What's inside

- SPEC.md       — the canonical contract
- DIALECTS.md   — the five existing versions reconciled
- contract.py   — formal type + five rules as predicates
- validators.py — text-level quick audits
- audit.py      — batch scan files for frame violations

## Usage

    from differential_frame.contract import Noun, in_frame
    from differential_frame.validators import quick_audit
    from differential_frame.audit import audit_file, summarize

    # quick text check
    quick_audit("He is fundamentally lazy.")
    # -> {'in_frame': False, 'recommendation': 'flag: narrative drift...'}

    # batch
    results = audit_file('some_repo/README.md')
    print(summarize(results))

## License

CC0. Copy, re-publish, propagate.
