# CTNH-ASTRAL REGISTRY DOMAIN

## OVERVIEW
Astral 的注册面（19 个 Java 文件）：方块（星界 / 月球 / 火星世界生成方块与火箭部件）、物品、单方块机器与多方块、环境类型与维度登记、火箭实体类型、音效与音乐、配方类型 / 条件 / 修饰符、创造模式标签页。

## STRUCTURE
```text
registry/                                 # 共 19 个 Java 文件
├── CABlocks.java, CAItems.java, CTNHBlockInfo.java, CACreativeModeTabs.java
├── CAEnvironments.java
├── CAMachines.java, CAMultiblocks.java
├── CARocketBlocks.java, CARocketEntityTypes.java
├── CARecipeTypes.java, CARecipeConditions.java, CARecipeModifiers.java
├── CARegistrate.java
├── sound/     (3)  CAMusics, CASoundDefinitionsProvider, CASoundEvents
└── worldgen/  (3)  AstralBlocks, MarsBlocks, MoonBlocks
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Registrate 根 | `registry/CARegistrate.java`（继承 CTNH-Lib `CNRegistrate`，提供 `movingEntity(...)`） |
| 方块构建辅助 | `registry/CABlocks.java`（`createStoneLikeBlock` / `createLogLikeBlock` / `createSandLikeBlock` / `createFlowerBlock` / `createTallGrassBlock` / `createDoublePlantBlock`） |
| 星界方块 | `registry/worldgen/AstralBlocks.java`（`ASTRAL_LOG`, `ASTRAL_STONE`, `ASTRAL_COBBLESTONE`, `ASTRAL_SAND`, `ASTRAL_SAPLING`, `BLUE_FLOWER`, `PINK_FLOWER`, `ASTRAL_GRASS`, `ASTRAL_TALL_GRASS`；`ASTRAL_DIRT` / `ASTRAL_GRASS_BLOCK` 字段在此声明） |
| 月球方块 | `registry/worldgen/MoonBlocks.java`（地质冰块与斜长岩、`MOON_SAND` / `MOONLIGHT_SAND` / `LUMINOUS_MOON_SAND`、`MOONLIGHT_CRYSTAL` / `LAYERED_MOONLIGHT_CRYSTAL`、硅晶系列 `IRIDESCENT_SILICON_CRYSTAL` / `SILICON_CRUST` / `SILICON_GRAVEL` / `SILICON_BRECCIA` / `BUDDING_SILICON_CRYSTAL` / 三档硅晶芽 / `SILICON_CRYSTAL`） |
| 火星方块 | `registry/worldgen/MarsBlocks.java`（火星岩 / 风化层 / 苔藓 / 干冰 / 玄武岩、星门框架 / 柱 / 核心 / 折光棱镜、遗迹机器、火星橡木系列） |
| 额外泥土与草方块 | `registry/CTNHBlockInfo.java`（静态块给 `AstralBlocks.ASTRAL_DIRT`、`AstralBlocks.ASTRAL_GRASS_BLOCK` 赋值，掉落走 `api/loot/LootBuilder`） |
| 物品 | `registry/CAItems.java`（辅助方法；`init()` 未注册任何物品，注册内容全为注释） |
| 环境类型与维度登记 | `registry/CAEnvironments.java`（`ATMOSPHERE` / `TEMPERATURE` / `CORROSION` / `RADIATION`，气体标识 `OXYGEN` / `NITROGEN` / `CARBON_DIOXIDE`，`registerDimension` / `registerBiomeModifier` / `registerClimateSource` / `registerBlockTemperature`） |
| 单方块机器 | `registry/CAMachines.java`（`OXYGEN_ENRICHER`，MV / HV / EV 三档） |
| 多方块 | `registry/CAMultiblocks.java`（`ROCKET_ASSEMBLY_PLATFORM`，9 宽 × 7 高 × 11 深图案，外壳 `AllBlocks.ANDESITE_CASING`，框架 `GTMaterials.StainlessSteel`） |
| 火箭部件 | `registry/CARocketBlocks.java`（`BASIC_ROCKET_THRUSTER` 推力 1200、`HV_ROCKET_FUEL_TANK` 容量 16000；`RocketPartStats` 映射供组装平台累加） |
| 火箭实体类型 | `registry/CARocketEntityTypes.java`（`ROCKET_CONTRAPTION`，`SimpleContraptionEntityRenderer` + `ContraptionVisual`） |
| 配方类型 | `registry/CARecipeTypes.java`（`ROCKET_ASSEMBLY_PLATFORM_RECIPE`, `OXYGEN_ENRICHER_RECIPES`） |
| 配方条件 | `registry/CARecipeConditions.java`（`OXYGEN` → `OxygenCondition`） |
| 配方修饰符 | `registry/CARecipeModifiers.java`（`environmentRequirements(...)`，按条件类型去重后追加） |
| 创造模式标签页 | `registry/CACreativeModeTabs.java`（`MACHINE`，图标 `AstralBlocks.ASTRAL_STONE`） |
| 音效 | `registry/sound/CASoundEvents.java`（`AMBIENT_ASTRAL`）、`CAMusics.java`（`ASTRAL_BGM`）、`CASoundDefinitionsProvider.java` |

## CONVENTIONS
- 注册类沿用 `CA` 前缀；创造模式标签页在 `CABlocks` / `CAMachines` / `CAMultiblocks` 的静态块里通过 `REGISTRATE.creativeModeTab(() -> CACreativeModeTabs.MACHINE)` 绑定。
- **初始化入口分层**：`CTNHAstralGTAddon.registerTagPrefixes()` 依次调用 `CABlocks.init()`（内部 `AstralBlocks.init()` → `MarsBlocks.init()` → `MoonBlocks.init()` → `CARocketBlocks.init()`）、`CAItems.init()`、`CTNHBlockInfo.init()`、`CATagPrefixes.init()`；`registerElements()` 调 `CAElements.init()`；`addRecipes()` 调 `CARecipes.init(provider)`。其余注册走 `CommonProxy.init()`（环境、网络、音效、附魔、医疗条件、伤害类型、创造标签、世界生成、实体类型）与 `CommonProxy.registerMachines(...)`（`CAMachines.init()` → `CAMultiblocks.init()`）。
- **`CTNHBlockInfo` 的赋值职责**：`ASTRAL_DIRT` / `ASTRAL_GRASS_BLOCK` 在 `AstralBlocks` 中只声明字段，实际创建在 `CTNHBlockInfo` 的静态块里完成，因此 `CTNHBlockInfo.init()` 必须排在 `CABlocks.init()` 之后、`CATagPrefixes.init()` 之前（`AstralBlocks.ASTRAL_STONE` 是矿脉 prefix 的基块）。
- **战利品表**：需要精准采集派发的方块用 `api/loot/LootBuilder.createSingleItemTableWithSilkTouch(block, itemLike)`（`AstralBlocks` / `MoonBlocks` / `CTNHBlockInfo`）；普通方块用 `RegistrateBlockLootTables::dropSelf`。
- **机器绑定配方类型的时机**：`CAMultiblocks` 的 `ROCKET_ASSEMBLY_PLATFORM` 与 `CAMachines` 的 `OXYGEN_ENRICHER` 都直接引用 `CARecipeTypes` 常量，改动配方类型 id 会同时影响注册与配方生成。
- **火箭部件元数据**：`CARocketBlocks` 在 `STATS` 里按 `CTNHAstral.id(name)` 存 `RocketPartStats(thrust, fuelCapacity)`；组装平台通过 `getStats(block)`（内部 `BuiltInRegistries.BLOCK.getKey(block)` 反查键）读取，新增部件必须走 `registerThruster` / `registerFuelTank` → `registerRocketPart` 才能进入统计。
- **环境登记时机**：`CAEnvironments.init()` 由 `CommonProxy.init()` 调用，内部依次登记 fallback、`CACelestialBodies.all()` 的天体维度、`Level.NETHER` / `Level.END`、`SolarSystemEnvironments.BIOME_MODIFIERS` 与 `VanillaEnvironments.BLOCK_TEMPERATURE_SOURCES`；所有登记入口都先调 `EnvironmentType.requireRegistrationOpen()`，重复键直接抛异常。
- **配方条件组合**：`CARecipeModifiers.environmentRequirements(...)` 每次应用都新建条件实例，只追加配方中尚不存在的同类型条件，不按机器或配方类型推断需求。
- **音效注册两段式**：`CASoundEvents.SOUND_EVENTS` 是 `DeferredRegister<SoundEvent>`，在 `CommonProxy.init()` 里 `register(eventBus)`；`CASoundDefinitionsProvider` 在 `gatherData` 的客户端分支产出 `sounds.json`。

## ANTI-PATTERNS
- 同一个条目同时从 `registry/` 和 `CommonProxy` 两处注册。
- 在 `common/machine/**` 内直接注册方块 / 物品 / 机器，绕过 `registry/**`。
- 引用物品 / 方块用 `ResourceLocation` 字符串 + `ForgeRegistries` 查找，而非 `CABlocks.*` / `CAItems.*` / `CAMaterials.*` 静态对象。
- 新增火箭部件时绕过 `registerRocketPart`，导致 `CARocketBlocks.STATS` 缺失、推力与燃料统计为 0。
- 在 `CATagPrefixes.init()` 之前引用矿脉 prefix，或让 `AstralBlocks.ASTRAL_STONE` 早于 `CABlocks.init()` 求值。
- 改动 `ASTRAL_DIRT` / `ASTRAL_GRASS_BLOCK` 的创建位置后不检查 `CTNHBlockInfo.init()` 在 GT addon 钩子里的次序。
- 在 `CAEnvironments` 里重复登记同一维度 / 群系 / 气候源 / 方块温度源（会抛 `IllegalArgumentException`）。

## SCOPE
适用于 `src/main/java/com/ctnh/ctnhastral/registry` 及其子包。

## READ WHEN
- 新增或修改 Astral 方块、物品、机器、多方块、火箭部件、实体类型、音效或环境登记。
- 新增配方类型、条件或修饰符。

## SOURCE OF TRUTH
- `registry/CARegistrate.java` 与 `CTNHAstralGTAddon.java` / `CommonProxy.init()` 的钩子顺序。
- 环境登记集合：`registry/CAEnvironments.java`。

## WORKFLOW
1. 先确定条目属于哪个注册类分组（世界生成方块 / 火箭部件 / 机器 / 音效 / 环境 ...）。
2. 核对 GT addon 钩子顺序与世界生成方块的初始化依赖。
3. 跑 `:modules:CTNH-Astral:build`；新增注册对象进 `runClient` 检查是否出现在创造栏。
