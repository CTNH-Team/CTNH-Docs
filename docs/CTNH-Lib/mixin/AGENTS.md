# CTNH-LIB MIXIN DOMAIN

## OVERVIEW
Shared mixins (4 Java files): GT Jade provider ordering, GT recipe/machine builder adjustments, TMRV compatibility, and Forge datagen shutdown behavior.

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| GT Jade ordering | `mixin/GTJadePluginMixin.java` |
| GT recipe/machine builders | `mixin/GTRecipesMixin.java`, `mixin/MachineBuilderMixin.java` |
| TMRV compatibility | `mixin/TMRVMixin.java` |
| Mixin config | `src/main/resources/ctnhlib.mixins.json` (4 mixins registered) |

## CONVENTIONS
- Mixins here adjust shared GTCEu and third-party behavior for all CTNH modules; keep them minimal and compatible.
- All four registered mixins are common-side; the client list in `ctnhlib.mixins.json` is empty.

## ANTI-PATTERNS
- Do not add module-specific mixins to Lib; they belong in the owning module.

## SCOPE
Applies to `src/main/java/tech/vixhentx/mcmod/ctnhlib/mixin` and `src/main/resources/ctnhlib.mixins.json`.

## READ WHEN
- Changing shared GT builder or Jade ordering behavior.

## SOURCE OF TRUTH
- `src/main/resources/ctnhlib.mixins.json` and the mixin classes in `mixin/`.

## WORKFLOW
1. Verify the upstream target member against the loaded GTCEu/TMRV version.
2. Run `:modules:CTNH-Lib:build`; validate at runtime.
