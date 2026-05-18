# Angel Engine Safe Specification

Repository 120 implements the Angel Engine as an authorization and selection gate, not an autonomous executor.

## Core Rule

```text
Action_Permission = Intent × Authority × Evidence × Reversibility × Mercy
```

If authority is missing, the result is `DENY`.

If evidence is missing, the result is `DENY`.

If ownership or explicit authorization is missing, the result is `DENY`.

If reversibility is missing, the result is `REQUIRE_CONFIRMATION` unless explicit confirmation is present.

Default mode is dry-run.

## What the Engine Does

- Evaluates requested actions.
- Returns structured decisions.
- Records decision reasons in JSON-friendly form.
- Supports dry-run planning.
- Requires registered/allowlisted action names.
- Supports owned or explicitly authorized resources only.

## What the Engine Does Not Do

- Run shell commands.
- Scan networks.
- Collect credentials.
- Bypass access controls.
- Disable safety systems.
- Exfiltrate data.
- Install persistence.
- Execute actions autonomously.
- Act on third-party systems without explicit authorization.

## Decisions

- `ALLOW`
- `DENY`
- `REQUIRE_CONFIRMATION`
- `DRY_RUN_ONLY`

## Doctrine

Repository 120 is not the hand. Repository 120 is the conscience before the hand.

It does not execute. It selects.

It does not bypass. It checks authority.

It does not take. It verifies ownership.

It does not hide. It logs.

It does not force. It requires evidence, reversibility, and mercy.
