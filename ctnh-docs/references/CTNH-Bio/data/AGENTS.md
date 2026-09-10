# CTNH-BIO DATA DOMAIN

## OVERVIEW
`src/generated/resources` 的数据生成源码（28 个 Java 文件）：配方生成器、lang、掉落表、材料与 tag。

## STRUCTURE
```
data/
├─ CBDatagen.java, CBElements.java
├─ lang/                      # ChineseLangHandler, EnglishLangHandler
│  └─ utils/                  # EntityPropertyLangUtil
├─ loot/                      # CBLootTableProvider
├─ materials/                 # CommonMaterials, OrganicMaterials
├─ recipe/
│  ├─ CBRecipeBuilder.java, CBRecipeCategories.java, CogniRecipeBuilder.java
│  ├─ CommonRecipes.java, CustomTags.java, LivingMachineRecipes.java, RecipeRemoval.java
│  ├─ VanillaRecipeProvider.java, VanillaRecipes.java
│  ├─ living/                 # BasicLivingRecipes, BioReactorRecipes, BioelectricForgeRecipes,
│  │                          #   DecomposerRecipes, DigesterRecipes
│  └─ multi/                  # CogniRecipes, GreatFleshRecipes, HostileObservationRecipes
└─ tags/                      # BlockTags, FluidTags, ItemTags
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| 数据生成入口 | `data/CBDatagen.java`（lang / block tags / item tags / fluid tags 注册到 registrate 的 data generator） |
| GT 元素注册 | `data/CBElements.java`（`CBElements.init()` 由 `CTNHBioGTAddon.registerElements()` 调用） |
| 配方生成 | `data/recipe/`（CommonRecipes, VanillaRecipes, LivingMachineRecipes, RecipeRemoval） |
| 构建器 | `data/recipe/CBRecipeBuilder.java`, `CogniRecipeBuilder.java` |
| 活体机器配方 | `data/recipe/living/`（BioReactor, BioelectricForge, Decomposer, Digester, BasicLiving） |
| 多方块配方 | `data/recipe/multi/`（Cogni, GreatFlesh, HostileObservation） |
| lang | `data/lang/`, `data/lang/utils/EntityPropertyLangUtil.java`（中文经 CTNH-Lib `ProviderTypes.CNLANG` 走 `@CN` 处理器） |
| 掉落表 | `data/loot/CBLootTableProvider.java`（类存在，当前不在 `CBDatagen.init()` 中注册） |
| 材料 | `data/materials/`（CommonMaterials, OrganicMaterials；由 `registry/CBMaterials.init()` 触发 `register()`） |
| tag | `data/tags/`（BlockTags, FluidTags, ItemTags） |

## CONVENTIONS
- Bio 专属活体机器配方放本域；跨模块通用配方通常归 Core。
- **GTM 动态包**：经 `CTNHBioGTAddon.addRecipes()` 注册的 GT/GMT 配方是运行时动态数据包，`runData` 对其不产出 JSON；静态 `src/generated/resources` 只含 tags/lang/models/loot_tables/非 GT 配方。
- `src/generated/resources` 由 `:modules:CTNH-Bio:runData` 产出，禁止手改。
- 手写静态 JSON 在 `src/main/resources/data/ctnhbio/`（`mob_crushing_recipes/` 6 个、`loot_categories/despoil_loot.json`）；重新生成前先确认该文件属于哪个源码根。
- 配方移除走 `data/recipe/RecipeRemoval.java`（`CTNHBioGTAddon.removeRecipes()` 调用），不要用 Mixin 删配方。
- `data/recipe/CustomTags.java` 目前是空类，不要据此假定存在自定义 tag 生成逻辑。

## ANTI-PATTERNS
- 假定所有配方 JSON 都是生成的；先确认文件在 `src/main/resources` 还是 `src/generated/resources`。
- 手改 `src/generated/resources` 下的产物。
- 期望 `runData` 产出 GT/GTM 配方 JSON。

## SCOPE
`src/main/java/com/moguang/ctnhbio/data` 及其全部子包。

## READ WHEN
- 新增 Bio 配方、lang、掉落表、材料或 tag。

## SOURCE OF TRUTH
- `data/CBDatagen.java` 与 `data/recipe/` 下的 provider。

## WORKFLOW
1. 改对应 provider，然后跑 `:modules:CTNH-Bio:runData`。
2. 检查 generated 资源 diff，再跑 `spotlessCheck`。
