# CTNH-ASTRAL MODULE

## OVERVIEW
CTNH-Astral 是 CTNH 的星界模块，包根 `com.ctnh.ctnhastral`，mod id `ctnhastral`，92 个 Java 文件。承载 Ad Astra 星球内容扩展（火箭组装 / 发射 / 跨维度转移、月球与火星自定义维度）、GTCEu 材料与元素、附魔、TerraBlender 生物群系与地表规则、自定义世界生成（生物群系 / 维度 / 密度函数 / 噪声设置 / 结构 / 地物 / 雕刻器），以及氧气与大气环境系统。入口类：`CTNHAstral`（mod 主类）、`CTNHAstralGTAddon`（GT addon，注册 tag prefix / 元素 / 配方）；代理为 `CommonProxy` / `ClientProxy`。

## STRUCTURE
源码根 `modules/CTNH-Astral/src/main/java/com/ctnh/ctnhastral/`（括号内为该域 Java 文件数）

```text
ctnhastral/                                     # 共 92 个 Java 文件
├── CTNHAstral / CTNHAstralGTAddon              # mod 入口、GT addon
├── api/        (1)   loot/LootBuilder
├── client/     (3)   ClientProxy, RocketLaunchHud, render/MoonEffects
├── common/     (20)  CommonProxy, CAFluidInteractions
│   ├── block/           (7) AstralGrass, AstralGrassBlock, AstralTallGrassBlock, AstralFlowerBlock,
│   │                        AstralSaplingBlock, MarsSaplingBlock, SiliconBuddingBlock
│   ├── enchantment/     (1) VacuumSealEnchantment
│   ├── entity/          (1) RocketContraptionEntity
│   ├── event/           (1) RocketDimensionTravelHandler
│   ├── machine/         (2) multiblock/RocketAssemblyPlatformMachine, simple/OxygenEnricherMachine
│   ├── oxygen/          (5) AtmosphereType, OxygenAreaSource, OxygenEnvironment,
│   │                        OxygenEnvironmentService, OxygenMachineRules
│   └── recipe/          (1) OxygenCondition
├── data/       (43)  CAElements, CAEnchantments, CAMaterials, CARecipes, CATagPrefixes, GTMateralAdjust
│   ├── lang/            (2) ChineseLangHandler, EnglishLangHandler
│   ├── tags/            (1) CABiomeTagsProvider
│   └── worldgen/        (34) 根 8：CABiomes, CADensityFunctions, CADimensions, CADimensionTypes,
│   │                         CANetherRegion, CANoiseSetting, CAOverworldRegion, CASurfaceRuleData
│       ├── biome/       (4) AstralBiomes, BiomeParameters, MoonBiomes, NetherBiomes
│       ├── carver/      (4) CAConfiguredCarvers, CAWorldCarvers, MoonCraterCarver, MoonCraterCarverConfig
│       ├── feature/     (5) AcidPoolFeature, CAConfiguredFeatures, CAFeatures, CAPlacements, MarsDeadVolcanoFeature
│       └── structure/   (13) AstralMeteor{Placer,Structure,StructurePiece}, CAStructures, CAStructureSets,
│                             Mars{ResearchGraveyard,StargateRuins}Structure(+Piece),
│                             MoonAbandonedOutpostStructure, MoonCrater{Placer,Structure,StructurePiece}
├── mixin/      (4)   adastra/{OxygenApilmplMixin, TemperatureApilmplMixin},
│                     minecraft/{NoiseBasedChunkGeneratorMixin, ServerGamePacketListenerImplMixin}
├── registry/   (18)  CARegistrate, CABlocks, CAItems, CACreativeModeTabs, CAMachines, CAMultiblocks,
│                     CARocketBlocks, CARocketEntityTypes, CARecipeTypes/Conditions/Modifiers, CTNHBlockInfo,
│                     sound/{CAMusics, CASoundDefinitionsProvider, CASoundEvents},
│                     worldgen/{AstralBlocks, MarsBlocks, MoonBlocks}
└── utils/      (1)   ModUtils
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| mod 入口 / GT addon | `CTNHAstral.java`, `CTNHAstralGTAddon.java` |
| 代理与公共启动 | `common/CommonProxy.java`, `client/ClientProxy.java` |
| 氧气 / 大气环境 | `common/oxygen/{OxygenEnvironmentService, OxygenEnvironment, OxygenAreaSource, OxygenMachineRules, AtmosphereType}` |
| 氧气配方条件 | `common/recipe/OxygenCondition.java`, `registry/CARecipeConditions.java` |
| 真空密封附魔 | `common/enchantment/VacuumSealEnchantment.java`, `data/CAEnchantments.java` |
| 火箭实体与状态 | `common/entity/RocketContraptionEntity.java`, `registry/CARocketEntityTypes.java` |
| 火箭组装 / 发射多方块 | `common/machine/multiblock/RocketAssemblyPlatformMachine.java`, `registry/CAMultiblocks.java` |
| 火箭部件与推力 / 燃料 | `registry/CARocketBlocks.java` |
| 跨维度转移 | `common/event/RocketDimensionTravelHandler.java` |
| 发射 HUD / 月球天空 | `client/RocketLaunchHud.java`, `client/render/MoonEffects.java`, `client/ClientProxy.java` |
| 供氧机 | `common/machine/simple/OxygenEnricherMachine.java`, `registry/CAMachines.java` |
| 材料 / 元素 / tag prefix | `data/{CAMaterials, CAElements, CATagPrefixes, GTMateralAdjust}.java` |
| 配方 | `data/CARecipes.java`, `registry/{CARecipeTypes, CARecipeModifiers}.java` |
| 世界生成 | `data/worldgen/`（根维度类 + `biome/` + `carver/` + `feature/` + `structure/`） |
| 世界生成方块 | `registry/worldgen/{AstralBlocks, MarsBlocks, MoonBlocks}.java`, `registry/CTNHBlockInfo.java` |
| 数据生成 | `common/CommonProxy.gatherData()`, `data/tags/CABiomeTagsProvider.java`, `registry/sound/CASoundDefinitionsProvider.java` |
| 语言 | `data/lang/{ChineseLangHandler, EnglishLangHandler}.java` |
| 上游补丁 | `mixin/`, `src/main/resources/ctnhastral.mixins.json` |
| 资源 | `src/main/resources/assets/ctnhastral/`（models, planet_renderers, shaders, sounds, textures）、`src/main/resources/data/ctnhastral/`（biome, planets, recipes, tags）、`src/generated/resources/` |

## DOMAIN GUIDE ROUTING
| Source area | Guide | Read before |
|-------------|-------|-------------|
| `api/**` | `ctnh-docs/references/CTNH-Astral/api/AGENTS.md` | 新增战利品表构建器或公共 API 面 |
| `client/**` | `ctnh-docs/references/CTNH-Astral/client/AGENTS.md` | 修改代理启动、火箭 HUD、月球天空与着色器 |
| `common/**` | `ctnh-docs/references/CTNH-Astral/common/AGENTS.md` | 修改机器、火箭实体与转移、氧气系统、附魔、方块 |
| `data/**` | `ctnh-docs/references/CTNH-Astral/data/AGENTS.md` | 新增材料、元素、tag prefix、配方、世界生成、语言 |
| `mixin/**` | `ctnh-docs/references/CTNH-Astral/mixin/AGENTS.md` | 打补丁到 Ad Astra / MC 区块生成 / 网络包处理 |
| `registry/**` | `ctnh-docs/references/CTNH-Astral/registry/AGENTS.md` | 新增任何注册对象（方块 / 物品 / 机器 / 多方块 / 实体 / 音效 / 配方类型） |
| `utils/**` | `ctnh-docs/references/CTNH-Astral/utils/AGENTS.md` | 复用工具类而非另起实现 |

## CONVENTIONS
- **命名空间与前缀**：包根 `com.ctnh.ctnhastral`，mod id `ctnhastral`；注册类统一 `CA` 前缀（`CARegistrate`, `CABlocks`, `CAItems`, `CAMachines`, `CARocketBlocks` ...）。
- **GTM 动态包**：GT 配方经 `CTNHAstralGTAddon.addRecipes()` → `CARecipes.init(provider)` 注册为运行时动态数据包，`runData` 对其**不产出 JSON**；静态 `src/generated/resources` 只含 lang / blockstates / models / loot_tables / 世界生成与 minecraft tags。验证方式为游戏内或 `ConfigHolder.dev.dumpRecipes`。
- **注册对象优先**：引用物品 / 方块 / 流体**必须**使用静态注册对象（`CABlocks.X`, `CAItems.X`, `CAMaterials.X`, `GTMaterials.X`, `TagPrefix.ingot`），**禁止** `ResourceLocation` 字符串解析 + `ForgeRegistries` 查找；字符串 ID 仅限无注册对象的场景（上游 mod 专属 ID、配方 ID、tag key、维度 ID，例如 `utils/ModUtils.AdAstraRL`）。
- **世界生成集中**：世界生成类一律放 `data/worldgen`；维度类直接在 `worldgen` 根，没有 `dimension/` 子包；5 个维度为 `ctnhastral:astral_planet`、`astral_orbit`、`moon`、`mars`、`venus`。
- **注册触发顺序**：`registerTagPrefixes()` 依赖 `CABlocks.init()` → `AstralBlocks/MarsBlocks/MoonBlocks/CARocketBlocks` 先于 `CATagPrefixes.init()` 完成静态初始化。
- **月球流体**：`CANoiseSetting.MOON` 的默认流体是 `CAMaterials.Seawater`；Astral 流体贴图（seawater / acid / starlight / starmetal）在 `assets/ctnhastral/textures/block/fluids/`。
- **静态材料模型**：`assets/gtceu/models/item/materials_sets/starsteel/**` 是该材料图标集的静态模型资源，随 GTCEu 命名空间查找，不是生成物。

## ANTI-PATTERNS
- 假定 `assets/gtceu/**` 下的资源归 Astral 所有；Astral 自己的流体贴图在 `assets/ctnhastral/textures/block/fluids/`。
- 只改一个世界生成注册表而不检查关联的 biome / carver / feature / noise / dimension 类。
- 改动 Ad Astra 氧气 / 温度行为时，不同步检查 `ctnhastral.mixins.json` 条目与上游 `OxygenApiImpl` / `TemperatureApiImpl` 目标。
- 用字符串 ID + `ForgeRegistries` 查找代替已存在的静态注册对象。
- 期望 `runData` 产出 GT 配方 JSON 并据此验证配方。
- 在 `common/**` 内直接注册方块 / 物品 / 机器，绕过 `registry/**`。

## COMMANDS
```bash
./gradlew :modules:CTNH-Astral:build              # 编译 + 校验
./gradlew :modules:CTNH-Astral:spotlessApply      # 格式化（提交前必跑）
./gradlew :modules:CTNH-Astral:runData            # 数据生成（不含 GT 动态配方）
./gradlew :modules:CTNH-Astral:runClient          # 游戏内验证火箭 / 供氧 / 维度
```

## SCOPE
适用于 `modules/CTNH-Astral` 及其子模块仓库。它是通过根路由表加载的参考指南，不是额外的源码树指令文件。

## READ WHEN
- 新增或修改星界内容、材料、世界生成、维度、火箭或氧气代码。
- 改动 Ad Astra 或区块生成 / 网络包相关的 mixin 钩子。
- 修改火箭跨维度转移的状态持久化与落点逻辑。

## SOURCE OF TRUTH
- 注册与生命周期：`CTNHAstral.java`, `CTNHAstralGTAddon.java`, `common/CommonProxy.java`。
- Forge 元数据与 mixin：`src/main/resources/META-INF/mods.toml`, `src/main/resources/ctnhastral.mixins.json`。
- 世界生成：`CommonProxy.gatherData()` 的 `RegistrySetBuilder` 引导与 `data/worldgen/` 下的类。
- 本目录层级文档：`ctnh-docs/references/CTNH-Astral/**`。

## WORKFLOW
1. 把改动的符号映射到域，先读该域的 `AGENTS.md`（见 DOMAIN GUIDE ROUTING）。
2. 检查 GT addon 钩子顺序与 `CommonProxy.gatherData()` 里的世界生成引导是否同步。
3. 跑最窄的 Gradle 任务（`runData` 处理数据生成，`build` 编译校验）。
4. 结构变化（新增 / 删除类、新子包）时同步更新本文件与对应域文档。
