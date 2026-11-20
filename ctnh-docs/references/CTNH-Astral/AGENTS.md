# CTNH-ASTRAL MODULE

## OVERVIEW
CTNH-Astral 是 CTNH 的星界模块，包根 `com.ctnh.ctnhastral`，mod id `ctnhastral`，135 个 Java 文件。承载天体与星球内容：火箭组装 / 发射 / 星图选点 / 跨维度落地、月球与火星等自定义维度、类型化环境模型（气压 / 气体分压 / 温度 / 腐蚀 / 辐射）、GTCEu 材料与元素、真空密封附魔与医疗条件桥、TerraBlender 生物群系区域，以及集中式世界生成（生物群系 / 维度 / 密度函数 / 噪声设置 / 结构 / 地物 / 地形）。入口类：`CTNHAstral`（mod 主类）、`CTNHAstralGTAddon`（GT addon，注册 tag prefix / 元素 / 配方）；代理为 `CommonProxy` / `ClientProxy`。

## STRUCTURE
源码根 `modules/CTNH-Astral/src/main/java/com/ctnh/ctnhastral/`（括号内为该域 Java 文件数）

```text
ctnhastral/                                     # 共 135 个 Java 文件
├── CTNHAstral / CTNHAstralGTAddon              # mod 入口、GT addon
├── api/        (1)   loot/LootBuilder
├── client/     (6)   ClientEnvironmentTemperature, ClientProxy, RocketLaunchHud,
│                     gui/screen/CelestialSelectionScreen,
│                     render/{MoonEffects, SiliconCrystalColors}
├── common/     (49)  CommonProxy, CAFluidInteractions
│   ├── block/           (8) AstralGrass, AstralGrassBlock, AstralTallGrassBlock, AstralFlowerBlock,
│   │                        AstralSaplingBlock, MarsSaplingBlock, MoonlightCrystalBlock,
│   │                        SiliconBuddingBlock
│   ├── enchantment/     (1) VacuumSealEnchantment
│   ├── entity/          (1) RocketContraptionEntity
│   ├── environment/     (10) Atmosphere, BlockTemperature, Corrosion, Environment, EnvironmentEmission,
│   │                         EnvironmentType, NaturalTemperature, PlanetEnvironmentService,
│   │                         Radiation, Temperature
│   ├── event/           (2) CelestialTravelHandler, RocketDimensionTravelHandler
│   ├── machine/         (2) multiblock/RocketAssemblyPlatformMachine, simple/OxygenEnricherMachine
│   ├── medical/         (2) MedicalConditionEventHandler, PlayerThermalProtectionEvent
│   ├── network/         (5) CANetwork, C2SRequestTemperaturePacket, C2STeleportToBodyPacket,
│   │                         S2COpenCelestialScreenPacket, S2CTemperaturePacket
│   ├── oxygen/          (1) OxygenMachineRules
│   ├── recipe/          (1) OxygenCondition
│   ├── space/           (1) CASpaceConstants
│   └── universe/        (13) CACelestialBodies, CelestialBody, CelestialBodyType, CelestialDisplay,
│                             CelestialPosition, CelestialRingDisplay, CelestialTeleportTargets,
│                             CelestialTeleporter, CelestialEntityTeleporter, DirectCelestialTeleporter,
│                             OrbitCelestialTeleporter, OrbitalCelestialPosition, StaticCelestialPosition
├── data/       (54)  CADamageTypeTagsProvider, CADamageTypes, CAElements, CAEnchantments, CAMaterials,
│                     CAMedicalConditions, CARecipes, CATagPrefixes, GTMateralAdjust
│   ├── environment/     (3) AstralEnvironments, SolarSystemEnvironments, VanillaEnvironments
│   ├── lang/            (2) ChineseLangHandler, EnglishLangHandler
│   ├── tags/            (1) CABiomeTagsProvider
│   └── worldgen/        (39) 根 2：CAWorldgen, WorldgenKeys
│       ├── biome/       (3) MoonBiomeSource, ParameterOverlayRegion, WorldgenBiomes
│       ├── feature/     (8) AcidPoolFeature, MarsDeadVolcanoFeature, MoonCraterFeature, MoonCraterLayout,
│       │                    MoonCraterShape, MoonSiliconFeature, MoonWastelandRocksFeature,
│       │                    MoonlightDesertFeature
│       ├── preset/      (6) AstralWorldgen, MarsWorldgen, MoonWorldgen, PlanetTerrain, VanillaWorldgen,
│       │                    VenusWorldgen
│       ├── structure/   (9) AstralMeteor{Placer,Structure,StructurePiece},
│       │                    Mars{ResearchGraveyard,StargateRuins}Structure(+Piece),
│       │                    MoonAbandonedOutpostStructure, MoonSubsurfaceSeaStructure
│       └── terrain/    (11) LayeredFluidPicker, MoonCanyon{Layout,Terrain}, MoonGeologyTerrain,
│                             MoonHighlands, MoonIcefield, MoonLavaTubes, MoonSiliconLandscape,
│                             MoonSubsurfaceSea, MoonSurfaceTransition, TerrainNoise
├── mixin/      (3)   minecraft/{ChunkGeneratorMixin, NoiseBasedChunkGeneratorMixin,
│                     ServerGamePacketListenerImplMixin}
├── registry/   (19)  CABlocks, CACreativeModeTabs, CAEnvironments, CAItems, CAMachines, CAMultiblocks,
│                     CARecipeTypes/Conditions/Modifiers, CARegistrate, CARocketBlocks,
│                     CARocketEntityTypes, CTNHBlockInfo,
│                     sound/{CAMusics, CASoundDefinitionsProvider, CASoundEvents},
│                     worldgen/{AstralBlocks, MarsBlocks, MoonBlocks}
└── utils/      (1)   ModUtils
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| mod 入口 / GT addon | `CTNHAstral.java`, `CTNHAstralGTAddon.java` |
| 代理与公共启动 | `common/CommonProxy.java`, `client/ClientProxy.java` |
| 环境值类型与代数契约 | `common/environment/{EnvironmentType, Environment, Atmosphere, Temperature}` |
| 环境查询与排放生命周期 | `common/environment/PlanetEnvironmentService.java`（`getEnvironment` / `emit` / `cease`） |
| 环境类型与维度登记 | `registry/CAEnvironments.java`（`ATMOSPHERE` / `TEMPERATURE` / `CORROSION` / `RADIATION`） |
| 维度与群系环境数值 | `data/environment/{VanillaEnvironments, SolarSystemEnvironments, AstralEnvironments}.java` |
| 氧气配方条件 | `common/recipe/OxygenCondition.java`, `registry/CARecipeConditions.java` |
| 机器耗氧 / 进气规则 | `common/oxygen/OxygenMachineRules.java` |
| 真空密封附魔 | `common/enchantment/VacuumSealEnchantment.java`, `data/CAEnchantments.java` |
| 医疗条件桥 | `common/medical/{MedicalConditionEventHandler, PlayerThermalProtectionEvent}.java`, `data/CAMedicalConditions.java`, `data/CADamageTypes.java` |
| 天体定义与星图数据 | `common/universe/{CACelestialBodies, CelestialBody, CelestialBodyType, CelestialDisplay}.java` |
| 跨维度落点与传送器 | `common/universe/{CelestialEntityTeleporter, CelestialTeleportTargets, CelestialTeleporter}.java` |
| 网络通道与包 | `common/network/CANetwork.java` + 同包四个 packet 记录 |
| 航天常量 | `common/space/CASpaceConstants.java`（`ORBIT_ALTITUDE` / `LAUNCH_COUNTDOWN`） |
| 火箭实体与同步字段 | `common/entity/RocketContraptionEntity.java`, `registry/CARocketEntityTypes.java` |
| 火箭跨维度转移 | `common/event/RocketDimensionTravelHandler.java` |
| 星图选点后的传送 | `common/event/CelestialTravelHandler.java` |
| 组装 / 发射多方块 | `common/machine/multiblock/RocketAssemblyPlatformMachine.java`, `registry/CAMultiblocks.java` |
| 火箭部件与推力 / 燃料 | `registry/CARocketBlocks.java` |
| 发射 HUD / 星图界面 / 星球天空 | `client/RocketLaunchHud.java`, `client/gui/screen/CelestialSelectionScreen.java`, `client/render/MoonEffects.java` |
| 供氧机 | `common/machine/simple/OxygenEnricherMachine.java`, `registry/CAMachines.java` |
| 材料 / 元素 / tag prefix | `data/{CAMaterials, CAElements, CATagPrefixes, GTMateralAdjust}.java` |
| 配方 | `data/CARecipes.java`, `registry/{CARecipeTypes, CARecipeConditions, CARecipeModifiers}.java` |
| 世界生成键表 | `data/worldgen/WorldgenKeys.java`（`Biomes`, `Dimensions`, `DimensionTypes`, `NoiseSettings`, `Density`, `ConfiguredFeatures`, `PlacedFeatures`, `Structures`, `StructureSets`, `BiomeTags`） |
| 世界生成注册与装配 | `data/worldgen/CAWorldgen.java`, `common/CommonProxy.gatherData()` |
| 各世界数值预设 | `data/worldgen/preset/`（`MoonWorldgen`, `MarsWorldgen`, `VenusWorldgen`, `AstralWorldgen`, `VanillaWorldgen`, `PlanetTerrain`） |
| 月球地形与流体分层 | `data/worldgen/terrain/`（`MoonSubsurfaceSea`, `MoonCanyonTerrain`, `MoonGeologyTerrain`, `LayeredFluidPicker`） |
| 月球群系源与区域适配 | `data/worldgen/biome/{MoonBiomeSource, ParameterOverlayRegion, WorldgenBiomes}.java` |
| 世界生成方块 | `registry/worldgen/{AstralBlocks, MarsBlocks, MoonBlocks}.java`, `registry/CTNHBlockInfo.java` |
| 数据生成 | `common/CommonProxy.gatherData()`（`CAWorldgen.addRegistries(...)` + `Registries.DAMAGE_TYPE`）、`data/{CADamageTypeTagsProvider, tags/CABiomeTagsProvider}.java`, `registry/sound/CASoundDefinitionsProvider.java` |
| 语言 | `data/lang/{ChineseLangHandler, EnglishLangHandler}.java` |
| 上游 / 原版补丁 | `mixin/`, `src/main/resources/ctnhastral.mixins.json` |
| 资源 | `src/main/resources/assets/ctnhastral/`（models, shaders, sounds, textures）、`src/main/resources/assets/gtceu/`（`materials_sets/starsteel`）、`src/main/resources/data/ctnhastral/`（biome, tags）、`src/main/resources/data/minecraft/tags/worldgen/biome/`、`src/generated/resources/` |

## DOMAIN GUIDE ROUTING
| Source area | Guide | Read before |
|-------------|-------|-------------|
| `api/**` | `ctnh-docs/references/CTNH-Astral/api/AGENTS.md` | 新增战利品表构建器或公共 API 面 |
| `client/**` | `ctnh-docs/references/CTNH-Astral/client/AGENTS.md` | 修改代理启动、火箭 HUD、星图界面、星球天空与着色器 |
| `common/**` | `ctnh-docs/references/CTNH-Astral/common/AGENTS.md` | 修改机器、火箭与转移、环境 / 氧气系统、医疗条件、方块、网络 |
| `data/**` | `ctnh-docs/references/CTNH-Astral/data/AGENTS.md` | 新增材料、元素、tag prefix、配方、环境定义、世界生成、语言 |
| `mixin/**` | `ctnh-docs/references/CTNH-Astral/mixin/AGENTS.md` | 打补丁到 MC 区块生成 / 网络包处理 |
| `registry/**` | `ctnh-docs/references/CTNH-Astral/registry/AGENTS.md` | 新增任何注册对象（方块 / 物品 / 机器 / 多方块 / 实体 / 音效 / 配方类型 / 环境类型） |
| `utils/**` | `ctnh-docs/references/CTNH-Astral/utils/AGENTS.md` | 复用工具类而非另起实现 |

## CONVENTIONS
- **命名空间与前缀**：包根 `com.ctnh.ctnhastral`，mod id `ctnhastral`；注册类统一 `CA` 前缀（`CARegistrate`, `CABlocks`, `CAItems`, `CAMachines`, `CARocketBlocks`, `CAEnvironments` ...）。资源 id 一律经 `CTNHAstral.id(name)` 构造。
- **GTM 动态包**：GT/GMT 配方经 `CTNHAstralGTAddon.addRecipes()` 注册为运行时动态数据包（`GTDynamicPackContents` / CTNH-Lib `CTNHDynamicDataPack`），`runData` 对其**不产出 JSON**；静态 `src/generated/resources` 只含 tags / lang / models / blockstates / loot_tables / worldgen / 非 GT 配方。验证方式为游戏内或 `ConfigHolder.dev.dumpRecipes`。
- **注册对象优先**：引用物品 / 方块 / 流体**必须**使用静态注册对象（`CABlocks.X`, `CAItems.X`, `CAMaterials.X`, `MoonBlocks.X`, `GTMaterials.X`, `TagPrefix.ingot`），**禁止** `ResourceLocation` 字符串解析 + `ForgeRegistries` 查找；字符串 ID 仅限无注册对象的场景（上游 mod 专属 ID、配方 ID、tag key、维度 ID）。
- **环境模型**：所有环境数值是 `EnvironmentType<V, D>` 登记的不可变值 + 有符号增量；来源（维度基准、群系修饰、方块温度、机器 / 设备排放）只贡献增量，`Environment.applyDelta` 是唯一合成路径。类型与静态修饰在 `FMLLoadCompleteEvent` 经 `EnvironmentType.freeze()` 冻结，之后不再接受新类型。
- **维度环境显式声明**：`CAEnvironments.init()` 从 `CACelestialBodies.all()` 逐个登记天体维度，另加 `Level.NETHER` / `Level.END`；未登记的维度读 `VanillaEnvironments.FALLBACK`。
- **世界生成三层分工**：`WorldgenKeys` 只持有 `ResourceKey` / `TagKey` 身份，不含数值与注册副作用；`CAWorldgen` 负责 Forge `DeferredRegister`（feature / biome source / structure type / piece type）与 `RegistrySetBuilder` 装配；`data/worldgen/preset/` 的每个世界类提供该世界的数值（群系、地物、噪声设置、维度、结构集）。
- **注册触发顺序**：`registerTagPrefixes()` 依赖 `CABlocks.init()` → `AstralBlocks/MarsBlocks/MoonBlocks/CARocketBlocks` 先于 `CATagPrefixes.init()` 完成静态初始化；`CAWorldgen.init(eventBus)` 在 `CommonProxy.init()` 内、`REGISTRATE.registerRegistrate()` 之前调用。
- **月球液体分层**：`NoiseGeneratorSettings` 的 defaultFluid 只描述海平面流体，月球噪声设置的 defaultFluid 为空气；`CAWorldgen.LAVA_LEVELS` 只登记 `MOON` / `MARS` / `ASTRAL_PLANET` / `ORBIT` 四个噪声设置，`CAWorldgen.fluidPicker(...)` 对未登记的设置返回 `null`（不改写 `globalFluidPicker`）。月球卤水由 `MoonSubsurfaceSea` 的地形调色板写入。
- **Astral 自有流体贴图**：`assets/ctnhastral/textures/block/fluids/`（seawater / moon_enriched_brine / acid / starlight / starmetal）。
- **静态材料模型**：`assets/gtceu/models/item/materials_sets/starsteel/**` 是该材料图标集的静态模型资源，随 GTCEu 命名空间查找，不是生成物。

## ANTI-PATTERNS
- 假定 `assets/gtceu/**` 下的资源归 Astral 所有；Astral 自有流体贴图在 `assets/ctnhastral/textures/block/fluids/`。
- 只改一个世界生成注册表而不检查关联的 biome / feature / preset / noise / dimension 类。
- 绕过 `WorldgenKeys` 在 preset 里直接写 `ResourceLocation` 字符串构造注册键。
- 在环境来源里写覆盖路径或提前截断负增量；来源只贡献增量，约束只在 `apply` 阶段执行。
- 在 `FMLLoadCompleteEvent` 之后注册新的 `EnvironmentType` 或静态群系修饰。
- 用字符串 ID + `ForgeRegistries` 查找代替已存在的静态注册对象。
- 期望 `runData` 产出 GT 配方 JSON 并据此验证配方。
- 在 `common/**` 内直接注册方块 / 物品 / 机器，绕过 `registry/**`。

## COMMANDS
```bash
./gradlew :modules:CTNH-Astral:build              # 编译 + 校验
./gradlew :modules:CTNH-Astral:spotlessApply      # 格式化（提交前必跑）
./gradlew :modules:CTNH-Astral:runData            # 数据生成（不含 GT 动态配方）
./gradlew :modules:CTNH-Astral:runClient          # 游戏内验证火箭 / 环境 / 星图 / 维度
```

## SCOPE
适用于 `modules/CTNH-Astral` 及其子模块仓库。它是通过根路由表加载的参考指南，不是额外的源码树指令文件。

## READ WHEN
- 新增或修改星界内容、材料、世界生成、维度、火箭、环境或氧气代码。
- 改动区块生成 / 网络包处理相关的 mixin 钩子。
- 修改火箭跨维度转移的状态持久化与落点逻辑。
- 调整环境类型、维度基准或排放生命周期。

## SOURCE OF TRUTH
- 注册与生命周期：`CTNHAstral.java`, `CTNHAstralGTAddon.java`, `common/CommonProxy.java`。
- Forge 元数据与 mixin：`src/main/resources/META-INF/mods.toml`, `src/main/resources/ctnhastral.mixins.json`。
- 世界生成：`data/worldgen/CAWorldgen.java` 的注册与 `RegistrySetBuilder` 装配，`data/worldgen/WorldgenKeys.java` 的键表。
- 环境：`common/environment/**` 的模型与 `registry/CAEnvironments.java` 的登记。
- 本目录层级文档：`ctnh-docs/references/CTNH-Astral/**`。

## WORKFLOW
1. 把改动的符号映射到域，先读该域的 `AGENTS.md`（见 DOMAIN GUIDE ROUTING）。
2. 检查 GT addon 钩子顺序与 `CommonProxy.gatherData()` 里的世界生成引导是否同步。
3. 跑最窄的 Gradle 任务（`runData` 处理数据生成，`build` 编译校验）。
4. 结构变化（新增 / 删除类、新子包）时同步更新本文件与对应域文档。
