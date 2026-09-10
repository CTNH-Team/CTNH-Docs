# CTNH-MANA NETWORKING DOMAIN

## OVERVIEW
Mana 的网络层（7 个 Java 文件）：`CMNetworking` 注册 6 个数据包，覆盖 Caduceus 轮盘、索引/命运、拮抗与虚境入侵。

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| 网络注册 | `networking/packets/CMNetworking.java`（`init()` 基于 `LDLNetworking.NETWORK`：C2S 注册 `CaduceusPacket`, `IndexFortunaPacket`；S2C 注册 `IndexTargetParticlePacket`, `IndexTargetBlockPacket`, `AntagonismPacket`, `ZenithInvadePacket`） |
| 拮抗包 | `networking/packets/AntagonismPacket.java` |
| Caduceus 包 | `networking/packets/CaduceusPacket.java` |
| 索引包 | `networking/packets/IndexFortunaPacket.java`, `IndexTargetBlockPacket.java`, `IndexTargetParticlePacket.java` |
| 虚境入侵包 | `networking/packets/ZenithInvadePacket.java` |

## CONVENTIONS
- `CMNetworking.init()` 由 `common/CommonProxy.onCommonSetup(FMLCommonSetupEvent)` 调用；注册入口不在 `event/`。
- 方向约定明确：客户端发起的操作（轮盘选择、命运抽取）走 C2S；服务端驱动的表现（索引标记、拮抗提示、虚境入侵）走 S2C。
- 发送统一用 `LDLNetworking.NETWORK` 的 helper（如 `sendToServer` / `sendToTrackingChunk`），不新建独立通道。
- 客户端接收侧的表现分发落在 `client/`（如 `ZenithInvadePacket` → `client/ZenithInvadeClient`），数据包类本身不写渲染逻辑。

## ANTI-PATTERNS
- 在 `event/EventHandler` 或其它类里另行初始化网络（注册入口只在 `CMNetworking.init()`）。
- 新增数据包后漏掉 `CMNetworking.init()` 的注册调用。
- 在数据包类中直接操作客户端界面/渲染，或让服务端侧依赖客户端类。
- 改动 Caduceus / Saber 行为时只改包不改 `ClientProxy` 的物品属性谓词（反之亦然）。

## SCOPE
适用于 `src/main/java/com/magicbee/ctnhmana/networking` 及其子包。

## READ WHEN
- 新增或修改 Mana 数据包、收发方向或注册入口。
- 改动索引标记、拮抗提示或虚境入侵的同步表现。

## SOURCE OF TRUTH
- `networking/packets/` 各数据包类与 `CMNetworking.init()`。
- 初始化调用点：`common/CommonProxy.onCommonSetup()`。

## WORKFLOW
1. 新增数据包 → 写类，再在 `CMNetworking.init()` 按 C2S/S2C 注册。
2. 同步更新客户端接收侧（`client/`）或服务端处理侧。
3. 跑 `:modules:CTNH-Mana:build`，在游戏内验证收发。
