# CTNH-BIO COMMON DOMAIN

## OVERVIEW
Bio 的公共装配与通用内容（7 个 Java 文件）：`CommonProxy` 注册枢纽、配方条件、通用物品、磨碎配方与血清。

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| 公共代理 | `common/CommonProxy.java` |
| 配方条件 | `common/condition/EffectCondition.java` |
| 通用物品 | `common/item/AssemblyStepItem.java`, `common/item/OrganicVialItem.java` |
| 磨碎配方 | `common/recipe/MobCrushingRecipe.java`, `common/recipe/MobCrushingRecipeManager.java` |
| 血清 | `common/serum/PrimordialSerum.java` |

## CONVENTIONS
- `CommonProxy()` 构造时调用 `CommonProxy.init()` 并注册自身到 mod 事件总线，同时注册 `CBSerums.SERUMS`。
- `CommonProxy.init()` 顺序：`CBEntities.init()` → `CBCreativeModeTabs.init()` → `CBDatagen.init()` → `CTNHBio.REGISTRATE.registerRegistrate()` → `PropertyOperators.init()` → `EntityProperties.init()`；依赖属性注册表的代码必须排在其后。
- `CommonProxy` 通过 `addGenericListener` 接管 GT 注册事件：`MachineDefinition`（`CBMachines.init()` + `CBMultiblocks.init()`）、`GTRecipeType`（`CBRecipeTypes.init()`）、`RecipeConditionType`（`CBRecipeConditions.init()`）、`GTRecipeCategory`（`CBRecipeCategories.init()`）、`SoundEntry`（`CBSoundEntries.init()`）。
- 材料注册走 `MaterialEvent` → `CBMaterials.init()`；`MaterialRegistryEvent` 创建 `ctnhbio` 材料注册表；`FMLCommonSetupEvent` 中把 Biomancy `DECOMPOSING_RECIPE_TYPE` 挂到 `CBRecipeTypes.DECOMPOSER_RECIPES.getProxyRecipes()`。
- `CommonProxy.gatherData(GatherDataEvent)` 在 `event.includeClient()` 时调 CTNH-Lib `CTNHPonderLang.init(new CTNHBioPonderPlugin())`，抽取 Ponder 场景 / tag 的 lang 键；`ClientProxy` 的 `onClientSetup` 把同一插件注册进 `PonderIndex`。
- 磨碎配方是 Bio 自有配方面（配 `integration/jei/MobCrushingCategory` 与 EMI Mixin），数据来自 `src/main/resources/data/ctnhbio/mob_crushing_recipes/`。

## ANTI-PATTERNS
- 绕过 `CommonProxy` 的初始化顺序，去用依赖 `PropertyOperators` / `EntityProperties` 的注册表。
- 在 `common/` 里重复 `registry/` 的注册逻辑。

## SCOPE
`src/main/java/com/moguang/ctnhbio/common` 及其全部子包。

## READ WHEN
- 修改 `CommonProxy` 装配顺序、血清或通用配方逻辑。
- 调整 Ponder 思索 lang 的抽取接线。

## SOURCE OF TRUTH
- `common/CommonProxy.java`、`client/ClientProxy.java` 与 `event/EventHandler.java`。

## WORKFLOW
1. 加钩子前先确认 `CommonProxy.init()` 与 `addGenericListener` 的注册时序。
2. 跑 `:modules:CTNH-Bio:build`。
