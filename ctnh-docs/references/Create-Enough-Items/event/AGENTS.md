# CREATE-ENOUGH-ITEMS EVENT DOMAIN

## OVERVIEW
`event/` 是 CEI 的事件处理域（1 个 Java 文件）：客户端 tick 驱动 tooltip 烘焙队列，完成后回写 EMI 搜索的 tooltip 索引。

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| 客户端事件处理 | `event/ForgeClientEventHandler.java` |
| 烘焙队列本体 | `utils/emi/TooltipBakeQueue.java` |

## CONVENTIONS
- `ForgeClientEventHandler` 标注 `@Mod.EventBusSubscriber(modid = CreateEnoughItems.MODID, bus = Mod.EventBusSubscriber.Bus.FORGE, value = Dist.CLIENT)`；`onClientTick` 只处理 `TickEvent.Phase.END`。
- 每 20 tick（`GTValues.CLIENT_TIME % 20 == 0`）推进一次 `TooltipBakeQueue.INSTANCE.tick()`（每批 128 个堆栈）；队列耗尽后置 `TooltipBakeQueue.ready = true`，调用 `queue.tooltips.generate()` 并写回 `EmiSearch.tooltips`。
- `TooltipBakeQueue.INSTANCE` 为 `null` 时直接跳过，不报错。

## ANTI-PATTERNS
- 把事件接线塞进 registry 类。

## SCOPE
适用于 `src/main/java/com/ctnh/cei/event`。

## READ WHEN
- 在 CEI 中新增 Forge 生命周期事件处理。

## SOURCE OF TRUTH
- `event/` 下的类与 `utils/emi/TooltipBakeQueue.java`。

## WORKFLOW
1. 确定 Forge 事件与其注册点。
2. 跑 `:modules:Create-Enough-Items:build`。
