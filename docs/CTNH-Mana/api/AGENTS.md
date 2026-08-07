# CTNH-MANA API DOMAIN

## OVERVIEW
Public API surfaces for Mana (18 Java files): magic multiblock predicates/maps, effects, recipe conditions, network contracts, and custom logic.

## STRUCTURE
```text
api/
|-- effect/                    # 8: BladeUnleashedEffect, IndexTargetEffect, KarmaEffect, KarmaFortunaEffect, ShroudGazeEffect, SoulLeechEffect, TaintedBloodEffect, WishingFlyEffect
|-- mixin/                     # IBloodAltarLogic
|-- networks/                  # BotaniaEffectPacketExtend, BotaniaExtendEffectType
|-- pattern/                   # CMBlockMaps, CMPredicates
|-- recipe/condition/          # BloodAltarCondition, HellForgeCondition, InfusionCellCastingCondition, ZenithCondition
`-- recipe/customlogic/        # IndustrialSalvagingLogic
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Pattern helpers | `api/pattern/` (CMBlockMaps, CMPredicates) |
| Effects | `api/effect/` (8) |
| Recipe conditions | `api/recipe/condition/` (4) |
| Custom logic | `api/recipe/customlogic/IndustrialSalvagingLogic.java` |
| Network APIs | `api/networks/` (Botania packet extensions) |
| Mixin APIs | `api/mixin/IBloodAltarLogic.java` |

## CONVENTIONS
- API classes must not leak client-only classes into common construction paths.

## ANTI-PATTERNS
- Do not add gameplay logic to API classes; keep implementation in `common/` or `registry/`.

## SCOPE
Applies to `src/main/java/com/moguang/ctnhmana/api` and its child packages.

## READ WHEN
- Exposing magic multiblock patterns or recipe surfaces to other code.

## SOURCE OF TRUTH
- `api/pattern/` contracts and `registry/` wiring.

## WORKFLOW
1. Confirm the surface is genuinely shared before adding it to `api/`.
2. Run `:modules:CTNH-Mana:build`.