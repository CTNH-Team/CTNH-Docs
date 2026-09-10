# CREATE-ENOUGH-ITEMS DATA DOMAIN

## OVERVIEW
`data/` 是 CEI 的数据生成钩子（1 个 Java 文件）：目前只挂 lang processor。

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Datagen 钩子 | `data/CEIDatagen.java` |
| 语言资源 | `src/main/resources/assets/cei/lang/`（`en_us.json`、`zh_cn.json`） |

## CONVENTIONS
- `CEIDatagen.init()` 仅调用 `REGISTRATE.addLangProcessor()`；模块内不存在 `src/generated` 目录。
- 语言与资源文件直接放在 `src/main/resources/assets/cei/lang/`。

## ANTI-PATTERNS
- 日后若出现 `src/generated/resources`，手改它；应经 `runData` 重新生成。

## SCOPE
适用于 `src/main/java/com/ctnh/cei/data`。

## READ WHEN
- 新增 CEI datagen 输出。

## SOURCE OF TRUTH
- `data/CEIDatagen.java` 与 `common/CommonProxy.init()` 的接线。

## WORKFLOW
1. 改 `CEIDatagen` 后跑 `:modules:Create-Enough-Items:runData`。
2. 核对 lang 输出差异。
