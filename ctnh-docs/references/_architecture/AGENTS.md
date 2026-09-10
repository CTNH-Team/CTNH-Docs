# CTNH ARCHITECTURE CONTRACT — Machine / Trait / Capability / Jade

## OVERVIEW
本文件是 CTNH 机器架构的**规范锚点**：机器与 trait 的所有权边界、字段同步与持久化规则、recipe capability 分层、Jade 数据最小化原则，以及把既有模块迁移到该架构的步骤。

来源是 GTCEu/CTNH 的 Trait/Jade 重构。**旧的 GTM2 结构只作设计参考，不是迁移目标**；现行对齐对象是 vendored 上游工作树 `CTNH-Modules/modules/GregTech-Modern`（核实时 HEAD `b00a3a43`）。该重构已在上游落地，CTNH 侧按本文件的所有权边界消费它，不要另起一套。

规范条款（边界、字段规则、Jade 最小化、迁移步骤）**立即生效**，适用于所有新代码与所有被触及的旧代码。§9 记录每条机制当前落在哪个类、由哪个提交引入。

本文件不由 `CTNH-Docs` 的自动同步流程生成：CI 的 `scripts/verify_docs.py` 把写入范围限定在 `ctnh-docs/references/<Module>/**/AGENTS.md`，本文件（`_architecture/`）在其白名单之外，出现改动即整轮失败，属手工维护的长期契约。

## 1. 总体边界

- `MetaMachine` 与 `MetaMachineBlockEntity` 保持分离。机器负责行为、trait 与 capability；方块实体只负责世界承载和 Forge/Jade 入口。
- trait 是机器内部的**内聚行为单元**。需要同步或持久化的字段放进 trait，由 LowDragLib 的 managed field 系统处理。
- **不为旧调用保留大规模兼容层。** 迁移时改调用方和所有权边界，而不是加转发层。
- **trait 在构造阶段挂载完毕，且由代码强制。** `MetaMachine.attachTrait(...)` 的 javadoc 即 "All traits should be initialized while MetaMachine is creating. you cannot add them on the fly."；`MachineTraitHolder.attach` 在 holder 关闭后抛 `IllegalStateException("Traits must be attached before the machine is loaded")`，而 `MetaMachine.onLoad()` 第一件事就是 `traitHolder.seal()`。父类工厂需要的特殊参数通过**构造参数（工厂闭包）**传入，禁止 `Object... args` 扩散和延迟绑定。
- 类引用使用正常 import。实现代码里禁止硬写完整包名，禁止新增 `rawtypes` / `unchecked` 兼容 helper。

## 2. Trait 生命周期、同步与持久化

`MachineTrait` 是 `abstract class ... implements IEnhancedManaged`（`GregTech-Modern/.../api/machine/trait/MachineTrait.java`），当前实际提供的入口：

| 入口 | 用途 |
|------|------|
| `onMachineLoad()` / `onMachineUnload()` | 机器加载/卸载（**拼写是 `Unload`，小写 l**，不是 `UnLoad`） |
| `onMachineDestroyed()` | 机器被破坏 |
| `onNeighborChanged(Block, BlockPos, boolean isMoving)` | 邻居变化 |
| `onWorkAllowedChanged(boolean isWorkAllowed)` | 工作许可变化 |
| `onChanged()` | managed field 变化回调，默认转发 `machine.onChanged()` |
| `hasCapability(@Nullable Direction side)` | 由 `capabilityValidator` 决定的侧面暴露判定 |
| `updateModelData(ModelData.Builder)` / `getRenderState()` / `setRenderState(MachineRenderState)` / `scheduleRenderUpdate()` | 渲染状态 |
| `writeJadeData(CompoundTag, BlockAccessor)` / `appendJadeTooltip(CompoundTag, ITooltip, BlockAccessor, IPluginConfig)` / `jadePriority()` | trait 自己的 Jade 数据与展示（详见 §8） |
| `saveCustomPersistedData(CompoundTag, boolean forDrop)` / `loadCustomPersistedData(CompoundTag)` | managed field 之外的自定义 NBT |
| `validMachineClasses()` | 声明该 trait 允许挂载的机器类型；非空时 `attach` 会校验，不匹配抛 `IllegalArgumentException` |
| `getTraitPriority()` / `setTraitPriority(int)` | 同类型多 trait 的排序权重，默认 1 |
| `getFieldHolder()` | managed field holder（`final`，不可覆写） |

生命周期由 `MetaMachine` 分发，trait 不要自己去找这些信号：

| 信号 | 驱动位置 |
|------|----------|
| 加载 | `MetaMachine.onLoad()`：`traitHolder.seal()` → `traitHolder.all().forEach(MachineTrait::onMachineLoad)` |
| 卸载 | `MetaMachine.onUnload()`：`...::onMachineUnload`（随后是 `coverContainer` 与 server tick 退订） |
| 破坏 | `MetaMachine.onMachineDestroyed()`：`...::onMachineDestroyed` |
| 邻居变化 | `MetaMachine.onNeighborChanged(Block, BlockPos, boolean)`：先 `traitHolder.all().forEach(trait -> trait.onNeighborChanged(...))`，再 `coverContainer` |
| 工作许可变化 | **不在 `MetaMachine` 上**：`WorkLogic.setWorkingEnabled` → `IWorkLogicMachine.notifyWorkingEnabledChanged` → `metaMachine.getAllTraits().forEach(trait -> trait.onWorkAllowedChanged(value))`。只有实现 `IWorkLogicMachine` 的机器会派发这条信号 |

挂载与排序：`attachTrait(trait)` 校验 trait 归属（不能挂到别的机器）、`validMachineClasses()` 并去重，然后按 `getTraitPriority()` **降序**维护 `all()` 与 `byType` 列表；同名/同实例的重复 attach 是幂等的。

字段规则：

- `@DescSynced`：常规客户端状态同步，适用于界面、模型、客户端逻辑需要持续读取的数据。
- `@Persisted`：机器存档持久化。
- 两者可同时使用，但必须确认该字段**确实既需要同步又需要保存**。
- managed field 系统承载不了的数据走 `saveCustomPersistedData` / `loadCustomPersistedData`。
- **同一份数据禁止同时用注解与 attach 式持久化。** 用字段承载的优先注解持久化；不用字段承载的优先 attach 式持久化。两者并存会产生重复协议和所有权不清。

attach 式持久化（当前实现）：`attachPersistentTrait(String name, T trait[, int priority])`（`MetaMachine` → `MachineTraitHolder.attachPersistent`）。

- 持久化 trait 的 `@Persisted` 字段由 `MachineTraitHolder.savePersistentData / loadPersistentData` 统一写到机器 NBT 的 `traits` 子 tag 下，键就是注册的 `name`；`MetaMachine.saveCustomPersistedData / loadCustomPersistedData` 先调 holder，再回调各 trait。
- holder 把 trait 的 sync storage 用 `SyncOnlyStorage` 包一层挂到机器根 storage：只暴露同步字段，`getPersistedFields()` 返回空、`hasDirtyPersistedFields()` 恒 false。这样同一份字段不会被地方持久化两次，也不会泄漏到机器 NBT 根部。
- GameTest `MachineTraitPersistenceTest#autoOutputUsesNamespacedPersistence` 就是这条契约的回归测试：断言 `traits/auto_output` 存在、NBT 里没有 `autoOutputTrait`、`autoOutputItems` 不在机器 NBT 根。
- `name` 用稳定的蛇形键，同一机器内不可重复（重复抛 `Duplicate persistent trait`）。GT 既有键：`auto_output`、`circuit_slot`、`battery_slot`、`exhaust_vent`；CTNH 既有键：`auto_output`（CTNH-Core `DigitalMiner`）、`circuit_slot`（CTNH-Energy `MEPartMachine`）、`extended_circuit_slot`（CTNH-Mana `ExtendedCentralControlBus`）、`mana`（CTNH-Mana `FlowerCakeMachine`）。

## 3. Trait 查找

- 调用方需要某类 trait 时，**按类型查找**：`MetaMachine.getTrait(Class)`、`getTraits(Class)`、`getTraitOrThrow(Class)`、`getTraitOptional(Class)`；按名字取持久化 trait 用 `getPersistentTrait(String)`。不要遍历全部 trait 再 `instanceof`。
- 类型索引已经存在，由 `MachineTraitHolder` 维护：`ClassValue` 缓存每个 trait 类的**父类链与全部接口**（`collectTypes`），`attach` 时逐类型登记到 `byType` 并按 `traitPriority` 降序排序，取出的是 `Collections.unmodifiableList`。
- 因此 `getTrait(SomeInterface.class)` 能取到实现该接口的 trait（例如 `getTraitOptional(IParallelTrait.class)`、`getTrait(CoilMachineTrait.class)`）；同类型有多个时 `first(...)` 返回优先级最高的那个。
- 新增 trait 时不要在机器基类堆类型特判；让 trait 自己实现能力与生命周期，能力差异用 `api/machine/trait/feature/` 下的接口表达（`IInteractionTrait` / `IRenderingTrait` / `IFrontFacingTrait` 由 `MetaMachine` 通过 `getTraits(...)` 分发，`IAttachConfiguratorsTrait` 供 GUI 配置器挂载，`IMultiblockMachineTrait` 供多方块生命周期复用）。
- 上游仍有少量绕开索引的写法（如 `SteamWorkableMachine.onLoad` 遍历 `getTraits()` 找 `IRecipeHandler`），属遗留，不要照抄。

## 4. Capability 分层

四层职责互不越界：

| 层 | 职责 |
|----|------|
| Forge capability | 对外暴露机器的物品、流体、能量访问能力 |
| Recipe capability | 描述配方内容、网络编码、匹配、并行限制与 XEI/EMI 逻辑 |
| Machine trait | 持有具体 handler/container，负责机器侧状态与行为 |
| Machine 子类 | 只负责机器特有规则；禁止把 capability 分发全塞进基类 |

能量容器由 tiered machine 的工厂创建：`TieredEnergyMachine` 构造期 `attachTrait(energyContainerFactory.apply(this))`。子类的特殊容器若需额外参数，用**构造时传入的工厂闭包**，让父类调用 `createEnergyContainer` 时仍能保留子类参数；不要用延迟绑定绕开构造参数问题。

`MetaMachine.getCapability` 的分发也走 trait 索引（`firstCapability` / `firstInterface` → `getTraits(type)`），物品/流体侧再叠加 `AutoOutputTrait` 的输出面判断（见 §5）。

## 5. AutoOutput

自动输出的**唯一所有者是 `AutoOutputTrait`**（`api/machine/trait/AutoOutputTrait.java`，`extends MachineTrait implements IAttachConfiguratorsTrait, IFrontFacingTrait, IInteractionTrait, IRenderingTrait`）：

- 输出方向、是否允许从输出侧输入、自动输出开关、订阅刷新都属于 trait：`autoOutputItems` / `autoOutputFluids`（`@Persisted @DescSynced @RequireRerender`）、`allowInputFromOutputSideItems` / `allowInputFromOutputSideFluids`（`@Persisted`）、`outputFacingItems` / `outputFacingFluids`（`@Persisted @DescSynced @RequireRerender`）、`ticksPerCycle`（默认 5）。
- 创建方式：`AutoOutputTrait.ofItems(machine, IItemHandler...)` / `ofFluids(machine, IFluidHandler...)` / 构造器 `(machine, List<IItemHandler>, List<IFluidHandler>[, useDefaultToolHandlers])`，可用 `setItemOutputValidator` / `setFluidOutputValidator` 限定允许的输出面。CTNH 侧样例：CTNH-Core `common/machine/simple/DigitalMiner` → `AutoOutputTrait.ofItems(this, exportItems)` + `attachPersistentTrait("auto_output", autoOutput)`。
- 读取方式：`hasAutoOutputItem/Fluid`、`isAutoOutputItems/Fluids` + `setAutoOutputItems/Fluids`、`getOutputFacingItems/Fluids` + `setOutputFacingItems/Fluids`、`is/setAllowInputFromOutputSideItems/Fluids`、`get/setTicksPerCycle`。CTNH-Energy `event/ForgeEventHandler` 与 `mixin/ae2/misc/PartPlacementMixin` 即 `machine.getTrait(AutoOutputTrait.class)` 后直接调这些方法。
- 机器不持有 item/fluid 自动输出字段，也不保留委托方法：`isAutoOutputItems` / `setAutoOutputItems` 这类签名在 GTCEu 源码树中只存在于 `AutoOutputTrait` 自身，调用方（`MachineModel`、`AutoOutputItemConfigHandler`、`MachineConfigCopyBehaviour` 等）直接对着 trait 读。
- 机器 UI 与配置器直接绑定 trait 暴露的 API：`AutoOutputItemConfigHandler` / `AutoOutputFluidConfigHandler` 的字段类型就是 `AutoOutputTrait`；`AutoOutputTrait.attachConfigurators` 挂自动输出开关，扳手改输出面、螺丝刀切自动输出/允许输入都由 trait 自己实现 `IInteractionTrait`。
- 邻居变化、加载、配置变化的订阅状态由 trait 管理：`onMachineLoad` 里订阅 `NotifiableItemStackHandler` / `NotifiableFluidTank` 的 changed listener 并在服务端 tick 刷新，`onMachineUnload` 全部退订，`onNeighborChanged` 重新评估相邻 handler（`GTTransferUtils.hasAdjacentItemHandler` / `hasAdjacentFluidHandler`）。
- Jade 信息由 trait 自己写入：`writeJadeData` 写 `item` / `fluid` 子 tag（direction / allowInput / auto / 相邻方块），`jadePriority()` 返回 600，`appendJadeTooltip` 负责渲染；统一机器 provider 只负责触发 trait（见 §8）。
- `MetaMachine.getItemHandlerCap` / `getFluidHandlerCap` 通过 `getTrait(AutoOutputTrait.class)` 判断该侧是否为输出面，从而把 IO 降级为 `IO.OUT`——能力分发读的也是 trait。

迁移顺序固定：**先让 trait 成为唯一所有者 → 再删机器字段与旧委托方法 → 最后清理旧分发接口**。该序列在 vendored 上游已走完：`IAutoOutputItem` / `IAutoOutputFluid` / `IAutoOutputBoth` 随 `AutoOutputTrait` 一并删除，GTCEu 与 CTNH 八个模块全树 0 引用；CTNH 不再需要这三个名字。

残余：vendored 上游的蒸汽机器仍自持输出面字段（`SteamWorkableMachine.outputFacing` + `SteamMachine.setOutputFacing`），不在 `AutoOutputTrait` 内。CTNH 新代码不要复制这种双所有权写法。

## 6. RecipeLogic 与配方输出 Jade

配方输出不使用独立的输出 provider，也不新建专门的输出 trait。`RecipeOutputProvider` 已删除（提交 `0c96d142c`），输出解释回归 `RecipeCapability`。

`RecipeLogic extends WorkLogic`，Jade 分工如下：

| 位置 | 职责 |
|------|------|
| `WorkLogic.writeJadeData` | 状态数据：`active` / `progress` / `maxProgress` / `workingEnabled` / `suspendAfter` / `waitingReason`；`jadePriority()` = 800 |
| `RecipeLogic.appendJadeTooltip` | 先 `super`（进度条、暂停提示），再输出机器模式列表，工作时调 `RecipeJadeTooltip.appendRunningRecipe(this, lastRecipe, ...)`，最后输出 `failureReasonsMap` 的失败原因 |
| `RecipeJadeTooltip.appendRunningRecipe` | 依次遍历 `inputs`(IO.IN) / `tickInputs`(IO.IN, tick) / `outputs`(IO.OUT) / `tickOutputs`(IO.OUT, tick)，再追加并行信息（`gtceu.multiblock.total_runs` / `parallel.exact` / `batch_enabled` / `subtick_parallels`） |
| `RecipeCapability.appendJadeRecipeTooltip` | 各 capability 自己解释内容并加自己的标题 |

- 遍历统一走 `ContentListMap.forEachEntry`，逐 capability 调 `capability.appendJadeRecipeTooltip(io, tick, values, logic, tooltip, accessor, config)`。
- 物品 capability：只在 `io == IO.OUT && !tick` 时输出，标题 `gtceu.top.item_auto_output`，处理范围数量（`RangedItemIngredient` → `gtceu.gui.content.range`）与概率输出（按 `recipe.getTotalRuns()` 与 `chanceFunction` 折算）。流体 capability 对称（`gtceu.top.fluid_auto_output`、范围容量、概率）。EU capability 只在 `tick` 时输出，写 `gtceu.top.energy_consumption` / `gtceu.top.energy_production` 与安培/电压行。
- 新增气体、数据或其他 capability 时只实现自己的 `appendJadeRecipeTooltip`，**`RecipeLogic` 不得增加类型判断**。
- **Jade 中禁止重复序列化 `lastRecipe`**：`RecipeLogic` 不覆写 `writeJadeData`，服务端数据里根本没有 `lastRecipe`；tooltip 用的是客户端已同步的 `@DescSynced lastRecipe` 对象。能耗、并行、模式、失败原因等只要能由客户端状态推导，就不写入 Jade NBT。

## 7. ContentListMap 顺序

- 遍历统一走 `forEachEntry(EntryConsumer)`。**禁止在调用方遍历 `entrySet()`（或 `asMap().entrySet()`）再手动排序。** `keySet()` / `entrySet()` / `asMap()` 仍是 public API，这条规矩靠人守。
- 泛型擦除集中在 `ContentListMap` 内部（`acceptCaptured`），调用方使用泛型化的 `EntryConsumer`，不要新增 raw helper。
- 顺序基准是 `RecipeCapability.COMPARATOR`，当前实现为 `Comparator.<RecipeCapability<?>>comparingInt(o -> o.sortIndex).thenComparing(o -> o.name)`；`sortIndex` 在 `RecipeCapability` 构造时按 `index++` 递增分配，同名（同 sortIndex）时以 capability name 兜底。
- 底层容器是 `new TreeMap<>(RecipeCapability.COMPARATOR)`，**顺序由 comparator 保证**（不再依赖插入序）。仍然要求经 `forEachEntry` 取用，是因为一旦把裸 `Map` 泄进业务代码、或调用方自己排一遍，capability 顺序就会与配方语义脱节。

## 8. Jade 架构

已落地**单一机器入口**：`integration/jade/provider/MachineJadeProvider.java`（uid `gtceu:machine`）是 `MetaMachine` 唯一的 Jade provider。

- 服务端 `appendServerData`：取 `MetaMachineBlockEntity` → `machine.writeJadeData(machineData, accessor)` → 遍历 `machine.getAllTraits()`，每个 trait 写进以 `trait.getClass().getName()` 为键的子 tag，**空 section 不写入**。
- 客户端 `appendTooltip`：先 `machine.appendJadeTooltip(...)`，再按 `MachineTrait::jadePriority` **倒序**遍历 trait 调各自的 `appendJadeTooltip`。
- 机器侧：`MetaMachine.writeJadeData` / `appendJadeTooltip` 是 `final`，转发到可覆写的 `writeMachineJadeData` / `appendMachineJadeTooltip`（默认写 `workingEnabled` / `suspendAfter`（无 `WorkLogic` trait 时）以及维护问题）。机器特有信息写在这里，trait 信息写在自己的 `writeJadeData` / `appendJadeTooltip` 里。
- trait 侧：`MachineTrait.writeJadeData(CompoundTag, BlockAccessor)` / `appendJadeTooltip(...)` / `jadePriority()`（默认 0）。已落地的贡献者与优先级：`WorkLogic` 与 `RecipeLogic` 800、`NotifiableEnergyContainer` 700、`AutoOutputTrait` 600、`ParallelHatchTrait` 600、`ExhaustVentTrait` 600，以及 AE2 集成的 `GridNodeHost`（`MachineTrait` 子类，写 `gridNodeState`）。

`integration/jade/provider/` 现在只有 6 个文件，全部由 `GTJadePlugin` 注册，**没有集中优先级注册器**：

| 文件 | 身份 | 注册方式 |
|------|------|----------|
| `MachineJadeProvider` | MetaMachine 唯一入口，uid `gtceu:machine` | `registerBlockDataProvider` + `registerBlockComponent` |
| `CableBlockProvider` | 线缆方块 | `BlockEntity.class` block data + `Block.class` block component |
| `StainedColorProvider` | 染色信息 | 同上 |
| `GTItemStorageProvider` | 物品存储视图，uid `gtceu:custom_item_storage`（量子箱、样板缓冲代理） | `registerItemStorage` / `registerItemStorageClient` |
| `GTFluidStorageProvider` | 流体存储视图 | `registerFluidStorage` / `registerFluidStorageClient` |
| `FluidPipeStorageProvider` | 流体管道存储视图（`FluidPipeBlockEntity`） | 同上 |

CTNH 侧现状：

- 旧的集中优先级注册器**已删除**：CTNH-Lib `jade/GTProvidersRegistrar` 与 `jade/JadePriorityManager`（连同 `mixin/GTJadePluginMixin`）在提交 `f9951f9`「移除gt jade相关」(2026-09-03) 移除，CTNH-Lib 当前已无 `jade` 包。**不要再引用这两个类，也不要新增同类集中注册器。**
- 仍在注册的 CTNH Jade plugin：CTNH-Energy `integration/jade/CTNHEnergyJadePlugin`（`AEDeviceEUProvider`，`BlockEntity` + `Block`）、CTNH-Mana `integration/jade/CTNHManaJadePlugin`（`ThirdEyeStatusProvider`）、CTPP `integration/jade/CTPPJadePlugin.PlaceableEmitterProvider`（注册在 `MetaMachineBlock.class` 上）。
- 已停用但源码仍在：CTNH-Core `registry/jade/CTNHJadePlugin.init()` 全为注释；CTNH-Core `api/jade/` 的 `MultithreadRecipeLogicProvider` / `MultithreadRecipeOutputProvider` / `ThreadStatusProvider` 三个文件**整文件被注释**（0 行可执行代码），无任何注册；CTNH-Energy `integration/jade/AdMEPatternBufferProvider` / `AdMEPatternBufferProxyProvider` 同样整文件注释且注册行已注释。

无论哪种形态，以下两条恒定生效：

- **只有仍被注册且承担独立功能的 provider 才保留。** 功能迁走后删除旧的机器专用 provider，而不是继续隐藏注册。
- **Jade 服务端数据只保留客户端无法从机器/trait 已同步状态推导出的信息。**

## 9. 目标态 vs 当前实现

旧版本此处的“迁移目标”**已全部在 vendored 上游落地**。下表给出实现位置与引入提交，供引用时核对：

| 原目标态 | 现状 | 证据 |
|----------|------|------|
| trait 类型索引 holder | 已落地 `MachineTraitHolder`（`byType` / `first` / `persistent`，`ClassValue` 类型缓存 + 优先级排序），`MetaMachine.getTrait/getTraits/getTraitOrThrow/getTraitOptional/getPersistentTrait` 经它取用 | `api/machine/trait/MachineTraitHolder.java`；`bc9caae73`「新trait系统初步」、`a0eef66e9`「将cap分发搬到MetaMachine」、`f2d7ea008`「规范化trait attach」 |
| trait 基类新增邻居/工作许可/销毁回调 | 已落地 `onNeighborChanged(Block, BlockPos, boolean)` / `onWorkAllowedChanged(boolean)` / `onMachineDestroyed()`；邻居由 `MetaMachine.onNeighborChanged` 驱动，工作许可由 `IWorkLogicMachine.notifyWorkingEnabledChanged` 驱动 | `api/machine/trait/MachineTrait.java`、`api/machine/MetaMachine.java`、`api/machine/feature/IWorkLogicMachine.java`；`43557a27f`「AutoOutputTrait」 |
| 统一 `AutoOutputTrait`，删除 `IAutoOutputItem` / `IAutoOutputFluid` / `IAutoOutputBoth` | 已落地：三个接口在 GTCEu 全树 0 引用（`git log --all -S` 显示由 `43557a27f` 移除），自动输出状态、工具交互、配置器、Jade 全部归 `AutoOutputTrait` | `api/machine/trait/AutoOutputTrait.java`；`43557a27f`、`3c2bab670`「清理量子箱/缸字段」 |
| 取消独立配方输出 provider，输出解释回归 `RecipeCapability` | 已落地：`RecipeOutputProvider` 在 `0c96d142c`「recipeOutput jadeinfo」(2026-09-02) 删除，`RecipeJadeTooltip` 遍历 `ContentListMap` 调 `RecipeCapability.appendJadeRecipeTooltip` | `integration/jade/RecipeJadeTooltip.java`、`ItemRecipeCapability` / `FluidRecipeCapability` / `EURecipeCapability` |
| attach 式持久化 trait API | 已落地 `attachPersistentTrait(name, trait[, priority])`：`@Persisted` 字段写到机器 NBT 的 `traits/<name>`，`SyncOnlyStorage` 保证不重复持久化 | `MachineTraitHolder.savePersistentData/loadPersistentData`、`MetaMachine.saveCustomPersistedData/loadCustomPersistedData`、GameTest `MachineTraitPersistenceTest` |
| 单一机器 Jade 入口 + trait 侧 `jadePriority()` | 已落地 `MachineJadeProvider`（MetaMachine 唯一 provider）+ 机器/ trait 两组 Jade 回调 + 倒序优先级 | `integration/jade/provider/MachineJadeProvider.java`、`MetaMachine.writeJadeData/appendJadeTooltip`、`MachineTrait.jadePriority`；`d471ebc6a`「重构jade」(2026-09-02) |
| `ContentListMap` 以 comparator 保序、name 兜底 | 已落地：`TreeMap<>(RecipeCapability.COMPARATOR)`，comparator 为 `comparingInt(sortIndex).thenComparing(name)` | `api/recipe/content/ContentListMap.java`、`api/capability/recipe/RecipeCapability.java`；`0c96d142c` |

因此 §3 / §5 / §6 / §7 / §8 描述的都是**现行实现**，不要再当作未来目标态引用。仍未完成的只剩 CTNH 侧收尾与两处已知残余：

| 待办 / 残余 | 现状 | 证据 |
|-------------|------|------|
| 删除 CTNH-Core `api/jade/` 三个死 provider | 整文件注释、无注册，`CTNHJadePlugin.init()` 亦全注释 | `CTNH-Core/.../api/jade/{MultithreadRecipeLogicProvider, MultithreadRecipeOutputProvider, ThreadStatusProvider}.java`、`registry/jade/CTNHJadePlugin.java` |
| 处理 CTNH-Energy 的独立 provider | `AdMEPatternBufferProvider` / `AdMEPatternBufferProxyProvider` 整文件注释且注册行已注释；`AEDeviceEUProvider` 仍由 `CTNHEnergyJadePlugin` 注册在 `BlockEntity` / `Block` 上 | `CTNH-Energy/.../integration/jade/*`、`common/CommonProxy.java` |
| 迁移 CTNH-Mana / CTPP 的机器 Jade 信息 | `ThirdEyeStatusProvider`、`PlaceableEmitterProvider`（注册在 `MetaMachineBlock.class`）仍是独立 block component，未走 trait/机器回调 | `CTNHManaJadePlugin.java`、`CTPPJadePlugin.java` |
| 工作许可回调派发面不全 | `onWorkAllowedChanged` 只由 `IWorkLogicMachine.notifyWorkingEnabledChanged` 触发，非 `WorkLogic` 机器的 trait 收不到该信号 | `api/machine/feature/IWorkLogicMachine.java`（全树仅此一处派发） |
| 蒸汽机器输出面仍由机器自持 | `SteamWorkableMachine.outputFacing` + `SteamMachine.setOutputFacing`，不在 `AutoOutputTrait` 内（vendored 上游残余） | `api/machine/steam/SteamWorkableMachine.java`、`SteamMachine.java` |

## 10. 迁移一个模块的步骤

1. 列出模块现有 machine、block entity、capability、旧 provider 与接口。
2. 为每个状态确定**唯一所有者**：机器、trait，或 recipe capability。
3. 先实现 trait 的字段、生命周期与 capability 暴露，再迁移机器调用方。
4. 把旧 provider 的状态读取改为统一 Jade trait/机器回调。
5. 删除旧机器字段、委托方法、provider 与接口，不留重复兼容层。
6. 检查 `@DescSynced`、`@Persisted` 与自定义 NBT 是否重复。
7. 检查 Jade 是否重复传输客户端已有的数据。
8. 用 `ContentListMap.forEachEntry` 遍历 recipe capability，不直接操作 raw map。
9. 规范 import，执行 `spotlessApply`。
10. 运行模块 `compile`/`build`；有运行时展示变化时再做游戏内或 GameTest 验证。

## 11. ANTI-PATTERNS

- 机械地把旧 provider 代码复制进 trait，导致 trait 仍承担多个不相关职责。
- 机器字段与 trait 字段并存，形成双重所有权。
- Jade 已能从客户端状态读取的信息仍通过 NBT 二次同步。
- 在调用方遍历 `entrySet()` 并手动排序，绕过 `forEachEntry`。
- 使用完整包名，或新增 `rawtypes` / `unchecked` 兼容 helper。
- 用 `Object... args` 或延迟绑定规避构造参数问题。
- 新建 Jade 集中优先级注册器（CTNH-Lib `JadePriorityManager` 已在 `f9951f9` 删除），或继续引用 `GTProvidersRegistrar` / `JadePriorityManager`。
- 把 §9 已落地的 API 继续当作“尚不存在的目标态”描述，或反过来把仍是待办/残余的写法当作既定契约。

## 12. CTNH 侧现有 trait 实现面

迁移与评审时的实际落点（`MachineTrait` 子类、`RecipeLogic` / `WorkLogic` 子类与 `Notifiable*` 子类）：

| 模块 | 位置 |
|------|------|
| CTNH-Core | `common/machine/trait/`（`ScalableReservoirComputingLogic extends RecipeLogic`、`SimpleComputationContainer extends NetworkedComputationContainer`、`providable_net/{ProvidableNetTrait, ProvidableNetInfo, ProviderInfo}`，其中 `ProvidableNetTrait extends MachineTrait implements IMultiblockMachineTrait`）；`api/recipe/DigitalMinerLogic extends WorkLogic`；机器内联 `RecipeLogic` 子类：`INFFluidDrillLogic`、`VoidMinerRecipeLogic`、`NeutronActivatorLogic`、`DigestingTankLogic`、`ProcessControlRecipeLogic`；Creative/Circuit/Drone 部件的 `Notifiable*` 子类（`InfinityFluidTank`、`InfinityItemStackHandler`、`InfinityEnergyContainer`、`CircuitItemHandler`、`DroneHolderHandler`）；`common/machine/simple/DigitalMiner` 使用 `AutoOutputTrait.ofItems` + `attachPersistentTrait("auto_output", ...)` |
| CTNH-Lib | `api/CrossParallelRecipeLogic extends RecipeLogic`（跨并行共享逻辑，被 CTNH-Core `MeadowMachine`、CTNH-Mana `CrossParallelManaMultiBlockMachine` 复用）与 `api/ICrossParallelRecipeLogicMachine`。原 `jade/` 包已删除（`f9951f9`） |
| CTNH-Bio | `api/machine/trait/`（`NeuralModelContainer`、`NotifiableEntityContainer`、`NotifiableNutrientHandler`，均为 `NotifiableRecipeHandlerTrait<T>`，其中 `NeuralModelContainer` 另实现 `ICapabilityTrait` / `IItemHandlerModifiable`）；`BasicLivingRecipeLogic`（`BasicLivingMachine` 内联）、`CogniAssemblerRecipeLogic`（`CogniAssemblerMachine` 内联）；`machine/multiblock/part/ParabioticBridgePartMachine` 的 `ParabioticBridgeHandler extends NotifiableItemStackHandler` |
| CTNH-Energy | `common/machine/handler/` 的 `MEStorageEUHandler`（另实现 `IEnergyContainer`）/ `MEStorageFluidHandler` / `MEStorageItemHandler`（`NotifiableRecipeHandlerTrait<T>`）；`PowerStationEnergyBank extends MachineTrait`（`common/multi/PowerSubstationMachine` 内联）；`getTrait(AutoOutputTrait.class)` 见 `event/ForgeEventHandler`、`mixin/ae2/misc/PartPlacementMixin`；`attachPersistentTrait("circuit_slot", ...)` 见 `common/machine/MEPartMachine` |
| CTPP | `NotifiableStressTrait extends NotifiableRecipeHandlerTrait<Float> implements ICapabilityTrait`；`KineticRecipeLogic extends RecipeLogic` |
| CTNH-Mana | `api/machine/trait/`（`BTManaContainerTrait`、`MysticSpireManaTrait`、`ExtendedControlBusCircuitTrait`，均 `extends MachineTrait`，前两者实现 Botania `ManaReceiver`）；`ZenithMatrixRecipeLogic extends RecipeLogic` |
| CTNH-Astral | `OxygenEnricherRecipeLogic extends RecipeLogic`（`OxygenEnricherMachine` 内联） |

GTCEu 侧 trait 基础设施在 `modules/GregTech-Modern/src/main/java/com/gregtechceu/gtceu/api/machine/trait/`：22 个顶层类（`MachineTrait`、`MachineTraitHolder`、`AutoOutputTrait`、`RecipeLogic`、`WorkLogic`、`ICapabilityTrait`、`Notifiable*`、`*ComputationPortTrait`、`BatterySlotTrait`、`ProgrammableCircuitSlotTrait`、`CleanroomReceiverTrait`、`Catalyst*Handler`、`*ProxyTrait`、`NetworkedComputationContainer` 等），另有 `trait/feature/` 的 6 个接口（`IAttachConfiguratorsTrait`、`IFrontFacingTrait`、`IInteractionTrait`、`IMultiblockMachineTrait`、`IParallelTrait`、`IRenderingTrait`）。它是 **vendored 上游**：只有任务明确针对 GTCEu 内部时才改动。

## SCOPE
适用于所有 CTNH 模块的机器、trait、capability 与 Jade 代码。改动上述任一面之前先读本文件，再读对应模块与域指南。

## READ WHEN
- 新增或修改 machine trait、recipe capability、`RecipeLogic` 子类。
- 新增或调整 Jade provider、Jade 数据写入。
- 决定某个字段该同步、该持久化，还是两者都要。
- 把某模块迁移到 trait 所有权架构。
