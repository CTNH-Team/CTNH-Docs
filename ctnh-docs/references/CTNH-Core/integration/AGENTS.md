# CTNH-CORE INTEGRATION DOMAIN

## OVERVIEW
Core 负责的可选第三方集成（7 个 Java 文件）：EMI、Create Diesel、Legendary Survival、FTB Essentials，以及 CTPP（可放置发射器隐藏）。

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| EMI 插件 | `integration/emi/CTNHCoreEmiPlugin.java`, `integration/emi/CTNHExtraEmiPlugin.java` |
| Create Diesel | `integration/creatediesel/DistillationCategoryLayout.java`, `integration/creatediesel/GTBedrockOilBridge.java` |
| Legendary Survival | `integration/legendary/ArmorModifier.java`, `integration/legendary/UnderfloorHeatingSystemTempModifier.java` |
| FTB Essentials | `integration/ftbessentials/AsyncRtpManager.java`；并发参数在 `CTNHConfig.Rtp` |
| CTPP 发射器隐藏 | `integration/emi/CTNHCoreEmiPlugin.java#CTPPDisable()`，遍历 `CTPPMachines.PLACEABLE_EMITTER` |

## CONVENTIONS
- 集成保持隔离与可选；不得成为 common 代码的硬依赖。
- 宽泛的跨 mod 配方兼容一般归 Core（聚合方），feature 模块只保留各自的机制集成。
- Legendary Survival 的 modifier 与地暖系统机器（Underfloor Heating System）配合。
- FTB Essentials 经 `modImplementation("dev.ftb.mods:ftb-essentials-forge:...")` 引入（编译与运行都在类路径上）；`AsyncRtpManager` 以滑动窗口的异步区块加载搜索实现 `/rtp`，依赖 `mixin/mc/ServerChunkCacheAccessor`。
- RTP 并发由 `CTNHConfig.rtp`（`CTNHConfig.Rtp`）提供并逐次读取：`rtpWindowSize`（单次搜索窗口，默认 2，范围 1..8）、`rtpMaxGlobalInFlight`（全部玩家合计的全局在途上限，默认 4，范围 1..32）、`rtpFallbackConcurrency`（3x3 兜底邻居并发，默认 2，范围 1..8）；各值经 `windowSize()` / `maxGlobalInFlight()` / `fallbackConcurrency()` 取下限 1。`AsyncRtpManager.requestChunk` 对区块 future 加 30s 超时（`CHUNK_TIMEOUT_SECONDS`），超时与完成回调统一经 `server.execute` 回服务端线程再释放全局在途名额。
- Create Diesel 集成核心是 `DistillationCategoryLayout`，为可变高度的蒸馏配方动态居中；其客户端 mixin 在 `mixin/creatediesel/` 与 `mixin/emi/`。
- EMI `CTNHCoreEmiPlugin.initialize()` 在 `EIODisable()`/`CreateDisable()` 之外还会调用 `CTPPDisable()`：遍历 `CTPPMachines.PLACEABLE_EMITTER`，把 `definition::getItem` 加进禁用栈 —— 可放置发射器机器物品是无法获取的中间产物（放置/掉落走原版 GT 发射器部件，注册在空创造栏，不应出现在 EMI 中）。禁用方式为 `registry.disableStack(EmiStack.of(item.get()))`。

## ANTI-PATTERNS
- 把可选集成搬进基础模块。
- 让非集成代码在类加载期就要求集成类存在。

## SCOPE
适用于 `src/main/java/io/github/cpearl0/ctnhcore/integration`。

## READ WHEN
- 改动 Core 中的 EMI、Create Diesel、Legendary Survival、FTB Essentials 或 CTPP 兼容。

## SOURCE OF TRUTH
- `integration/emi/`、`integration/creatediesel/`、`integration/legendary/`、`integration/ftbessentials/` 下的类；接线在 `common/CommonProxy.java`。

## WORKFLOW
1. 改钩子前先确认集成目标 mod 的版本。
2. 集成依赖 mixin 时检查 mixin JSON 条目。
3. 跑 `:modules:CTNH-Core:build`，并在装有目标 mod 的运行时验证。
