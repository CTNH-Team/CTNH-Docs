# CTNH-LIB COMMON DOMAIN

## OVERVIEW
共享服务端引导 `CommonProxy` 与运行时辅助物品 `MultiblockHelper`（2 个 Java 文件）。

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| 通用代理 / 事件接线 | `common/CommonProxy.java` |
| 运行时辅助物品 | `common/MultiblockHelper.java` |

## CONVENTIONS
- `CommonProxy(FMLJavaModLoadingContext)` 在构造中：注册到 mod 事件总线 → `MinecraftForge.EVENT_BUS.register(CommonProxy.class)`（`RegisterCommandsEvent` 这类 Forge 总线事件必须挂全局总线）→ `init()`；随后经 GTCEu `GTRegistration.REGISTRATE` 注册物品 `mutiblock_helper`（id 拼写照源码保留）。
- `CommonProxy.init()` 是空实现；Lib 内不做 `GTProvidersRegistrar` / Jade 初始化。
- `commonSetup(FMLCommonSetupEvent)` 中 `event.enqueueWork(CTNHLibNetworking::init)` 完成网络通道注册。
- `registerPackFinders(AddPackFindersEvent)` 仅在 `PackType.SERVER_DATA` 下以 `GTPackSource("ctnhlib:filter_data", ..., Pack.Position.TOP, DataFilterPack::new)` 挂载静态过滤包。
- `registerCommands(RegisterCommandsEvent)` 转调 `CTNHCommands.register(dispatcher, buildContext)`。
- `MultiblockHelper extends ComponentItem implements IInteractionItem`：右键两次取两个角点（`state` 0→1→2，NBT 键 `block_x_f/y_f/z_f` 与 `block_x_s/y_s/z_s`），潜行右键清除或在 `state == 2` 时调 `check_form` 输出 `FactoryBlockPattern` 代码文本到控制台。它用 `ForgeRegistries.BLOCKS.getKey(block)` 只为渲染方块 id，不用于配方物品反查。
- 提示文案用 `ctnh.terminal.*` 键（由消费模块提供）。

## ANTI-PATTERNS
- 往通用代理塞游戏内容；Lib 只承载共享基础设施。
- 在 `CommonProxy` 里重新引入 Jade 注册调用。
- 用字符串 ID + `ForgeRegistries` 反查来代替静态注册对象（`MultiblockHelper` 中的 `getKey` 仅用于输出 id 文本）。

## SCOPE
适用于 `src/main/java/tech/vixhentx/mcmod/ctnhlib/common`。

## READ WHEN
- 改 Lib 引导顺序、网络初始化、数据包挂载或运行时辅助物品。

## SOURCE OF TRUTH
- `common/CommonProxy.java` 与 `CTNHLib.java`。

## WORKFLOW
1. 先确认 `CommonProxy` 的初始化顺序，再加钩子。
2. 跑 `:modules:CTNH-Lib:build`。
