# CTNH-BIO UTILS DOMAIN

## OVERVIEW
Bio 的共享工具类（7 个 Java 文件）：机器名解析、配方修饰符、分解配方转换、战利品生成、输入回调接口与若干小工具。

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| 机器中英文名 | `utils/CBMachineNames.java`（`getCNName` / `getENName` + 等级映射表） |
| 配方修饰符 | `utils/CBRecipeModifiers.java`（`BASIC_LIVING_MODIFIER`） |
| Biomancy 分解配方转换 | `utils/DecomposingRecipeHandler.java`（`toGTrecipe(DecomposingRecipe)`） |
| 战利品生成 | `utils/DespoilLootHelper.java`（`generateDespsoilLoot(...)`） |
| 按键 + 坐标回调 | `utils/IKeyPressedWithCoord.java` |
| 随机与小工具 | `utils/RandomUtils.java`, `utils/VialCraftingRemainingItem.java` |

## CONVENTIONS
- 工具类保持无状态、可用静态方法调用；不要在这里持有注册对象或机器状态。
- `utils/CBRecipeModifiers.BASIC_LIVING_MODIFIER` 当前所有分支都返回 `null`（不修改配方）；活体机器实际使用的修饰符在 `api/recipe/CBRecipeModifiers.java`，两处不要混淆。
- `CBMachineNames` 的名字表在静态初始化时填充，只做查表，不要在其中触发注册。

## ANTI-PATTERNS
- 重复实现 CTNH-Lib `utils/` 或 GTCEu 已有的共享工具。
- 把机器专属逻辑塞进 `utils/` 让多个域共享（应放 `api/machine/` 或对应 trait）。

## SCOPE
本域覆盖 `src/main/java/com/moguang/ctnhbio/utils` 下的全部类。

## READ WHEN
- 需要复用 Bio 范围内的通用辅助逻辑。

## SOURCE OF TRUTH
- `utils/` 下的工具类实现。

## WORKFLOW
1. 先查 CTNH-Lib `utils/` 是否已有同名能力。
2. 改完跑 `:modules:CTNH-Bio:build`。
