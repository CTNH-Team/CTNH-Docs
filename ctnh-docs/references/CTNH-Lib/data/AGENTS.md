# CTNH-LIB DATA DOMAIN

## OVERVIEW
数据包运行时支撑：GT 动态包宿主、静态数据包过滤、共享配方移除注册（3 个 Java 文件）。

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| 动态包宿主 | `data/CTNHDynamicDataPack.java`（`addRecipe` / `addAdvancement` / `clearServer` / `writeJson` / `getRecipeLocation` / `getAdvancementLocation` / `getTagLocation`） |
| 静态数据包过滤 | `data/DataFilterPack.java` |
| 共享移除注册 | `data/recipe/RecipeRemovalHelper.java`：`FILTERS`、`remove()`、`clear()`、`getFilters()`、`RemoveFilter` |
| 过滤字段 | `RemoveFilter`：`id`/`id(List)`、`idRegex`、`mod`、`type`、`not`、`or`、`matches(ResourceLocation)`、`derivedType()` |
| 静态过滤 API | `DataFilterPack`：`FILTERED`、`removeRecipe(...)`、`removeRecipeType(...)`、`removeData(...)`、`RawRL` |
| 生效点 | `../mixin/AGENTS.md`：`RecipeManagerApplyMixin`、`GTRecipesMixin` |

## CONVENTIONS
- 过滤在 `RecipeManager` 解析数据包配方之前生效（`RecipeManagerApplyMixin` 在 `apply*` HEAD 剔除 map 键）；动态配方不受影响。
- `RemoveFilter` 顶层字段按 AND 组合；`not` 命中即排除，`or` 要求至少一个子过滤器命中；`type` 由 namespace + 路径首段推导（`derivedType`）。
- 模块在重载自己的规则前必须先 `RecipeRemovalHelper.clear()` 再重新注册（当前模块只调 `remove()`，未显式清空）。当前注册方：Core `data/recipe/RecipeRemoval`，Mana `CTNHManaGTAddon` / `data/recipe/ManaRecipeRemoval`。
- `DataFilterPack` 走 `GTPackSource("ctnhlib:filter_data")`，元数据 `filter.block` 由 `FILTERED`（`RawRL`）序列化；`RawRL.of` / `ofType` 会校验 namespace 与 path 字符集并对非法输入抛 `IllegalArgumentException`；消费方为 Bio `data/recipe/RecipeRemoval`。
- `CTNHDynamicDataPack` 目前**仅 Lib 内部定义**，尚无模块调用；GT 侧动态包经 `GTDynamicPackContents` 与 `ConfigHolder.dev.dumpRecipes` 落盘到 `gtceu/dumped/data`。

## ANTI-PATTERNS
- 在模块内重新实现移除逻辑；应走 `RecipeRemovalHelper` 或 `DataFilterPack`。
- 想在这里过滤动态 GT 配方；该 mixin 只剔除数据包 map 键。
- 用字符串 ID + `ForgeRegistries` 反查来构造过滤目标；用注册对象或明确的配方 id。

## SCOPE
只管数据包入口（动态包 / 静态过滤 / 移除注册）。不做配方创建。

## READ WHEN
- 跨模块增删数据包配方、改移除过滤条件或动态包行为。

## SOURCE OF TRUTH
- `tech.vixhentx.mcmod.ctnhlib.data` 下的源码；生效点见 `mixin/`。

## WORKFLOW
1. 经 `RecipeRemovalHelper.remove(...)` 或 `DataFilterPack.remove*` 注册规则。
2. 确认对应 mixin 生效路径（`RecipeManagerApplyMixin` 剔 map 键 / `GTRecipesMixin` 清 `FILTERED`）。
3. 进游戏验证被移除的配方确实消失。
