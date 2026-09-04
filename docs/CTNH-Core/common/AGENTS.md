# CTNH-CORE COMMON DOMAIN

## OVERVIEW
Shared (client+server) implementation for Core: CommonProxy, blocks, block entities, capabilities, enchantments, entities, GUIs, items, machines, recipes, and world handling. This is the largest domain (125 Java files), dominated by the multiblock machine hierarchy.

## STRUCTURE
```text
common/
|-- CommonProxy.java              # registration hub
|-- block/                        # CoilType, PhotovoltaicBlock, TurbineRotorBlock, CTNHFusionCasingType, SpaceStructuralFramework, MaterialTurbineRotorBlock
|   `-- blockdata/                # IPBData, ISSFData, PlanetMinerData (block data attachments)
|-- blockentity/                  # TurbineRotorBE
|-- capability/                   # EIOCapacitorProvider (EIO capacitor capabilities, namespace/remap helpers)
|-- enchantment/                  # TemperatureEnchantment
|-- entity/monster/               # astralslime/AstralSlime, sightseerspitter/SightSeerSpitter
|-- gui/                          # WPAAcceleratorGui, MachineModeFancyConfiguratorTest (legacy leftover), SimpleNumberInputWidget
|   |-- terminal/                 # TerminalInputWidget
|   `-- widget/                   # SimpleNumberInputWidget
|-- item/                         # ArkOfHomoItem, AstronomyCircuitItem, MEAdvancedTerminalItem, SnowCitySwordItem, ThrowableSummoner, TurbineRotorItem, ConnectTerminalItem, ProgramItem, MultiblockHelper, SingleItemHandler, TagPrefixBehavior, CatalystBehavior, IThrowableItem, IDroneItem, IDataItem, MaterialTurbineRotorItem, TestingTerminalBehavior
|   `-- debug/                    # ReloadItem
|-- machine/
|   |-- cover/                    # CreativeEnergyCover
|   |-- multiblock/               # KineticElectricMultiblockMachine, LargeBottleMachine, MultiblockComputationMachine, SlaughterHouseMachine, UnderfloorHeatingMachine
|   |   |-- electric/             # 29 top-level machines (34 incl. multithread/ and rareearth/): WideParticleAccelerator, NeutronActivatorMachine, PlanetMiner, LargeDigitalMinerMachine, VoidMinerProcessingMachine (+VoidMinerRecipeLogic), INFFluidDrillMachine (+INFFluidDrillLogic), MegaLCRMachine, NeuroMatrixCompiler, ScalableReservoirComputingMachine, Superconducting_Penning_Trap, ...
|   |   |   |-- multithread/      # CNCAlloySmelter
|   |   |   `-- rareearth/        # ProcessControlMachine, ProcessControlProfile, ProcessControlledCoilMultiblockMachine, ProcessControlledElectricMultiblockMachine
|   |   |-- generator/            # 12 machines: Arc_Generator, Arc_Reactor, ChemicalGeneratorMachine, HyperPlasmaTurbineMachine, LargeNaquadahReactorMachine, MegaTurbineMachine, NanoscaleTriboelectricGenerator, NaqReactorMachine, PhotoVoltaicDroneStation, PhotovoltaicPowerStationMachine, WaterPowerStationMachine, WindPowerArrayMachine
|   |   |-- kinetic/              # 5: IndustrialPrimitiveBlastFurnaceMachine, KineticCentrifugeMachine, KineticMixerMachine, MeadowMachine, NoEnergyMachine
|   |   |-- part/                 # 12 parts: CTNHPartAbility, CatalystHatchPartMachine, CircuitBusPartMachine, CompilerMachine, CreativeEnergyHatchPartMachine, CreativeInputBusPartMachine, CreativeInputHatchPartMachine, CreativeLaserHatchPartMachine, DroneHolderMachine, HighSpeedPipeBlock, NeutronAcceleratorMachine, NeutronSensorMachine
|   |   `-- quantum/              # quantum_core
|   |-- simple/                   # DigitalMiner, EfficiencyGeneratorMachine, HighPerformanceComputerMachine, SimpleComputationMachine
|   `-- trait/                    # ScalableReservoirComputingLogic, SimpleComputationContainer
|       `-- providable_net/       # IProviableNetHandlerMachine, ProvidableNetHandler, ProvidableNetInfo, ProviderInfo
|-- recipe/                       # KeepIngredientShapedRecipe, NeutronActivatorCondition, PlantCasingCondition, TierCasingCondition
|   `-- builder/                  # CTNHRecipeBuilder
`-- world/                        # CTNHChunkLoading
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Common proxy | `common/CommonProxy.java` |
| Blocks/block data | `common/block/`, `common/block/blockdata/` |
| Block entities | `common/blockentity/` |
| Capabilities | `common/capability/` |
| Enchantments | `common/enchantment/` |
| Entities | `common/entity/monster/` |
| GUIs | `common/gui/`, `common/gui/terminal/`, `common/gui/widget/` |
| Items | `common/item/`, `common/item/debug/` |
| Electric multiblocks | `common/machine/multiblock/electric/` (29 + multithread + rareearth) |
| Generator multiblocks | `common/machine/multiblock/generator/` (12) |
| Kinetic multiblocks | `common/machine/multiblock/kinetic/` (5) |
| Machine parts | `common/machine/multiblock/part/` (12) |
| Simple machines | `common/machine/simple/` (4) |
| Machine traits | `common/machine/trait/`, `common/machine/trait/providable_net/` |
| Recipe builders | `common/recipe/`, `common/recipe/builder/` |
| World | `common/world/CTNHChunkLoading.java` |

## CONVENTIONS
- `CommonProxy.java` registers config, registrate, recipe conditions, machines, recipe types, datagen, creative tabs, and client/server setup listeners.
- Machine implementations live here; their registrate entries live in `registry/machines/` and `registry/CTNHMachines.java`.
- Electric multiblocks follow `*Machine` naming (some legacy files use `*_old` or snake_case); parts implement `CTNHPartAbility`.
- The `rareearth/` subpackage under electric machines contains process-control machine abstractions and their profiles; treat it as part of the electric multiblock hierarchy.

## TRAIT OWNERSHIP
所有权与字段规则以 `docs/_architecture/AGENTS.md` 为准（§1 边界、§2 字段、§4 capability 分层）。Core 侧落点：

- `common/machine/trait/`：`ScalableReservoirComputingLogic`（`RecipeLogic` 子类）、`SimpleComputationContainer`（`NetworkedComputationContainer` 子类）、`providable_net/`（`ProvidableNetHandler`、`ProvidableNetInfo`、`ProviderInfo`、`IProviableNetHandlerMachine`）。
- 机器内联 `RecipeLogic` 子类：`INFFluidDrillLogic`、`VoidMinerRecipeLogic`、`NeutronActivatorLogic`、`DigestingTankLogic`、`ProcessControlRecipeLogic`。
- 部件侧 `Notifiable*` 子类：`CircuitItemHandler`、`InfinityEnergyContainer`、`InfinityItemStackHandler`、`InfinityFluidTank`、`DroneHolderHandler`。

硬约束：

- **一份状态只能有一个所有者。** 机器字段与 trait 字段禁止并存形成双重所有权；迁移时先让 trait 成为唯一所有者，再删机器字段与委托方法。
- trait 在构造阶段挂载完毕（`attachTraits` 不支持运行期添加）；父类工厂需要的子类参数用构造时传入的工厂闭包，禁止 `Object... args` 与延迟绑定。
- `@DescSynced` 与 `@Persisted` 各有语义，同用前确认字段确实既需同步又需保存；managed field 装不下的走 `saveCustomPersistedData` / `loadCustomPersistedData`。同一份数据禁止注解与 attach 式持久化并存。
- 新增 trait 不要在机器基类堆类型特判；让 trait 自己实现能力与生命周期。


## ANTI-PATTERNS
- Do not bypass `CommonProxy` registration order; registry dependencies are deliberate.
- Do not put client-only rendering in common machine classes.
- Do not treat `WPA_old.java` or `MachineModeFancyConfiguratorTest` as current implementation; both are legacy leftovers.

## SCOPE
Applies to `src/main/java/io/github/cpearl0/ctnhcore/common` and its child packages.

## READ WHEN
- Implementing blocks, machines, items, capabilities, or entities in Core.
- Changing CommonProxy registration or Forge event wiring.

## SOURCE OF TRUTH
- `common/CommonProxy.java` (registration), `registry/` (entries), `event/ForgeEventHandler.java` (runtime hooks).

## WORKFLOW
1. Confirm the behavior belongs in Core rather than a feature module.
2. Check `CommonProxy` registration and any GT addon hooks that reference the new content.
3. Run the narrowest Gradle task; regenerate data when datagen inputs changed.
