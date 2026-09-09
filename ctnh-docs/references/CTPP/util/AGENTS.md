# CTPP UTIL DOMAIN

## OVERVIEW
Shared helper utilities for CTPP (6 Java files). `CTPPValues` (MT tiers) removed — mechanical tier now uses `GTValues.VNF`.

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Tooltips | `util/CommonTooltips.java` (kinetic_overclock, input_speed, mechanical_tier_machine) |
| Slot/custom interfaces | `util/ICustomSlot.java`, `util/IMatrix3dAccess.java`, `util/IWorkingMachineStep.java` |
| Item axis builder | `util/ItemAxisBuilder.java` |
| Math | `util/MathUtil.java` |

## CONVENTIONS
- Keep helpers free of registry dependencies where possible.
- Mechanical tier display now via `GTValues.VNF[tier]`; `CTPPValues.MT` and its lang keys `ctpp.ctppvalues.mt.*` / `ctpp.commontooltips.mechanical_tier` (old) are removed — do not reference.

## ANTI-PATTERNS
- Do not duplicate helpers that exist in CTNH-Lib `utils/`.
- Do not reintroduce `CTPPValues`.

## SCOPE
Applies to `src/main/java/com/mo_guang/ctpp/util`.

## READ WHEN
- Reusing CTPP-wide helper logic.

## SOURCE OF TRUTH
- The utility classes in `util/`.
- `GTValues.VNF` for tier names.

## WORKFLOW
1. Check CTNH-Lib `utils/` first for an existing shared helper.
2. Run `:modules:CTPP:build` after changes.
