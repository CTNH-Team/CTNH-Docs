# CTNH-CORE API DOMAIN

## OVERVIEW
Core 对外的公共 API 面（17 个 Java 文件）：多方块构建器、机器 feature 钩子、GUI/Jade/配方接入点与材料数据辅助。Core 之外的代码通过这些面构建机器与配方，而不触碰实现类。

## STRUCTURE
```text
api/
|-- CTNHMultiblockBuilder.java
|-- Pattern/                   # AsynBlockPattern, CTNHBlockMaps, CTNHBoilerFireboxType, CTNHPredicates
|-- data/material/             # CTNHMaterialIconSet, CTNHMaterialIconType, CTNHPropertyKeys, CatalystProperty
|-- gui/                       # CTNHGuiTextures
|-- jade/                      # MultithreadRecipeLogicProvider, MultithreadRecipeOutputProvider, ThreadStatusProvider
|-- machine/feature/           # IDigitalMiner, IDynamicCasing（ICoilMachine 已删除 → 改用 GTCEu CoilMachineTrait）
|-- machine/multiblock/        # UnlimitedItemStackTransfer
`-- recipe/                    # DigitalMinerLogic
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| 多方块构建器 | `api/CTNHMultiblockBuilder.java`, `api/machine/multiblock/` |
| 机器 feature | `api/machine/feature/`（`IDigitalMiner`, `IDynamicCasing`） |
| 线圈处理（已迁移） | GTCEu `com.gregtechceu.gtceu.common.machine.trait.multiblock.CoilMachineTrait`，经 `getTraitOrThrow()` 获取 —— 原 `api/machine/feature/ICoilMachine` 已删除 |
| 图案辅助 | `api/Pattern/`（`AsynBlockPattern`, `CTNHBlockMaps`, `CTNHPredicates`） |
| AE 图案 NPE 修复 | `api/Pattern/AsynBlockPattern.java` —— `extractInventory` / `searchAEStorage` 在 `AEItemKey.of` 前先判 `context.foundItemStack != null && !isEmpty()` |
| 材料数据 | `api/data/material/`（icon set/type、property key、catalyst property） |
| GUI 贴图 | `api/gui/CTNHGuiTextures.java` |
| Jade provider（已停用） | `api/jade/`（多线程配方/输出/线程状态，三份文件整体注释；见下节） |
| 配方 API | `api/recipe/`（`DigitalMinerLogic`） |

## CONVENTIONS
- API 类不得把仅客户端类泄漏进 common 构造路径。
- 对外暴露机器时优先给接口面（`IDigitalMiner`, `IDynamicCasing`），而非具体实现。
- `api/jade/` 的 provider 接口与 `registry/jade/CTNHJadePlugin` 目前均为停用状态（见下节）；不要再按「接口 + 插件注册」的旧模型扩展它们。
- GT/GMT 配方属运行时动态数据包（`*GTAddon.addRecipes()` → `GTDynamicPackContents` / CTNH-Lib `CTNHDynamicDataPack`），`runData` 对其不产出 JSON。详见模块主文档 CONVENTIONS。
- 引用物品/方块/流体**必须**使用静态注册对象（`GTMaterials.Iron`, `CTNHBlocks.*`, `TagPrefix.ingot`, `AEItems.X` 等），**禁止** `ResourceLocation` 字符串解析 + `ForgeRegistries` 查找，除非该对象不存在。
- 线圈迁移：本模块已删除 `ICoilMachine`；调用方改为在机器上查询 `CoilMachineTrait`（示例：`BlazeBlastFurnaceMachine`, `FermentingTankMachine`）。

## JADE PROVIDERS
`api/jade/` 的 `MultithreadRecipeLogicProvider`、`MultithreadRecipeOutputProvider`、`ThreadStatusProvider` 是 GTCEu `RecipeLogicProvider` / `RecipeOutputProvider` 的多线程变体，**当前全部处于停用状态**：三个文件整体被注释（`ThreadStatusProvider` 79 行、`MultithreadRecipeLogicProvider` 200 行、`MultithreadRecipeOutputProvider` 319 行均为注释行），`registry/jade/CTNHJadePlugin` 的 `init()` 方法体也整体注释，没有任何注册调用生效。

- 它们不再是现行注册路径：GTCEu 上游已收敛为单一机器入口 `com.gregtechceu.gtceu.integration.jade.provider.MachineJadeProvider`（由 GTCEu `integration/jade/GTJadePlugin` 注册，`integration/jade/provider/` 现仅 6 个 provider）。CTNH-Lib 的 `jade/GTProvidersRegistrar`、`jade/JadePriorityManager` 连同整个 `jade/` 包已在 f9951f9「移除gt jade相关」中删除，Lib 侧对应指南也已一并移除，不要在 Lib 重建 provider 排序。
- 迁移方向与条款以 `references/_architecture/AGENTS.md` §6/§8/§9 为准；改动这三个类或 `CTNHJadePlugin` 前先读架构契约，不要把它们当成生效中的 provider 去接线。
- Jade 服务端数据只写客户端推导不出的信息：`lastRecipe` 已由 `@DescSynced` 同步，禁止在 Jade 中重复序列化；能耗、并行、线程状态能推导则不写 NBT。

## ANTI-PATTERNS
- 在 API 类里加玩法逻辑；实现应留在 `common/` 或 `registry/`。
- 从共享 API 面引用模块专属类。
- 重新引入 `ICoilMachine`；应使用 `CoilMachineTrait`。
- 把已注释停用的 `api/jade/` provider 重新接线，或重建 CTNH-Lib 已删除的 `JadePriorityManager` / `GTProvidersRegistrar`（上游已收敛为 GTCEu `MachineJadeProvider`）。

## SCOPE
适用于 `src/main/java/io/github/cpearl0/ctnhcore/api` 及其子包。

## READ WHEN
- 向其他 CTNH 模块暴露新的机器、feature 或配方面。
- 改动多方块构建器或机器 feature 钩子。

## SOURCE OF TRUTH
- `api/CTNHMultiblockBuilder.java` 与 `api/machine/feature/` 契约。
- `registry/` 的注册接线与 `common/CommonProxy.java`。

## WORKFLOW
1. 先确认该面确实需要共享，再放进 `api/`。
2. 检查 Core 与各 feature 模块中的消费方调用点。
3. 跑 `:modules:CTNH-Core:build` 与最窄的相关消费方任务。
