# CTPP SYNCDATA DOMAIN

## OVERVIEW
CTPP 的同步数据接入（1 个 Java 文件）：为接线柱链路状态提供 LDLib 托管访问器。

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| 链路访问器 | `syncdata/TerminalLinkStateAccessor.java`（`extends CustomObjectAccessor<TerminalLinkState>`，`INSTANCE` 单例） |
| 被托管的状态类型 | `api/terminal/TerminalLinkState.java`（`IManaged` + `FieldManagedStorage`，字段带 `@DescSynced` 与 `@Persisted`）、`api/terminal/TerminalProperties.java` |
| 注册站点 | `integration/ldlib/CTPPLDLibPlugin.java`（`register(NbtTagPayload.class, NbtTagPayload::new, TerminalLinkStateAccessor.INSTANCE, 50)`） |
| 使用方 | `common/blockentity/VoltageTerminalBlockEntity.java`（自带 `FieldManagedStorage`）、`common/terminal/TerminalNetwork.java` |

## CONVENTIONS
- 访问器读写走 `IManagedAccessor`：`serialize` 用 `readFromReadonlyField`；`deserialize` 要求 payload 是 `NbtTagPayload` 且内含 `CompoundTag`，否则抛 `IllegalArgumentException`，随后经 `writeToReadonlyField` 写回新建实例。
- 链路状态的同步与持久化由 `TerminalLinkState` 自身的托管字段注解负责；访问器只做集合元素的载荷编解码，不额外写 NBT。
- 该访问器必须先于接线柱同步生效，注册在 `CTPPLDLibPlugin.onLoad()`。

## ANTI-PATTERNS
- 绕过访问器直接对链路写 NBT 或手工同步。
- 给 `TerminalLinkState` 的字段再叠加一套 attach 式持久化（与 `@Persisted` 形成双重所有权）。

## SCOPE
适用于 `src/main/java/com/mo_guang/ctpp/syncdata`。

## READ WHEN
- 改动接线柱线缆的同步或链路状态持久化。
- 改动 `TerminalLinkState` 的字段集合。

## SOURCE OF TRUTH
- `syncdata/TerminalLinkStateAccessor.java`、`api/terminal/TerminalLinkState.java` 与 `common/blockentity/VoltageTerminalBlockEntity.java`。

## WORKFLOW
1. 改字段时同时核对 `TerminalLinkState` 的注解与访问器行为。
2. 跑 `:modules:CTPP:build`；接线柱同步需进游戏验证。
