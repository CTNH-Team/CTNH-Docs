# CTPP NETWORK DOMAIN

## OVERVIEW
CTPP 的网络包（11 个 Java 文件，全部在 `network/packet/`）：工具箱、接线柱选线，以及发射器光束。

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| 工具箱动作 / 打开 | `network/packet/CTPPToolboxActionPacket.java`, `CTPPToolboxOpenNearestPacket.java` |
| 工具箱绑定 / 过滤 | `network/packet/CTPPToolboxBindingsPacket.java`, `CTPPToolboxMenuFiltersPacket.java` |
| 工具箱快照 | `network/packet/CTPPToolboxSnapshotPacket.java`, `CTPPToolboxSnapshotRequestPacket.java` |
| 接线柱选线 | `network/packet/CTPPTerminalWireSelectionPacket.java`, `CTPPTerminalCancelWireSelectionPacket.java` |
| 发射器光束 | `network/packet/SetEmitterBeamPacket.java`, `DelEmitterBeamPacket.java`, `PickEmitterPacket.java` |
| 注册站点 | `registry/CTPPNetwork.java`（`GTNetwork.register`；`init()` 由 `CommonProxy` 构造函数调用） |

## CONVENTIONS
- 包一律经 `GTNetwork.register(...)` 注册在 `registry/CTPPNetwork.java`，并用 `NetworkDirection` 标明方向：`CTPPToolboxActionPacket`、`CTPPToolboxSnapshotRequestPacket`、`CTPPToolboxOpenNearestPacket`、`CTPPTerminalCancelWireSelectionPacket`、`PickEmitterPacket` 为 `PLAY_TO_SERVER`；`CTPPToolboxBindingsPacket`、`CTPPToolboxSnapshotPacket`、`CTPPToolboxMenuFiltersPacket`、`CTPPTerminalWireSelectionPacket`、`SetEmitterBeamPacket`、`DelEmitterBeamPacket` 为 `PLAY_TO_CLIENT`。
- 包只做传输与校验，业务落在 `common/toolbox/`、`common/terminal/`、`common/beam/` 与 `client/` 的对应类。

## ANTI-PATTERNS
- 用 CTNH-Lib 的网络通道注册 CTPP 包（必须走 `registry/CTPPNetwork.java` 的 GT 通道）。
- 在包里直接实现业务逻辑而不复用 `common/` 服务类。

## SCOPE
适用于 `src/main/java/com/mo_guang/ctpp/network` 及其子包。

## READ WHEN
- 新增或改动 CTPP 的网络包。
- 改动工具箱、接线柱选线或发射器光束的客户端-服务端交互。

## SOURCE OF TRUTH
- `network/packet/` 各类与 `registry/CTPPNetwork.java` 的注册表。

## WORKFLOW
1. 先在 `CTPPNetwork.init()` 中核对注册与方向。
2. 跑 `:modules:CTPP:build`；涉及交互时进游戏验证。
