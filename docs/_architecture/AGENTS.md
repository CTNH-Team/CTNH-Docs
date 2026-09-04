# CTNH ARCHITECTURE CONTRACT — Machine / Trait / Capability / Jade

## OVERVIEW
本文件是 CTNH 机器架构的**规范锚点**：机器与 trait 的所有权边界、字段同步与持久化规则、recipe capability 分层、Jade 数据最小化原则，以及把既有模块迁移到该架构的步骤。

来源是 GTCEu/CTNH 的 Trait/Jade 重构准则。**上游 GTM2 仅作设计参考，不是迁移目标。**

规范条款（边界、字段规则、Jade 最小化、迁移步骤）**立即生效**，适用于所有新代码与所有被触及的旧代码。其中依赖尚未落地类型的条款在下方 §9「目标态 vs 当前实现」中逐条标注，读文档的人不应假设那些类型已存在。

本文件不由 `CTNH-Docs` 的自动同步流程生成：`scripts/doc_gen.py` 只写 `docs/<Module>/**/AGENTS.md`，`_architecture/` 在其写入白名单之外，属手工维护的长期契约。

## 1. 总体边界

- `MetaMachine` 与 `MetaMachineBlockEntity` 保持分离。机器负责行为、trait 与 capability；方块实体只负责世界承载和 Forge/Jade 入口。
- trait 是机器内部的**内聚行为单元**。需要同步或持久化的字段放进 trait，由 LowDragLib 的 managed field 系统处理。
- **不为旧调用保留大规模兼容层。** 迁移时改调用方和所有权边界，而不是加转发层。
- **trait 在构造阶段挂载完毕。** `MetaMachine.attachTraits(...)` 的契约是 "All traits should be initialized while MetaMachine is creating. you cannot add them on the fly."，不存在运行期挂载。父类工厂需要的特殊参数通过**构造参数（工厂闭包）**传入，禁止 `Object... args` 扩散和延迟绑定。
- 类引用使用正常 import。实现代码里禁止硬写完整包名，禁止新增 `rawtypes` / `unchecked` 兼容 helper。

## 2. Trait 生命周期、同步与持久化

`MachineTrait` 是 `abstract class ... implements IEnhancedManaged`，当前实际提供的入口：

| 入口 | 用途 |
|------|------|
| `onMachineLoad()` / `onMachineUnLoad()` | 机器加载/卸载；注意拼写是 `UnLoad`（大写 L） |
| `onChanged()` | managed field 变化回调 |
| `hasCapability(@Nullable Direction)` | 由 `capabilityValidator` 决定的侧面暴露判定 |
| `updateModelData(ModelData.Builder)` / `getRenderState()` / `setRenderState(...)` / `scheduleRenderUpdate()` | 渲染状态 |
| `saveCustomPersistedData(CompoundTag, boolean forDrop)` / `loadCustomPersistedData(CompoundTag)` | managed field 之外的自定义 NBT |
| `getFieldHolder()` | managed field holder（`final`，不可覆写） |

`MetaMachine` 侧由 `traits.forEach(MachineTrait::onMachineLoad / onMachineUnLoad)` 驱动。**邻居变化与工作许可变化目前是机器/cover 层的回调**（`onNeighborChanged`、`onWorkAllowedChanged` 在 `MetaMachine` 及 cover 上，不在 trait 基类），trait 需要这类信号时经由其宿主机器转发。

字段规则：

- `@DescSynced`：常规客户端状态同步，适用于界面、模型、客户端逻辑需要持续读取的数据。
- `@Persisted`：机器存档持久化。
- 两者可同时使用，但必须确认该字段**确实既需要同步又需要保存**。
- managed field 系统承载不了的数据走 `saveCustomPersistedData` / `loadCustomPersistedData`。
- **同一份数据禁止同时用注解与 attach 式持久化。** 用字段承载的优先注解持久化；不用字段承载的优先 attach 式持久化。两者并存会产生重复协议和所有权不清。

## 3. Trait 查找

- 调用方需要某类 trait 时，**按类型查找**，不要遍历全部 trait 再 `instanceof`。
- 新增 trait 时不要在机器基类堆类型特判；让 trait 自己实现能力与生命周期。
- 当前 `MetaMachine.traits` 是 `List<MachineTrait>`，尚无类型索引（见 §9）。在索引落地前，按类型取用的逻辑集中在机器或 helper 中，不要在业务调用点散落 `instanceof` 链。

## 4. Capability 分层

四层职责互不越界：

| 层 | 职责 |
|----|------|
| Forge capability | 对外暴露机器的物品、流体、能量访问能力 |
| Recipe capability | 描述配方内容、网络编码、匹配、并行限制与 XEI/EMI 逻辑 |
| Machine trait | 持有具体 handler/container，负责机器侧状态与行为 |
| Machine 子类 | 只负责机器特有规则；禁止把 capability 分发全塞进基类 |

能量容器由 tiered machine 的工厂创建。子类的特殊容器若需额外参数，用**构造时传入的工厂闭包**，让父类调用 `createEnergyContainer` 时仍能保留子类参数；不要用延迟绑定绕开构造参数问题。

## 5. AutoOutput

自动输出的**唯一所有者是 AutoOutput trait**：

- 输出方向、是否允许从输出侧输入、自动输出开关、订阅刷新都属于 trait。
- 机器不持有 item/fluid 自动输出字段，也不保留委托方法。
- 机器 UI 与配置器直接绑定 trait 暴露的 API。
- 邻居变化、加载、配置变化的订阅状态由 trait 管理。
- Jade 信息由 trait 自己写入；统一机器 provider 只负责触发 trait。

迁移顺序固定：**先让 trait 成为唯一所有者 → 再删机器字段与旧委托方法 → 最后清理旧分发接口**（`IAutoOutputItem` / `IAutoOutputFluid` / `IAutoOutputBoth`）。

## 6. RecipeLogic 与配方输出 Jade

配方输出不使用独立的输出 provider，也不新建专门的输出 trait。

`RecipeLogic` 负责：

- 当前 recipe、工作状态与配方上下文；
- 读取客户端已同步的 `lastRecipe`；
- 通过 `ContentListMap.forEachEntry` 遍历所有输出 capability；
- 按 capability 的稳定顺序分发 tooltip；
- 添加统一的配方输出标题。

`RecipeCapability` 负责解释自己的输出：物品 capability 处理 `ItemStack`、范围数量与概率输出；流体 capability 处理 `FluidStack`、范围容量与概率输出。将来新增气体、数据或其他 capability 时只实现自己的解释逻辑，**`RecipeLogic` 不得增加类型判断**。

**Jade 中禁止重复序列化 `lastRecipe`** —— 该字段已通过 `@DescSynced` 同步到客户端。能耗、并行、模式、失败原因等只要能由客户端状态推导，就不写入 Jade NBT。

## 7. ContentListMap 顺序

- 遍历统一走 `forEachEntry(EntryConsumer)`。**禁止在调用方遍历 `asMap().entrySet()` 再手动排序。**
- 泛型擦除集中在 `ContentListMap` 内部，调用方使用泛型化的 `EntryConsumer`，不要新增 raw helper。
- 顺序基准是 `RecipeCapability.COMPARATOR`，当前实现为 `Comparator.comparingInt(o -> o.sortIndex)`，`sortIndex` 在 capability 注册时按 `index++` 递增分配。
- 当前底层容器是 `Reference2ObjectArrayMap`（插入序），**顺序并非由容器结构保证**。因此依赖 capability 顺序的代码必须显式经过 comparator 或 `forEachEntry`，不能假定 map 迭代序等于 capability 序。

## 8. Jade 架构

目标形态是**单一机器入口**：provider 取到机器 → 调用机器的 Jade 写入回调 → 遍历全部 trait，各 trait 写自己的 section → tooltip 阶段按 trait 的 Jade 优先级倒序调用。机器类提供机器特有信息，trait 通过同名方法提供 trait 信息。

当前形态是**多 provider + 集中优先级注册**：GTCEu `integration/jade/provider/` 有 26 个 provider，由 CTNH-Lib `jade/GTProvidersRegistrar` 通过 `JadePriorityManager` 以显式优先级注册（block data 与 block component 两套，数值越小越先执行）：

```text
1100 ElectricContainerBlockProvider   1900 ExhaustVentBlockProvider
1200 WorkLogicMachineProvider         2000 SteamBoilerBlockProvider
1300 ControllableBlockProvider        2100 AutoOutputBlockProvider
1400 RecipeLogicProvider              2200 CableBlockProvider
1500 ParallelProvider                 2300 MachineModeProvider
1600 RecipeOutputProvider             2400 StainedColorProvider
1700 MultiblockStructureProvider      2500 HazardCleanerBlockProvider
1800 MaintenanceBlockProvider         2600 TransformerBlockProvider
                                      2700 PrimitivePumpBlockProvider
                                      2750 DataBankBlockProvider
                                      2800 EnergyConverterModeProvider
```

无论哪种形态，以下两条恒定生效：

- **只有仍被注册且承担独立功能的 provider 才保留。** 功能迁走后删除旧的机器专用 provider，而不是继续隐藏注册。
- **Jade 服务端数据只保留客户端无法从机器/trait 已同步状态推导出的信息。**

## 9. 目标态 vs 当前实现

下列类型/成员是**迁移目标，在当前 checkout 中不存在**。已在 GregTech-Modern 全部本地 ref 上用 `git log --all -S` 确认无任何提交引入过。左列名称仅用于统一迁移时的命名，**不要当作现存 API 引用**；在别处提及时必须同样标注为目标态。

| 目标态 | 当前实现 |
|--------|----------|
| trait 类型索引 holder（拟名 `MachineTraitHolder`，沿父类结构建索引、调用方 `byType` 取用） | `MetaMachine.traits` 为 `List<MachineTrait>`，无索引；按类型取用需自行集中处理 |
| trait 基类新增 `onNeighborChanged` / `onWorkAllowedChanged` / `onMachineDestroyed` | 基类只有 §2 表中的入口；邻居与工作许可回调在机器与 cover 层，trait 需经宿主机器转发 |
| 统一 `AutoOutputTrait`，删除 `IAutoOutputItem` / `IAutoOutputFluid` / `IAutoOutputBoth` | 三个接口在 GregTech-Modern 有 56 处引用（`SimpleTieredMachine`、Quantum Tank/Chest、Drum、Buffer、Pump、ItemCollector、Fisher、BlockBreaker、`MachineModel`、`AutoOutputBlockProvider` 等）。**CTNH 八个模块零引用**，迁移面完全落在 vendored 上游 |
| 取消独立配方输出 provider，输出解释回归 `RecipeCapability` | GTCEu `RecipeOutputProvider` 仍在，由 Lib 以 1600 注册；CTNH-Core `api/jade/` 另有 `MultithreadRecipeOutputProvider` / `MultithreadRecipeLogicProvider` / `ThreadStatusProvider` 三个下游变体需一并迁移 |
| attach 式持久化 trait API（拟名 `attachPersistentTrait`） | 不存在；managed field 之外的持久化目前只有 `saveCustomPersistedData` / `loadCustomPersistedData` |
| 单一机器 Jade 入口（拟名 `MachineJadeProvider`）+ trait 侧 `jadePriority()` 排序 | 26 个 provider + `JadePriorityManager` 显式优先级注册（见 §8） |
| `ContentListMap` 以带 comparator 的有序 map 天然保序，comparator 以 `sortIndex` 为主、capability name 兜底 | 底层 `Reference2ObjectArrayMap`（插入序）；`RecipeCapability.COMPARATOR` 只有 `comparingInt(sortIndex)`，无 name 兜底 |

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
- 把本文件描述的目标态类型当作现存 API 写进模块文档或代码注释。

## 12. CTNH 侧现有 trait 实现面

迁移与评审时的实际落点（`RecipeLogic` 子类与 `Notifiable*` trait 子类）：

| 模块 | 位置 |
|------|------|
| CTNH-Core | `common/machine/trait/`（`ScalableReservoirComputingLogic`、`SimpleComputationContainer`、`providable_net/`）；机器内联 `RecipeLogic` 子类若干（`INFFluidDrillLogic`、`VoidMinerRecipeLogic`、`NeutronActivatorLogic`、`DigestingTankLogic`、`ProcessControlRecipeLogic`）；Creative/Circuit/Drone 部件的 `Notifiable*` 子类 |
| CTNH-Lib | `api/CrossParallelRecipeLogic`（跨并行共享逻辑，被多模块机器复用） |
| CTNH-Bio | `api/machine/trait/`（`NeuralModelContainer`、`NotifiableEntityContainer`、`NotifiableNutrientHandler`，均为 `NotifiableRecipeHandlerTrait<T>`）；`BasicLivingRecipeLogic`、`CogniAssemblerRecipeLogic` |
| CTNH-Energy | `MEStorageEUHandler` / `MEStorageFluidHandler` / `MEStorageItemHandler`（`NotifiableRecipeHandlerTrait<T>`）；`PowerStationEnergyBank extends MachineTrait` |
| CTPP | `NotifiableStressTrait extends NotifiableRecipeHandlerTrait<Float> implements ICapabilityTrait`；`KineticRecipeLogic` |
| CTNH-Mana | `ZenithMatrixRecipeLogic` |
| CTNH-Astral | `OxygenEnricherRecipeLogic` |

GTCEu 侧 trait 基础设施在 `modules/GregTech-Modern/src/main/java/com/gregtechceu/gtceu/api/machine/trait/`（17 个类，含 `MachineTrait`、`RecipeLogic`、`WorkLogic`、`ICapabilityTrait`、`Notifiable*`、`*ComputationPortTrait`）。它是 **vendored 上游**：只有任务明确针对 GTCEu 内部时才改动。

## SCOPE
适用于所有 CTNH 模块的机器、trait、capability 与 Jade 代码。改动上述任一面之前先读本文件，再读对应模块与域指南。

## READ WHEN
- 新增或修改 machine trait、recipe capability、`RecipeLogic` 子类。
- 新增或调整 Jade provider、Jade 数据写入。
- 决定某个字段该同步、该持久化，还是两者都要。
- 把某模块迁移到 trait 所有权架构。
