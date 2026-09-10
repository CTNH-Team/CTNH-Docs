# CTNH-LIB API DOMAIN

## OVERVIEW
被多个 CTNH 模块消费的共享常量与跨并行配方逻辑（3 个 Java 文件）。

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| 共享常量 | `api/CTNHValues.java`（`DYE_COLOR_CN` 染料中文名、`VNC` / `VNCF` 电压等级中文名） |
| 跨并行配方逻辑 | `api/CrossParallelRecipeLogic.java`（`MAX_MERGED = 64`、`mergedRecipe`、`recipeIDs`） |
| 机器侧契约 | `api/ICrossParallelRecipeLogicMachine.java`（`modifyRecipeAfterMerge(recipe, group)`） |

## CONVENTIONS
- 这里的 API 被功能模块消费；保持稳定、不引入模块依赖、不放模块专属实现。
- `CrossParallelRecipeLogic extends RecipeLogic`：`findAndHandleRecipe()` 按 `RecipeHandlerGroup` 逐个尝试合并匹配配方（`tyrMergeMatchedRecipe`，受 `MAX_MERGED` 限制），`mergeRecipe()` 累加 `inputs/outputs/tickInputs/tickOutputs`、合并 `data`、`parallels` 相加、`tier`/`duration` 取大；合并配方 id 为 `gtceu:merged/<category>/<random>`，结束后由 `setupMergedRecipe()` 落状态并清空 `recipeIDs`。
- 机器侧实现 `ICrossParallelRecipeLogicMachine`：`createRecipeLogic()` 返回 `CrossParallelRecipeLogic`，合并后经 `modifyRecipeAfterMerge()` 做最终校验（返回非空即失败并写入 `failureReasonsMap`）。当前消费方：Core `common/machine/multiblock/kinetic/MeadowMachine`、Mana `common/multiblock/CrossParallelManaMultiBlockMachine`。

## RECIPE LOGIC BOUNDARY
`CrossParallelRecipeLogic` 是 `RecipeLogic` 子类，被多个模块的机器复用。约束以 `references/_architecture/AGENTS.md` §6/§7 为准：

- 遍历 recipe 内容统一走 `ContentListMap.forEachEntry`；不要遍历 `asMap().entrySet()` 再手排。顺序基准是 `RecipeCapability.COMPARATOR`（按 `sortIndex`），底层容器是插入序的 `Reference2ObjectArrayMap`，**不要假定 map 迭代序等于 capability 序**。
- 输出内容的解释归各 `RecipeCapability`；`RecipeLogic` 不加 capability 类型判断。
- 泛型擦除集中在 `ContentListMap` 内部，调用方用泛型 `EntryConsumer`，不要新增 `rawtypes`/`unchecked` helper。

## ANTI-PATTERNS
- 把模块专属常量加进 `CTNHValues`；应放所属模块。
- 在 `api/` 引入模块依赖或模块专属实现。

## SCOPE
适用于 `src/main/java/tech/vixhentx/mcmod/ctnhlib/api`。

## READ WHEN
- 新增被多个模块共用的常量或跨并行配方行为。

## SOURCE OF TRUTH
- `api/CrossParallelRecipeLogic.java` 及其机器侧接口 `api/ICrossParallelRecipeLogicMachine.java` 的契约。

## WORKFLOW
1. 确认该常量/逻辑被不止一个模块使用。
2. 改签名前检查消费方（Core `MeadowMachine`、Mana `CrossParallelManaMultiBlockMachine` 等）。
3. 跑 `:modules:CTNH-Lib:build`。
