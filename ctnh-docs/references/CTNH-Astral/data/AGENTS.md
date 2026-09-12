# CTNH-ASTRAL DATA DOMAIN

## OVERVIEW
Astral 的数据注册与数据生成（43 个 Java 文件）：材料、元素、tag prefix、GT 配方、语言，以及集中式世界生成（生物群系、维度、密度函数、噪声设置、地表规则、结构、地物、雕刻器）。

## STRUCTURE
```text
data/                                     # 共 43 个 Java 文件
├── CAElements.java, CAEnchantments.java, CAMaterials.java, CARecipes.java,
│   CATagPrefixes.java, GTMateralAdjust.java
├── lang/        (2)  ChineseLangHandler, EnglishLangHandler
├── tags/        (1)  CABiomeTagsProvider
└── worldgen/    (34)
    ├── 根 (8)        CABiomes, CADensityFunctions, CADimensions, CADimensionTypes,
    │                 CANetherRegion, CANoiseSetting, CAOverworldRegion, CASurfaceRuleData
    ├── biome/ (4)    AstralBiomes, BiomeParameters, MoonBiomes, NetherBiomes
    ├── carver/ (4)   CAConfiguredCarvers, CAWorldCarvers, MoonCraterCarver, MoonCraterCarverConfig
    ├── feature/ (5)  AcidPoolFeature, CAConfiguredFeatures, CAFeatures, CAPlacements, MarsDeadVolcanoFeature
    └── structure/ (13) AstralMeteorPlacer, AstralMeteorStructure, AstralMeteorStructurePiece,
                        CAStructures, CAStructureSets,
                        MarsResearchGraveyardStructure(+Piece), MarsStargateRuinsStructure(+Piece),
                        MoonAbandonedOutpostStructure, MoonCraterPlacer,
                        MoonCraterStructure, MoonCraterStructurePiece
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| 材料 | `data/CAMaterials.java`（`Moonstone`, `Marsstone`, `Venusstone`, `Mercurystone`, `Glaciostone`, `AstralStone`, `Starlight`, `Starmetal`, `Seawater`, `Acid`） |
| 元素 | `data/CAElements.java`（`STARMETAL`，编号 120，符号 `St`） |
| 上游材料调整 | `data/GTMateralAdjust.java`（给 `GTMaterials.Sulfur` 补带方块的液体属性，388K） |
| 矿脉 tag prefix | `data/CATagPrefixes.java`（`oreAstralStone`, `oreMoonStone`, `oreVenusStone`, `oreMarsStone`, `oreMercuryStone`, `oreGlacioStone`） |
| 附魔注册 | `data/CAEnchantments.java`（`VACUUM_SEAL`），实现类在 `common/enchantment/VacuumSealEnchantment.java` |
| GT 配方 | `data/CARecipes.java`（`CARecipes.init(consumer)`） |
| 语言 | `data/lang/` |
| 生物群系 tag | `data/tags/CABiomeTagsProvider.java`（把 `CABiomes.ACID_VALLEY` 加入 `BiomeTags.IS_NETHER`） |
| 世界生成根 | `data/worldgen/`（`CABiomes`, `CADimensions`, `CADimensionTypes`, `CANoiseSetting`, `CASurfaceRuleData`, `CAOverworldRegion`, `CANetherRegion`, `CADensityFunctions`） |
| TerraBlender 区域 | `data/worldgen/CAOverworldRegion.java`（权重 2，`PLAGUE_WASTELAND`）、`CANetherRegion.java`（权重 5，`ACID_VALLEY`） |
| 生物群系 | `data/worldgen/biome/`（`AstralBiomes`, `MoonBiomes`, `NetherBiomes`, `BiomeParameters`） |
| 雕刻器 | `data/worldgen/carver/`（`MoonCraterCarver` + `MoonCraterCarverConfig`） |
| 地物 | `data/worldgen/feature/`（`AcidPoolFeature`, `MarsDeadVolcanoFeature`） |
| 结构 | `data/worldgen/structure/`（5 组结构 + 各自的 Piece/Placer） |

## CONVENTIONS
- **世界生成集中**：世界生成类一律放 `data/worldgen`；维度类直接在 `worldgen` 根，没有 `dimension/` 子包。
- **材料集**：10 个材料在 `data/CAMaterials` 中声明；`StarsteelIcon`（`new MaterialIconSet("starsteel", METALLIC)`）对应静态模型资源 `assets/gtceu/models/item/materials_sets/starsteel/**`。
- **月球海水**：`CAMaterials.Seawater` 是 Astral 的海水流体（`GTMaterials.SaltWater` 只作上游保留）；`GTMateralAdjust` 不调整 SaltWater 的方块与贴图，`CANoiseSetting.MOON` 用它作为默认流体。
- **矿脉 tag prefix 条件化**：只有 `oreAstralStone` 在类初始化时创建；其余 5 个在 `CATagPrefixes.init()` 中当 `LDLib.isModLoaded("ad_astra")` 时创建，随后统一 `addSecondaryMaterial(...)` 追加对应石粉。`oreAstralStone` 依赖 `AstralBlocks.ASTRAL_STONE`，因此必须在 `CABlocks.init()` 之后才调用。
- **GT 配方**：`CARecipes.init(provider)` 经 `CTNHAstralGTAddon.addRecipes()` 调用，产出 MV/HV/EV 三档供氧机装配配方、`oxygen_enricher` 富集配方与 `rocket_assemble` 火箭组装配方——这些都是运行时动态数据包，`runData` 不产 JSON。
- **数据生成**：`CommonProxy.gatherData()` 的 `RegistrySetBuilder` 引导 10 个注册表（carver / biome / configured_feature / placed_feature / dimension_type / level_stem / noise_settings / structure / structure_set / density_function），输出到 `src/generated/resources`；静态 `src/main/resources/data/ctnhastral/` 另有手写的 `biome/`、`planets/`、`recipes/`（nasa_workbench 火箭配方、space_station 空间站配方）、`tags/`。
- **动态注册不要靠 JSON 推断**：地物、结构与维度的实际注册由 `RegistrySetBuilder` 驱动，静态 JSON 缺失不代表世界生成缺失。

## ANTI-PATTERNS
- 只改一个世界生成注册表而不检查关联的 biome / carver / feature / noise / dimension 类。
- 把维度类另起 `dimension/` 子包，破坏 `CommonProxy.gatherData()` 的引导路径。
- 在 `data/` 里直接用字符串 ID 拼方块/物品引用，而非 `CABlocks.*` / `CAMaterials.*` 静态对象。
- 期望 `runData` 产出 GT 配方 JSON 并据此验证配方。
- 新增矿脉前缀时遗漏 `addSecondaryMaterial(...)`，导致副产石粉缺失。

## SCOPE
适用于 `src/main/java/com/ctnh/ctnhastral/data` 及其子包。

## READ WHEN
- 新增星界材料、流体、元素、tag prefix、配方、世界生成、维度或语言。
- 调整生物群系分布、地表规则或维度噪声设置。

## SOURCE OF TRUTH
- `data/` 下的类与 `CommonProxy.gatherData()` 的引导。

## WORKFLOW
1. 改动世界生成前先把关联注册表当成一组通读。
2. 影响数据生成时跑 `:modules:CTNH-Astral:runData`；GT 配方用游戏内或 `ConfigHolder.dev.dumpRecipes` 验证。
