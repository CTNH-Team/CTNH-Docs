# CTNH-BIO REGISTRY DOMAIN

## OVERVIEW
Bio 的注册中枢（17 个 Java 文件）：物品、方块、实体、机器、多方块、材料、效果、血清、音效、tag、配方类型、配方、配方 capability、配方条件与创造栏。

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Registrate 根 | `registry/CBRegistrate.java`（`extends` CTNH-Lib `CNRegistrate`） |
| 物品 / 方块 / 实体 | `registry/CBItems.java`, `registry/CBBlocks.java`, `registry/CBEntities.java`, `registry/CBMaterialItems.java` |
| 机器 / 多方块 | `registry/CBMachines.java`, `registry/CBMultiblocks.java` |
| 材料 / 效果 / 血清 / 音效 / tag | `registry/CBMaterials.java`, `registry/CBMobEffects.java`, `registry/CBSerums.java`, `registry/CBSoundEntries.java`, `registry/CBTags.java` |
| 配方类型 / 配方 / capability / 条件 | `registry/CBRecipeTypes.java`, `registry/CBRecipes.java`, `registry/CBRecipeCapabilities.java`, `registry/CBRecipeConditions.java` |
| 创造栏 | `registry/CBCreativeModeTabs.java` |
| 机器配方修饰符 | `api/recipe/CBRecipeModifiers.java`（`BIO_TIER_CHECK`, `BIO_ELECTRIC_OVERCLOCK`, `BIO_OC_NON_PERFECT`, `autoBatchMode`） |

## CONVENTIONS
- 注册类统一 `CB` 前缀，且只在 `registry/` 内声明与初始化。
- `CTNHBioGTAddon` 是 GT 侧入口：`initializeAddon()` → `CBItems.init()` + `CBBlocks.init()`；`registerRecipeCapabilities()` → `CBRecipeCapabilities.init()`（把 `NUTRIENT` / `ENTITY` / `MODEL` / `COGNI_ITEM` 注册到 `GTRegistries.RECIPE_CAPABILITIES`）；`addRecipes(provider)` → `CBRecipes.init(provider)`；`removeRecipes(consumer)` → `RecipeRemoval.init(consumer)`；`registerElements()` → `CBElements.init()`。
- `CBRecipes.init` 的挂载顺序：`LivingMachineRecipes` → `DecomposerRecipes` → `BasicLivingRecipes` → `GreatFleshRecipes` → `BioelectricForgeRecipes` → `BioReactorRecipes` → `DigesterRecipes` → `HostileObservationRecipes` → `CommonRecipes` → `CogniRecipes` → `VanillaRecipes` → `recipeAddition`（为非 GT 工具配方）。
- 机器注册经 `CBRegistrate` 的两个 builder：`livingMachine(tier, name, ...)`（机器名 = `GTValues.VN[tier]` 小写 + `_` + `name`；`LivingMetaMachineItem` / `LivingMetaMachineBlockEntity`；配方修饰符 `BIO_OC_NON_PERFECT` + `autoBatchMode`；`hasBER(false)`；客户端经 `LivingMetaMachineBERProvider.registerRenderer` 注册渲染）与 `biomultiblock(name, ...)`（`allowFlip(false).allowExtendedFacing(false)`）。
- `CBRecipeConditions.EFFECT` 注册到 `GTRegistries.RECIPE_CONDITIONS`（`init()` 为空实现，注册在静态初始化）。
- `CBSerums` 用 `DeferredRegister` + `makeRegistry`，`PRIMORDIAL_SERUM` 由 `CommonProxy` 构造期注册到 mod 事件总线。
- `CBTags` 用 `TagUtil` 定义 `growable` / `growing_replaceable` / `forge:hatch` / `growable_block` / `forge:foods` / Biomancy 肉 tag / 营养与胃酸流体 tag。

## ANTI-PATTERNS
- 同一个条目既在 `registry/` 注册、又在 `CommonProxy` 里重复注册。
- 在 `registry/` 之外（`common/`、`machine/`、`api/`）声明或初始化注册对象。
- 绕过 `CBRegistrate` 的 `livingMachine` / `biomultiblock` builder 直接手搓活体机器注册，导致 BE、渲染与配方修饰符不一致。

## SCOPE
本域覆盖 `src/main/java/com/moguang/ctnhbio/registry` 下的全部类。

## READ WHEN
- 新增或修改 Bio 的物品、方块、实体、机器、多方块、材料、血清或配方类型。

## SOURCE OF TRUTH
- `registry/CBRegistrate.java` 与 `CTNHBioGTAddon.java` 的钩子顺序。

## WORKFLOW
1. 先确定条目属于哪个注册类分组。
2. 核对 GT addon 钩子顺序与数据生成引用。
3. 涉及数据时跑 `:modules:CTNH-Bio:runData`，否则跑 `:modules:CTNH-Bio:build`。
