# CTNH-ENERGY API DOMAIN

## OVERVIEW
Shared API surfaces for Energy (8 Java files): predicates, EU item context, multiblock/CPU contracts, pattern provider logic, and maintaining context.

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Predicates | `api/CEPredicates.java` |
| EU item context | `api/EUItemContext.java` |
| CPU auto-multiply | `api/IAutoMultiplyCPU.java` |
| Ghost key target | `api/IGhostKeyTarget.java` |
| Pattern provider logic | `api/IPatternProviderLogic.java` |
| Maintaining context | `api/IMaintainingContext.java` |
| Upgradeable menu | `api/IUpgradeableMenu.java` |

## CONVENTIONS
- API classes must not leak client-only classes into common construction paths.
- `IAutoMultiplyCPU` and `IPatternProviderLogic` back quantum computer and pattern buffer behavior.
- `IMaintainingContext` provides get/set for a maintaining amount, used by `MaintainingCardItem`.

## ANTI-PATTERNS
- Do not add gameplay logic to API classes; keep implementation in `common/` or `registry/`.

## SCOPE
Applies to `src/main/java/tech/luckyblock/mcmod/ctnhenergy/api`.

## READ WHEN
- Exposing a new Energy API surface to other CTNH modules.

## SOURCE OF TRUTH
- `api/` classes and their consumers in `common/`.

## WORKFLOW
1. Confirm the surface is genuinely shared before adding it to `api/`.
2. Run `:modules:CTNH-Energy:build`.