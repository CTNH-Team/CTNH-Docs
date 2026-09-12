# CTPP INTEGRATION DOMAIN

## OVERVIEW
CTPP 的 Jade、JEI 与 LDLib 对接（5 个 Java 文件）；EMI 对接在 CTNH-Core。

## STRUCTURE
```text
integration/
|-- jade/                      # CTPPJadePlugin（含内部 PlaceableEmitterProvider）
|-- jei/                       # CTPPJeiPlugin
|   `-- category/              # FanAcidWashingCategory, FanBreathingCategory
`-- ldlib/                     # CTPPLDLibPlugin
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| JEI 插件 | `integration/jei/CTPPJeiPlugin.java`（`IModPlugin`；注册 `CTPPRecipeTypeInfo.BREATHING` / `ACIDWASHING` 的配方类别） |
| 风扇类别 | `integration/jei/category/`（`FanAcidWashingCategory`, `FanBreathingCategory`） |
| Jade 插件 | `integration/jade/CTPPJadePlugin.java`（`IWailaPlugin` + 内部 `PlaceableEmitterProvider`） |
| LDLib 插件 | `integration/ldlib/CTPPLDLibPlugin.java`（`@LDLibPlugin`；`onLoad()` 把 `TerminalLinkStateAccessor` 注册进 `TypedPayloadRegistries`，优先级 50） |
| EMI（已迁出） | CTNH-Core `integration/emi/`——不要在本模块重建 `integration/emi/CTPPEmiPlugin.java` |

## CONVENTIONS
- 集成类保持隔离与可选，不得成为 `common/` 的硬依赖。
- `CTPPLDLibPlugin` 是接线柱链路同步的前提：`api/terminal/TerminalLinkState` 的托管字段依赖这里注册的 payload 访问器。
- 应力配方提示由 `StressRecipeCapability.appendJadeRecipeTooltip(...)` 直接产出，Jade 插件不重复序列化配方信息。

## ANTI-PATTERNS
- 让集成类成为 common 代码的硬依赖。
- 在 CTPP 中重新引入 `CTPPEmiPlugin`（它在 Core）。
- 重新加回 `KineticOutputMachineProvider`；Jade 侧只用 `CTPPJadePlugin`。
- 在 Jade provider 中重复序列化客户端已能推导的数据（如 `lastRecipe`）。

## SCOPE
适用于 `src/main/java/com/mo_guang/ctpp/integration` 及其子包。

## READ WHEN
- 改动 CTPP 的 JEI 配方类别或 Jade 提示。
- 改动接线柱链路的 LDLib payload 注册。

## SOURCE OF TRUTH
- `integration/` 各类与其注册站点。
- `integration/ldlib/CTPPLDLibPlugin.java` 的 payload 注册。

## WORKFLOW
1. 改挂钩前确认目标 mod 版本与对应 API。
2. 跑 `:modules:CTPP:build`；带目标 mod 进游戏验证。
