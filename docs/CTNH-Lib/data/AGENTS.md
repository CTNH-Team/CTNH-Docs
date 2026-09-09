# CTNH-LIB DATA DOMAIN

## OVERVIEW
Dynamic datapack, filter, and recipe-removal support shared by CTNH modules (3 Java files).

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Dynamic datapack | `data/CTNHDynamicDataPack.java` |
| Data filter pack | `data/DataFilterPack.java` |
| Recipe-removal registry | `data/recipe/RecipeRemovalHelper.java` (`RemoveFilter`, `remove()`/`clear()`/`getFilters()`) |
| Removal enforcement | `mixin/RecipeManagerApplyMixin.java` (see mixin domain) |

## CONVENTIONS
- `CTNHDynamicDataPack` implements `PackResources` and serializes `FinishedRecipe` into GTCEu's `GTDynamicPackContents` at runtime; this is why GT/GMT recipes registered via `*GTAddon.addRecipes()` never appear as `runData` output. See the root AGENTS.md CONVENTIONS.
- `CTNHDynamicDataPack.addRecipe()` writes recipe/advancement/tag IDs as `ResourceLocation` paths; with dev dump enabled it also dumps recipes to `gtceu/dumped/data`.
- The `ctnhlib:filter_data` server data pack source is added from `common/CommonProxy.java`.
- `DataFilterPack` provides runtime datapack filtering.
- `RecipeRemovalHelper` is the shared ID-only removal registry; filters registered via `remove()` are applied by `RecipeManagerApplyMixin` before `RecipeManager` parses datapack recipes. Dynamic recipes are not affected.
- `RemoveFilter` top-level fields are AND-combined (`id`/`idRegex`/`mod`/`type`); `not` excludes matching child filters, `or` requires a matching child filter. `mod` matches `ResourceLocation.getNamespace()`, `type` matches derived `namespace:firstPathSegment`.
- Call `clear()` before a module registers its reload rules; `getFilters()` exposes the live list for the mixin.

## ANTI-PATTERNS
- Do not add module-specific datapack content here; register packs in the owning module.
- Do not use `RecipeRemovalHelper` for dynamic GT/GMT recipes; the mixin only strips datapack `RecipeManager` entries.

## SCOPE
Applies to `src/main/java/tech/vixhentx/mcmod/ctnhlib/data`.

## READ WHEN
- Changing runtime datapack or filter behavior.
- Changing shared recipe-removal filters.

## SOURCE OF TRUTH
- `data/CTNHDynamicDataPack.java`, `data/DataFilterPack.java`, `data/recipe/RecipeRemovalHelper.java`, and the CommonProxy wiring.

## WORKFLOW
1. Check datapack registration flow in `common/CommonProxy.java`.
2. Run `:modules:CTNH-Lib:build` after changes.
