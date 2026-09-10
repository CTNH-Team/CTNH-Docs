# CTPP UTIL DOMAIN

## OVERVIEW
CTPP 的共享工具（6 个 Java 文件）。`CTPPValues`（MT 等级表）已移除——机械等级改用 `GTValues.VNF`。

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| 通用 tooltip | `util/CommonTooltips.java`（`KINETIC_OVERCLOCK`、`INPUT_SPEED`、`MECHANICAL_TIER_MACHINE`，lang key 前缀 `ctpp.commontooltips.*`） |
| 槽位与自定义接口 | `util/ICustomSlot.java`, `util/IMatrix3dAccessor.java`, `util/IWorkingMachineStep.java` |
| 物品朝向构建 | `util/ItemAxisBuilder.java` |
| 数学工具 | `util/MathUtil.java`（如 `rotateByVec`，被 `KineticGeneratorMachine` 用于旋转 contraption 的转速方向） |

## CONVENTIONS
- 机械等级相关文案统一用 `GTValues.VNF[tier]`；`CTPPValues.MT` 与其 lang key（`ctpp.ctppvalues.mt.*`、旧的 `ctpp.commontooltips.mechanical_tier`）已不存在，不要引用。
- tooltip 常量以 `@CN` / `@EN` 注解的 `Lang` 字段声明，随 datagen 产出 lang；不要在代码里写死可翻译字符串。
- 工具类保持无注册依赖；需要注册对象的逻辑放回对应域。

## ANTI-PATTERNS
- 重新引入 `CTPPValues`。
- 复制 CTNH-Lib `utils/` 或本模块其他域已有的能力。

## SCOPE
适用于 `src/main/java/com/mo_guang/ctpp/util`。

## READ WHEN
- 需要 CTPP 范围内的共享 helper。
- 改动动能 tooltip 或机械等级显示。

## SOURCE OF TRUTH
- `util/` 下的工具类。
- 机械等级与电压名以 `GTValues.VNF` 为准。

## WORKFLOW
1. 先在 CTNH-Lib `utils/` 与本模块其他域找现成能力。
2. 跑 `:modules:CTPP:build`。
