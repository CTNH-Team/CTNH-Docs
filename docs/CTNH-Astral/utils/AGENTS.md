# CTNH-ASTRAL UTILS DOMAIN

## OVERVIEW
Shared helper utilities for Astral (1 Java file).

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Mod utils | `utils/ModUtils.java` |

## CONVENTIONS
- Keep helpers free of registry dependencies where possible.

## ANTI-PATTERNS
- Do not duplicate helpers that exist in CTNH-Lib `utils/`.

## SCOPE
Applies to `src/main/java/com/ctnh/ctnhastral/utils`.

## READ WHEN
- Reusing Astral-wide helper logic.

## SOURCE OF TRUTH
- The utility classes in `utils/`.

## WORKFLOW
1. Check CTNH-Lib `utils/` first for an existing shared helper.
2. Run `:modules:CTNH-Astral:build` after changes.
