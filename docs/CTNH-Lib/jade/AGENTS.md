# CTNH-LIB JADE DOMAIN

## OVERVIEW
Jade provider 排序基础设施：所有 CTNH 模块共享的有序 GT provider 注册（2 个 Java 文件）。

架构约束见 `docs/_architecture/AGENTS.md` §8（Jade 架构）与 §2/§6（Jade 数据最小化）。本文件只描述本域的实现与现状。

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Provider registrar | `jade/GTProvidersRegistrar.java` |
| RecipeLogic provider registration | `jade/GTProvidersRegistrar.java`（block data + block component） |
| Priority manager | `jade/JadePriorityManager.java` |

## CURRENT REGISTRATION ORDER
`GTProvidersRegistrar` 通过 `JadePriorityManager` 注册 GTCEu `integration/jade/provider/` 的 26 个 provider，分 block data 与 block component 两套，**数值越小越先执行**：

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

新增 provider 时在相邻区间取值，不要挤占既有数值；跨模块 provider 的相对次序由这张表决定。

## CONVENTIONS
- `GTProvidersRegistrar` 通过 `JadePriorityManager` 加载有序 GT provider；`JadePriorityManager` 让功能模块以显式优先级注册/注销 block data 与 component provider。
- `RecipeLogicProvider` 同时注册为 block data（`recipe_logic_data`, 1400）与 block component（`recipe_logic_component`, 1400）；两者必须同时启用，否则 block data 与 component 的 GT tooltip 会不一致。
- 功能模块经此共享面注册 Jade provider，不直接注册。
- Core 的 `registry/jade/CTNHJadePlugin`、Core `api/jade/` 的三个多线程 provider、Energy `integration/jade/`、Bio `integration/jade/`、Mana `integration/jade/`、CTPP `integration/jade/` 都经这个 manager。
- **Jade 服务端数据只写客户端推导不出的信息。** 已通过 `@DescSynced` 同步的字段（尤其 `lastRecipe`）禁止再序列化进 Jade NBT；能耗、并行数、机器模式、失败原因只要能由客户端状态推导就不要写。
- 统一单入口机器 provider 是迁移目标（`_architecture` §9），当前形态是上表的多 provider 注册。迁移时先把状态读取移到机器/trait 回调，再删旧 provider 与其注册行——不要保留隐藏注册。

## ANTI-PATTERNS
- 不要绕过 `JadePriorityManager` 排序 GT provider；CTNH 模块依赖可预测的 block data/component 优先级。
- 不要注释掉 `RecipeLogicProvider` 的 block data 或 block component 任一注册；两者必须保持同步。
- 不要把客户端已同步的状态再通过 Jade NBT 二次传输。
- 不要保留已无独立功能的机器专用 provider（无论是否仍注册）。

## SCOPE
Applies to `src/main/java/tech/vixhentx/mcmod/ctnhlib/jade`.

## READ WHEN
- 修改 Jade provider 排序或新增共享 provider 基础设施。
- 判断某条 Jade 信息该由服务端 NBT 传输还是客户端推导。

## SOURCE OF TRUTH
- `jade/GTProvidersRegistrar.java`、`jade/JadePriorityManager.java`，以及 Core `registry/jade/` 的用法。
- 架构约束：`docs/_architecture/AGENTS.md`。

## WORKFLOW
1. 先看 `_architecture` §8 的目标形态与本文件的现状表。
2. 检查优先级 manager 契约再改排序。
3. 用某个消费模块的 Jade provider 做运行时验证。
4. Run `:modules:CTNH-Lib:build`.
