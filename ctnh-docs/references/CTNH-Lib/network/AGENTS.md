# CTNH-LIB NETWORK DOMAIN

## OVERVIEW
共享网络：供客户端高亮渲染使用的方块高亮数据包（1 个 Java 文件）。

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| 数据包 | `network/packets/BlockHighlightPacket.java`（`extends PacketIntLocation`） |
| 通道注册 | `registrate/CTNHLibNetworking.java`（见 registrate 域） |
| 客户端渲染 | `client/render/highlight/{HighlightHandler, HighlightRender}` |

## CONVENTIONS
- `BlockHighlightPacket(BlockPos)` 经 `NETWORK.sendToPlayer(...)` 下发（当前发送方：Core `common/item/TestingTerminalBehavior`）；接收端在 `execute` 里校验 `level` / `pos` / `level.isLoaded(pos)`，然后调 `HighlightHandler.highlight(pos, dimension, System.currentTimeMillis() + 10000, ColorData.RED)`。
- 通道注册在 `registrate/CTNHLibNetworking.init()`（`NETWORK.registerS2C(BlockHighlightPacket.class)`），由 `common/CommonProxy.commonSetup` 的 `enqueueWork` 触发。
- 数据包只传位置；颜色与存活时长由接收端决定。

## ANTI-PATTERNS
- 把模块专属数据包加进 Lib；应注册在所属模块。
- 在数据包里塞客户端可自行推导的状态或长载荷。

## SCOPE
适用于 `src/main/java/tech/vixhentx/mcmod/ctnhlib/network`。

## READ WHEN
- 改方块高亮数据包或共享网络行为。

## SOURCE OF TRUTH
- `network/packets/BlockHighlightPacket.java` 与 `registrate/CTNHLibNetworking.java`。

## WORKFLOW
1. 改包后先确认 `CTNHLibNetworking` 的注册未变。
2. 跑 `:modules:CTNH-Lib:build`，进游戏验证高亮显示与到期消失。
