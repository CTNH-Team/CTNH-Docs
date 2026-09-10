# CTNH-LIB COMMAND DOMAIN

## OVERVIEW
共享聊天辅助与 `/ctnh` 检查命令，外加仅开发用的矿脉观察命令（3 个 Java 文件）。

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| 命令注册 | `command/CTNHCommands.java`（`/ctnh` 根，permission 0；`/ctnh showores` permission 2） |
| 手持检查 | `command/CTNHCommands.java#executeHand`（`/ctnh hand`） |
| 标签检查 | `command/CTNHCommands.java#executeShowTag`（`/ctnh showtag item\|block\|fluid <tag>`，带标签补全） |
| 开发用矿脉观察 | `command/CTNHCommands.java#executeShowOres`（`/ctnh showores <radius 1-4>`，仅玩家） |
| 注册表 / NBT 读取 | `command/CTNHCommandInspector.java` |
| 点击复制聊天行 | `command/CTNHCommandChatHelper.java`（`MAX_VALUE_LINE_LENGTH = 256`） |
| Lang keys | `src/main/resources/assets/ctnhlib/lang/{en_us,zh_cn}.json`（`command.ctnhlib.*`） |

## CONVENTIONS
- 命令经 `common/CommonProxy#registerCommands(RegisterCommandsEvent)` 调 `CTNHCommands.register(dispatcher, buildContext)` 注册（Forge 总线事件）。
- 玩家可见输出统一经 `CTNHCommandChatHelper`：`labeledLines` 超过 `MAX_VALUE_LINE_LENGTH`（256）时拆成可复制续行并追加 `command.ctnhlib.value.truncated` 摘要行；值行统一带 `ClickEvent.Action.COPY_TO_CLIPBOARD` 与悬浮提示。
- `CTNHCommandInspector` 用 `ForgeRegistries.{ITEMS,BLOCKS,FLUIDS}.getKey(...)` 只为渲染注册键（`/ctnh hand` 的 id 行、`showtag` 成员），不做字符串 → 对象的反查；Lib 内唯一的同类用法在 `common/MultiblockHelper`（生成模式代码文本时渲染方块 id）。
- `/ctnh showores <radius>` 是开发用命令（permission 2、仅玩家）：遍历玩家周围 `radius`（1-4）个区块柱，跳过未加载区块与 `hasOnlyAir` 段，保留匹配 `forge:ores` 方块标签的方块，其余非空气方块经 `level.setBlock(..., Blocks.AIR.defaultBlockState(), Block.UPDATE_CLIENTS)` 清除，最后用 `command.ctnhlib.showores.done` 汇报 cleared / kept / skipped / elapsedMs。
- `/ctnh showtag` 用 `SUGGEST_TAGS` 按请求的注册表补全已知标签；未知标签与空标签分别报 `command.ctnhlib.error.unknown_tag` / `empty_tag`。
- `@SuppressWarnings("removal")` 标在 `CTNHCommands` 上，用于压制 Brigadier/Forge 弃用 API 警告。

## ANTI-PATTERNS
- 把模块专属命令加进 Lib；应注册在所属模块。
- 把 `showores` 半径放宽到 4 以上或在正式存档执行；它会破坏性清除方块。
- 在命令里用字符串 ID + `ForgeRegistries` 反查注册对象（只允许渲染注册键）。

## SCOPE
适用于 `src/main/java/tech/vixhentx/mcmod/ctnhlib/command`。

## READ WHEN
- 改共享聊天辅助、检查命令行为或 `showores` 开发工具。

## SOURCE OF TRUTH
- `command/CTNHCommands.java` 及其注册点（`common/CommonProxy` 的 `RegisterCommandsEvent`）。
- 文案以 `src/main/resources/assets/ctnhlib/lang/{en_us,zh_cn}.json` 为准。

## WORKFLOW
1. 先判断命令属于 Lib 还是功能模块。
2. 改 `showores` 后在测试存档验证 `forge:ores` 过滤与 `Block.UPDATE_CLIENTS` 传播。
3. 跑 `:modules:CTNH-Lib:build`。
