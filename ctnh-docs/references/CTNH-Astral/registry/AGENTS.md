# CTNH-ASTRAL REGISTRY DOMAIN

## OVERVIEW
Astral 的注册面（18 个 Java 文件）：方块（含月球/火星/星界世界生成方块与火箭部件）、物品、单方块机器与多方块、火箭实体类型、音效与音乐、配方类型/条件/修饰符、创造模式标签页。

## STRUCTURE
```text
registry/                                 # 共 18 个 Java 文件
├── CARegistrate.java, CABlocks.java, CAItems.java, CACreativeModeTabs.java
├── CAMachines.java, CAMultiblocks.java
├── CARocketBlocks.java, CARocketEntityTypes.java
├── CARecipeTypes.java, CARecipeConditions.java, CARecipeModifiers.java
├── CTNHBlockInfo.java
├── sound/     (3)  CAMusics, CASoundDefinitionsProvider, CASoundEvents
└── worldgen/  (3)  AstralBlocks, MarsBlocks, MoonBlocks
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Registrate 根 | `registry/CARegistrate.java`（继承 CTNH-Lib `CNRegistrate`，提供 `movingEntity(...)`） |
| 方块构建辅助 | `registry/CABlocks.java`（`createStoneLikeBlock` / `createLogLikeBlock` / `createSandLikeBlock` / `createFlowerBlock` / `createTallGrassBlock` / `createDoublePlantBlock`） |
| 星界世界生成方块 | `registry/worldgen/AstralBlocks.java` |
| 月球方块 | `registry/worldgen/MoonBlocks.java`（含 `BUDDING_SILICON_CRYSTAL` 与三档硅晶芽） |
| 火星方块 | `registry/worldgen/MarsBlocks.java`（含星门框架/柱/核心/折光棱镜、遗迹机器） |
| 额外泥土与草方块 | `registry/CTNHBlockInfo.java`（`ASTRAL_DIRT`, `ASTRAL_GRASS_BLOCK`，掉落走 `api/loot/LootBuilder`） |
| 物品 | `registry/CAItems.java`（辅助方法；`init()` 未注册任何物品，注册内容全为注释） |
| 单方块机器 | `registry/CAMachines.java`（`OXYGEN_ENRICHER`，MV/HV/EV 三档） |
| 多方块 | `registry/CAMultiblocks.java`（`ROCKET_ASSEMBLY_PLATFORM`，9×7×11 图案，外壳 `AllBlocks.ANDESITE_CASING`，框架不锈钢） |
| 火箭部件 | `registry/CARocketBlocks.java`（`BASIC_ROCKET_THRUSTER` 推力 1200、`HV_ROCKET_FUEL_TANK` 容量 16000；`RocketPartStats` 映射供组装平台累加） |
| 火箭实体类型 | `registry/CARocketEntityTypes.java`（`ROCKET_CONTRAPTION`，`SimpleContraptionEntityRenderer`） |
| 配方类型 | `registry/CARecipeTypes.java`（`ROCKET_ASSEMBLY_PLATFORM_RECIPE`, `OXYGEN_ENRICHER_RECIPES`） |
| 配方条件 | `registry/CARecipeConditions.java`（`OXYGEN` → `oxygen_condition`） |
| 配方修饰符 | `registry/CARecipeModifiers.java`（`oxygenRequirement`，去重后追加 `OxygenCondition`） |
| 创造模式标签页 | `registry/CACreativeModeTabs.java`（`MACHINE`） |
| 音效 | `registry/sound/CASoundEvents.java`（`AMBIENT_ASTRAL`）、`CAMusics.java`（`ASTRAL_BGM`）、`CASoundDefinitionsProvider.java` |

## CONVENTIONS
- 注册类沿用 `CA` 前缀；创造模式标签页在 `CABlocks` / `CAMachines` / `CAMultiblocks` 的静态块里通过 `REGISTRATE.creativeModeTab(() -> CACreativeModeTabs.MACHINE)` 绑定。
- **初始化入口分层**：`CTNHAstralGTAddon.registerTagPrefixes()` 依次调用 `CABlocks.init()`（内部 `AstralBlocks.init()` → `MarsBlocks.init()` → `MoonBlocks.init()` → `CARocketBlocks.init()`）、`CAItems.init()`、`CTNHBlockInfo.init()`、`CATagPrefixes.init()`；`registerElements()` 调 `CAElements.init()`；`addRecipes()` 调 `CARecipes.init(provider)`。其余注册走 `CommonProxy.init()`（音效、附魔、创造标签、地物、雕刻器、实体类型）与 `CommonProxy.registerMachines(...)`（`CAMachines.init()` → `CAMultiblocks.init()`）。
- **战利品表**：需要精准采集派发的方块用 `api/loot/LootBuilder.createSingleItemTableWithSilkTouch(block, itemLike)`；普通方块用 `RegistrateBlockLootTables::dropSelf`。
- **机器绑定配方类型的时机**：`CAMultiblocks` 的 `ROCKET_ASSEMBLY_PLATFORM` 与 `CAMachines` 的 `OXYGEN_ENRICHER` 都直接引用 `CARecipeTypes` 常量，改动配方类型 id 会同时影响注册与配方生成。
- **火箭部件元数据**：`CARocketBlocks` 在 `STATS` 里按方块 id 存 `RocketPartStats(thrust, fuelCapacity)`；组装平台通过 `getStats(block)` 读取，新增部件必须走 `registerThruster` / `registerFuelTank` 才能进入统计。

## ANTI-PATTERNS
- 同一个条目同时从 `registry/` 和 `CommonProxy` 两处注册。
- 在 `common/machine/**` 内直接注册方块/物品/机器，绕过 `registry/**`。
- 引用物品/方块用 `ResourceLocation` 字符串 + `ForgeRegistries` 查找，而非 `CABlocks.*` / `CAItems.*` / `CAMaterials.*` 静态对象。
- 新增火箭部件时绕过 `registerRocketPart`，导致 `CARocketBlocks.STATS` 缺失、推力与燃料统计为 0。
- 在 `CATagPrefixes.init()` 之前引用矿脉 prefix，或让 `oreAstralStone` 早于 `AstralBlocks.ASTRAL_STONE` 求值。

## SCOPE
适用于 `src/main/java/com/ctnh/ctnhastral/registry` 及其子包。

## READ WHEN
- 新增或修改 Astral 方块、物品、机器、多方块、火箭部件、实体类型或音效。
- 新增配方类型、条件或修饰符。

## SOURCE OF TRUTH
- `registry/CARegistrate.java` 与 `CTNHAstralGTAddon.java` / `CommonProxy.init()` 的钩子顺序。

## WORKFLOW
1. 先确定条目属于哪个注册类分组（世界生成方块 / 火箭部件 / 机器 / 音效 ...）。
2. 核对 GT addon 钩子顺序与世界生成方块的初始化依赖。
3. 跑 `:modules:CTNH-Astral:build`；新增注册对象进 `runClient` 检查是否出现在创造栏。
