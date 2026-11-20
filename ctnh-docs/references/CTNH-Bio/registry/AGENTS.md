# CTNH-BIO REGISTRY DOMAIN

## OVERVIEW
Bio 的注册中枢（17 个 Java 文件）：物品、方块、实体、机器、多方块、材料、效果、血清、音效、tag、配方类型、配方、配方 capability、配方条件与创造栏。

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Registrate 根 | `registry/CBRegistrate.java`（`extends` CTNH-Lib `CNRegistrate`） |
| 物品 / 方块 / 实体 | `registry/CBItems.java`, `registry/CBBlocks.java`, `registry/CBEntities.java`, `registry/CBMaterialItems.java` |
| 湿件元件 / 电路基板 / 生物核心 | `registry/CBItems.java`（`WETWARE_CAPACITOR` 等五个湿件元件、`WETWARE_CIRCUIT_BOARD` 与 `WETWARE_PRINTED_CIRCUIT_BOARD`、`BIO_CORES` 等级数组与 `SYNET_CORE` / `META_CORE` / `NOVA_CORE` / `OMNI_CORE`） |
| 物品 tooltip 文案 | `registry/CBItems.java` 类顶部 `@CN` / `@EN` 注解的 `static Lang` 字段（`WetwareCapacitorTooltip` … `WetCircuitBoardTooltip`） |
| 流体容器物品 | `registry/CBItems.java` 的 `ORGANIC_VIAL` / `ORGANIC_BEAKER`（`OrganicFluidStats.create(...)` + `cellName()`） |
| 机器 / 多方块 | `registry/CBMachines.java`, `registry/CBMultiblocks.java` |
| 材料 / 效果 / 血清 / 音效 / tag | `registry/CBMaterials.java`, `registry/CBMobEffects.java`, `registry/CBSerums.java`, `registry/CBSoundEntries.java`, `registry/CBTags.java` |
| 配方类型 / 配方 / capability / 条件 | `registry/CBRecipeTypes.java`, `registry/CBRecipes.java`, `registry/CBRecipeCapabilities.java`, `registry/CBRecipeConditions.java` |
| 创造栏 | `registry/CBCreativeModeTabs.java` |
| 机器配方修饰符 | `api/recipe/CBRecipeModifiers.java`（`BIO_TIER_CHECK`, `BIO_ELECTRIC_OVERCLOCK`, `BIO_OC_NON_PERFECT`, `autoBatchMode`） |

## CONVENTIONS
- 注册类统一 `CB` 前缀，且只在 `registry/` 内声明与初始化。
- `CTNHBioGTAddon` 是 GT 侧入口：`initializeAddon()` → `CBItems.init()` + `CBBlocks.init()`；`registerRecipeCapabilities()` → `CBRecipeCapabilities.init()`（把 `NUTRIENT` / `ENTITY` / `MODEL` / `COGNI_ITEM` 注册到 `GTRegistries.RECIPE_CAPABILITIES`）；`addRecipes(provider)` → `CBRecipes.init(provider)`；`removeRecipes(consumer)` → `RecipeRemoval.init(consumer)`；`registerElements()` → `CBElements.init()`。
- `CBRecipes.init` 的挂载顺序：`LivingMachineRecipes` → `DecomposerRecipes` → `BasicLivingRecipes` → `GreatFleshRecipes` → `BioelectricForgeRecipes` → `BioReactorRecipes` → `DigesterRecipes` → `HostileObservationRecipes` → `CommonRecipes` → `CogniRecipes` → `VanillaRecipes` → `recipeAddition`（为非 GT 工具配方）。
- 机器注册经 `CBRegistrate` 的两个 builder：`livingMachine(tier, name, ...)`（机器名 = `GTValues.VN[tier]` 小写 + `_` + `name`；`LivingMetaMachineItem` / `LivingMetaMachineBlockEntity`；配方修饰符 `BIO_OC_NON_PERFECT` + `autoBatchMode`；`hasBER(false)`；客户端经 `LivingMetaMachineBERProvider.registerRenderer` 注册渲染）与 `biomultiblock(name, ...)`（`allowFlip(false).allowExtendedFacing(false)`）。`CBMultiblocks.HOSTILE_OBSERVER` 走 `REGISTRATE.multiblock(...)` 自行注册（`HostileObserverMachine` 不是活体机器），并自己调 `allowFlip(false).allowExtendedFacing(false)`。
- `CBRecipeConditions.EFFECT` 注册到 `GTRegistries.RECIPE_CONDITIONS`（`init()` 为空实现，注册在静态初始化）。
- `CBSerums` 用 `DeferredRegister` + `makeRegistry`，`PRIMORDIAL_SERUM` 由 `CommonProxy` 构造期注册到 mod 事件总线。
- `CBTags` 用 `TagUtil` 定义 `growable` / `growing_replaceable` / `forge:hatch` / `growable_block` / `forge:foods` / Biomancy 肉 tag / 营养与胃酸流体 tag。
- 湿件元件与电路基板用 GTCEu `ComponentItem::create` 注册；tooltip 经 `CBItems.attach(new TooltipBehavior(list -> ...))` 挂载，文案取自类顶部 `@CN` / `@EN` 注解的 `static Lang` 字段（类注解 `@Category("item")` + `@Suffix("tooltip")`），tooltip 不硬编码字面量；物品显示名另由条目的 `.cnlang(...)` / `.lang(...)` 提供。
- `WETWARE_CIRCUIT_BOARD` 与 `WETWARE_PRINTED_CIRCUIT_BOARD` 共用 `WetCircuitBoardTooltip`；湿件元件稀有度取 Biomancy `ModRarities.RARE`，四个生物核心取 `ModRarities.VERY_RARE`，核心 tooltip 用 `Lang[]`（首行等级 + 描述行）。
- `CBItems.init()` 先调 `CBMaterialItems.generateTools()`，再按 `GTValues` 等级索引填 `BIO_CORES`：LV 直接引用 Biomancy `ModItems.PRIMORDIAL_CORE`，MV / HV / EV / IV 为模块自有的 `SYNET_CORE` / `META_CORE` / `NOVA_CORE` / `OMNI_CORE`。
- 湿件与幽匿组装中间品（`WETWARE_PROCESSOR_COMPUTER_UNFINISHED`、`WETWARE_PROCESSOR_MAINFRAME_UNFINISHED`、`SCULK_CELL_UNFINISHED`）用 `common/item/AssemblyStepItem`，步骤号存于物品 NBT 的 `COGNI_AESSEMBLY_STEP` 常量（键字符串为 `cogin_assembly_step`，定义在 `data/recipe/CogniRecipeBuilder`）。
- 流体容器物品用 `OrganicFluidStats.create(capacity, maxFluidTemperature, gasProof, acidProof, cryoProof, plasmaProof, allowPartialFill)` + `cellName()`（`ICustomDescriptionId` 把所含流体名代入物品名模板的 `%s`），并 `setData(ProviderType.ITEM_MODEL, NonNullBiConsumer.noop())` 关掉自动模型；`ORGANIC_VIAL` 容量 `FluidType.BUCKET_VOLUME / 10`、另挂 `VialCraftingRemainingItem`，`ORGANIC_BEAKER` 容量 `FluidType.BUCKET_VOLUME / 2`、耐酸且允许部分填充。

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
