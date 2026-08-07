# CTNH-CORE UTILS DOMAIN

## OVERVIEW
Shared helper utilities for Core (8 Java files): tooltips, machine utils, recipe helpers, math, and structure utilities.

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Tooltips | `utils/CTNHCommonTooltips.java` |
| Machine utils | `utils/CTNHMachineUtils.java`, `utils/CoilTierHelper.java` |
| Recipe helpers | `utils/CTNHRecipeHelper.java` |
| Data structures | `utils/LayeredBiMap.java`, `utils/OrientedItem.java` |
| Math/structures | `utils/MathUtils.java`, `utils/StructureUtils.java` |

## CONVENTIONS
- Helpers are static utilities unless state requires an instance; keep them free of registry dependencies where possible.

## ANTI-PATTERNS
- Do not duplicate helpers that already exist in CTNH-Lib `utils/`.
- Do not add gameplay logic here; utils are for shared mechanics.

## SCOPE
Applies to `src/main/java/io/github/cpearl0/ctnhcore/utils`.

## READ WHEN
- Reusing Core-wide tooltip, machine, or recipe logic.

## SOURCE OF TRUTH
- The utility classes in `utils/`; shared CTNH helpers in CTNH-Lib `docs/CTNH-Lib/utils/AGENTS.md`.

## WORKFLOW
1. Check CTNH-Lib `utils/` first for an existing shared helper.
2. Add Core-specific helpers here only when Lib sharing is not appropriate.
3. Run `:modules:CTNH-Core:build` after changes.
