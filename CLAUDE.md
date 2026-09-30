# CLAUDE.md

Guidance for Claude Code when working in this repository.

## Project

`differential-frame-core` defines the canonical contract for the Differential
Frame and reconciles the five existing dialect versions into a single
authoritative specification. The Python package provides the contract as code,
validators, and an audit tool that scans text and code for contract
violations.

## Layout

- `SPEC.md` — canonical contract (authoritative).
- `DIALECTS.md` — the five existing versions reconciled against `SPEC.md`.
- `differential_frame/contract.py` — the formal contract expressed in code.
- `differential_frame/validators.py` — primitive checks (`is_valid_noun`,
  `has_bounds`, ...).
- `differential_frame/audit.py` — scan text/code for contract violations.
- `tests/` — `pytest` suites mirroring each module.
- `LICENSE` — CC0 1.0.

When `SPEC.md` and code disagree, `SPEC.md` is the source of truth — update
the code, do not silently change the spec.

## Conventions

- Python 3.10+, standard library only unless a dependency is justified.
- Run tests with `pytest` from the repo root.
- Keep `validators.py` free of I/O; `audit.py` is the only module that reads
  files or scans text.
- Public API is whatever `differential_frame/__init__.py` re-exports — treat
  everything else as internal.

## Development branch

Active work happens on `claude/add-claude-md-structure-5jJCi`. Commit and push
to that branch; do not push to `main` without explicit instruction.

<!-- clone-refspec-note v1 -->
## Cloning and pushing
Shallow clones are single-branch by default.
Before pushing any branch other than main, run:

    git config remote.origin.fetch '+refs/heads/*:refs/remotes/origin/*'
    git fetch --depth 1

Or clone with: git clone --depth 1 --no-single-branch <url>
Without this, the first push of a new branch
fails the tracking-ref check even when the
commit landed.
<!-- /clone-refspec-note v1 -->
