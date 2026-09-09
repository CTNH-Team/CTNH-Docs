# CTNH-BIO UTILS DOMAIN

## OVERVIEW
Shared helper utilities for Bio (7 Java files).

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Machine names | `utils/CBMachineNames.java` |
| Recipe modifiers | `utils/CBRecipeModifiers.java` |
| Decomposing | `utils/DecomposingRecipeHandler.java` |
| Loot helpers | `utils/DespoilLootHelper.java` |
| Input handling | `utils/IKeyPressedWithCoord.java` |
| Random/vial helpers | `utils/RandomUtils.java`, `utils/VialCraftingRemainingItem.java` |

## CONVENTIONS
- Keep helpers free of registry dependencies where possible.

## ANTI-PATTERNS
- Do not duplicate helpers that exist in CTNH-Lib `utils/`.

## SCOPE
Applies to `src/main/java/com/moguang/ctnhbio/utils`.

## READ WHEN
- Reusing Bio-wide helper logic.

## SOURCE OF TRUTH
- The utility classes in `utils/`.

## WORKFLOW
1. Check CTNH-Lib `utils/` first for an existing shared helper.
2. Run `:modules:CTNH-Bio:build` after changes.
