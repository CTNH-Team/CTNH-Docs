# CTPP EVENT DOMAIN

## OVERVIEW
CTPP 的 Forge 事件处理器（2 个 Java 文件），均以 `@Mod.EventBusSubscriber(modid = CTPP.MODID, bus = Mod.EventBusSubscriber.Bus.FORGE)` 注册。

## STRUCTURE
```text
event/
|-- ForgeEventHandler.java
`-- PlaceableEmitterEventHandler.java
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| 命令注册与线缆周期 | `event/ForgeEventHandler.java`（`RegisterCommandsEvent` 注册工具箱与接线柱命令；`TickEvent.LevelTickEvent` 驱动 `TerminalWireHazardManager.tick(level)`；`TickEvent.ServerTickEvent` 驱动 `TerminalWireDamageDebug.tick(server)`；`LevelEvent.Unload` 调 `TerminalWireHazardManager.unload(level)`；`PlayerEvent.PlayerLoggedOutEvent` 清理调试状态） |
| 发射器放置 | `event/PlaceableEmitterEventHandler.java`（`EventPriority.LOW` 的 `PlayerInteractEvent.RightClickBlock`） |

## CONVENTIONS
- 事件处理器只做转发与生命周期挂钩，具体逻辑落在 `common/` 的对应服务类（`TerminalWireHazardManager`、`TerminalWireDamageDebug`、`CTPPMachines`）。
- `PlaceableEmitterEventHandler.onRightClickBlock` 的语义：非潜行时先让被点击方块自身的交互跑完，只有它未消费点击才放置发射器；无论是否放置都取消事件，避免原版重跑 `use()`，客户端只回 `InteractionResult.SUCCESS`。
- `tierFor(Item)` 把原版 GT 发射器物品（`GTItems.EMITTER_LV`…`EMITTER_OpV`）映射到 `CTPPMachines.PLACEABLE_EMITTER` 的等级索引；UHV 及以上物品在 GTCEu 高阶内容关闭时为 `null`，代码已判空。

## ANTI-PATTERNS
- 把事件接线塞进 `registry/` 类。
- 在事件处理器里直接实现业务逻辑，而不复用 `common/` 的服务类。
- 忽略 `EventPriority.LOW` 与取消语义，导致原版方块交互被吞掉。

## SCOPE
适用于 `src/main/java/com/mo_guang/ctpp/event`。

## READ WHEN
- 新增 CTPP 的 Forge 生命周期事件处理。
- 改动可放置发射器或光束相关事件。

## SOURCE OF TRUTH
- `event/` 两个类的注解与注册站点。
- 其调用的 `common/` 服务类与 `common/CommonProxy.java`。

## WORKFLOW
1. 先定位 Forge 事件与其注册站点，再决定逻辑归属。
2. 跑 `:modules:CTPP:build`；涉及交互时进游戏验证。
