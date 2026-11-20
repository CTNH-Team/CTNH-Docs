# CTNH-ASTRAL MIXIN DOMAIN

## OVERVIEW
MC 区块生成与网络包处理的补丁（3 个 Java 文件）。三个 Mixin 全部位于 `mixin/minecraft/` 分组，且都在 `ctnhastral.mixins.json` 的 `mixins` 列表中登记，`client` 列表为空。

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| 月球地形布局初始化 | `mixin/minecraft/ChunkGeneratorMixin.java` → `ChunkGenerator.createState` 的 `HEAD` |
| 月球地表群系替换 | `mixin/minecraft/NoiseBasedChunkGeneratorMixin.java` → `buildSurface` 的 `@ModifyArg` |
| 月球峡谷雕刻与地表收尾 | `mixin/minecraft/NoiseBasedChunkGeneratorMixin.java` → `applyCarvers` 的 `RETURN` |
| 分层流体选择器绑定 | `mixin/minecraft/NoiseBasedChunkGeneratorMixin.java` → 构造器 `RETURN` + `@Shadow @Final @Mutable globalFluidPicker` |
| 跳跃触发发射 | `mixin/minecraft/ServerGamePacketListenerImplMixin.java` → `handlePlayerInput` 的 `TAIL` |
| Mixin 配置 | `src/main/resources/ctnhastral.mixins.json` |

## CONVENTIONS
- 新增 Mixin 必须同时补 `ctnhastral.mixins.json` 的 `mixins` 数组条目；`package` 固定为 `com.ctnh.ctnhastral.mixin`，按目标分组放子包（当前只有 `minecraft/`）。
- 注入方法命名用 `ctnhastral$` 前缀（`ctnhastral$initializeMoonLayouts`, `ctnhastral$surfaceBiomes`, `ctnhastral$carveCanyons`, `ctnhastral$bindFluidPicker`, `ctnhastral$launchRocketOnJump`），便于在崩溃日志里识别。
- 三个注入都以 `getBiomeSource() instanceof MoonBiomeSource moon` 为门控：非月球群系源的生成器保持原版行为。
- `ChunkGeneratorMixin` 在 `createState` 的 `HEAD` 调 `moon.initialize(generator, randomState, seed)`，把结构集 lookup、随机状态与种子交给群系源，月球峡谷 / 陨石坑布局在此绑定。
- `NoiseBasedChunkGeneratorMixin` 在 `buildSurface` 的 `SurfaceSystem.buildSurface` 调用点用 `@ModifyArg` 把 `BiomeManager` 实参换成 `moon.surfaceBiomes(original)`，使地表规则读取群系源维护的地表群系。
- `NoiseBasedChunkGeneratorMixin` 在 `applyCarvers` 的 `RETURN` 只在 `GenerationStep.Carving.AIR` 阶段执行 `MoonCanyonTerrain.carve(chunk, moon.canyons(), moon.canyonTerrain())`，随后 `moon.finishSurface(chunk)` 补齐地表。
- `NoiseBasedChunkGeneratorMixin` 在构造器 `RETURN` 用 `CAWorldgen.fluidPicker(settings)` 覆盖 `globalFluidPicker`：返回 `null`（未登记 `LAVA_LEVELS` 的噪声设置）时不覆盖；群系源是 `MoonBiomeSource` 时再把最终 picker 传给它（`moon.bindTerrainFluids(globalFluidPicker)`）。
- `ServerGamePacketListenerImplMixin` 在 `handlePlayerInput` 的 `TAIL` 检测 `packet.isJumping()`，转交 `RocketAssemblyPlatformMachine.handleRocketPassengerJump(player)`；机器成型、火箭存在性等判断都在机器侧，Mixin 只做转发。

## ANTI-PATTERNS
- 改动 MC 区块生成行为时不同步检查 `ctnhastral.mixins.json` 条目与目标方法签名（`buildSurface` / `applyCarvers` 的 `@ModifyArg` 索引与描述符必须与当前映射一致）。
- 只改一个注入点而让月球群系源的状态（布局、地表群系、流体）与其它注入点漂移。
- 在 `ServerGamePacketListenerImplMixin` 内实现发射逻辑，而不是转发给多方块机器。
- 在 Mixin 中直接引用 `client/` 的类导致双端类加载失败。
- 在 `ctnhastral$surfaceBiomes` 里无条件替换 `BiomeManager`，绕过 `MoonBiomeSource` 门控影响其他维度。

## SCOPE
适用于 `src/main/java/com/ctnh/ctnhastral/mixin` 与 `src/main/resources/ctnhastral.mixins.json`。

## READ WHEN
- 补丁 Minecraft 的区块生成、地表规则或网络包处理行为。
- 调整月球地形布局、峡谷雕刻或流体分层的注入点。

## SOURCE OF TRUTH
- `src/main/resources/ctnhastral.mixins.json` 与 `mixin/` 下的类。

## WORKFLOW
1. 对照当前加载的 MC 版本核对目标成员是否存在（`ChunkGenerator.createState`、`NoiseBasedChunkGenerator.buildSurface` / `applyCarvers` / `<init>`、`ServerGamePacketListenerImpl.handlePlayerInput`）。
2. 跑 `:modules:CTNH-Astral:build`；Mixin 变更必须在 `runClient` 中运行验证，编译通过不代表注入成功。
