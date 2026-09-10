# CREATE-ENOUGH-ITEMS COMMON DOMAIN

## OVERVIEW
`common/` 是 CEI 的公共启动域（1 个 Java 文件）：`CommonProxy` 注册 registrate、挂载 datagen lang processor，并为 GTCEu 的 `MachineDefinition` / `GTRecipeType` / `RecipeConditionType` 注册空监听占位。

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| 公共代理 | `common/CommonProxy.java` |

## CONVENTIONS
- `CommonProxy` 构造函数调用 `init()`；`init()` 依次取 mod 事件总线、`CreateEnoughItems.REGISTRATE.registerRegistrate()`、`CEIDatagen.init()`，再为 `MachineDefinition`、`GTRecipeType`、`RecipeConditionType` 挂 `addGenericListener`。
- `registerMachines` / `registerRecipeTypes` / `registerRecipeConditions` 目前是空实现；只有 CEI 真的要注册 GTCEu 内容时才往里填。
- 本模块依赖 `:modules:CTNH-Lib`，不依赖 CTNH-Core。

## ANTI-PATTERNS
- 把 EMI UI 行为挪到 CTNH-Core；EMI 定制属于 CEI。
- 在空监听里塞入 GTCEu 注册却不补上真实的注册路径。

## SCOPE
适用于 `src/main/java/com/ctnh/cei/common`。

## READ WHEN
- 改动 CEI 启动流程、registrate 注册或 GTCEu 监听占位。

## SOURCE OF TRUTH
- `common/CommonProxy.java` 与 `CreateEnoughItems.java`。

## WORKFLOW
1. 加钩子前先确认 `CommonProxy.init()` 的顺序。
2. 跑 `:modules:Create-Enough-Items:build`。
