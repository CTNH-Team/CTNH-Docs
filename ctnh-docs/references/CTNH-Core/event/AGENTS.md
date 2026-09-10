# CTNH-CORE EVENT DOMAIN

## OVERVIEW
Core 运行时行为的 Forge 事件处理器与后台任务管理器（5 个 Java 文件）。

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| 主事件处理器 | `event/ForgeEventHandler.java` |
| 客户端事件 | `event/ForgeClientEventHandler.java` |
| 维度飞行 | `event/DimensionFlightHandler.java` |
| 构建任务 | `event/BuildTaskManager.java` |
| 网络事件 | `event/ProvidableNetEventHandler.java` |

## CONVENTIONS
- 事件订阅者与注册表回调是生命周期入口；顺着注解追踪，不要按普通 Java 调用方找。
- Capability 挂载钩子（EIO 电容 capability、命名空间/remap 辅助）经由 `common/capability/` 从这里接线。
- `ProvidableNetEventHandler` 与 `common/machine/trait/providable_net/` 的机器配合。
- `ForgeEventHandler` 还承载灵魂火把彩蛋（`onSoulTorchEasterEgg`），会生成烟花并播放 `easter_egg_clown` 音效事件。

## ANTI-PATTERNS
- 把事件逻辑搬进注册类；生命周期接线留在 `event/`。
- 让仅客户端事件订阅者从 common 路径可达。

## SCOPE
适用于 `src/main/java/io/github/cpearl0/ctnhcore/event`。

## READ WHEN
- 在 Core 中新增 Forge 生命周期、capability 或网络事件处理。
- 排查几乎没有普通 Java 调用方的运行时钩子。

## SOURCE OF TRUTH
- `event/ForgeEventHandler.java`、`event/ForgeClientEventHandler.java`，以及 `common/CommonProxy.java` 中的 mod 事件总线接线。

## WORKFLOW
1. 确定 Forge 事件与它的注册位置。
2. 同时检查 common 与 client 两个事件处理器类。
3. 跑 `:modules:CTNH-Core:build`，可用时在运行时验证该面。
