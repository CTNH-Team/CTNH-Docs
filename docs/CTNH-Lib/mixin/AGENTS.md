# CTNH-LIB MIXIN DOMAIN

## OVERVIEW
Shared mixins (4 Java files): GT recipe/machine builder adjustments, RecipeManager datapack removal, TMRV compatibility.

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| GT recipe/machine builders | `mixin/GTRecipesMixin.java`, `mixin/MachineBuilderMixin.java` |
| Datapack recipe removal | `mixin/RecipeManagerApplyMixin.java` (`@Mixin(RecipeManager)`, priority 1100) |
| TMRV compatibility | `mixin/TMRVMixin.java` |
| Mixin config | `src/main/resources/ctnhlib.mixins.json` (4 mixins registered) |

## CONVENTIONS
- Mixins here adjust shared GTCEu and third-party behavior for all CTNH modules; keep them minimal and compatible.
- All four registered mixins are common-side; the client list in `ctnhlib.mixins.json` is empty.
- `RecipeManagerApplyMixin` injects at `apply*` HEAD and drops `map.keySet()` entries matching any `RecipeRemovalHelper.getFilters()` filter; no-op when filter list is empty.
- `GTJadePluginMixin` / Jade priority ordering was removed in f9951f9 along with `jade/GTProvidersRegistrar.java` and `jade/JadePriorityManager.java`; do not reintroduce Jade ordering here.

## ANTI-PATTERNS
- Do not add module-specific mixins to Lib; they belong in the owning module.
- Do not re-add Jade-related mixins; Jade provider ordering is now owned outside Lib.

## SCOPE
Applies to `src/main/java/tech/vixhentx/mcmod/ctnhlib/mixin` and `src/main/resources/ctnhlib.mixins.json`.

## READ WHEN
- Changing shared GT builder behavior.
- Changing shared datapack recipe-removal enforcement.

## SOURCE OF TRUTH
- `src/main/resources/ctnhlib.mixins.json` and the mixin classes in `mixin/`.

## WORKFLOW
1. Verify the upstream target member against the loaded GTCEu/TMRV version.
2. Run `:modules:CTNH-Lib:build`; validate at runtime.
