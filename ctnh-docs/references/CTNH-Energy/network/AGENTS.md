# CTNH-ENERGY NETWORK DOMAIN

## OVERVIEW
CTNH-Energy 的网络层（2 个 Java 文件）：LDLib 网络包与同步载荷。

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| 网络注册 | `registry/CENetWorking.init()`（`LDLNetworking.NETWORK.registerC2S(QCOpenCPUMenuPacket.class)`），由 `common/CommonProxy.init()` 调用 |
| C2S 包 | `network/packets/QCOpenCPUMenuPacket`（继承 LDLib `PacketIntLocation`；校验目标是 `QuantumComputerMENetworkPortBlockEntity` 后经 `MenuOpener.open` 打开 `AEMenus.QUANTUM_COMPUTER`） |
| 同步载荷 | `network/syncdata/AEKeyPayLoad`（继承 LDLib `ObjectTypedPayload<AEKey>`；NBT 走 `AEKey.toTagGeneric/fromTagGeneric`，网络走 `AEKey.writeKey/readKey`） |
| 载荷类型注册 | `integration/ldlib/CELDLibPlugin.onLoad()`（`registerSimple(AEKeyPayLoad.class, AEKeyPayLoad::new, AEKey.class, 100)`） |

## CONVENTIONS
- 网络包走 LDLib 网络通道（`CENetWorking` 集中注册），不要另起 Forge `SimpleChannel`。
- 载荷的数据部分用 LDLib `ObjectTypedPayload` 注册类型，序列化只做编解码，不夹带业务判断。
- 服务端处理包前必须校验方块实体类型与区块已加载，再打开菜单。
- 新增载荷类型要同时在 `CELDLibPlugin` 登记，否则同步时无法解析。

## ANTI-PATTERNS
- 在 `common/` 机器类里直接构造并发送网络包而绕过注册的包类型。
- 为同一个载荷同时提供 LDLib 与 Forge 两套编解码路径。
- 在包处理里跳过方块实体类型校验直接开菜单。

## SCOPE
`modules/CTNH-Energy/src/main/java/tech/luckyblock/mcmod/ctnhenergy/network/` 及其子包，注册入口在 `registry/CENetWorking`。

## READ WHEN
- 新增或修改 Energy 的网络包、同步载荷
- 调整量子计算机 CPU 菜单的打开流程

## SOURCE OF TRUTH
`network/` 下的包与载荷类，以及 `registry/CENetWorking`、`common/CommonProxy.init()` 的注册顺序。

## WORKFLOW
1. 先在 `CENetWorking` 注册包类型；载荷类型在 `CELDLibPlugin` 注册。
2. `:modules:CTNH-Energy:build` 编译；联机行为在游戏内验证（客户端 + 服务端）。