# CTNH-MANA UTILS DOMAIN

## OVERVIEW
Shared helper utilities for Mana (3 Java files).

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Mana utils | `utils/CTNHManaUtils.java` |
| Environment | `utils/EnvUtils.java` |
| Mod utils | `utils/ModUtils.java` |

## CONVENTIONS
- Keep helpers free of registry dependencies where possible.

## ANTI-PATTERNS
- Do not duplicate helpers that exist in CTNH-Lib `utils/`.

## SCOPE
Applies to `src/main/java/com/moguang/ctnhmana/utils`.

## READ WHEN
- Reusing Mana-wide helper logic.

## SOURCE OF TRUTH
- The utility classes in `utils/`.

## WORKFLOW
1. Check CTNH-Lib `utils/` first for an existing shared helper.
2. Run `:modules:CTNH-Mana:build` after changes.
