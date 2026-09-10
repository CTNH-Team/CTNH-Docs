# CTNH-BIO MACHINE DOMAIN

## OVERVIEW
活体机器实现（7 个 Java 文件）：Brain in a Vat、Hostile Observer、Great Flesh、Cogni 组装机及其多方块部件。

## STRUCTURE
```
machine/
├─ braininavat/              # Brain, BrainInAVatMachine
├─ bioobservation/           # HostileObserverMachine
├─ greatflesh/               # GreatFleshMachine
└─ multiblock/               # CogniAssemblerMachine
   └─ part/                 # NeuralModelAccessorMachine, ParabioticBridgePartMachine
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Brain in a Vat | `machine/braininavat/`（`Brain`, `BrainInAVatMachine`；注册于 `registry/CBMachines.java`） |
| 敌对观测 | `machine/bioobservation/HostileObserverMachine.java`（注册于 `registry/CBMultiblocks.java`） |
| 血肉聚合 | `machine/greatflesh/GreatFleshMachine.java`（注册于 `registry/CBMultiblocks.java`） |
| Cogni 组装机 | `machine/multiblock/CogniAssemblerMachine.java`（内联 `CogniAssemblerRecipeLogic`，`partSorter` 供 `CBMultiblocks` 使用） |
| 多方块部件 | `machine/multiblock/part/NeuralModelAccessorMachine.java`, `ParabioticBridgePartMachine.java`（含内联 `ParabioticBridgeHandler`） |

## CONVENTIONS
- 机器实现只依赖 `api/` 契约：单方块机器继承 `api/machine/BasicLivingMachine`，多方块继承 `api/machine/multiblock/WorkableLivingMultiblockMachine`。
- 多方块部件用 `api/machine/multiblock/CBPartAbility` 声明能力（`NEURAL_MODEL_ACCESSOR`），图案里通过 `Predicates.abilities(...)` 引用。
- registrate 条目只在 `registry/CBMachines.java` / `registry/CBMultiblocks.java` 声明，机器类不自行注册，也不写 `@Mod.EventBusSubscriber`。
- 机器特有规则放机器子类，通用规则放 `api/machine/` 基类；跨机器的营养 / 模型 / 实体状态由 `api/machine/trait/` 的 trait 持有。

## ANTI-PATTERNS
- 把机器逻辑塞进配方类或注册类。
- 在机器类里另存一份与 trait 重复的状态（营养值、模型容器等）。
- 在本域直接操作注册 API 注册物品 / 方块 / 机器。

## SCOPE
`src/main/java/com/moguang/ctnhbio/machine` 及其全部子包。

## READ WHEN
- 新增或修改 Bio 活体机器与多方块部件。

## SOURCE OF TRUTH
- `machine/` 下的实现与 `api/machine/` 的契约；注册以 `registry/CBMachines.java` / `registry/CBMultiblocks.java` 为准。

## WORKFLOW
1. 先确认机器的注册条目与所属 API 契约（`BasicLivingMachine` 还是 `WorkableLivingMultiblockMachine`）。
2. 跑 `:modules:CTNH-Bio:build`；机器行为在游戏内验证。
