# CTNH-LIB MIXIN DOMAIN

## OVERVIEW
Shared mixins (3 Java files): GT recipe/machine builder adjustments, TMRV compatibility.

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| GT recipe/machine builders | `mixin/GTRecipesMixin.java`, `mixin/MachineBuilderMixin.java` |
| TMRV compatibility | `mixin/TMRVMixin.java` |
| Mixin config | `src/main/resources/ctnhlib.mixins.json` (3 mixins registered) |

## CONVENTIONS
- Mixins here adjust shared GTCEu and third-party behavior for all CTNH modules; keep them minimal and compatible.
- All three registered mixins are common-side; the client list in `ctnhlib.mixins.json` is empty.
- `GTJadePluginMixin` / Jade priority ordering was removed in f9951f9 along with `jade/GTProvidersRegistrar.java` and `jade/JadePriorityManager.java`; do not reintroduce Jade ordering here.

## ANTI-PATTERNS
- Do not add module-specific mixins to Lib; they belong in the owning module.
- Do not re-add Jade-related mixins; Jade provider ordering is now owned outside Lib.

## SCOPE
Applies to `src/main/java/tech/vixhentx/mcmod/ctnhlib/mixin` and `src/main/resources/ctnhlib.mixins.json`.

## READ WHEN
- Changing shared GT builder behavior.

## SOURCE OF TRUTH
- `src/main/resources/ctnhlib.mixins.json` and the mixin classes in `mixin/`.

## WORKFLOW
1. Verify the upstream target member against the loaded GTCEu/TMRV version.
2. Run `:modules:CTNH-Lib:build`; validate at runtime.
