# Flow Gates

Use only three top-level gates.

## Qualification Gate

Qualification result is one of:

- `PASS`
- `PASS_WITH_ASSUMPTIONS`
- `BLOCKED`

Do not proceed past blocking unknowns. Non-blocking unknowns may proceed as explicit assumptions.

Can reliable planning begin?

## Build Readiness

**Build Readiness:** before substantial implementation, verify that scope, solution, and evaluation criteria are sufficiently clear for the target delivery level.

Result: `PASS | PASS_WITH_ASSUMPTIONS | BLOCKED`.

Are scope, solution, and success criteria sufficiently clear for the requested delivery depth?

## Release Readiness

Does the current result satisfy the requested delivery target and acceptance criteria?

Other checks remain local acceptance criteria rather than new gate objects.
