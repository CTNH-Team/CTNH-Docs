# CTPP COMMON DOMAIN

## OVERVIEW
CTPP 的共享实现（71 个 Java 文件）：`CommonProxy`、方块与方块实体、动能机器逻辑、风扇处理、工具箱系统、可放置发射器/反射镜/光束，以及接线柱线缆危害。

## STRUCTURE
```text
common/
|-- CommonProxy.java
|-- beam/                      # BeamChunkIndex, EmitterBeam, EmitterBeamTracker, IBeamRedirector
|-- block/                     # CTPPToolboxBlock, GeneratorCoilBlock, KineticMachineBlock, MagnetBlock（强度查询工具类）,
|                              MagnetPlacementHelper, MirrorBlock, VoltageTerminalBlock
|-- blockentity/               # CTPPToolboxBlockEntity, GeneratorCoilBlockEntity, IKineticBlockEntityExtension,
|                              KineticMachineBlockEntity, VoltageTerminalBlockEntity
|-- command/                   # CTPPTerminalCommands（/ctpp wire_damage_debug）、CTPPToolboxCommands
|-- condition/                 # MechanicalTierCondition（用 GTValues.VNF）、RPMCondition
|-- data/                      # GTArmInteractionPointTypes；model/CTPPMachineModels
|-- gui/widget/                # EmitterAngleDialWidget
|-- item/                      # CTPPToolboxItem, GTHammerItem, GTWireCutterItem；debug/ContraptionDebugToolItem
|-- kinetic/fan/
|   |-- acidwashing/           # AcidWashingProcessingType, AcidwashingRecipe
|   |-- breathing/             # BreathingFanProcessingType, BreathingRecipe
|   `-- oiling/                # OilingRecipe
|-- machine/                   # IKineticMachine, NotifiableStressTrait, SimpleKineticElectricWorkableMachine
|   |-- multiblock/            # BigDamMachine, ComplexRotatingMachine, KineticGeneratorMachine, KineticMultiblockMachine,
|   |                          # KineticOutputMachine, KineticTurbineMachine, KineticWorkableMultiblockMachine,
|   |                          # 以及定义在 KineticMultiblockMachine.java 内的 KineticRecipeLogic
|   |   |-- part/              # KineticPartMachine, MechanicalUpgradePartMachine
|   |   `-- windmillController/ # WindMillControlMachine, WindmillManager, WindmillSavedData
|   `-- simple/                # CarbonBrushesGeneratorMachine, ElectricGearBoxMachine, PlaceableEmitterMachine
|-- menu/                      # CTPPToolboxHostSlot, CTPPToolboxMenu, CTPPToolboxSlot
|-- terminal/                  # TerminalNetwork, TerminalWireDamageDebug, TerminalWireHazardManager, TerminalWirePayment
`-- toolbox/                   # 13: CTPPToolboxBinding(s), CTPPToolboxBlockRegistry, CTPPToolboxEvents, CTPPToolboxInventory,
                               CTPPToolboxItemCapability, CTPPToolboxOperations, CTPPToolboxSavedData, CTPPToolboxService,
                               CTPPToolboxSnapshot, CTPPToolboxSounds, CTPPToolboxSourceId, CTPPToolboxStackData
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| 公共代理与初始化顺序 | `common/CommonProxy.java` |
| 动能机器基类与 trait | `common/machine/IKineticMachine.java`, `common/machine/NotifiableStressTrait.java`, `common/machine/SimpleKineticElectricWorkableMachine.java` |
| 动能多方块 | `common/machine/multiblock/`（同速判定、应力输出、涡轮、风力控制等） |
| 应力发电等级惩罚 | `common/machine/multiblock/KineticGeneratorMachine.java`（`maxKineticInputTier`、`getTierPenalty()`、显示行 `info4`） |
| 风扇处理配方类 | `common/kinetic/fan/{acidwashing,breathing,oiling}/`（类型注册在 `data/recipe/fanprocessing/`） |
| 工具箱系统 | `common/toolbox/`（13 个类；操作入口 `CTPPToolboxOperations`） |
| 工具箱菜单 | `common/menu/` |
| 机器模型 | `common/data/model/CTPPMachineModels.java` |
| Create 手臂交互点 | `common/data/GTArmInteractionPointTypes.java`（在 `CommonProxy.commonSetup()` 注册） |
| 配方条件实现 | `common/condition/{RPMCondition, MechanicalTierCondition}.java` |
| 接线柱方块/实体 | `common/block/VoltageTerminalBlock.java`, `common/blockentity/VoltageTerminalBlockEntity.java`, `common/terminal/` |
| 反射镜与光束 | `common/block/MirrorBlock.java`, `common/beam/{EmitterBeam, IBeamRedirector}.java` |
| 可放置发射器 | `common/machine/simple/PlaceableEmitterMachine.java`（托管字段 `zenith` / `azimuth` / `transferDisabled` / `consumptionAmps`） |
| 线缆危害与支付 | `common/terminal/TerminalWireHazardManager.java`, `common/terminal/TerminalWirePayment.java`, `api/terminal/TerminalWireGeometry.java` |
| 线缆调试 | `common/terminal/TerminalWireDamageDebug.java`, `common/command/CTPPTerminalCommands.java`（`/ctpp wire_damage_debug on/off`） |

## CONVENTIONS
- `CommonProxy` 构造顺序：`init()` → `CTPPNetwork.init()` → `MainConfig.init()` → 注册自身到 mod 事件总线；`init()` 内依次做创造栏、菜单、Registrate、datagen、风扇 DeferredRegister、机器/配方条件/配方类型泛型监听。
- `CommonProxy.commonSetup()` 注册 Create 手臂交互点类型 `ctpp:gt_machine`，并为所有 `VOLTAGE_TERMINALS` 注册自定义旋转行为。
- `CTPPGTAddon.initializeAddon()` 初始化方块/BE/方块映射并注册放置助手；`registerRecipeCapabilities()` 调 `CTPPRecipeCapabilities.init()`；`registerMultiblockPreviewHighlighters()` 注册三个 part 能力的高亮色；`addRecipes()` 调 `CTPPRecipes.init(provider)`。
- 配方 builder 在顶层 `data/recipe/`，不在 `common/` 下；风扇处理类型在 `data/recipe/fanprocessing/`。
- `CTPPToolboxItem.initCapabilities()` 提供 `CTPPToolboxItemCapability`；工具箱的装备/卸下/补充/存放全部经 `CTPPToolboxOperations`。
- `TerminalNetwork.handleUse()` 经 `TerminalWirePayment.prepare(...)` 生成全有或全无的细线抽取计划，不直接扣物品栏。
- 动能多方块要求所有输入仓同速：`KineticWorkableMultiblockMachine.checkInputSpeedConsistent()`（容差 0.01）设置 `speedConsistent`，未通过时 `onWorking()` 失败并显示 `sameSpeedRequired`。
- `RPMCondition` 对 `IKineticMachine` 用 `getKineticHolder().getSpeed()`、对 `KineticWorkableMultiblockMachine` 用 `Math.abs(controller.speed)` 与要求转速比较。
- `KineticGeneratorMachine`：`onStructureFormed()` 从 `KineticPartMachine`（`IO.IN`）取最大等级存入 `maxKineticInputTier`，`getTierPenalty() = (maxKineticInputTier - MV) * 0.1` 且仅在 `>= HV` 时生效；效率下限 10%（`Math.max(Math.min(base, 0.1), base - penalty)`）；`onStructureInvalid()` 重置等级与磁场强度；输出上限 `tier > 0 ? tier*4*V[tier] : 32`，显示行 `info0`–`info4`。
- `PlaceableEmitterMachine` 的 `zenith` / `azimuth` / `transferDisabled` / `consumptionAmps` 是托管字段，依赖 LDLib 的 ref 更新完成同步与脏标记；`adjustAngle()` / `setAngles()` 等 setter 内不要手动 `markDirty()`。
- `VoltageTerminalBlockEntity` 在 `addLink()` 与首次 `serverTick()`（`terminalWiresRegistered` 守卫）时把链路注册进 `TerminalWireHazardManager`，移除时反注册。
- `OilingRecipe.matches()` 当前恒返回 `false`（1/12 槽位照常声明），涂油处理尚未接通。

## TRAIT / CAPABILITY LAYERING
动能应力的分层落点（约束以 `references/_architecture/AGENTS.md` §4 为准）：

| 层 | 实现 |
|----|------|
| Recipe capability | `api/StressRecipeCapability`（`"su"`, Float），并行上限经 `getMaxParallelByInput`；`CTPPRecipeCapabilities.SU` 是其别名 |
| Machine trait | `NotifiableStressTrait extends NotifiableRecipeHandlerTrait<Float> implements ICapabilityTrait`，持有应力 I/O 状态 |
| RecipeLogic | `KineticRecipeLogic`（定义在 `KineticMultiblockMachine.java` 内） |
| Machine 子类 | 只放动能机器特有规则（RPM/tier 判定、结构约束） |

- 应力 I/O 不要用裸 JSON 键拼；`StressRecipeCapability` 与 `CTPPRecipeBuilder`（`.inputStress()` / `.outputStress()`）配套使用。
- 并行计算属 recipe capability 与 `CTPPParallelLogic`，不要在机器子类里重算。
- 机器字段与 trait 字段禁止并存形成双重所有权。

## ANTI-PATTERNS
- 改动能/电动机器等级时只改注册代码，不核对生成的模型与配方。
- 绕过 `TerminalWirePayment` 直接扣线材；必须走计划以保证原子性。
- 在 `PlaceableEmitterMachine` 的角度/功耗 setter 里手动 `markDirty()`。
- 在 `VoltageTerminalRenderer` 或 `TerminalWireHazardManager` 中重复 `TerminalWireGeometry` 的数学。
- 在 `common/` 内用物品/方块 ID 字符串反查注册对象，而非 `CTPPBlocks.*` / `CTPPItems.*` 等静态对象。

## SCOPE
适用于 `src/main/java/com/mo_guang/ctpp/common` 及其子包。

## READ WHEN
- 在 CTPP 中实现动能机器、风扇处理、工具箱系统或 `CommonProxy` 接线。
- 修改接线柱、线缆危害、反射镜/光束或可放置发射器逻辑。

## SOURCE OF TRUTH
- `common/CommonProxy.java` 与 `CTPPGTAddon.java` 的挂钩顺序。
- `common/terminal/TerminalWirePayment.java` 与 `common/terminal/TerminalNetwork.java`。
- `common/machine/multiblock/KineticGeneratorMachine.java` 的等级惩罚与效率。
- `common/machine/simple/PlaceableEmitterMachine.java` 的托管字段。

## WORKFLOW
1. 加行为前先核对 `CommonProxy` 的初始化顺序。
2. 涉及应力 I/O 时确认 recipe capability 注册与 builder 用法。
3. 跑 `:modules:CTPP:build`；涉及机器行为在游戏内验证。
