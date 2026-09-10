# CTNH-ENERGY DATA DOMAIN

## OVERVIEW
`src/generated/resources` 的数据生成源（3 个 Java 文件）：`CEDatagen` 与中英 lang 处理器。

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Datagen 入口 | `data/CEDatagen`（`REGISTRATE.addLangProcessor()`；`ProviderType.LANG` → `EnglishLangHandler`；CTNH-Lib `ProviderTypes.CNLANG` → `ChineseLangHandler`） |
| Lang | `data/lang/EnglishLangHandler`, `data/lang/ChineseLangHandler` |
| Ponder lang 抽取 | `common/CommonProxy.gatherData()` → CTNH-Lib `CTNHPonderLang.init(new CTNHEnergyPonderPlugin())` |
| 注解式 lang | `@CN` / `@EN` 标注的静态 `Lang` 字段（如 `common/item/MaintainingCardItem`、`registry/CEMultiblock`、`event/ForgeClientEventHandler`），由 `addLangProcessor()` 收集 |

## CONVENTIONS
- `src/generated/resources` 由 `:modules:CTNH-Energy:runData` 产出；不要手改生成物。
- GT/GMT 配方经 `*GTAddon.addRecipes()` 注册为运行时动态数据包，`runData` 对其**不产出** JSON；详见模块主文档 CONVENTIONS。
- 维持卡 lang 键位于 `ctnhenergy.maintainingcarditem.*`（`configuretooltip`, `currentamounttooltip`, `settingstitle`, `stockingamount`）。
- 工具提示分类键位于 `ctnhenergy.tooltip.*`（如 `omni_thread_num`, `auto_multiply`）。
- Jade 相关键位于 `config.jade.plugin_ctnhenergy.*` 与 `ctnhenergy.jade.ae_eu.*`。
- 本模块生成物只有 lang、blockstates、models、loot_tables 与 `data/gtceu/tags`；没有世界生成与配方 JSON。

## ANTI-PATTERNS
- 手改 `src/generated/resources` 下的文件。
- 在 datagen 之外调用 `REGISTRATE.genLang(...)`，或在场景类之外散落双语字符串。

## SCOPE
`modules/CTNH-Energy/src/main/java/tech/luckyblock/mcmod/ctnhenergy/data/` 及其子包。

## READ WHEN
- 新增或修改 Energy 的 lang 键、工具提示、Jade 显示名
- 调整 datagen 产物

## SOURCE OF TRUTH
`data/CEDatagen`、`data/lang/*` 与 `common/CommonProxy.gatherData()` 的接线。

## WORKFLOW
1. 改对应 provider（或加 `@CN` / `@EN` 注解），再跑 `:modules:CTNH-Energy:runData`。
2. 检查 `src/generated/resources` 差异；跑 `spotlessCheck`。
