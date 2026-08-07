# CTNH-LIB DATA DOMAIN

## OVERVIEW
Dynamic datapack and filter support shared by CTNH modules (2 Java files).

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Dynamic datapack | `data/CTNHDynamicDataPack.java` |
| Data filter pack | `data/DataFilterPack.java` |

## CONVENTIONS
- `CTNHDynamicDataPack` implements `PackResources` and serializes `FinishedRecipe` into GTCEu's `GTDynamicPackContents` at runtime; this is why GT/GMT recipes registered via `*GTAddon.addRecipes()` never appear as `runData` output. See the root AGENTS.md CONVENTIONS.
- `CTNHDynamicDataPack.addRecipe()` writes recipe/advancement/tag IDs as `ResourceLocation` paths; with dev dump enabled it also dumps recipes to `gtceu/dumped/data`.
- The `ctnhlib:filter_data` server data pack source is added from `common/CommonProxy.java`.
- `DataFilterPack` provides runtime datapack filtering.

## ANTI-PATTERNS
- Do not add module-specific datapack content here; register packs in the owning module.

## SCOPE
Applies to `src/main/java/tech/vixhentx/mcmod/ctnhlib/data`.

## READ WHEN
- Changing runtime datapack or filter behavior.

## SOURCE OF TRUTH
- `data/CTNHDynamicDataPack.java`, `data/DataFilterPack.java`, and the CommonProxy wiring.

## WORKFLOW
1. Check datapack registration flow in `common/CommonProxy.java`.
2. Run `:modules:CTNH-Lib:build` after changes.
