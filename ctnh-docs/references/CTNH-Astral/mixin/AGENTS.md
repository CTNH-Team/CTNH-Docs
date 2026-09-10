# CTNH-ASTRAL MIXIN DOMAIN

## OVERVIEW
Ad Astra 氧气/温度、MC 区块生成与网络包处理的补丁（4 个 Java 文件）。四个 Mixin 均已在 `ctnhastral.mixins.json` 的 `mixins` 列表中登记，`client` 列表为空。

## STRUCTURE
```text
mixin/
├── adastra/      # OxygenApilmplMixin, TemperatureApilmplMixin
└── minecraft/    # NoiseBasedChunkGeneratorMixin, ServerGamePacketListenerImplMixin
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Ad Astra 氧气 | `mixin/adastra/OxygenApilmplMixin.java` → `earth.terrarium.adastra.common.systems.OxygenApiImpl` |
| Ad Astra 温度 | `mixin/adastra/TemperatureApilmplMixin.java` → `earth.terrarium.adastra.common.systems.TemperatureApiImpl` |
| 区块流体选择 | `mixin/minecraft/NoiseBasedChunkGeneratorMixin.java` → `createFluidPicker` |
| 跳跃触发发射 | `mixin/minecraft/ServerGamePacketListenerImplMixin.java` → `handlePlayerInput` |
| Mixin 配置 | `src/main/resources/ctnhastral.mixins.json` |

## CONVENTIONS
- 新增 Mixin 必须同时补 `ctnhastral.mixins.json` 的 `mixins` 数组条目；`package` 固定为 `com.ctnh.ctnhastral.mixin`。
- 两个 Ad Astra Mixin 都注入 `entityTick` 的 `HEAD`（`cancellable = true`, `remap = false`），命中条件为 `VacuumSealEnchantment.hasFullEnchant(entity)` 或 `OxygenEnvironmentService.hasBreathableAtmosphere(level, entity.blockPosition())`；两者必须保持同一判定，否则会出现"有氧但过热"或反之的割裂体验。
- `NoiseBasedChunkGeneratorMixin` 整体替换 `createFluidPicker` 返回值：`y < min(minY + 10, seaLevel)` 用岩浆，其余用 `settings.defaultFluid()`。这是月球海水等默认流体真正生效的位置。
- `ServerGamePacketListenerImplMixin` 在 `handlePlayerInput` 的 `TAIL` 检测跳跃，转交 `RocketAssemblyPlatformMachine.handleRocketPassengerJump(player)`；机器可用性、是否已组装等判断都在机器侧，Mixin 只做转发。
- 注入方法命名用 `ctnhastral$` 前缀（如 `ctnhastral$overrideFluidPicker`），便于在崩溃日志里识别。

## ANTI-PATTERNS
- 改动 Ad Astra 氧气/温度行为时，不同步检查 mixin JSON 条目与上游 API 目标类/方法签名。
- 只改一个 Ad Astra Mixin 而让另一个的判定条件漂移。
- 在 `ServerGamePacketListenerImplMixin` 内实现发射逻辑，而不是转发给多方块机器。
- 在 Mixin 中直接引用 `common/` 之外的客户端类导致双端类加载失败。

## SCOPE
适用于 `src/main/java/com/ctnh/ctnhastral/mixin` 与 `src/main/resources/ctnhastral.mixins.json`。

## READ WHEN
- 补丁 Ad Astra 或 Minecraft 的区块生成 / 网络包处理行为。
- 调整氧气、温度或真空伤害的判定入口。

## SOURCE OF TRUTH
- `src/main/resources/ctnhastral.mixins.json` 与 `mixin/` 下的类。

## WORKFLOW
1. 对照当前加载的 Ad Astra / MC 版本核对目标成员是否存在。
2. 跑 `:modules:CTNH-Astral:build`；Mixin 变更必须在 `runClient` 中运行验证，编译通过不代表注入成功。
