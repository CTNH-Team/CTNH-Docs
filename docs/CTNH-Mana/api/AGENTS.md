# CTNH-MANA API DOMAIN

## OVERVIEW
Public API surfaces for Mana (16 Java files): magic multiblock predicates/maps, effects, recipe conditions, and network contracts.

## STRUCTURE
```text
api/
|-- effect/                    # 7: BladeUnleashedEffect, IndexTargetEffect, KarmaEffect, KarmaFortunaEffect, ShroudGazeEffect, SoulLeechEffect, WishingFlyEffect
|-- mixin/                     # IBloodAltarLogic
|-- networks/                  # BotaniaEffectPacketExtend, BotaniaExtendEffectType
|-- pattern/                   # CMBlockMaps, CMPredicates
`-- recipe/condition/          # BloodAltarCondition, HellForgeCondition, InfusionCellCastingCondition, ZenithCondition
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Pattern helpers | `api/pattern/` (CMBlockMaps, CMPredicates) |
| Effects | `api/effect/` (7) |
| Recipe conditions | `api/recipe/condition/` (4) |
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
