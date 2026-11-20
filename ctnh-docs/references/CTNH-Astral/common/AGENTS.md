# CTNH-ASTRAL COMMON DOMAIN

## OVERVIEW
Astral 的共享启动与实现核心（49 个 Java 文件）：`CommonProxy` 与 `CAFluidInteractions`、世界生成方块实现类、真空密封附魔、火箭实体与火箭组装 / 发射 / 跨维度转移、供氧机、类型化环境模型（`environment/`）、天体定义与传送器（`universe/`）、网络通道（`network/`）、医疗条件桥（`medical/`）、氧气消费规则（`oxygen/`）、航天常量（`space/`）。

## STRUCTURE
```text
common/                                    # 共 49 个 Java 文件
├── CommonProxy.java, CAFluidInteractions.java
├── block/           (8) AstralGrass, AstralGrassBlock, AstralTallGrassBlock, AstralFlowerBlock,
│                        AstralSaplingBlock, MarsSaplingBlock, MoonlightCrystalBlock, SiliconBuddingBlock
├── enchantment/     (1) VacuumSealEnchantment
├── entity/          (1) RocketContraptionEntity
├── environment/     (10) Atmosphere, BlockTemperature, Corrosion, Environment, EnvironmentEmission,
│                         EnvironmentType, NaturalTemperature, PlanetEnvironmentService, Radiation,
│                         Temperature
├── event/           (2) CelestialTravelHandler, RocketDimensionTravelHandler
├── machine/         (2) multiblock/RocketAssemblyPlatformMachine, simple/OxygenEnricherMachine
├── medical/         (2) MedicalConditionEventHandler, PlayerThermalProtectionEvent
├── network/         (5) CANetwork, C2SRequestTemperaturePacket, C2STeleportToBodyPacket,
│                        S2COpenCelestialScreenPacket, S2CTemperaturePacket
├── oxygen/          (1) OxygenMachineRules
├── recipe/          (1) OxygenCondition
├── space/           (1) CASpaceConstants
└── universe/        (13) CACelestialBodies, CelestialBody, CelestialBodyType, CelestialDisplay,
                         CelestialPosition, CelestialRingDisplay, CelestialTeleportTargets,
                         CelestialTeleporter, CelestialEntityTeleporter, DirectCelestialTeleporter,
                         OrbitCelestialTeleporter, OrbitalCelestialPosition, StaticCelestialPosition
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| 公共代理与注册顺序 | `common/CommonProxy.java` |
| 酸性流体交互 | `common/CAFluidInteractions.java`（`CAMaterials.Acid` + 水 → `Blocks.MUD`，+ 岩浆 → `Blocks.TUFF`） |
| 环境类型代数契约 | `common/environment/EnvironmentType.java`（`register` / `registerScalar` / `freeze` / `requireRegistrationOpen`） |
| 环境快照与增量 | `common/environment/{Environment, EnvironmentEmission, Atmosphere, Temperature, Corrosion, Radiation}.java` |
| 环境查询与排放生命周期 | `common/environment/PlanetEnvironmentService.java`（`getEnvironment`, `emit`, `cease`） |
| 自然温度与方块温度 | `common/environment/{NaturalTemperature, BlockTemperature}.java`, `registry/CAEnvironments.java` |
| 氧气配方条件 | `common/recipe/OxygenCondition.java` |
| 机器耗氧 / 进气规则 | `common/oxygen/OxygenMachineRules.java`（`hasRequiredAtmosphere`） |
| 真空密封附魔 | `common/enchantment/VacuumSealEnchantment.java` |
| 火箭实体与同步字段 | `common/entity/RocketContraptionEntity.java` |
| 火箭跨维度转移 | `common/event/RocketDimensionTravelHandler.java` |
| 星图选点后的传送 | `common/event/CelestialTravelHandler.java` |
| 组装 / 发射多方块 | `common/machine/multiblock/RocketAssemblyPlatformMachine.java` |
| 供氧机 | `common/machine/simple/OxygenEnricherMachine.java` |
| 医疗条件桥 | `common/medical/MedicalConditionEventHandler.java` |
| 玩家热防护贡献事件 | `common/medical/PlayerThermalProtectionEvent.java` |
| 网络通道 | `common/network/CANetwork.java` |
| 天体定义 | `common/universe/{CACelestialBodies, CelestialBody, CelestialBodyType, CelestialDisplay, CelestialRingDisplay}.java` |
| 天体位置与轨道 | `common/universe/{CelestialPosition, StaticCelestialPosition, OrbitalCelestialPosition}.java` |
| 跨维度落点 | `common/universe/{CelestialEntityTeleporter, CelestialTeleportTargets, CelestialTeleporter, DirectCelestialTeleporter, OrbitCelestialTeleporter}.java` |
| 航天常量 | `common/space/CASpaceConstants.java`（`ORBIT_ALTITUDE = 1000.0D`, `LAUNCH_COUNTDOWN = 200`） |
| 世界生成方块类 | `common/block/`（星辉草木、火星树苗、月辉晶石、硅晶母岩） |

## CONVENTIONS
- **启动顺序**：`CommonProxy.init()` 依次调 `CAEnvironments.init()`、`CANetwork.init()`，挂 `GTRecipeType` / `MachineDefinition` / `RecipeConditionType` 泛型监听（分别转发 `CARecipeTypes.init()`、`CAMachines.init()` + `CAMultiblocks.init()`、`CARecipeConditions.init()`），注册 `CASoundEvents.SOUND_EVENTS` 与 `CAEnchantments.Enchantments`，调 `CAMedicalConditions.init()`、`CADamageTypes.init()`、`CACreativeModeTabs.init()`、`CAWorldgen.init(eventBus)`、`CARocketEntityTypes.init()`，最后 `REGISTRATE.registerRegistrate()` 并挂 `CNLANG` / `ProviderType.LANG` 语言处理器。新增钩子要放在依赖它的注册之前。
- **材料与调整**：`registerMaterials(MaterialEvent)` 调 `CAMaterials.init()` → `GTMateralAdjust.init()`（把 `GTMaterials.Sulfur` 补成带方块的液体）；`commonSetup` 的 `event.enqueueWork(...)` 里再调 `CAMaterials.tagPrefixIgnore()`。
- **commonSetup**：`event.enqueueWork(...)` 内依次执行 `CAMaterials.tagPrefixIgnore()`、`CAFluidInteractions.register()`、`CAWorldgen.commonSetup()`；TerraBlender 的 OVERWORLD / NETHER 区域与地表规则挂在 `CAWorldgen.commonSetup()`（`VanillaWorldgen.overworldRegion()` / `netherRegion()` / `overworldSurface()` / `netherSurface()`）。
- **loadComplete**：`FMLLoadCompleteEvent` 的 `event.enqueueWork(...)` 只做 `EnvironmentType.freeze()`，冻结后环境类型与静态群系修饰不再接受新增。
- **gatherData**：`DatapackBuiltinEntriesProvider` 的注册表集合来自 `CAWorldgen.addRegistries(new RegistrySetBuilder())`，再追加 `Registries.DAMAGE_TYPE` → `CADamageTypes::bootstrap`；命名空间集合为 `{ctnhastral, gtceu}`（damage type 键位于 gtceu 命名空间）。客户端侧加 `CASoundDefinitionsProvider`，服务端侧用同一 provider 的 `getRegistryProvider()` 供 `CADamageTypeTagsProvider` 与 `CABiomeTagsProvider` 取 lookup。
- **环境模型**：`EnvironmentType<V, D>` 自持默认值、零增量、加法、缩放与约束；值对象不可变，增量可交换相加，负增量不在中途截断。`Environment.get(type)` 对缺失类型回落该类型默认值；`Environment.applyDelta(delta)` 是唯一合成入口，维度基准本身不被修改。
- **环境合成顺序**：`PlanetEnvironmentService.getEnvironment(level, pos)` = 维度基准（`CAEnvironments.dimension(...)`）+ 群系修饰（`CAEnvironments.biomeModifier(...)`）+ 自然温度偏移（`definition.temperature().offsetK(...)`，气候源经 `CAEnvironments.climate(...)`）+ 可选方块温度（`definition.blockTemperatureEnabled()` 时叠加 `BlockTemperature.offsetK(...)`）+ 同维度有效排放增量。查询只接受 `ServerLevel`，区域合成为 O(区数)，不加载区块。
- **排放生命周期**：`emit(level, emission, lifetimeTicks)` 以 `emission.source()` 为同源键写入并计算到期 tick，租期必须为正数；`cease(level, source)` 按同源键撤销，重复撤销无副作用；过期记录在下次查询时清除。排放不跨世界会话持久化。
- **氧气 / 燃烧规则**：`OxygenMachineRules.hasRequiredAtmosphere(machine)` 在正面外侧取 `PlanetEnvironmentService` 快照：总压 ≥ `MIN_COMBUSTION_PRESSURE = 0.2F` 且氧分压 ≥ `MIN_COMBUSTION_OXYGEN = 0.16F`；非 `ServerLevel` 直接返回 `true`。
- **氧气条件**：`OxygenCondition extends RecipeCondition<OxygenCondition>`，`perTick()` 为 `true`，`testCondition` 在 `ConfigHolder.INSTANCE.gameplay.hazardsEnabled` 关闭时直接放行，否则交给 `OxygenMachineRules.hasRequiredAtmosphere(recipeLogic.getMachine())`；类型注册在 `CARecipeConditions.OXYGEN`。工具提示文案来自 `@CN` / `@EN` 注解的 `Lang` 字段。
- **供氧机**：`OxygenEnricherMachine extends SimpleTieredMachine`，进口仓 `setFilter` 只接受 `GTMaterials.Oxygen`；`isActive() && isWorkingEnabled()` 时每 20 tick 经 `getOffsetTimer() % 20` 续期 40 tick 的排放：范围 `12 + tier × 4`，密封体积上限 `min(8192, max(256, range² × 4))`，向六个方向播种对可通行空间做 FloodFill，取最大密封集；增量固定为 +8 K 温度与 0.21 atm 总压 / 0.21 氧分压。密封集为空时退化为 `EnvironmentEmission.Sphere(range)`。`onUnload` / `onMachineRemoved` 调 `cease` 撤销。
- **附魔**：`VacuumSealEnchantment` 是 `Rarity.VERY_RARE` 的四槽护甲附魔，注册 id `ctnhastral:vacuum_seal`（`CAEnchantments.VACUUM_SEAL`），`isTradeable()` 为 `false`、`isTreasureOnly()` 为 `true`，成本区间 165～200；`hasFullEnchant(entity)` 要求玩家全部护甲槽都带该附魔（创造 / 旁观直接通过）。
- **火箭实体**：`RocketContraptionEntity.create(Level, Contraption, Vec3)` 无控制器，内部走 `createDetached(level, contraption, persistenceAnchor, pivot)`；`getController()` 返回 `null`，`setPersistenceAnchor()` 只把 `controllerPos` 当作惰性锚点以满足 `SimpleRotatingContraptionEntity` 的序列化要求。`ensureSeatsRegistered()` 按 `SeatBlock` 自动补登记座位。
- **座位跨维度映射**：`rememberTransferSeat(passenger, localSeat)` 记录乘客与本地座位，`writeAdditional` 写入 `RocketTransferPassenger` / `RocketTransferSeat`，`readAdditional` 读回后由 `applyTransferSeat()` 写进 `contraption.getSeatMapping()`；`mountAtSeat(passenger, localSeat)` 按座位索引挂载，座位未知时退到第一个座位。
- **火箭实体持久化**：`writeAdditional` / `readAdditional` 读写 `RocketAssembled`、`RocketLaunching`、`RocketLaunchTicks`、`RocketCountdownTicks`、`RocketLanding`、`RocketLandingPad`、`RocketThrust`、`RocketFuelCapacity`、`RocketRemainingFuel`；缺 `RocketRemainingFuel` 时回落到 `RocketFuelCapacity`，缺 `RocketCountdownTicks` 时回落到 `200`，读取服务端侧会移除持久化数据键 `CTNHAstralRocket` 并恢复 `setRunning(true)`。
- **火箭同步字段**：`DATA_MOTION` / `DATA_ASSEMBLED` / `DATA_LAUNCHING` / `DATA_LAUNCH_TICKS` / `DATA_COUNTDOWN_TICKS` / `DATA_LANDING` 是客户端唯一数据来源；`setRocketStats` / `setRocketLaunchState` / `setContraptionMotion` 的服务端分支才赋值。`onSyncedDataUpdated` 在客户端把 `DATA_MOTION` 回灌到 `setContraptionMotion`。
- **客户端插值**：`lerpTo(x, y, z, yRot, xRot, lerpSteps, teleport)` 在 `teleport` 或 `lerpSteps <= 0` 时直接落位，否则缓存目标并在 `tickLerpMovement()` 中按 `1 / lerpSteps` 逐步逼近位置与朝向。
- **组装平台持久化**：`RocketAssemblyPlatformMachine` 用 LDLib `@Persisted` 托管字段 `rocketThrust`(`RocketThrust`)、`rocketFuelCapacity`(`RocketFuelCapacity`)、`rocketRemainingFuel`(`RocketRemainingFuel`)、`launching`(`RocketLaunching`)、`launchTicks`(`RocketLaunchTicks`)，值变化自动驱动 dirty 与保存，无需手动 `markDirty()`；`loadCustomPersistedData` 在缺 `RocketRemainingFuel` 时把燃料补满。
- **组装与发射**：组装从 `collectRocketBlocksForAssembly()` 出发，种子是 Create 座位 tag（`CREATE_SEATS` 或 `create:*_seat` 方块），推力与燃料容量按 `CARocketBlocks.getStats(block)` 累加；发射由玩家跳跃触发（`handleRocketPassengerJump` → `findPlatformBelowRocket` → `handlePassengerJump`），倒计时 `CASpaceConstants.LAUNCH_COUNTDOWN = 200`，之后每 tick 扣 `max(1, rocketThrust / 240)` 燃料，加速度 `min(0.18, (0.025 + thrust / 140000) × min(1, poweredTicks / 120))`，纵向速度上限 `1.8`，横向速度乘 `0.88`；高度达到 `CASpaceConstants.ORBIT_ALTITUDE = 1000` 时给乘客发 `S2COpenCelestialScreenPacket`、登记 `CelestialTravelHandler.openScreen(...)` 并清空火箭数据。
- **跨维度转移**：`RocketDimensionTravelHandler` 在 `EntityTravelToDimensionEvent` 中按玩家 UUID 记录 `PendingTransfer`（火箭实例 + contraption NBT 快照 + `RocketState` + 座位），先 `player.stopRiding()`；到达后在 `PlayerChangedDimensionEvent` 中用 `AllBlocks.ANDESITE_CASING` 铺半径 4 的着陆平台，把火箭放到 `min(padY + 1 + 128, maxBuildHeight - 4)` 并 `beginLanding(pad)`，`mountAtSeat` 失败时 `ejectPassengers()`。`changeDimension` 未返回火箭时用快照 `Contraption.fromNBT` 重建，再 `RocketState.apply(rocket)` 恢复推力 / 燃料 / 发射态。
- **星图选点**：`CelestialTravelHandler.openScreen(player, fromBodyId, rocketTier, rocketId)` 记录 600 tick 会话；`travel(player, bodyId)` 校验会话有效期、目标可旅行、目标 tier 与火箭 tier，用 `IN_FLIGHT` 防重入，再 `player.changeDimension(destination, CelestialEntityTeleporter.of(target))`；失败时释放 `IN_FLIGHT`。`PlayerChangedDimensionEvent` / `PlayerLoggedOutEvent` 清理会话。
- **传送落点**：`CelestialEntityTeleporter` 委托天体的 `CelestialTeleporter`，异常时回落到 `CelestialTeleportTargets.clampY(level, seaLevel + 32)`；`CelestialTeleportTargets.surface(...)` 先同步加载区块再按 `MOTION_BLOCKING_NO_LEAVES` 取地表。
- **降落**：`beginLanding` 后服务端每 tick 以 `LANDING_MAX_SPEED = 1.2` 为上限、`LANDING_ACCELERATION = 0.04` 加速下降，到达 `padY + 1` 归零并结束降落。
- **网络通道**：`CANetwork.CHANNEL` 的协议版本为 `"2"`，按注册顺序分配 `S2COpenCelestialScreenPacket`、`C2STeleportToBodyPacket`、`C2SRequestTemperaturePacket`（`PLAY_TO_SERVER`）、`S2CTemperaturePacket`（`PLAY_TO_CLIENT`）。温度请求只允许查询玩家 64 格内已加载区块，每游戏刻段（`gameTime / 20`）最多 16 次。
- **医疗条件桥**：`MedicalConditionEventHandler` 单向依赖环境层与 GT `IMedicalConditionTracker`；阈值为 `LOW_PRESSURE_THRESHOLD = 0.0618F`、`BREATHABLE_OXYGEN = 0.16F`、`SEVERE_HYPOXIA_OXYGEN = 0.12F`，缺氧毛速率 +2/s，节拍 `DAMAGE_INTERVAL = 40`；`GT hazardsEnabled=false` 时整体关停。装备侧的热 / 冷防护通过 `PlayerThermalProtectionEvent` 追加，不在环境快照里改写。

## TRAIT OWNERSHIP
`OxygenEnricherMachine` 内联 `OxygenEnricherRecipeLogic extends RecipeLogic`。约束以 `ctnh-docs/references/_architecture/AGENTS.md` 为准，本域重点：

- 环境状态（`common/environment/`）的所有权归 `PlanetEnvironmentService` 的维度区表；机器只提交 `EnvironmentEmission`，不在机器侧二次缓存快照。
- 需要客户端读取的环境状态走 `S2CTemperaturePacket` + `client/ClientEnvironmentTemperature`，不要为 HUD 另开一条 NBT 通道。
- `OxygenEnricherRecipeLogic` 只做结果判定：`matchRecipe` 检查进口仓是否为氧气，失败返回 `ActionResult.fail(NO_OXYGEN_INPUT, null, IO.IN)`，`findAndHandleRecipe` 在无配方且无失败原因时 `setWaiting(NO_OXYGEN_INPUT)`；`RecipeLogic` 不做 capability 类型判断。
- 供氧分发状态归 `PlanetEnvironmentService` 的区表，随 `onLoad` / `onUnload` / `onMachineRemoved` 生命周期续期与撤销，不要放进取能逻辑。

## ANTI-PATTERNS
- 绕过 `CommonProxy` 的注册顺序自建初始化路径。
- 在 `RocketDimensionTravelHandler` 里用组装平台控制器定位火箭；转移只用火箭实体实例与 `RocketState` 捕获 / 回填。
- 把火箭转移状态写回 `CTNHAstralRocket` 持久化数据键；实体 NBT 字段才是权威来源。
- 对 `RocketAssemblyPlatformMachine` 的 `@Persisted` 火箭字段调用 `markDirty()`。
- 在 `common/` 内用物品 / 方块 ID 字符串反查注册对象，而非 `CABlocks.*` / `CAItems.*` / `CAMaterials.*` 等静态对象。
- 在机器侧直接改环境基准或缓存环境快照；来源只提交增量，合成只经 `PlanetEnvironmentService`。
- 在 `FMLLoadCompleteEvent` 之后注册 `EnvironmentType` 或静态群系修饰。
- 在服务端分支之外调用 `setRocketStats` / `setRocketLaunchState`。

## SCOPE
适用于 `src/main/java/com/ctnh/ctnhastral/common` 及其子包。

## READ WHEN
- 修改 Astral 启动、附魔、火箭、供氧系统或方块实现。
- 修改火箭跨维度转移的状态持久化、座位映射、落点或降落行为。
- 修改环境类型、环境合成顺序、排放生命周期或医疗条件阈值。
- 新增网络包或天体传送路径。

## SOURCE OF TRUTH
- `common/CommonProxy.java` 与 `CTNHAstral.java`。
- 火箭转移与降落：`common/event/{RocketDimensionTravelHandler, CelestialTravelHandler}.java`, `common/entity/RocketContraptionEntity.java`, `common/machine/multiblock/RocketAssemblyPlatformMachine.java`。
- 环境系统：`common/environment/**` 与 `registry/CAEnvironments.java`。
- 氧气消费：`common/recipe/OxygenCondition.java`, `common/oxygen/OxygenMachineRules.java`。

## WORKFLOW
1. 新增钩子前先核对 `CommonProxy.init()` / `commonSetup` / `loadComplete` 的顺序与依赖。
2. 火箭相关改动把 `RocketDimensionTravelHandler` 的捕获 / 回填与实体 NBT 读写放在一起追。
3. 环境相关改动同时检查 `EnvironmentType` 冻结时机与 `PlanetEnvironmentService` 的增量合成。
4. 跑 `:modules:CTNH-Astral:build`；火箭、供氧与环境行为必须进 `runClient` 验证。
