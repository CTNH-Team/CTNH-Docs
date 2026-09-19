# CTNH-CORE MODULE

## OVERVIEW
CTNH-Core 是 CTNH 整合包的核心模块，包根 `io.github.cpearl0.ctnhcore`，432 个 Java 文件。承载 GT/GregTech 机器实现（多元件多方块、发电机、动力机器）、材料与配方链、注册与数据生成、跨 mod 集成以及 Mixin 补丁。入口类：`CTNHCore`（mod 主类）、`CTNHCoreGTAddon`（GT addon，注册配方类型/材料/机器）、`CTNHConfig`（配置）；代理为 `CommonProxy` / `ClientProxy`。

## STRUCTURE
源码根 `modules/CTNH-Core/src/main/java/io/github/cpearl0/ctnhcore/`（括号内为该域 Java 文件数）

```
ctnhcore/
├── CTNHCore / CTNHCoreGTAddon / CTNHConfig      # mod 入口、GT addon、配置
├── api/        (17) CTNHMultiblockBuilder；Pattern/{CTNHBlockMaps, CTNHPredicates, AsynBlockPattern, CTNHBoilerFireboxType}；
│                     data/material/{CTNHMaterialIconSet, CTNHMaterialIconType, CTNHPropertyKeys, CatalystProperty}；
│                     gui/CTNHGuiTextures；jade/{MultithreadRecipeLogicProvider, MultithreadRecipeOutputProvider, ThreadStatusProvider}（整体注释停用）；
│                     machine/feature/{IDigitalMiner, IDynamicCasing}；machine/multiblock/UnlimitedItemStackTransfer；recipe/DigitalMinerLogic
├── client/     (22) ClientProxy, ClientUtil；model/{ModelBase, ModelDefinition, TemplateModel, TurbineRotorModel}；
│                     ponder/{CTNHCorePonderPlugin, CTNHCorePonderSceneBuilder, CTNHCorePonderScenes, CTNHCorePonderTags,
│                             Electric/{GregTechMultiblocks, NeutronActivator}, Kinetic/{Meadow, MechanicalExporter}}；
│                     renderer/{ArcBlockRender, AstralPlanetSpecialEffects, DynamicCasingRender, HyperPlasmaTurbineRender,
│                               MartialMoralityEyeRender, TurbineRotorRender, utils/RenderUtils}；util/SnowOverlayQuadOffset
├── common/     (124) 代理与机器/方块/物品实现
│   ├── block/ (CTNHFusionCasingType, CoilType, MaterialTurbineRotorBlock, PhotovoltaicBlock, SpaceStructuralFramework,
│   │           TurbineRotorBlock, blockdata/{IPBData, ISSFData, PlanetMinerData})
│   ├── blockentity/TurbineRotorBE；capability/EIOCapacitorProvider；enchantment/TemperatureEnchantment
│   ├── entity/monster/{astralslime/AstralSlime, sightseerspitter/SightSeerSpitter}
│   ├── gui/ (MachineModeFancyConfiguratorTest, SimpleNumberInputWidget, WPAAcceleratorGui,
│   │         terminal/TerminalInputWidget, widget/SimpleNumberInputWidget)
│   ├── item/ (18) ArkOfHomoItem, AstronomyCircuitItem, CatalystBehavior, ConnectTerminalItem, IDataItem, IDroneItem,
│   │              IThrowableItem, MEAdvancedTerminalItem/Behavior, MultiblockHelper, ProgramItem,
│   │              TurbineRotorItem/MaterialTurbineRotorItem, TagPrefixBehavior, ThrowableSummoner, debug/ReloadItem ...
│   ├── machine/ cover/CreativeEnergyCover；multiblock/{KineticElectricMultiblockMachine, LargeBottleMachine,
│   │            MultiblockComputationMachine, SlaughterHouseMachine, UnderfloorHeatingMachine}
│   │   ├── electric/ (29) AstronomicalMachine, BioMachine, ChemicalPlantMachine, FactoryMachine, MegaLCRMachine,
│   │   │                   NeutronActivatorMachine, PlanetMiner, WideParticleAccelerator, multithread/CNCAlloySmelter,
│   │   │                   rareearth/{ProcessControlMachine, ProcessControlProfile, ProcessControlled*MultiblockMachine} ...
│   │   ├── generator/ (12) Arc_Generator, Arc_Reactor, ChemicalGeneratorMachine, HyperPlasmaTurbineMachine,
│   │   │                    LargeNaquadahReactorMachine, MegaTurbineMachine, NanoscaleTriboelectricGenerator,
│   │   │                    NaqReactorMachine, PhotoVoltaicDroneStation, PhotovoltaicPowerStationMachine,
│   │   │                    WaterPowerStationMachine, WindPowerArrayMachine
│   │   ├── kinetic/ (5) IndustrialPrimitiveBlastFurnaceMachine, KineticCentrifugeMachine, KineticMixerMachine,
│   │   │                 MeadowMachine, NoEnergyMachine
│   │   ├── part/ (12) CTNHPartAbility, CatalystHatchPartMachine, CircuitBusPartMachine, CompilerMachine,
│   │   │                Creative*HatchPartMachine, DroneHolderMachine, HighSpeedPipeBlock,
│   │   │                NeutronAcceleratorMachine, NeutronSensorMachine
│   │   └── quantum/quantum_core
│   ├── simple/ (DigitalMiner, EfficiencyGeneratorMachine, HighPerformanceComputerMachine, SimpleComputationMachine)
│   ├── trait/ (ScalableReservoirComputingLogic, SimpleComputationContainer,
│   │           providable_net/{ProvidableNetInfo, ProvidableNetTrait, ProviderInfo})
│   ├── recipe/ (KeepIngredientShapedRecipe, NeutronActivatorCondition, PlantCasingCondition, TierCasingCondition,
│   │            builder/CTNHRecipeBuilder)
│   └── world/CTNHChunkLoading
├── data/       (149) CTNHCoreDatagen, CTNHMaterialFlags, CreateRecipeTypes；item/CrystalItems；machines/GTNNMachines；
│                     materials/ (26 个材料集，如 RareEarthMaterials, NaquadahMaterials, WetWareLineMaterials ...)；
│                     recipe/ (34 顶层 + age/10 + chain/30 + multiblock/11 + create/6 + migrated/4 + mana/3 + wood/3 +
│                              utils/3 + cogniassembly/1 + immersiveaircraft/1 + modmodify/2 + generated/1)；
│                     tags/ (8) CTNH*TagsProvider, ItemTags, StoneTags, TagClearHelper；worldgen/CTNHBiomeModifiers
├── event/      (5)   BuildTaskManager, DimensionFlightHandler, ForgeClientEventHandler, ForgeEventHandler,
│                     ProvidableNetEventHandler
├── integration/(7)   creatediesel/{DistillationCategoryLayout, GTBedrockOilBridge}；
│                     emi/{CTNHCoreEmiPlugin, CTNHExtraEmiPlugin}；ftbessentials/AsyncRtpManager；
│                     legendary/{ArmorModifier, UnderfloorHeatingSystemTempModifier}
├── mixin/      (47)  按目标 mod 分组：aecs, apotheosis, ars_nouveau, avaritia, create, creatediesel, dategen,
│                     eclipticseasons, eio, emi, ftbchunks, ftbessentials, gtceu(+orevein), javd, legendarysurvival,
│                     mc, tmrv, vintageimprovements；顶层 ChunkMixin, ChunkSerializerMixin, TagLoaderMixin
├── registry/   (50) 注册中枢：CTNHRegistration/CTNHRegistrate, CTNHItems, CTNHBlocks, CTNHBlockEntities,
│                     CTNHMultiblockMachines, CTNHRecipeTypes/Categories/Recipes/Conditions/Modifiers,
│                     machines/{CTNHMachines, GTMachineModify, multiblock/*}, material/{CTNHMaterials, CTNHMaterialFlags,
│                     CTNHMaterialBlocks, GTMaterialAddon}, ores/* (7), adventure/CTNHEnchantments, jade/CTNHJadePlugin（停用），
│                     sound/CTNHSoundEvents ...
└── utils/      (8)  CTNHCommonTooltips, CTNHMachineUtils, CTNHRecipeHelper, CoilTierHelper, LayeredBiMap,
                     MathUtils, OrientedItem, StructureUtils
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| mod 入口 / addon / 配置 | `CTNHCore`, `CTNHCoreGTAddon`, `CTNHConfig` |
| 注册框架与注册对象 | `registry/CTNHRegistration`, `registry/CTNHRegistrate`, `registry/CTNHItems`, `registry/CTNHBlocks`, `registry/CTNHBlockEntities`, `registry/CTNHCreativeModeTabs` |
| 机器注册与 GT 机器改动 | `registry/machines/CTNHMachines`, `registry/machines/GTMachineModify`, `registry/machines/multiblock/{MultiblocksA, MultiblocksB, MultiblocksC, GTNNMultiblocks, Mechanical, HyperPlasmaTurbineRegister, WindPowerArrayRegister}` |
| 配方类型 / 条件 / 修饰符 | `registry/CTNHRecipeTypes`, `registry/CTNHRecipeCategories`, `registry/CTNHRecipeConditions`, `registry/CTNHRecipeModifiers` |
| 材料与材料标志 | `registry/material/{CTNHMaterials, CTNHMaterialFlags, CTNHMaterialBlocks, GTMaterialAddon}`；材料集定义在 `data/materials/*` |
| 矿物与矿脉 | `registry/ores/*`（按维度拆分）, `registry/CTNHOres`, `registry/CTNHWorldgenLayers`, `registry/CTNHFluidVeins` |
| 多方块机器实现 | `common/machine/multiblock/electric/**`（29）、`generator/**`（12）、`kinetic/**`（5）、`part/**`（12）、`quantum/**`、顶层 5 个通用多方块 |
| 多方块构建与图案 | `api/CTNHMultiblockBuilder`, `api/Pattern/{CTNHBlockMaps, CTNHPredicates, AsynBlockPattern, CTNHBoilerFireboxType}` |
| 方块数据 / 方块实体 | `common/block/blockdata/{IPBData, ISSFData, PlanetMinerData}`, `common/blockentity/TurbineRotorBE`, `common/block/*` |
| 机器 GUI / widget | `common/gui/**`（含 `WPAAcceleratorGui`, `terminal/TerminalInputWidget`）, `api/gui/CTNHGuiTextures` |
| 客户端渲染 / 模型 / Ponder | `client/renderer/**`, `client/model/*`, `client/ponder/**` |
| 配方实现 | `data/recipe/**`（顶层 34；`age/`, `chain/`, `create/`, `multiblock/`, `migrated/`, `mana/`, `wood/`, `utils/`）, `data/recipe/CTNHCoreRecipeAddition` |
| 配方移除 | `data/recipe/RecipeRemoval`（只登记过滤规则；通用过滤与 `RecipeManager.apply()` 注入由 CTNH-Lib `RecipeRemovalHelper` 提供） |
| 数据生成 | `data/CTNHCoreDatagen`, `data/tags/**`, `data/worldgen/CTNHBiomeModifiers` |
| 跨 mod 集成 | `integration/**`（creatediesel, emi, ftbessentials, legendary） |
| Mixin 补丁 | `mixin/**`（按目标 mod 分组）；GT/GTCEu 相关在 `mixin/gtceu/**` |
| 通用工具 | `utils/{CTNHMachineUtils, CTNHRecipeHelper, CoilTierHelper, StructureUtils, MathUtils}` |

## DOMAIN GUIDE ROUTING
| Source area | Guide | Read before |
|-------------|-------|-------------|
| `api/**` | `ctnh-docs/references/CTNH-Core/api/AGENTS.md` | 新增多方块构建器 / 图案谓词 / 机器 feature 接口 |
| `client/**` | `ctnh-docs/references/CTNH-Core/client/AGENTS.md` | 新增渲染器 / 模型 / Ponder 场景 |
| `common/**` | `ctnh-docs/references/CTNH-Core/common/AGENTS.md` | 新增或修改机器、物品、方块、BE、GUI |
| `data/**` | `ctnh-docs/references/CTNH-Core/data/AGENTS.md` | 新增材料、配方、tag、矿石与世界生成 |
| `event/**` | `ctnh-docs/references/CTNH-Core/event/AGENTS.md` | 监听 Forge 事件 / 构建任务 / 区块网络 |
| `integration/**` | `ctnh-docs/references/CTNH-Core/integration/AGENTS.md` | 对接 EMI / Create Diesel / FTB / Legendary 等外置 mod |
| `mixin/**` | `ctnh-docs/references/CTNH-Core/mixin/AGENTS.md` | 打补丁到上游 mod 或 MC 本体 |
| `registry/**` | `ctnh-docs/references/CTNH-Core/registry/AGENTS.md` | 新增任何注册对象（物品/方块/BE/机器/配方类型） |
| `utils/**` | `ctnh-docs/references/CTNH-Core/utils/AGENTS.md` | 复用工具类而非另起实现 |

## CONVENTIONS
- **GTM 动态包**：GT/GMT 配方经 `CTNHCoreGTAddon.addRecipes()` 注册为运行时动态数据包（`GTDynamicPackContents` / CTNH-Lib `CTNHDynamicDataPack`），`runData` 对其**不产出 JSON**；静态 `src/generated/resources` 只含 tags/lang/models/worldgen/非 GT 配方。验证方式为游戏内或 `ConfigHolder.dev.dumpRecipes`。
- **注册对象优先**：引用物品/方块/流体**必须**使用静态注册对象（`GTMaterials.Iron`, `CTNHBlocks.*`, `CTNHItems.*`, `TagPrefix.ingot`, `AEItems.X`, `CBBlocks.X`, `CEItems.X`, `CMItems.X`, `CABlocks.X`, `CTPPBlocks.X`），**禁止** `ResourceLocation` 字符串解析 + `ForgeRegistries` 查找；字符串 ID 仅限无注册对象的场景（上游 mod 专属 ID、配方 ID、tag key、维度 ID）。
- **翻译在注册处声明**：方块中文名不用 `@Key("block.ctnhcore.*")` + `Lang` 字段，一律在注册时声明。纯方块走 `registry/CTNHBlocks` 的 `createCoilBlock(ICoilType, cnName)` / `createFireboxCasing(BoilerFireboxType, cnName)` / `createTurbineRotorBlock(name, R, G, B, A, cnName)` / `createRotateCasing(name, map, cnName)` → `.cnlang(cnName)`；多方块在 registrate 链上直接 `.cnLangValue("…")`；分级机器走 `utils/CTNHMachineUtils` 的 `registerTieredMachines(name, cnname, …)`（内部 `.cnLangValue(VNF[tier] + cnname)`）与 `registerLargeCombustionEngine(…, cnName)`。玩家可见文案与 lang 键名保持稳定，新增内容一律用此写法。
- **发电机功率读取**：发电机类机器（`common/machine/multiblock/generator/**`、`common/machine/simple/EfficiencyGeneratorMachine`）计算并行、输出功率与 GUI 显示时，必须使用 `recipe.getOutputEUt()`（正数发电量）；`RecipeHelper.getRealEUtWithIO()` 返回带符号净 EU（发电配方为负），只适用于耗电机器，不要在发电机中使用。
- **注册中枢集中**：新注册对象一律落在 `registry/**`，机器实现在 `common/machine/**`、配方数据在 `data/**`，不要跨域散落注册代码。
- **配方驱动多方块基类**：需要配方类型/机器模式页签的电力多方块，注册 factory 的类必须是 `RecipeElectricMultiblockMachine` 或其子类（无自定义行为时用 `RecipeElectricMultiblockMachine::new`，否则用自定义子类）—— 它经 `RecipeMultiblockMachine` 实现 `IRecipeLogicMachine`；`WorkableElectricMultiblockMachine` 不实现该接口，用它注册会导致模式页签不显示、配方类型不生效。线圈机用 `CoilWorkableElectricMultiblockMachine::new`。`registry/CTNHRecipeModifiers.java#ebfOverclock()` 的类型判断同样指向 `RecipeElectricMultiblockMachine`。细节见 `registry/AGENTS.md`。
- **Mixin 按目标 mod 分组**：新增 Mixin 放到 `mixin/<targetmod>/`，避免堆在 `mixin/mc/`。
- **格式化**：类体起始不留空行，`spotlessCheck` 必须通过。

## ANTI-PATTERNS
- 在发电机/涡轮机中读取 `RecipeHelper.getRealEUtWithIO()` 作为发电量或输出功率（会得到负数，导致并行与 GUI 数值错误甚至配方判定失败）。
- 用字符串 ID + `ForgeRegistries` 查找代替已存在的静态注册对象。
- 对已有注册处中文名声明能力的方块/多方块再补 `@Key("block.ctnhcore.*")` + `Lang` 字段（`CTNHMachines` 中 50 个分级机器/仓室用这种写法，新增内容不要跟随）。
- 删除注册对象后留下悬空 lang 条目。
- 在 `common/machine/**` 内直接调用注册 API 注册物品/方块/配方类型（应走 `registry/**`）。
- 期望 `runData` 产出 GT 配方 JSON 并据此验证配方。
- 在通用工具类里复制 `utils/**` 已有能力（`CTNHRecipeHelper`, `CoilTierHelper` 等）。

## COMMANDS
```bash
./gradlew :modules:CTNH-Core:build              # 编译 + 校验
./gradlew :modules:CTNH-Core:spotlessApply      # 格式化（提交前必跑）
./gradlew :modules:CTNH-Core:runData            # 数据生成（不含 GT 动态配方）
./gradlew :modules:CTNH-Core:runClient          # 游戏内验证机器/配方
```

## SCOPE
本模块覆盖 CTNH 的核心机器、材料、配方、注册、数据生成、客户端渲染与上游 mod Mixin 补丁。

## READ WHEN
- 新增或修改 GT 多方块机器 / 发电机 / 动力机器
- 新增材料、材料标志或配方链
- 新增注册对象（物品、方块、BE、配方类型、创造栏）
- 修改标签、世界生成或矿石分布
- 打补丁到上游 mod / MC 本体
- 调整客户端渲染、模型或 Ponder 场景

## SOURCE OF TRUTH
- 源码：`modules/CTNH-Core/src/main/java/io/github/cpearl0/ctnhcore/`
- 资源与 mixin 配置：`modules/CTNH-Core/src/main/resources/`
- 生成物：`modules/CTNH-Core/src/generated/resources/`
- 本目录层级文档：`ctnh-docs/references/CTNH-Core/**`

## WORKFLOW
1. 先读本文件与对应域的 `AGENTS.md`（见 DOMAIN GUIDE ROUTING）。
2. 改动落在正确域：注册 → `registry/`，机器 → `common/machine/`，配方 → `data/recipe/`，渲染 → `client/renderer/`。
3. 修改后跑 `spotlessApply` 与 `:modules:CTNH-Core:build`。
4. GT 配方相关改动在游戏内或用 `ConfigHolder.dev.dumpRecipes` 验证，不要依赖 `runData`。
5. 结构变化（新增/删除类、新子包）时同步更新本文件与对应域文档。
