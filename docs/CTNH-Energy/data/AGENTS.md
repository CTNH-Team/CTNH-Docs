# CTNH-ENERGY DATA DOMAIN

## OVERVIEW
Datagen source for `src/generated/resources` (3 Java files): CEDatagen and lang handlers.

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Datagen entry | `data/CEDatagen.java` |
| Lang | `data/lang/ChineseLangHandler.java`, `data/lang/EnglishLangHandler.java` |

## CONVENTIONS
- `src/generated/resources` is produced by `:modules:CTNH-Energy:runData`; do not hand-edit generated JSON.
- GT/GMT recipes via `CTNHEnergyGTAddon.addRecipes()` are runtime dynamic-pack data: `runData` produces NO JSON for them. See root AGENTS.md CONVENTIONS.
- Ponder language entries are extracted during client datagen via `common/CommonProxy.gatherData()` and CTNH-Lib's `CTNHPonderLang`.

## ANTI-PATTERNS
- Do not hand-edit `src/generated/resources`.

## SCOPE
Applies to `src/main/java/tech/luckyblock/mcmod/ctnhenergy/data` and its child packages.

## READ WHEN
- Adding Energy lang or datagen output.

## SOURCE OF TRUTH
- `data/CEDatagen.java` and `common/CommonProxy.gatherData()` wiring.

## WORKFLOW
1. Edit the matching provider, then run `:modules:CTNH-Energy:runData`.
2. Inspect generated-resource diffs; run `spotlessCheck`.
