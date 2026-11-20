# CTNH-ASTRAL DATA DOMAIN

## OVERVIEW
Astral 的数据注册与数据生成（54 个 Java 文件）：材料、元素、tag prefix、GT 配方、附魔、医疗条件与伤害类型、语言，以及集中式世界生成（键表、注册装配、各世界数值预设、地形、群系、地物、结构）。

## STRUCTURE
```text
data/                                    # 共 54 个 Java 文件
├── CADamageTypeTagsProvider.java, CADamageTypes.java, CAElements.java, CAEnchantments.java,
│   CAMaterials.java, CAMedicalConditions.java, CARecipes.java, CATagPrefixes.java,
│   GTMateralAdjust.java
├── environment/  (3)   AstralEnvironments, SolarSystemEnvironments, VanillaEnvironments
├── lang/         (2)   ChineseLangHandler, EnglishLangHandler
├── tags/         (1)   CABiomeTagsProvider
└── worldgen/     (39)  根 2：CAWorldgen, WorldgenKeys
    ├── biome/    (3)   MoonBiomeSource, ParameterOverlayRegion, WorldgenBiomes
    ├── feature/  (8)   AcidPoolFeature, MarsDeadVolcanoFeature, MoonCraterFeature, MoonCraterLayout,
    │                   MoonCraterShape, MoonSiliconFeature, MoonWastelandRocksFeature,
    │                   MoonlightDesertFeature
    ├── preset/   (6)   AstralWorldgen, MarsWorldgen, MoonWorldgen, PlanetTerrain, VanillaWorldgen,
    │                   VenusWorldgen
    ├── structure/ (9)  AstralMeteor{Placer,Structure,StructurePiece},
    │                   Mars{ResearchGraveyard,StargateRuins}Structure(+Piece),
    │                   MoonAbandonedOutpostStructure, MoonSubsurfaceSeaStructure
    └── terrain/  (11)  LayeredFluidPicker, MoonCanyon{Layout,Terrain}, MoonGeologyTerrain,
                        MoonHighlands, MoonIcefield, MoonLavaTubes, MoonSiliconLandscape,
                        MoonSubsurfaceSea, MoonSurfaceTransition, TerrainNoise
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| 材料 | `data/CAMaterials.java`（`Moonstone`, `Marsstone`, `Venusstone`, `Mercurystone`, `Glaciostone`, `AstralStone`, `Starlight`, `Starmetal`, `Seawater`, `MoonEnrichedBrine`, `Acid`） |
| 元素 | `data/CAElements.java`（`STARMETAL`，编号 120，符号 `St`） |
| 上游材料调整 | `data/GTMateralAdjust.java`（给 `GTMaterials.Sulfur` 补带方块的液体属性） |
| 矿脉 tag prefix | `data/CATagPrefixes.java`（`oreAstralStone` + `init()` 内的 `oreMoonStone` / `oreVenusStone` / `oreMarsStone` / `oreMercuryStone` / `oreGlacioStone`） |
| 附魔注册 | `data/CAEnchantments.java`（`VACUUM_SEAL`），实现类在 `common/enchantment/VacuumSealEnchantment.java` |
| 医疗条件 | `data/CAMedicalConditions.java`（`HYPOXIA_MILD`, `HYPOXIA_SEVERE`, `HYPOTHERMIA`, `HYPERTHERMIA`） |
| 伤害类型 | `data/CADamageTypes.java`（`medical_condition/<name>` 键，`DamageScaling.NEVER` + `BYPASSES_ARMOR`） |
| 伤害类型标签生成 | `data/CADamageTypeTagsProvider.java`（`BYPASSES_ARMOR` 落盘 `data/ctnhastral/tags/damage_type/`） |
| GT 配方 | `data/CARecipes.java`（`CARecipes.init(consumer)`） |
| 维度环境数值 | `data/environment/{VanillaEnvironments, SolarSystemEnvironments, AstralEnvironments}.java` |
| 群系环境修饰表 | `data/environment/SolarSystemEnvironments.java` 的 `BIOME_MODIFIERS` |
| 语言 | `data/lang/` |
| 生物群系 tag | `data/tags/CABiomeTagsProvider.java`（把 `WorldgenKeys.Biomes.ACID_VALLEY` 加入 `BiomeTags.IS_NETHER`） |
| 世界生成键表 | `data/worldgen/WorldgenKeys.java`（`Biomes`, `Dimensions`, `DimensionTypes`, `NoiseSettings`, `Noise`, `Density`, `ConfiguredFeatures`, `PlacedFeatures`, `Structures`, `BiomeTags`, `StructureSets`, `VanillaDensity`） |
| 世界生成注册与装配 | `data/worldgen/CAWorldgen.java`（`init(eventBus)`, `commonSetup()`, `addRegistries(...)`, `fluidPicker(...)`） |
| 生物群系 | `data/worldgen/preset/`（`MoonWorldgen.biomes`, `MarsWorldgen.biomes`, `AstralWorldgen.biomes`, `VanillaWorldgen.biomes`） |
| TerraBlender 区域 | `data/worldgen/preset/VanillaWorldgen.java`（`overworldRegion()` 权重 2 → `PLAGUE_WASTELAND`；`netherRegion()` 权重 5 → `ACID_VALLEY`），适配器 `data/worldgen/biome/ParameterOverlayRegion.java` |
| 地表规则 | `data/worldgen/preset/{VanillaWorldgen, AstralWorldgen, MarsWorldgen, MoonWorldgen}.surface()` |
| 噪声设置与密度函数 | `data/worldgen/preset/{MoonWorldgen, MarsWorldgen, AstralWorldgen, PlanetTerrain}.java` |
| 月球群系源 | `data/worldgen/biome/MoonBiomeSource.java`（`initialize` / `surfaceBiomes` / `canyons` / `bindTerrainFluids`） |
| 月球地形 | `data/worldgen/terrain/`（`MoonSubsurfaceSea`, `MoonCanyonTerrain`, `MoonGeologyTerrain`, `MoonHighlands`, `MoonIcefield`, `MoonLavaTubes`, `MoonSiliconLandscape`, `MoonSurfaceTransition`, `TerrainNoise`） |
| 地物 | `data/worldgen/feature/`（`AcidPoolFeature`, `MarsDeadVolcanoFeature`, `MoonCraterFeature`, `MoonSiliconFeature`, `MoonWastelandRocksFeature`, `MoonlightDesertFeature`） |
| 结构 | `data/worldgen/structure/`（5 组结构 + 各自的 Piece / Placer） |

## CONVENTIONS
- **世界生成三层分工**：`WorldgenKeys` 只持有 `ResourceKey` / `TagKey` 身份，不含数值与注册副作用；`CAWorldgen` 负责 Forge `DeferredRegister` 与 `RegistrySetBuilder` 装配；`preset/` 的每个世界类按 `biomes` / `configuredFeatures` / `placedFeatures` / `noiseSettings` / `dimensionTypes` / `dimensions` / `structures` / `structureSets` 提供该世界数值。
- **注册表集合**：`CAWorldgen.addRegistries(...)` 依次挂 `BIOME`、`CONFIGURED_FEATURE`、`PLACED_FEATURE`、`DIMENSION_TYPE`、`LEVEL_STEM`、`NOISE_SETTINGS`、`STRUCTURE`、`STRUCTURE_SET`、`NOISE`、`DENSITY_FUNCTION`；`CommonProxy.gatherData()` 再追加 `DAMAGE_TYPE` → `CADamageTypes::bootstrap`。
- **Forge 注册项**：`CAWorldgen.init(eventBus)` 注册六个 `Feature`（`acid_pool`, `mars_dead_volcano`, `moon_crater`, `moonlight_desert`, `moon_wasteland_rocks`, `moon_silicon_landscape`）、`moon` 群系源编解码器、四个 `minecraft` 命名空间的结构类型与三个结构片段类型（`ctnh_meteor`, `ctnh_moon_abandoned_outpost`, `ctnh_mars_research_graveyard`, `ctnh_mars_stargate_ruins` / `ctnhastral_meteor`, `ctnhastral_mars_research_graveyard`, `ctnhastral_mars_stargate_ruins`），以及 `ctnhastral` 命名空间的 `moon_subsurface_sea` 结构类型与片段类型。
- **维度身份**：5 个维度为 `ctnhastral:astral_planet`、`astral_orbit`、`moon`、`mars`、`venus`，对应 `WorldgenKeys.Dimensions` / `WorldgenKeys.DimensionTypes` 同名键；`NoiseSettings` 另有 `orbit`。
- **材料集**：11 个材料在 `data/CAMaterials` 中声明；`StarsteelIcon`（`new MaterialIconSet("starsteel", METALLIC)`）对应静态模型资源 `assets/gtceu/models/item/materials_sets/starsteel/**`。`tagPrefixIgnore()` 把 `Moonstone` 的 `rock` 前缀与 `Marsstone` 的 `block` 前缀指到对应天然岩层方块。
- **矿脉 tag prefix**：`oreAstralStone` 在类初始化时经 `REGISTRATE.oreTagPrefix("astral_stone", ...)` 创建，基块由 supplier 延迟取 `AstralBlocks.ASTRAL_STONE`；其余 5 个在 `CATagPrefixes.init()` 中创建，随后统一 `addSecondaryMaterial(...)` 追加对应石粉。
- **GT 配方**：`CARecipes.init(consumer)` 经 `CTNHAstralGTAddon.addRecipes()` 调用，产出 MV / HV / EV 三档供氧机的 `ASSEMBLER_RECIPES` 配方、`rocket_assemble` 火箭组装配方与 `oxygen_enrichment` 富集配方——这些都是运行时动态数据包，`runData` 不产 JSON。
- **环境数据**：`data/environment/VanillaEnvironments` 提供 `OVERWORLD` / `NETHER` / `END` / `FALLBACK` 与 `BLOCK_TEMPERATURE_SOURCES`；`SolarSystemEnvironments` 提供 `SOL` / `MOON` / `MARS` / `VENUS` 与 `BIOME_MODIFIERS`；`AstralEnvironments` 提供 `PLANET` / `ORBIT`。数值只描述维度基准与增量，登记由 `registry/CAEnvironments` 完成。
- **伤害类型跨命名空间**：`CADamageTypes` 用 `simpleId("medical_condition/" + name)` 重建与 GT `MedicalCondition` 内建键一致的伤害类型，输出落在 `data/gtceu/damage_type/medical_condition/`；标签由 `CADamageTypeTagsProvider` 以 `ctnhastral` 命名空间落盘。
- **数据生成产物**：世界生成、伤害类型、标签经 `CommonProxy.gatherData()` 输出到 `src/generated/resources`；静态 `src/main/resources/data/ctnhastral/` 只含手写的 `biome/astral_meteor.json` 与 `tags/worldgen/biome/*.json`，另有 `data/minecraft/tags/worldgen/biome/stronghold_biased_to.json`。
- **动态注册不要靠 JSON 推断**：地物、结构、维度、噪声设置的实际注册由 `RegistrySetBuilder` 驱动，静态 JSON 缺失不代表世界生成缺失。
- **月球液体分层**：`LayeredFluidPicker` 以 `min(lavaLevel, seaLevel)` 为界，界下岩浆、界上海平面流体；`CAWorldgen.fluidPicker(...)` 只对 `LAVA_LEVELS`（`MOON`, `MARS`, `ASTRAL_PLANET`, `ORBIT`）返回 picker，其余返回 `null`。月球卤水由 `MoonSubsurfaceSea` 的调色板写入。

## ANTI-PATTERNS
- 只改一个世界生成注册表而不检查关联的 biome / feature / preset / noise / dimension 类。
- 在 `preset/` 或 `terrain/` 里直接构造注册键字符串，绕过 `WorldgenKeys`。
- 把维度类另起 `dimension/` 子包，破坏 `CAWorldgen.addRegistries(...)` 的装配路径。
- 在 `data/` 里直接用字符串 ID 拼方块 / 物品引用，而非 `CABlocks.*` / `CAMaterials.*` / `MoonBlocks.*` 静态对象。
- 期望 `runData` 产出 GT 配方 JSON 并据此验证配方。
- 新增矿脉前缀时遗漏 `addSecondaryMaterial(...)`，导致副产石粉缺失。
- 在 `CAWorldgen.fluidPicker(...)` 里对未登记 `LAVA_LEVELS` 的噪声设置返回 picker，改写原版液体分层。

## SCOPE
适用于 `src/main/java/com/ctnh/ctnhastral/data` 及其子包。

## READ WHEN
- 新增星界材料、流体、元素、tag prefix、配方、环境定义、世界生成、维度或语言。
- 调整生物群系分布、地表规则、月球地形或维度噪声设置。
- 调整医疗条件与伤害类型。

## SOURCE OF TRUTH
- `data/` 下的类与 `CommonProxy.gatherData()` 的引导。
- 世界生成键表：`data/worldgen/WorldgenKeys.java`；装配：`data/worldgen/CAWorldgen.java`。

## WORKFLOW
1. 改动世界生成前先把键表、注册装配与对应 preset 当成一组通读。
2. 影响数据生成时跑 `:modules:CTNH-Astral:runData`；GT 配方用游戏内或 `ConfigHolder.dev.dumpRecipes` 验证。
3. 新增环境数值时同步检查 `registry/CAEnvironments.init()` 的登记集合与 `EnvironmentType` 冻结时机。
