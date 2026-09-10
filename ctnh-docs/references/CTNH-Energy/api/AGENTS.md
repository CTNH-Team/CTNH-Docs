# CTNH-ENERGY API DOMAIN

## OVERVIEW
CTNH-Energy 的跨域契约面（8 个 Java 文件）：多方块结构谓词、EU 物品上下文、CPU 自动翻倍与样板提供者逻辑、电路样板、幽灵键拖放目标、可升级菜单。

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| 多方块谓词 | `api/CEPredicates`（`craftingUnitBlock()` 统计合成存储器容量到 `StorageKb` match context；`powerSubstationBatteries()` 统计各档电池到 `PowerSubstationMachine.BatteryMatchWrapper`；两者均带 lang 工具提示） |
| EU 物品上下文 | `api/EUItemContext`（`getStack` / `setStack` / `addOverflow` / `getTier`） |
| CPU 自动翻倍 | `api/IAutoMultiplyCPU`；实现 `mixin/ae2/cpu/CraftingCpuLogicMixin`，由 `mixin/omni/OmniCraftingBlockEntityMixin` 在 COMPLEX 家族合成单元上开启 |
| 电路样板 | `api/ICircuitPattern`（`CE$setCircuitNumber` / `CE$getCircuitNumber`，哨兵值 `NO_CIRCUIT = -1`）；主要实现 `common/pattern/DynamicProcessingPattern`，使用方 `common/circuit/CircuitPatternService` |
| 幽灵键目标 | `api/IGhostKeyTarget`（继承 `IGhostIngredientTarget`；`acceptKey` / `convertIngredient` 把 EMI 物品与流体转成 `AEKey`）；实现 `common/machine/gui/AEConfigSlotWidget` |
| 样板提供者逻辑 | `api/IPatternProviderLogic`（`CE$getBlockingMode()` 返回 `CESettings.BlockingType`）；实现 `mixin/ae2/patternprovider/PatternProviderMenuMixin`，界面消费方 `PatternProviderScreenMixin` |
| 维持上下文 | `api/IMaintainingContext`（`getMaintainingAmount` / `setMaintainingAmount`）；实现 `mixin/ae2/part/StackTransferContextImplMixin`，消费方为导入/导出总线与存储策略 mixin |
| 可升级菜单 | `api/IUpgradeableMenu`（`CE$getUpgrades()` / `CE$getToolbox()`） |

## CONVENTIONS
- 接口成员一律带 `CE$` 前缀，避免与 Mixin 目标类成员冲突。
- 契约只声明，不写玩法逻辑；实现落在 `common/` 或 `mixin/`。
- 哨兵值语义：`ICircuitPattern.NO_CIRCUIT` 表示不携带编程电路，读写时用 `CircuitPatternData.read/write` 而不是直接操作 NBT 键。
- `CEPredicates.init()` 是幂等惰性初始化，`craftingUnitBlock()` 首次调用会自行补调。

## ANTI-PATTERNS
- 把玩法逻辑写进 `api/`，或在 `api/` 里引用客户端专属类。
- 绕过 `ICircuitPattern` 直接读写 `ctnhenergy_circuit` / `Configuration` 标签。
- 在多处重复定义合成存储器容量表或电池遍历逻辑，而不复用 `CEPredicates`。

## SCOPE
`modules/CTNH-Energy/src/main/java/tech/luckyblock/mcmod/ctnhenergy/api/`。

## READ WHEN
- 需要让 `common/` 与 `mixin/` 共享一个新契约
- 新增多方块结构谓词或修改蓄能变电站 / 量子计算机的结构匹配规则
- 扩展电路样板、维持卡或样板提供者阻挡模式的接口面

## SOURCE OF TRUTH
`api/` 下的接口与谓词，以及其在 `common/`、`mixin/` 中的实现与消费点。

## WORKFLOW
1. 确认该面确实被两个以上域共享，才放进 `api/`。
2. 接口成员加 `CE$` 前缀；同步更新全部实现与消费点。
3. `:modules:CTNH-Energy:build` 编译。
