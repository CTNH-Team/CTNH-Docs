# CTNH-BIO INTEGRATION DOMAIN

## OVERVIEW
Bio 活体机器的 XEI / Jade / EMI / JEI 集成（7 个 Java 文件）。

## STRUCTURE
```
integration/
├─ emi/                       # CTNHBioEmiPlugin
├─ jade/                      # NutrientElement
├─ jei/                       # CTNHBioJeiPlugin, MobCrushingCategory, RelatedInfoJeiPlugin
└─ xei/
   ├─ entry/entity/           # EntityEntryList
   └─ handlers/entity/        # CycleEntityEntryHandler
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| EMI 插件 | `integration/emi/CTNHBioEmiPlugin.java` |
| Jade 元素 | `integration/jade/NutrientElement.java`（`extends snownee.jade.api.ui.Element`，渲染 `jade.nutrient.info`） |
| JEI 插件 | `integration/jei/CTNHBioJeiPlugin.java`, `RelatedInfoJeiPlugin.java` |
| 磨碎配方类别 | `integration/jei/MobCrushingCategory.java` |
| XEI 实体条目 | `integration/xei/entry/entity/EntityEntryList.java` |
| XEI 实体循环处理器 | `integration/xei/handlers/entity/CycleEntityEntryHandler.java` |

## CONVENTIONS
- `NutrientElement` 只负责渲染，数据来源是机器经 Jade 写入的营养字段（见 `api/machine/BasicLivingMachine.java` 的 `writeMachineJadeData` / `appendMachineJadeTooltip`）；属性与机器营养条本身的绘制在 `api/` 侧，不在这里重复取数。
- `integration/jei/MobCrushingCategory` 与 `common/recipe/MobCrushingRecipe.java` 成对，改动配方结构时同步改类别。
- 集成类保持可选、单向：只依赖 `api/` 契约与注册对象，不做 `common/` 代码的硬依赖。

## ANTI-PATTERNS
- 让公共代码硬依赖集成类（EMI / Jade / JEI / XEI 类不得出现在 `common/` 或 `api/` 的实现路径上）。
- 在集成层重复实现机器已在 Jade 数据中提供的推导信息。

## SCOPE
`src/main/java/com/moguang/ctnhbio/integration` 及其全部子包。

## READ WHEN
- 修改 Bio 的 XEI / EMI / JEI / Jade 集成。

## SOURCE OF TRUTH
- `integration/` 下的类与其注册点（`CommonProxy`、各 mod 的插件发现机制）。

## WORKFLOW
1. 改钩子前先确认目标 mod 的当前版本与 API。
2. 跑 `:modules:CTNH-Bio:build`；在装有目标 mod 的客户端运行时验证。
