# CREATE-ENOUGH-ITEMS REGISTRY DOMAIN

## OVERVIEW
`registry/` 是 CEI 的注册域（1 个 Java 文件）：`CEIRegistrate` 是 CTNH-Lib `CNRegistrate` 的薄封装，使用 mod id `cei`。

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Registrate | `registry/CEIRegistrate.java` |

## CONVENTIONS
- `CEIRegistrate.create()` 以 `CreateEnoughItems.MODID` 构造 `CNRegistrate` 子类。
- `CreateEnoughItems.REGISTRATE` 由 `CEIRegistrate.create()` 创建，并在 `CommonProxy.init()` 中 `registerRegistrate()`。
- 本模块无 `*GTAddon.java`；GTCEu 集成目前通过 EMI/GTCEu mixin 与配方检查工具完成。

## ANTI-PATTERNS
- 在此注册 GTCEu 内容，却不补 `CommonProxy` 中对应的监听实现。

## SCOPE
适用于 `src/main/java/com/ctnh/cei/registry`。

## READ WHEN
- 改动 CEI registrate 设置。

## SOURCE OF TRUTH
- `registry/CEIRegistrate.java` 与 `common/CommonProxy.init()`。

## WORKFLOW
1. 检查 `CommonProxy.init()` 中的 registrate 接线。
2. 跑 `:modules:Create-Enough-Items:build`。
