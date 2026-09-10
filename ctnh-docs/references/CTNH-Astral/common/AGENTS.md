# CTNH-ASTRAL COMMON DOMAIN

## OVERVIEW
Astral 的共享启动与实现核心（20 个 Java 文件）：`CommonProxy` 与 `CAFluidInteractions`、世界生成方块、真空密封附魔、火箭实体与跨维度转移、火箭组装/发射多方块、供氧机，以及 `oxygen/` 氧气与大气环境系统。常压环境判定已从机器控制器解耦，火箭转移不再依赖组装平台。

## STRUCTURE
```text
common/
├── CommonProxy.java, CAFluidInteractions.java
├── block/           (7) AstralGrass, AstralGrassBlock, AstralTallGrassBlock, AstralFlowerBlock,
│                        AstralSaplingBlock, MarsSaplingBlock, SiliconBuddingBlock
├── enchantment/     (1) VacuumSealEnchantment
├── entity/          (1) RocketContraptionEntity
├── event/           (1) RocketDimensionTravelHandler
├── machine/         (2) multiblock/RocketAssemblyPlatformMachine, simple/OxygenEnricherMachine
├── oxygen/          (5) AtmosphereType, OxygenAreaSource, OxygenEnvironment,
│                        OxygenEnvironmentService, OxygenMachineRules
└── recipe/          (1) OxygenCondition
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| 公共代理与注册顺序 | `common/CommonProxy.java` |
| 酸性流体交互 | `common/CAFluidInteractions.java`（`CAMaterials.Acid` + 水 → `Blocks.MUD`，+ 岩浆 → `Blocks.TUFF`） |
| 氧气环境解析 | `common/oxygen/OxygenEnvironmentService.java` |
| 氧气环境值对象 | `common/oxygen/OxygenEnvironment.java`, `common/oxygen/AtmosphereType.java` |
| 供氧源契约 | `common/oxygen/OxygenAreaSource.java`（`getOxygenSourcePos` / `getOxygenRange` / `isOxygenSourceActive`） |
| 机器耗氧规则 | `common/oxygen/OxygenMachineRules.java` |
| 氧气配方条件 | `common/recipe/OxygenCondition.java` |
| 真空密封附魔 | `common/enchantment/VacuumSealEnchantment.java` |
| 火箭实体与同步字段 | `common/entity/RocketContraptionEntity.java` |
| 火箭跨维度转移 | `common/event/RocketDimensionTravelHandler.java` |
| 组装/发射多方块 | `common/machine/multiblock/RocketAssemblyPlatformMachine.java` |
| 供氧机 | `common/machine/simple/OxygenEnricherMachine.java` |
| 世界生成方块类 | `common/block/`（星辉草木、火星树苗、硅晶芽） |

## CONVENTIONS
- **启动顺序**：`CommonProxy.init()` 依次挂 `GTRecipeType` / `MachineDefinition` / `RecipeConditionType` 泛型监听，注册 `CASoundEvents` 与 `CAEnchantments`，调 `CACreativeModeTabs.init()`、`CAFeatures.init(eventBus)`、`CAWorldCarvers.init(eventBus)`、`CARocketEntityTypes.init()`，最后 `REGISTRATE.registerRegistrate()` 并挂 `CNLANG` / `ProviderType.LANG` 语言处理器。新增钩子要放在依赖它的注册之前。
- **材料与调整**：`registerMaterials(MaterialEvent)` 调 `CAMaterials.init()` → `CAMaterials.tagPrefixIgnore()` → `GTMateralAdjust.init()`（把 `GTMaterials.Sulfur` 补成带方块的液体）。
- **commonSetup**：在 `event.enqueueWork(...)` 中调 `CAFluidInteractions.register()`，注册 TerraBlender 的 `CAOverworldRegion(2)` 与 `CANetherRegion(5)`，并挂 OVERWORLD（`CASurfaceRuleData.customSurface()`）与 NETHER（`acidValleySurface()`）地表规则。
- **gatherData**：`RegistrySetBuilder` 引导 `CONFIGURED_CARVER` / `BIOME` / `CONFIGURED_FEATURE` / `PLACED_FEATURE` / `DIMENSION_TYPE` / `LEVEL_STEM` / `NOISE_SETTINGS` / `STRUCTURE` / `STRUCTURE_SET` / `DENSITY_FUNCTION` 十个注册表；客户端侧只加 `CASoundDefinitionsProvider`，服务端侧另加 `CABiomeTagsProvider`。`registerMisc(RegisterEvent)` 单独初始化 5 个 `Structure` 类。
- **氧气系统**：`OxygenEnvironmentService.getEnvironment(level, pos)` 的判定顺序是 ① `OxygenApi.API.hasOxygen(level, pos)` → `BREATHABLE`；② 非 `ServerLevel` 直接返回 `VACUUM`；③ 在 32 格（`MAX_SOURCE_SEARCH`）范围内按区块扫描 `OxygenAreaSource` 方块实体，用 Ad Astra `FloodFill3D.run(..., TEST_FULL_SEAL, true)` 计算密闭区域并取最大连通集，命中则返回 `SEALED_OXYGENATED`；④ 否则 `VACUUM`。密闭块数上限为 `min(8192, max(256, range² × 4))`。
- **自然可呼吸维度**：`isNaturallyBreathable(level)` 对 `minecraft:overworld`、`nether`、`end` 及路径为 `earth` 的维度返回 `true`。
- **机器耗氧规则**：`OxygenMachineRules.requiresOxygen(GTRecipeType)` 目前只覆盖 `GTRecipeTypes.COMBUSTION_GENERATOR_FUELS`、`GAS_TURBINE_FUELS`、`STEAM_TURBINE_FUELS`。
- **供氧机**：`OxygenEnricherMachine extends SimpleTieredMachine implements OxygenAreaSource`，进口仓只接受 `GTMaterials.Oxygen`；范围 `12 + tier × 4`，启用条件为 `isActive() && isWorkingEnabled()`；每 20 tick（`getOffsetTimer() % 20`）重算 FloodFill 集合并按差集调 `OxygenApi.API.setOxygen/removeOxygen` 与 `TemperatureApi.API.setTemperature/removeTemperature`（宜居温度 `HABITABLE_TEMPERATURE = 22`）；`onUnload` / `onMachineRemoved` 会清空已分发区块。
- **附魔**：`VacuumSealEnchantment` 是 `Rarity.VERY_RARE` 的护甲附魔，注册 id `ctnhastral:vacuum_seal`（`CAEnchantments.VACUUM_SEAL`），不可交易且仅限宝藏；`hasFullEnchant(entity)` 要求玩家四个护甲槽全部带该附魔（创造/旁观直接通过）。
- **火箭实体**：`RocketContraptionEntity.create(Level, Contraption, Vec3)` 无控制器，内部走 `createDetached(level, contraption, persistenceAnchor, pivot)`；`getController()` 返回 `null`，`setPersistenceAnchor()` 只是把 `controllerPos` 当作惰性锚点以满足 `SimpleRotatingContraptionEntity` 的序列化要求。座位在 `ensureSeatsRegistered()` 中按 `SeatBlock` 自动补登记。
- **火箭实体持久化**：`writeAdditional` / `readAdditional` 读写 `RocketAssembled`、`RocketLaunching`、`RocketLaunchTicks`、`RocketCountdownTicks`、`RocketLanding`、`RocketLandingPad`、`RocketThrust`、`RocketFuelCapacity`、`RocketRemainingFuel`；旧存档缺 `RocketRemainingFuel` 或 `RocketCountdownTicks` 时分别回落到满燃料与 `200`，并在读取时移除遗留的持久化数据键 `CTNHAstralRocket`。
- **火箭同步字段**：`DATA_MOTION` / `DATA_ASSEMBLED` / `DATA_LAUNCHING` / `DATA_LAUNCH_TICKS` / `DATA_COUNTDOWN_TICKS` / `DATA_LANDING` 是客户端唯一数据来源；`setRocketStats` / `setRocketLaunchState` 仅在服务端赋值。
- **组装平台持久化**：`RocketAssemblyPlatformMachine` 用 LDLib `@Persisted` 托管字段 `rocketThrust`(`RocketThrust`)、`rocketFuelCapacity`(`RocketFuelCapacity`)、`rocketRemainingFuel`(`RocketRemainingFuel`)、`launching`(`RocketLaunching`)、`launchTicks`(`RocketLaunchTicks`)，值变化自动驱动 dirty 与保存，无需手动 `markDirty()`；`loadCustomPersistedData` 在缺 `RocketRemainingFuel` 时把燃料补满。
- **组装与发射**：组装从 `collectRocketBlocksForAssembly()` 出发（Create 座位 tag `create:seats` 或 `*_seat` 方块作为种子，在缓存的活动层范围内 BFS 连通），推力与燃料容量按 `CARocketBlocks.getStats(block)` 累加；发射由玩家跳跃触发，倒计时 `COUNTDOWN_TICKS = 200`，之后每 tick 扣 `max(1, rocketThrust / 240)` 燃料，加速度 `min(0.18, (0.025 + thrust / 140000) × min(1, poweredTicks / 120))`，纵向速度上限 `1.8`；高度达到 `AdAstraConfig.atmosphereLeave` 时给乘客打开 Ad Astra 行星选择界面并清空火箭数据。
- **跨维度转移**：`RocketDimensionTravelHandler` 在 `EntityTravelToDimensionEvent` 中按玩家 UUID 记录 `PendingTransfer`（火箭实例 + contraption NBT 快照 + `RocketState` 快速存档），先 `player.stopRiding()`；到达后在 `PlayerChangedDimensionEvent` 中用 `AllBlocks.ANDESITE_CASING` 铺半径 4 的着陆平台，把火箭放到 `min(padY + 1 + 128, maxBuildHeight - 4)` 并 `beginLanding(pad)`。`changeDimension` 失败时用快照 `Contraption.fromNBT` 重建，再 `RocketState.apply(rocket)` 恢复推力/燃料/发射态。
- **降落**：`beginLanding` 后服务端每 tick 以最大 `1.2`、每 tick 加速度 `0.04` 下降，到达 `padY + 1` 归零并结束降落。

## TRAIT OWNERSHIP
`OxygenEnricherMachine` 内联 `OxygenEnricherRecipeLogic extends RecipeLogic`。约束以 `references/_architecture/AGENTS.md` 为准，本域重点：

- 氧气/大气环境状态（`common/oxygen/`）的所有权归 service 与机器，不要在 trait 与机器间重复持有。
- 需要客户端读取的环境状态用 `@DescSynced` 承载，不要为 Jade/HUD 另开一条 NBT 通道。
- `OxygenEnricherRecipeLogic` 只做结果判定（`matchRecipe` 检查进口仓是否为氧气，失败返回 `ActionResult.fail`），`RecipeLogic` 不做 capability 类型判断；配方内容解释归 recipe capability。
- 供氧分发状态 `distributedBlocks` 归机器自身，随 `onLoad` / `onUnload` / `onMachineRemoved` 生命周期增删，不要放进取能逻辑。

## ANTI-PATTERNS
- 绕过 `CommonProxy` 的注册顺序自建初始化路径。
- 在 `RocketDimensionTravelHandler` 里重新引入基于组装平台控制器的传送逻辑；转移只用 `RocketState` 捕获/回填。
- 把火箭转移状态写回遗留的 `CTNHAstralRocket` 持久化数据键；实体 NBT 字段才是权威来源。
- 对 `RocketAssemblyPlatformMachine` 的 `@Persisted` 火箭字段调用 `markDirty()`。
- 在 `common/` 内用物品/方块 ID 字符串反查注册对象，而非 `CABlocks.*` / `CAItems.*` / `CAMaterials.*` 等静态对象。
- 新增氧气源时绕过 `OxygenAreaSource` 契约，或在机器与 service 之间重复缓存密闭区块集合。

## SCOPE
适用于 `src/main/java/com/ctnh/ctnhastral/common` 及其子包。

## READ WHEN
- 修改 Astral 启动、附魔、火箭、供氧系统或方块实现。
- 修改火箭跨维度转移的状态持久化、落点或降落行为。
- 调整氧气/温度判定与密闭空间算法。

## SOURCE OF TRUTH
- `common/CommonProxy.java` 与 `CTNHAstral.java`。
- 火箭转移与降落：`common/event/RocketDimensionTravelHandler.java`, `common/entity/RocketContraptionEntity.java`, `common/machine/multiblock/RocketAssemblyPlatformMachine.java`。
- 氧气系统：`common/oxygen/**`。

## WORKFLOW
1. 新增钩子前先核对 `CommonProxy` 的注册顺序与依赖。
2. 火箭相关改动把 `RocketDimensionTravelHandler` 的捕获/回填与实体 NBT 读写放在一起追。
3. 跑 `:modules:CTNH-Astral:build`；火箭与供氧行为必须进 `runClient` 验证。
