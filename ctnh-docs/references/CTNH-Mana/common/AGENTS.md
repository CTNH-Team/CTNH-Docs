# CTNH-MANA COMMON DOMAIN

## OVERVIEW
`common/` 是 CTNH-Mana 的实现核心（125 个 Java 文件，本模块最大域）：代理、多方块机器（31）、单方块机器与花、物品（8 个子包）、实体与 AI、方块与方块实体、能力、GUI、仓室、仪式适配器与仪式类型、虚境入侵服务端流程。

## STRUCTURE
```text
common/
├── CommonProxy.java, DigitalWosMachine.java
├── blockentity/
│   ├── flower/                # 7: AnattaLotusBlockEntity, BlackVeinMarigoldBlockEntity, BloodAntiarisBlockEntity, DemonFlytrapBlockEntity, GenethistleBlockEntity, ParaRosiaBlockEntity, TulpenmanieBlockEntity
│   ├── machine/               # FlowerCakeBlockEntity (MetaMachineBlockEntity + GeoBlockEntity 外壳)
│   └── WitherAconiteTrapBlockEntity.java
├── blocks/                    # 5: CoilType, FrameBlock, ManaIndicatorLight, RuneBlock, WitherAconiteTrapBlock
├── capability/                # DamageClampCapability
├── entity/                    # 5: AbstractRampageBee, DeltaSpark, GiantBee, OmegaSpark, RoyalServantBee
│   ├── ai/                    # 8: GiantBee*Goal(6), RoyalServant*Goal(2)
│   ├── navigation/            # RampageFlyingPathNavigation, RampageNodeEvaluator
│   └── projectile/            # BeeNukeProjectile, MaliciousThermalilyProjectile, WitherAconiteProjectile
├── event/zenith/              # 5: ZenithGlitchText, ZenithInvadeEffects, ZenithInvadeEvent, ZenithInvadeManager, ZenithInvadeMessages
├── gui/                       # 7: AnimationTextureY, ArcButtonWidget, BaseManaMachineGui, ExtendedCentralControlBusCircuitUi, ManaStatusGui, SelectableCircuitSlotWidget, ShroudUi
├── item/
│   ├── FlowerCakeItem.java, TooltipsBlockItem.java, ZenithDebugToolItem.java
│   ├── bloodmagicjade/        # JadeItem
│   ├── bosssummoner/          # BossSummonerBehavior, IThrowableItem, ThrowItem, ThrowableSummoner
│   ├── caduceus/              # CaduceusItem, MultiToolDefinition
│   ├── dungeon/               # PerfectMineKeyItem
│   ├── equipment/             # KoishiEyeItem, SaberWandItem, TaintedBloodWeepingEye, YurikoRingItem
│   ├── manafuelstick/         # IManaFuelStick
│   ├── manamachineupgrade/    # 9: BeeVisionUpgradeItem, BMUpgradeItemT1/T2, BTUpgradeItemT1/T2/T3, GTUpgradeItemT1/T2, ManaMachineUpgradeItem
│   └── rune/                  # IRuneItem, RuneElementType, SpireUpgradeRuneItem
├── machine/                   # 3: FlowerCakeBlock, FlowerCakeMachine, GemSublimatorMachine
├── multiblock/                # 31 类，含 ManaMultiBlockMachine, BaseManaMultiBlockMachine, CrossParallelManaMultiBlockMachine, MultiPatternMultiblockMachine, ManaReactor, HellForgeMachine, MysticSpire, ZenithMachine, ZenithMatrixMachine, ZenithSpire, EternalGarden, EternalWosMachine, WishingWill, ManaCondenserMachine, ManaFuelInfuserMachine, TwistedFusionMachine, IndustrialAltarMachine, MeteorCaptureMachine, DemonWillMachine, QuasarEye, NicollDysonBeams, ArcaneHighEnergyCompressionReactorCore, IndustrialSalvagingMachine, IndustrialGemInlayMachine, ManaForceTransformer, RitualMechanicalMachine, SpireMath, SpireBigMath, MachineUtils, ICentralStorageMachine, IChannelMachine
├── parts/                     # 5: CentralControlBus, CMPartsAbility, ExtendedCentralControlBus, ManaHatch, RedstoneSignalBroadcastHatch
│   └── ManaHatches/           # 3: BloodManaHatch, CreativeManaHatch, SparkManaHatch
├── ritual/                    # 2: MachineRitualSoulNetwork, MachineRitualStoneHost
└── ritualtypes/               # 6: RitualBeeSummon, RitualBossSummon, RitualCharger, RitualDragonCloud, RitualLifeExtractor, RitualShroudSight
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Common 代理 | `common/CommonProxy.java`（机器/配方类型/条件泛型监听、材质注册、物品/方块/BE、创造栏、粒子、音效、网络、datagen、配置；`onFMLoadComplete` 注册 Blood Magic 祭坛组件） |
| 多方块基类 | `common/multiblock/ManaMultiBlockMachine.java`（`hatch`/`hatchPos`、`ManaLevel`、`isZenithOpen`、`Zenith_Enhanced`）、`BaseManaMultiBlockMachine.java`（魔力消耗、升级件、`ManaStatusGui`/`ShroudUi` 标签页）、`CrossParallelManaMultiBlockMachine.java`（`recipeModifier` + `batchModeViewAware` + `parallelBudgetModifier` 三件套，供 `registry/multiblock/ManaMachine` 的 `mana_macerator`/`mana_bender` 使用）、`MultiPatternMultiblockMachine.java` |
| 多方块实现 | `common/multiblock/`（31） |
| 尖塔 | `common/multiblock/MysticSpire.java`（持有 `MysticSpireManaTrait`）+ `SpireMath.java`/`SpireBigMath.java` |
| 单方块机器 | `common/machine/`（`FlowerCakeMachine` 持有 `BTManaContainerTrait`，`FlowerCakeBlock` 委托；`GemSublimatorMachine` 配合 `api/machine/gem/GemSublimatorRules`） |
| 仓室与总线 | `common/parts/`：`ManaHatch`（`attachTrait(new BTManaContainerTrait(this, maxBTMana))`，BTMana 归属方）、`CMPartsAbility`（`MANAHATCH`, `SIGNALHATCH`, `CentralControlBus`, `ExtendedCentralControlBus`）、`ExtendedCentralControlBus`（`attachPersistentTrait("extended_circuit_slot", ...)`）、`ManaHatches/` 三种变体 |
| 物品 | `common/item/`（8 个子包 + 3 个顶层类）：`manamachineupgrade/`（9）中 `BTUpgradeItemT1/T2/T3` 是 Botania 升级件，`calculateNormalUpgrade` 的并行上限分别约 16 / 64 / 256，运行时每并行提速分别 1% / 5% / 5% |
| 实体与 AI | `common/entity/`（5 + ai 8 + navigation 2 + projectile 3） |
| 方块与方块实体 | `common/blocks/`（5）、`common/blockentity/flower/`（7）、`common/blockentity/machine/FlowerCakeBlockEntity.java` |
| 能力 | `common/capability/DamageClampCapability.java`（玩家护甲前原始伤害，供 `event/DamageClampHandler` 使用） |
| GUI | `common/gui/`（7） |
| 仪式 | `common/ritual/`（`MachineRitualStoneHost` 把 `RitualMechanicalMachine` 伪装成 Blood Magic `IMasterRitualStone`；`MachineRitualSoulNetwork`）、`common/ritualtypes/`（6） |
| 虚境入侵 | `common/event/zenith/`（5）；数据落 `data/ManaData` |
| 配方 builder | `data/recipe/builder/{botania, bloodmagic, apotheosis}/`（见 data 域文档） |

## CONVENTIONS
- 魔力存储归 trait：`ManaHatch` 与 `FlowerCakeMachine` 各自持有 `BTManaContainerTrait`（`implements ManaReceiver`），`MysticSpire` 持有 `MysticSpireManaTrait`（BigInteger 真实魔力）。`FlowerCakeMachine` 用 `attachPersistentTrait("mana", new BTManaContainerTrait(this, 1_000_000))`。`FlowerCakeBlockEntity` 只是 `MetaMachineBlockEntity + GeoBlockEntity` 渲染外壳。
- `ManaMultiBlockMachine` 自身不持有 `BTManaContainerTrait`；魔力经 `common/parts` 的仓室存取，`InfusionCellCastingCondition` 从机器取 `hatch` 判定。
- Blood Magic / Botania 配方 JSON 生成统一包在 `data/recipe/builder/` 的 builder 类里，`common/` 下没有 `recipe` 子包。
- 加载完成钩子：`CommonProxy.onFMLoadComplete()` 用 `BloodMagicAPI.INSTANCE.registerAltarComponent(CMBlocks.CASING_BLOODLOGIC.getDefaultState(), "CRYSTAL")`。
- GT/GMT 配方是运行时动态包数据（`CTNHManaGTAddon.addRecipes()`），`runData` 对其不产出 JSON。物品/方块/流体引用必须用 `CMItems.X`/`CMBlocks.X` 等静态对象，不得字符串查找。
- 多方块定义（图案、中文名、tooltip、配方类型接线）写在 `registry/multiblock/*`，`common/multiblock/` 只放实现。
- 跨配方并行的预算与升级分工：`CrossParallelManaMultiBlockMachine` 在每个配方的第一个 `recipeModifier` 里按「并行帽 − 已并入并行」「输入容量 − 已占用 EU/t」「材料/输出」三者取剩余额度，只做结构性 IO/EU 缩放；增益与超频延后到 `modifyRecipeAfterMerge` 统一按批次总并行计算。`ManaMachineUpgradeItem.calculateBatchUpgrade(...)` 是非流水线视野的批次定型入口，副作用（如 BT 魔力）每批次只触发一次；流水线视野在 `gtModifyRecipeAfterMerge` 内按 `GTUpgradeItemT2` 分支直接计算速度与 EU 减成，不调用升级件的 `calculateUpgrade`。`GTUpgradeItemT2` 把流水线总并行上限抬到 1024，其余升级（含无升级）为 512。

## ANTI-PATTERNS
- 在 BlockEntity 上重新引入魔力字段，或复制 trait 已持有的状态。
- 让 `ManaMultiBlockMachine` 自己持有魔力容器，绕过 `common/parts` 的仓室。
- 改动魔法集成面时只改 `common/`，不同步配方 builder、mixin、集成与客户端包。
- 把多方块图案/名称定义塞进 `common/multiblock/`（应在 `registry/multiblock/`）。
- 在 `common/` 内直接用字符串 ID 反查注册对象，而非 `CMItems.*` / `CMBlocks.*`。

## SCOPE
适用于 `src/main/java/com/magicbee/ctnhmana/common` 及其子包。

## READ WHEN
- 实现或修改多方块、机器、仓室、总线、仪式。
- 改动魔法物品、实体、AI、方块或方块实体。
- 改动机器 GUI 或魔力状态显示。
- 接入新的虚境入侵服务端流程。

## SOURCE OF TRUTH
- `common/` 各类与 `common/CommonProxy.java` 的注册编排。
- trait 定义：`api/machine/trait/BTManaContainerTrait.java`、`api/machine/trait/MysticSpireManaTrait.java`。
- 机器/trait/capability/Jade 的跨模块契约：`references/_architecture/AGENTS.md`。

## WORKFLOW
1. 先确认改动属于 `common/` 还是 `registry/`（定义在 registry，实现在 common）。
2. 涉及 trait 时同步检查 `attachTrait` / `attachPersistentTrait` 调用点与 Jade 显示路径。
3. 跑 `:modules:CTNH-Mana:build`；涉及注册数据时跑 `:modules:CTNH-Mana:runData`。