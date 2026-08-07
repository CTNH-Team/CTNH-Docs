# CTNH-BIO COMMON DOMAIN

## OVERVIEW
Shared bootstrap and common content for Bio (7 Java files): CommonProxy, recipe conditions, items, recipes, and serums.

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Common proxy | `common/CommonProxy.java` |
| Recipe conditions | `common/condition/EffectCondition.java` |
| Items | `common/item/AssemblyStepItem.java`, `common/item/OrganicVialItem.java` |
| Mob crushing recipes | `common/recipe/MobCrushingRecipe.java`, `common/recipe/MobCrushingRecipeManager.java` |
| Serums | `common/serum/PrimordialSerum.java` |

## CONVENTIONS
- `CommonProxy.java` initializes entities, creative tabs, datagen, registrate, `PropertyOperators`, `EntityProperties`, and Jade `LivingMachineStatusProvider`.
- `CommonProxy.registerCapabilities()` delegates to `api/capability/forge/CBCapabilities.java`.
- Mob crushing is a Bio-specific recipe surface (with JEI category and EMI mixins).

## ANTI-PATTERNS
- Do not bypass CommonProxy init order for registries that depend on PropertyOperators/EntityProperties.

## SCOPE
Applies to `src/main/java/com/moguang/ctnhbio/common` and its child packages.

## READ WHEN
- Changing CommonProxy wiring, serums, or common recipe logic.

## SOURCE OF TRUTH
- `common/CommonProxy.java` and `event/EventHandler.java`.

## WORKFLOW
1. Check `CommonProxy.init()` order before adding hooks.
2. Run `:modules:CTNH-Bio:build`.
