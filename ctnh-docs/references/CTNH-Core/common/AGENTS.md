# CTNH-CORE COMMON DOMAIN

## OVERVIEW
Core 的（客户端 + 服务端）共享实现：CommonProxy、方块、方块实体、capability、附魔、实体、GUI、物品、机器、配方与世界处理。这是最大的域（124 个 Java 文件），以多方块机器层级为主。

## STRUCTURE
```text
common/
|-- CommonProxy.java              # 注册中枢
|-- block/                        # CoilType, CTNHFusionCasingType, MaterialTurbineRotorBlock, PhotovoltaicBlock, SpaceStructuralFramework, TurbineRotorBlock
|   `-- blockdata/                # IPBData, ISSFData, PlanetMinerData（方块数据附加）
|-- blockentity/                  # TurbineRotorBE
|-- capability/                   # EIOCapacitorProvider（EIO 电容 capability 与命名空间/remap 辅助）
|-- enchantment/                  # TemperatureEnchantment
|-- entity/monster/               # astralslime/AstralSlime, sightseerspitter/SightSeerSpitter
|-- gui/                          # WPAAcceleratorGui, MachineModeFancyConfiguratorTest, SimpleNumberInputWidget
|   |-- terminal/                 # TerminalInputWidget
|   `-- widget/                   # SimpleNumberInputWidget
|-- item/                         # ArkOfHomoItem, AstronomyCircuitItem, MEAdvancedTerminalItem/Behavior, SnowCitySwordItem, ThrowableSummoner, TurbineRotorItem, MaterialTurbineRotorItem, ConnectTerminalItem, ProgramItem, MultiblockHelper, SingleItemHandler, TagPrefixBehavior, CatalystBehavior, IThrowableItem, IDroneItem, IDataItem, TestingTerminalBehavior
|   `-- debug/                    # ReloadItem
|-- machine/
|   |-- cover/                    # CreativeEnergyCover
|   |-- multiblock/               # KineticElectricMultiblockMachine, LargeBottleMachine（MultiblockFluidRendererTrait）, MultiblockComputationMachine（attachTrait NetworkedComputationContainer）, SlaughterHouseMachine/FactoryMachine（attachTrait storage）, UnderfloorHeatingMachine
|   |   |-- electric/             # 29 个顶层机器（含 multithread/ 与 rareearth/ 共 34 个 Java 文件）: WideParticleAccelerator, NeutronActivatorMachine, PlanetMiner, LargeDigitalMinerMachine, BlazeBlastFurnaceMachine（CoilMachineTrait）, FermentingTankMachine（CoilMachineTrait）...
|   |   |   |-- multithread/      # CNCAlloySmelter
|   |   |   `-- rareearth/        # ProcessControlMachine, ProcessControlProfile, ProcessControlledCoilMultiblockMachine, ProcessControlledElectricMultiblockMachine
|   |   |-- generator/            # 12 台：Arc_Generator, Arc_Reactor, ChemicalGeneratorMachine, HyperPlasmaTurbineMachine, LargeNaquadahReactorMachine, MegaTurbineMachine, NanoscaleTriboelectricGenerator, NaqReactorMachine, PhotoVoltaicDroneStation, PhotovoltaicPowerStationMachine, WaterPowerStationMachine, WindPowerArrayMachine
|   |   |-- kinetic/              # 5 台：IndustrialPrimitiveBlastFurnaceMachine, KineticCentrifugeMachine, KineticMixerMachine, MeadowMachine, NoEnergyMachine
|   |   |-- part/                 # 12 个部件：CTNHPartAbility, CatalystHatchPartMachine, CircuitBusPartMachine, CompilerMachine, CreativeEnergyHatchPartMachine, CreativeInputBusPartMachine, CreativeInputHatchPartMachine, CreativeLaserHatchPartMachine, DroneHolderMachine, HighSpeedPipeBlock, NeutronAcceleratorMachine, NeutronSensorMachine
|   |   `-- quantum/              # quantum_core
|   |-- simple/                   # DigitalMiner, EfficiencyGeneratorMachine, HighPerformanceComputerMachine, SimpleComputationMachine
|   `-- trait/                    # ScalableReservoirComputingLogic, SimpleComputationContainer
|       `-- providable_net/       # ProvidableNetInfo, ProvidableNetTrait, ProviderInfo
|-- recipe/                       # KeepIngredientShapedRecipe, NeutronActivatorCondition, PlantCasingCondition, TierCasingCondition
|   `-- builder/                  # CTNHRecipeBuilder
`-- world/                        # CTNHChunkLoading
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Common 代理 | `common/CommonProxy.java` |
| 方块/方块数据 | `common/block/`, `common/block/blockdata/` |
| 方块实体 | `common/blockentity/` |
| Capability | `common/capability/EIOCapacitorProvider.java` |
| 附魔 | `common/enchantment/TemperatureEnchantment.java` |
| 实体 | `common/entity/monster/` |
| GUI | `common/gui/`, `common/gui/terminal/`, `common/gui/widget/` |
| 物品 | `common/item/`, `common/item/debug/` |
| 电力多方块 | `common/machine/multiblock/electric/`（29 个顶层 + multithread + rareearth）—— 线圈走 `CoilMachineTrait` |
| 发电机多方块 | `common/machine/multiblock/generator/`（12） |
| 动力多方块 | `common/machine/multiblock/kinetic/`（5） |
| 机器部件 | `common/machine/multiblock/part/`（12） |
| 单方块机器 | `common/machine/simple/`（4） |
| 机器 trait | `common/machine/trait/`, `common/machine/trait/providable_net/` |
| 算力机器 | `common/machine/multiblock/MultiblockComputationMachine.java`（`attachTrait(new NetworkedComputationContainer(...))`） |
| 流体瓶机器 | `common/machine/multiblock/LargeBottleMachine.java`（`attachTrait(new MultiblockFluidRendererTrait(this, this::saveOffsets))`，`saveOffsets()` 返回 `Set<BlockPos>`） |
| 存储 trait | `common/machine/multiblock/SlaughterHouseMachine.java`, `electric/FactoryMachine.java`（`attachTrait(createMachineStorage(...))`，订阅经 `getRecipeLogic().getTraitSubscriptions()`） |
| 配方构建器 | `common/recipe/`, `common/recipe/builder/` |
| 世界 | `common/world/CTNHChunkLoading.java` |

## CONVENTIONS
- `CommonProxy.java` 注册 config、registrate、配方条件、机器、配方类型、datagen、创造栏，以及客户端/服务端 setup 监听器。
- 机器实现放在本域；其 registrate 条目在 `registry/machines/` 与 `registry/CTNHMachines.java`。
- 电力多方块遵循 `*Machine` 命名；`WPA_old.java` 整文件注释、不提供可用实现，勿作为模板；部件实现 `CTNHPartAbility`。
- electric 下的 `rareearth/` 子包是过程控制机器抽象与其 profile，属于电力多方块层级的一部分。
- GT/GMT 配方属运行时动态数据包（`*GTAddon.addRecipes()` → `GTDynamicPackContents` / CTNH-Lib `CTNHDynamicDataPack`），`runData` 对其不产出 JSON。
- 引用物品/方块/流体**必须**使用静态注册对象，**禁止** `ResourceLocation` 字符串解析 + `ForgeRegistries` 查找，除非该对象不存在。
- Trait 所有权：`NetworkedComputationContainer`、`NotifiableItemStackHandler`、`MultiblockFluidRendererTrait`、`CoilMachineTrait` 都在构造阶段经 `attachTrait()` 挂载，同一份状态不得再复制成机器字段。`BlazeBlastFurnaceMachine`/`FermentingTankMachine` 经 `getTraitOrThrow(CoilMachineTrait.class)` 查询线圈。
- 机器中文名在注册处声明（`.cnLangValue(...)` / 工厂 `cnName` 形参），不在 `common/` 里写 `@Key` + `Lang` 字段。见 registry 域文档。

## TRAIT OWNERSHIP
所有权与字段规则以 `references/_architecture/AGENTS.md` 为准（§1 边界、§2 字段、§4 capability 分层）。Core 侧落点：

- `common/machine/trait/`：`ScalableReservoirComputingLogic`（`RecipeLogic` 子类）、`SimpleComputationContainer`（`NetworkedComputationContainer` 子类）、`providable_net/`（`ProvidableNetTrait`、`ProvidableNetInfo`、`ProviderInfo`）。
- 机器内联 `RecipeLogic` 子类：`INFFluidDrillLogic`、`VoidMinerRecipeLogic`、`NeutronActivatorLogic`、`DigestingTankLogic`、`ProcessControlRecipeLogic`。
- 部件侧 `Notifiable*` 子类：`CircuitItemHandler`、`InfinityEnergyContainer`、`InfinityItemStackHandler`、`InfinityFluidTank`、`DroneHolderHandler`。
- trait 单一所有者：`MultiblockComputationMachine.computationContainer`、`SlaughterHouseMachine.machineStorage`、`FactoryMachine.machineStorage`、`NanoscaleTriboelectricGenerator.machineStorage`、`LargeBottleMachine` 流体偏移、`BlazeBlastFurnaceMachine`/`FermentingTankMachine` 线圈。

硬约束：

- **一份状态只能有一个所有者。** 机器字段与 trait 字段禁止并存形成双重所有权；改造时先让 trait 成为唯一所有者，再删机器字段与委托方法。
- trait 在构造阶段挂载完毕（`attachTraits` 不支持运行期添加）；父类工厂需要的子类参数用构造时传入的工厂闭包，禁止 `Object... args` 与延迟绑定。
- `@DescSynced` 与 `@Persisted` 各有语义，同用前确认字段确实既需同步又需保存；managed field 装不下的走 `saveCustomPersistedData` / `loadCustomPersistedData`。同一份数据禁止注解与 attach 式持久化并存。
- 新增 trait 不要在机器基类堆类型特判；让 trait 自己实现能力与生命周期。

## ANTI-PATTERNS
- 绕过 `CommonProxy` 的注册顺序；注册表依赖是刻意安排的。
- 在 common 机器类里放仅客户端渲染。
- 把整文件注释的 `WPA_old.java` 当成现行实现。`MachineModeFancyConfiguratorTest` 是 `CryotheumFreezer` 专用的侧栏子页签实现，不要照抄为通用模板（通用模式页签走 GTCEu `MachineModeFancyConfigurator`）。
- 重新引入机器自有的 `@DescSynced fluidBlockOffsets` 或 `ICoilMachine`；应使用 `MultiblockFluidRendererTrait` 与 `CoilMachineTrait`。
- 在本域给方块/机器补 `@Key("block.ctnhcore.*")` + `Lang` 字段伪造翻译（正确写法见 registry 域文档）。

## SCOPE
适用于 `src/main/java/io/github/cpearl0/ctnhcore/common` 及其子包。

## READ WHEN
- 在 Core 中实现方块、机器、物品、capability 或实体。
- 改动 CommonProxy 注册或 Forge 事件接线。

## SOURCE OF TRUTH
- `common/CommonProxy.java`（注册）、`registry/`（条目）、`event/ForgeEventHandler.java`（运行时钩子）。

## WORKFLOW
1. 先确认行为属于 Core 而非某个 feature 模块。
2. 检查 `CommonProxy` 注册与引用该内容的 GT addon 钩子。
3. 跑最窄的 Gradle 任务；datagen 输入变化时重新生成数据。
