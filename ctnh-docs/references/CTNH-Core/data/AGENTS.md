# CTNH-CORE DATA DOMAIN

## OVERVIEW
`src/generated/resources` 的数据生成源码（149 个 Java 文件）：按 age/chain/域拆分的配方生成器、tags、材料（26 个材料集）与世界生成 provider。

## STRUCTURE
```text
data/
|-- CTNHCoreDatagen.java          # datagen 入口
|-- CTNHMaterialFlags.java
|-- CreateRecipeTypes.java        # mechanicalTier 用 Math.min(tier, 5)，不是 *2
|-- item/                         # CrystalItems
|-- machines/                     # GTNNMachines
|-- materials/                    # 26 个材料集：BauxiteProcessingMaterials、BoronChainMaterials、GoldChainMaterials、NaquadahMaterials、PlatinumLineMaterials、RareEarthMaterials、RareearthBastnasiteChain 相关、WetWareLineMaterials、ZrHfSeparationMaterials ...
|-- tags/                         # CTNHBiomeTagsProvider, CTNHEntityTypeTagsProvider, CTNHExtraBlockTagsProvider, CTNHExtraFluidTagsProvider, CTNHExtraItemTagsProvider, ItemTags, StoneTags, TagClearHelper
|-- worldgen/                     # CTNHBiomeModifiers
`-- recipe/
    |-- CTNHCoreRecipeAddition.java  # addRecipes() 分发根
    |-- RecipeRemoval.java           # 只登记 ID 过滤规则（通用过滤在 CTNH-Lib）
    |-- WaferRecipes.java            # 精密电路晶圆掩膜
    |--（34 个顶层类）
    |-- age/                      # 10：LV..ZPM, PrimitiveKinetic
    |-- chain/                    # 30：AlumiumChain, BoronChain, BrineChain ...
    |-- cogniassembly/            # WetwareCircuit
    |-- create/                   # CafeRecipes, CreateOreExcavationRecipes, CreateRecipeJsonHelper, CreateRecipes, CreateVintageRecipe, DieselGeneratorRecipes
    |-- generated/                # HyperRotorRecipes
    |-- immersiveaircraft/        # ImmersiveAircraftRecipes
    |-- mana/                     # DigesterRecipes, MiscManaRecipes, TwistedFusionRecipes
    |-- migrated/                 # AE2ScriptRecipe, AvaritiaScriptRecipes, BioScriptRecipes, GtceuScriptRecipes
    |-- modmodify/                # EIORecipes
    |   `-- omnicells/            # QuantumOmniRecipes
    |-- multiblock/               # 11：AcceleratorRecipes, AstronomicalObservatoryRecipes, NaquadahReactorRecipes ...
    |-- utils/                    # ComputationModifier, KeepIngredientRecipeHelper, NuclearComposition
    `-- wood/                     # WoodMachineRecipes, WoodTypeEntries, WoodTypeEntry
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Datagen 入口 | `data/CTNHCoreDatagen.java` |
| 配方分发根 | `data/recipe/CTNHCoreRecipeAddition.java` |
| 铝土矿链 | `data/materials/BauxiteProcessingMaterials.java`（IMPURE/PURE_SODIUM_ALUMINATE_SOLUTION, RED_MUD, TITANYL_SULFATE）, `data/recipe/chain/AlumiumChain.java` |
| 硼链 | `data/materials/BoronChainMaterials.java`, `data/recipe/chain/BoronChain.java` |
| 金链改名 | `data/materials/GoldChainMaterials.java`（原 CrudeGoldRefiningMaterials） |
| 晶圆/精密电路 | `data/recipe/WaferRecipes.java` |
| Create 动力换算 | `data/CreateRecipeTypes.java`（tier 换算修正） |
| 按 age 的配方 | `data/recipe/age/`（LV..ZPM, PrimitiveKinetic） |
| 加工链 | `data/recipe/chain/`（30 条链） |
| Create/联动配方 | `data/recipe/create/`, `data/recipe/immersiveaircraft/`, `data/recipe/multiblock/` |
| 木材机器配方 | `data/recipe/wood/` |
| 迁移/脚本配方 | `data/recipe/migrated/` |
| 修改他 mod 配方 | `data/recipe/modmodify/`, `data/recipe/modmodify/omnicells/` |
| Mana 桥接配方 | `data/recipe/mana/` |
| 生成的配方 Java | `data/recipe/generated/` |
| 配方辅助 | `data/recipe/utils/` |
| 材料 | `data/materials/`（26 个材料集）, `data/CTNHMaterialFlags.java` |
| Tags/世界生成 | `data/tags/`, `data/worldgen/` |

## CONVENTIONS
- `src/generated/resources` 由 `:modules:CTNH-Core:runData` 产出；绝不手工编辑生成的 JSON。
- 经 `CTNHCoreGTAddon.addRecipes()` 注册的 GT/GMT 配方属运行时动态数据包（`GTDynamicPackContents` / CTNH-Lib `CTNHDynamicDataPack`）：`runData` 对其**不产出 JSON**，它们不出现在 `src/generated/resources` 是预期行为，不是失败。完整声明见模块主文档 CONVENTIONS。
- 配方生成器按 age、chain、Create/联动、迁移脚本、mod 修改、mana 桥接、多方块与木材域拆分。
- 配方删除：`data/recipe/RecipeRemoval.java` 只登记过滤规则（`id`/`idRegex`/`mod`/`type`/`not`/`or`），通用过滤与 `RecipeManager.apply()` 注入由 CTNH-Lib `RecipeRemovalHelper`（`mixin/RecipeManagerApplyMixin`）提供，Core 侧不重复实现。动态配方刻意不过滤。
- `gtceuRemovals()` 经"清理第三批remove"（6eb50b5d）收缩为 12 条精确 ID：`gtceu:shaped/ulv_machine_hull`、`gtceu:shaped/small_gear_andesite_alloy`、`gtceu:shaped/gear_andesite_alloy`、`gtceu:shaped/small_gear_wood`、`gtceu:shaped/gear_treated_wood`、`gtceu:extractor/extract_ammonium_chloride_dust`、4 条 `smashing_factory_recipes/.../macerate_*_rail`、`gtceu:basic_mechanism`、`gtceu:shaped/lv_thermal_centrifuge`。原有批量电解（`decomposition_electrolyzing_*`）、铂族泥（`pgs_from_*`）、`space_suit`/`space_helmet`、GTCEu 默认电动部件（`gtceu:shaped`/`gtceu:assembler` 的马达/活塞/传送带/泵/机械臂/流体调节器/发射器，均按 `idRegex` 登记）、`electric_circuit_lv/mv`、`lv_polarizer`、`foil_*`、`spring_*`、`asbestos`、`nan_certificate` 等条目不再登记。`idRegex` 机制与其余分组删除规则保留；`remove(new RemoveFilter...` 全文件约 250 处。
- age 电动马达配方：6eb50b5d 为 MV/HV/EV/IV 补齐 `assembler/electric_motor_<tier>`（`ASSEMBLER_RECIPES`，`duration(100).EUt(VA[LV])`，材料与同档 `crafttable/electric_motor_<tier>` 一致）；LV 的 assembler 电机配方此前已存在。各电压档因此同时提供 `crafttable/electric_motor_<tier>`（`VanillaRecipeHelper.addShapedRecipe`）与 `assembler/electric_motor_<tier>` 两条配方；EV/HV/IV 用 `GTRecipeTypes.ASSEMBLER_RECIPES`，MV 用静态导入 `ASSEMBLER_RECIPES`。同提交移除 LV 的 `addPolarizerRecipes()`，`gtceu:shaped/lv_polarizer` 的移除规则一并删除。
- 引用物品/方块/流体**必须**使用静态注册对象（`GTMaterials.Iron`, `CTNHBlocks.*`, `TagPrefix.ingot`, `AEItems.X` 等），**禁止** `ResourceLocation` 字符串解析 + `ForgeRegistries` 查找，除非该对象不存在。见模块主文档 CONVENTIONS。
- `CreateRecipeTypes` 的 mechanicalTier 换算为 `Math.min(GTUtil.getTierByVoltage(EUt), 5)`，适用于 MECHANICAL_PRESSOR/MIXER/CENTRIFUGE/SIFTER/LATHE；`*2` 已被移除。
- 铝土矿材料：`IMPURE_SODIUM_ALUMINATE_SOLUTION` 公式 `(TiO2)(?)+4NaAl(OH)4+nH2O`（原 Aluminium Hydroxide）、`PURE_SODIUM_ALUMINATE_SOLUTION` `NaAl(OH)4+H2O`、`RED_MUD` `(TiO2)(Fe(OH)3)(?)+nH2O`、`SODIUM_HYDROXIDE_BAUXITE` `(TiO2)(?)(Al2O3)2+4NaOH+nH2O` 等；lang 键 `impure/pure_sodium_aluminate_solution` 取代了 `aluminium_hydroxide_solution`。
- AlumiumChain 调参：绿蓝宝石/蓝宝石/红宝石离心改 `VA[HV]`，硅/镁 `VA[MV]`，Ti 产量略升、Al 产量略降，HCl 用量下降。

## ANTI-PATTERNS
- 手工编辑 `src/generated/resources`；应改 datagen Java 后跑 `runData`。
- 把宽泛的跨 mod 配方塞进 feature 模块；Core 才是聚合方。
- 新增加工链却不注册进分发根（`CTNHCoreRecipeAddition`）。
- 在 Core 侧重新实现配方删除的通用过滤逻辑（已由 CTNH-Lib `RecipeRemovalHelper` 提供）。

## SCOPE
适用于 `src/main/java/io/github/cpearl0/ctnhcore/data` 及其子包。

## READ WHEN
- 在 Core 中新增或修改配方、tags、材料或世界生成 provider。
- 排查生成的资源与 datagen 输出不一致。

## SOURCE OF TRUTH
- `data/CTNHCoreDatagen.java`、`data/recipe/CTNHCoreRecipeAddition.java` 与 `data/recipe/` 下的 provider。
- 生成产物：`src/generated/resources`。

## WORKFLOW
1. 找到匹配的配方域（age/chain/create/migrated/modmodify/mana/multiblock/wood）。
2. 改生成器，然后跑 `:modules:CTNH-Core:runData`。
3. 检查生成资源 diff；datagen 后跑 `spotlessCheck`。
