# CTPP UTIL DOMAIN

## OVERVIEW
Shared helper utilities for CTPP (7 Java files).

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Values/tooltips | `util/CTPPValues.java`, `util/CommonTooltips.java` |
| Slot/custom interfaces | `util/ICustomSlot.java`, `util/IMatrix3dAccess.java`, `util/IWorkingMachineStep.java` |
| Item axis builder | `util/ItemAxisBuilder.java` |
| Math | `util/MathUtil.java` |

## CONVENTIONS
- Keep helpers free of registry dependencies where possible.

## ANTI-PATTERNS
- Do not duplicate helpers that exist in CTNH-Lib `utils/`.

## SCOPE
Applies to `src/main/java/com/mo_guang/ctpp/util`.

## READ WHEN
- Reusing CTPP-wide helper logic.

## SOURCE OF TRUTH
- The utility classes in `util/`.

## WORKFLOW
1. Check CTNH-Lib `utils/` first for an existing shared helper.
2. Run `:modules:CTPP:build` after changes.