# CTNH-MANA DATA DOMAIN

## OVERVIEW
`data/` 是 CTNH-Mana 的数据层（55 个 Java 文件）：datagen 接线、SavedData、GT 配方注册源、跨 mod 配方 builder、tag 与双语 lang、材料定义。

## STRUCTURE
```text
data/
├── CMDatagen.java, ManaData.java
├── lang/                      # 3: AHCCRuneLang, ChineseLangHandler, EnglishLangHandler
├── materials/                 # BotaniaMaterials
├── recipe/                    # 顶层 35 个文件
│   ├── 33 个由 CTNHManaGTAddon.addRecipes() 直接调用；SalvagingRecipes 内再调 RuneSalvagingRecipes
│   ├── ManaRecipeRemoval.java          # 精确 ID 移除清单
│   ├── builder/apotheosis/    # 2: GemCuttingRecipeBuilder, SalvagingRecipeBuilder
│   ├── builder/bloodmagic/    # 2: BloodAltarRecipeBuilder, TartaricForgeRecipeBuilder
│   ├── builder/botania/       # 7: ElfPlateRecipeBuilder, ElvenTradeRecipeBuilder, ManaInfusionRecipeBuilder, PetalRecipeBuilder, RuneAltarRecipeBuilder, RuneRitualRecipeBuilder, TerraPlateRecipeBuilder
│   └── utils/                 # BotaniaIngredients
└── tags/                      # 2: FluidTypeTags, ItemTags
```
`addRecipes()` 直接接线的 33 个类：`BeamsRecipes`, `BloodAltarRecipes`, `BotaniaRecipes`, `DemonWillGeneratorRecipes`, `ElvenTradeRecipes`, `EternalGardenRecipes`, `EternalGardenSpecialRecipes`, `EternalWosRecipes`, `GaiaReactorRecipes`, `GemCuttingRecipes`, `HellForgeRecipes`, `MachineRecipes`, `ManaCircuitRecipes`, `ManaCondenserRecipes`, `ManaHatchRecipes`, `ManaMachineBlockRecipes`, `ManaMachineRecipes`, `ManaMachineUpgradeRecipes`, `ManaPoolRecipes`, `ManaReactorRecipes`, `ManaRecipes`, `ManaTransformerRecipes`, `MeteorCapturerRecipes`, `MeteorRitualGuideRecipes`, `PerfectMineKeyRecipes`, `RitualMechanicalRecipes`, `RuneAltarRecipes`, `runeRitualRecipes`, `SalvagingRecipes`, `TerraPlateRecipes`, `TwistCollapseRecipes`, `WishingWillRecipes`, `ZenithRecipes`。

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| 配方移除清单 | `data/recipe/ManaRecipeRemoval.java`（`final`，`REMOVED_RECIPE_IDS: List<String>` 共 36 条精确 ID，含 `extrabotany:pleiades_combat_maid_headgear/skirt/suit/boots` 四件女仆套；`init()` 无参，逐条 `RecipeRemovalHelper.remove(new RemoveFilter().id(recipeId))`） |
| GTAddon 移除入口 | `CTNHManaGTAddon.removeRecipes(Consumer<ResourceLocation> ignoredConsumer)`：先 `ManaRecipeRemoval.init()`，再用 `RemoveFilter` 删除 `bloodmagic:altar`、`botania:petal_apothecary`、`botania:runic_altar`、`botania:terra_plate`、`extrabotany:petal_apothecary`（`.type(...)`）与 `mythicbotany:.*_runic_altar`（`.idRegex(...)`）、`bloodmagic:soulforge`（`.type(...)`） |
| 配方重注册 | `CTNHManaGTAddon.changeId(Consumer<FinishedRecipe>)`：把被删配方的 ID 改写到 `ctnhmana` 命名空间后重新注册 |
| GT/机器配方 | `data/recipe/` 顶层 33 个 `*Recipes` 类 |
| 跨 mod builder | `data/recipe/builder/{botania(7), bloodmagic(2), apotheosis(2)}` + `data/recipe/utils/BotaniaIngredients` |
| 条件与自定义逻辑（被配方引用） | `api/recipe/condition/*`、`api/recipe/customlogic/*` |
| datagen 接线 | `data/CMDatagen.java`：`ProviderType.LANG` → `EnglishLangHandler`、CTNH-Lib `CNLANG` → `ChineseLangHandler`、`FLUID_TAGS` → `FluidTypeTags`、`ITEM_TAGS` → `ItemTags`，并先 `REGISTRATE.addLangProcessor()` |
| SavedData | `data/ManaData.java`（`SavedData`，名 `ctnhmana_manadata`，`ManaLevel` 按 `BT/BM/ARS/GT` 记录魔法等级，`isZenithOpen` / `getBooleanTag` / `setBooleanTag` 走通用 tag） |
| tag 与 lang | `data/tags/ItemTags.java`（元素、符文阶级、尖塔升级、`APOTHEOSIS_GEMS`）、`data/tags/FluidTypeTags.java`（`BLOOD`）、`data/lang/{EnglishLangHandler, ChineseLangHandler, AHCCRuneLang}` |
| 材料 | `data/materials/BotaniaMaterials.java`（配合 `registry/CMMaterials` 与 `registry/GTMaterialAddon`） |

## CONVENTIONS
- 遵循模块主文档的动态包与注册对象规则：`addRecipes()` 产出为运行时动态包，`runData` 不生成对应 JSON。
- 移除只能走 CTNH-Lib `RecipeRemovalHelper.RemoveFilter`：`.id(String)` 精确 ID、`.type(String)` 匹配 `modid:类型`（取配方 path 首段）、`.idRegex(String)` 正则；顶层字段按 AND 组合，另有 `.not(...)` / `.or(...)`。精确 ID 批量维护在 `ManaRecipeRemoval.REMOVED_RECIPE_IDS`。
- `apotheosis:salvaging/*` 的移除与重注册（改挂 `ctnhmana:salvaging/*`）必须与 `SalvagingRecipes` / `RuneSalvagingRecipes` 成对修改。
- 所有文案经 CTNH-Lib lang provider（`com.ctnhlang.CN` / `EN` 注解或 `Lang#translate()`）；lang handler 只做接线，不硬编码中文。
- `ITEM_TAGS` / `FLUID_TAGS` 用 `addOptional(ForgeRegistries.…getKey(...))` 写入，新增 tag 常量放 `registry/CMTags`。

## ANTI-PATTERNS
- 使用 `DataFilterPack.removeRecipeType` / `removeRecipe`，或自建 `Consumer<ResourceLocation>` 删除循环。
- 在 `ManaRecipeRemoval` + `CTNHManaGTAddon.removeRecipes` 之外用字符串 ID 删配方。
- 期望 `runData` 为 GT/动态配方产出 JSON。
- 用不变的 ID 重新注册被删配方（会被过滤），而不走 `changeId(...)`。
- 手改 `src/generated/resources` 下的产物。

## SCOPE
数据定义与配方数据；游戏逻辑落在 `api/recipe/*` 与 `common/multiblock/`，注册对象定义落在 `registry/*`。

## READ WHEN
- 编辑任意 `data/recipe/*`、`data/recipe/builder/*` 或 `ManaRecipeRemoval`。
- 新增/修改 tag 或双语 lang 条目。
- 新增材料或改动 `ManaData` 的持久化字段。

## SOURCE OF TRUTH
- `com.magicbee.ctnhmana.data` 目录树与 `CTNHManaGTAddon.addRecipes()` / `removeRecipes()`。
- CTNH-Lib 的 `tech.vixhentx.mcmod.ctnhlib.data.recipe.RecipeRemovalHelper`（`RemoveFilter` 语义以此为准）。

## WORKFLOW
1. 新增配方 → 在对应 `*Recipes` 类里写，并确认已在 `CTNHManaGTAddon.addRecipes()` 接线。
2. 删除外部配方 → 精确 ID 进 `ManaRecipeRemoval.REMOVED_RECIPE_IDS`，按类型/正则的进 `removeRecipes(...)`。
3. tag/lang 改动跑 `:modules:CTNH-Mana:runData`；配方改动在游戏内或 `ConfigHolder.dev.dumpRecipes` 验证。
4. `data/recipe/*` 增删或移除规则变化时同步更新本文件。