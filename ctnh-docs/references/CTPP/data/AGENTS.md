# CTPP DATA DOMAIN

## OVERVIEW
CTPP 的数据生成源（52 个 Java 文件）：配方 provider、tag 与模型，产出到 `src/generated/resources`。配方生成位于**顶层** `data/recipe/`（不存在 `common/data/recipe`）。

## STRUCTURE
```text
data/
|-- CTPPDatagen.java, CuriosTags.java, ToolboxBlockstates.java
|-- tags/                      # BlockTags, CustomTags, FluidTags, ItemTags
`-- recipe/
    |-- 12 顶层: CTPPRecipes, BigDamRecipes, BoomOfCreateRecipes, DieselGeneratorRecipes, ItemRecipes,
    |             KineticGeneratorRecipes, KineticSteamTurbineRecipes, PlaceableEmitterRecipes,
    |             SeaweedFarmRecipes, SmashingFactoryRecipes, ToolRecipes, WindmillControlRecipes
    |-- builder/               # AcidWashingRecipeGen, BreathingRecipeGen, CTPPProcessingRecipeBuilder,
    |                           CTPPRecipeBuilder, CTPPRecipeHelper, CTPPRecipeProvider
    |   |-- create/            # 11: Compacting, Crushing, Cutting, Filling, ItemApplication, MechanicalCrafting,
    |   |                       Milling, Mixing, Pressing, SequencedAssembly, Splashing
    |   |-- diesel/            # BasinFermenting, Distillation, Hammer, WireCutting
    |   `-- vintage/           # AbstractVintageRecipeBuilder, Centrifugation, Coiling, Curving, Hammering,
    |                           Pressurizing, Turning, Vacuumizing, Vibrating, VintageRecipeResult
    `-- fanprocessing/         # CTPPFanProcessingTypes, CTPPRecipeTypeInfo
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| datagen 入口 | `data/CTPPDatagen.java`（`init()` 与 `addToolboxData(event)`；后者由 `CommonProxy.gatherData()` 调用） |
| 配方生成 | `data/recipe/`（12 个顶层类，由 `CTPPGTAddon.addRecipes()` → `CTPPRecipes.init(provider)` 分发） |
| 可放置发射器配方 | `data/recipe/PlaceableEmitterRecipes.java`（对 LV–OpV 逐级生成 `placeable_emitter_<tier>` 成形配方） |
| Create builder | `data/recipe/builder/create/`（11） |
| Diesel builder | `data/recipe/builder/diesel/`（4） |
| Vintage builder | `data/recipe/builder/vintage/`（8 个 builder + 抽象基类 + `VintageRecipeResult`） |
| 风扇处理 | `data/recipe/fanprocessing/`（`CTPPFanProcessingTypes`、`CTPPRecipeTypeInfo`） |
| tag | `data/tags/`（BlockTags、CustomTags、FluidTags、ItemTags） |
| 工具箱方块状态 | `data/ToolboxBlockstates.java` |
| Curios tag | `data/CuriosTags.java` |
| 机器模型 | `common/data/model/CTPPMachineModels.java`（在 common 域） |

## CONVENTIONS
- `src/generated/resources` 由 `:modules:CTPP:runData` 产出（当前 444 个 JSON：`assets/ctpp/` 下的 lang/blockstates/models，以及 `data/{ctpp,create,curios,forge,gtceu,minecraft}/` 下的配方与 tag）；不要手改生成物。
- **GTM 动态包**：GT/GMT 配方经 `CTPPGTAddon.addRecipes()` 注册为运行时动态数据包（`GTDynamicPackContents` / CTNH-Lib `CTNHDynamicDataPack`），`runData` 对其**不产出 JSON**；静态 `src/generated/resources` 只含 tags/lang/models/worldgen/非 GT 配方。
- `MACERATOR_RECIPES` → `SMASHING_FACTORY_RECIPES` 的转换在 `CTPPRecipeTypes.init()` 内挂钩；`MIXER_RECIPES` → `KINETIC_MIXER_RECIPES` 的挂钩被注释掉，不要依赖。
- `MillingRecipeBuilder` 的 `processingTime` 默认 100 tick，必须为正（非正则抛 `IllegalArgumentException`），序列化为 `processingTime`。
- `PlaceableEmitterRecipes` 按 `CTPPMachines.PLACEABLE_EMITTER` 的等级表生成配方；GTCEu 高阶内容关闭时对应 emitter 物品为 `null`，代码已跳过。
- 静态机器部件模型在 `src/main/resources`；重生成前先确认路径。

## ANTI-PATTERNS
- 把所有配方 JSON 等同看待：风扇催化产物与静态资源位于不同源码根，GT 配方根本不在 JSON 里。
- 把 `MillingRecipeBuilder` 的 `processingTime` 设为 0 或负数。
- 手改生成的语言文件 / 方块状态 JSON。
- 期望 `runData` 产出 GT 配方 JSON 并据此验证配方。

## SCOPE
适用于 `src/main/java/com/mo_guang/ctpp/data` 及其子包。

## READ WHEN
- 新增 CTPP 的配方、tag 或模型。
- 修改 Create / Diesel / Vintage 配方 builder，尤其是 `MillingRecipeBuilder` 的处理时间。
- 修改发射器、工具箱或其他生成物。

## SOURCE OF TRUTH
- `data/CTPPDatagen.java` 与 `data/recipe/CTPPRecipes.java`。
- `data/recipe/builder/create/MillingRecipeBuilder.java` 的处理时间。
- `registry/CTPPRecipeTypes.java` 的 `init()` 转换挂钩。

## WORKFLOW
1. 改对应的 provider，再跑 `:modules:CTPP:runData`。
2. 检查生成资源差异；跑 `spotlessCheck`。
3. 改 `MillingRecipeBuilder` 时确认 `processingTime` 为正且 JSON 输出符合预期。
