# CTNH-MANA API DOMAIN

## OVERVIEW
Public API surfaces for Mana (35 Java files): magic multiblock predicates/maps, effects, recipe conditions, network contracts, custom logic, and mana traits.

## STRUCTURE
```text
api/
|-- effect/                    # 16: ArmorBreakEffect, BladeUnleashedEffect, IndexTargetEffect, KarmaEffect, KarmaFortunaEffect, MagicalAntagonismEffect, PainShieldEffect, PhysicalAntagonismEffect, RageEffect, RealityDissociationEffect, RootedEffect, ShroudGazeEffect, SoulLeechEffect, TaintedBloodEffect, WishingFlyEffect, WitherCloudEffect
|-- machine/gem/               # GemSublimatorRules
|-- machine/trait/             # 3: BTManaContainerTrait, ExtendedControlBusCircuitTrait, MysticSpireManaTrait
|-- mixin/                     # IBloodAltarLogic
|-- networks/                  # BotaniaEffectPacketExtend, BotaniaExtendEffectType
|-- pattern/                   # CMBlockMaps, CMPredicates
|-- recipe/condition/          # BloodAltarCondition, HellForgeCondition, InfusionCellCastingCondition, ZenithCondition
`-- recipe/customlogic/        # 6: DigitalWellOfSufferLogic, EternalGardenLogic, IndustrialGemCuttingLogic, IndustrialGemSublimatorGenericLogic, IndustrialGemSublimatorLogic, IndustrialSalvagingLogic
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Pattern helpers | `api/pattern/` (CMBlockMaps, CMPredicates) |
| Effects | `api/effect/` (16) |
| Mana traits | `api/machine/trait/` (BTManaContainerTrait implements ManaReceiver; MysticSpireManaTrait with BigInteger trueMana; ExtendedControlBusCircuitTrait with 32-lane CustomItemStackHandler) |
| Gem rules | `api/machine/gem/GemSublimatorRules.java` |
| Recipe conditions | `api/recipe/condition/` (4) |
| Custom logic | `api/recipe/customlogic/` (6) |
| Network APIs | `api/networks/` (Botania packet extensions) |
| Mixin APIs | `api/mixin/IBloodAltarLogic.java` |

## CONVENTIONS
- API classes must not leak client-only classes into common construction paths.
- BTMana persistence is trait-owned: `BTManaContainerTrait` (`@Persisted maxBTMana/BTMana`, `ManaReceiver`, `changeMana`/`sendMana`, `setMaxBTMana` clamps >=0) replaces former `ManaMachineBlockEntity` fields; `MysticSpireManaTrait` owns `trueMana`/`trueManaCapacity` String BigInteger + int cache via `SpireBigMath` and exposes `mysticOutboundTickCap`/`mysticInboundTickBudget`/`receiveMana`/`sendMana`; `ExtendedControlBusCircuitTrait` owns persisted `CustomItemStackHandler(laneCount)` filtered to `IntCircuitBehaviour::isIntegratedCircuit`.
- GT/GMT recipes are runtime dynamic-pack data (`CTNHManaGTAddon.addRecipes()` -> `CTNHDynamicDataPack`); `runData` produces NO JSON for them.
- Item/block/fluid references MUST use direct registration objects (`CMItems.X`, `CMBlocks.X`); never string `ResourceLocation` + `ForgeRegistries` lookup.

## RECIPE LOGIC BOUNDARY
`api/recipe/customlogic/` 的 6 个类与 `ZenithMatrixRecipeLogic` 都落在 `RecipeLogic` 层。约束以 `docs/_architecture/AGENTS.md` §6 为准：

- `RecipeLogic` 负责当前 recipe、工作状态、配方上下文，以及经 `ContentListMap.forEachEntry` 按 capability 顺序分发输出 tooltip。
- 输出内容的解释属 `RecipeCapability` 自己的职责；**不要在 `RecipeLogic` 里加 capability 类型判断**。
- 遍历 recipe 内容统一走 `forEachEntry`，不要遍历 `asMap().entrySet()` 再手排。
- `lastRecipe` 已由 `@DescSynced` 同步，Jade 中禁止重复序列化。

## ANTI-PATTERNS
- Do not add gameplay logic to API classes; keep implementation in `common/` or `registry/`.
- Do not persist mana on BlockEntity; the trait is the source of truth. Do not add Lombok `@Setter` to `maxBTMana` — use explicit clamping setter.

## SCOPE
Applies to `src/main/java/com/magicbee/ctnhmana/api` and its child packages.

## READ WHEN
- Exposing magic multiblock patterns or recipe surfaces to other code.
- Adding or changing mana storage/circuit traits.

## SOURCE OF TRUTH
- `api/pattern/` contracts and `registry/` wiring.
- `api/machine/trait/*` and `common/machine/FlowerCakeMachine` / `common/multiblock/MysticSpire` wiring.

## WORKFLOW
1. Confirm the surface is genuinely shared before adding it to `api/`.
2. Run `:modules:CTNH-Mana:build`.
