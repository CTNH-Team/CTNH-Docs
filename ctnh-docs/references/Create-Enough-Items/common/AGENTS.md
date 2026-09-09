# CREATE-ENOUGH-ITEMS COMMON DOMAIN

## OVERVIEW
Shared bootstrap for CEI: CommonProxy registers the CEI registrate, datagen lang processor, and no-op GTCEu registry listeners.

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Common proxy | `common/CommonProxy.java` |

## CONVENTIONS
- `CommonProxy.init()` creates `CreateEnoughItems.REGISTRATE` from `CEIRegistrate.create()`, calls `CEIDatagen.init()`, and registers no-op listeners for `MachineDefinition`, `GTRecipeType`, and `RecipeConditionType`; fill these only when CEI really registers GTCEu content.
- This module depends on `:modules:CTNH-Lib`; it does not depend on CTNH-Core.

## ANTI-PATTERNS
- Do not move EMI UI behavior into CTNH-Core; CEI owns EMI customization.

## SCOPE
Applies to `src/main/java/com/ctnh/cei/common`.

## READ WHEN
- Changing CEI bootstrap or registry listener wiring.

## SOURCE OF TRUTH
- `common/CommonProxy.java` and `CreateEnoughItems.java`.

## WORKFLOW
1. Check `CommonProxy.init()` order before adding hooks.
2. Run `:modules:Create-Enough-Items:build`.
