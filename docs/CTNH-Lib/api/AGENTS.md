# CTNH-LIB API DOMAIN

## OVERVIEW
Shared API values and cross-parallel recipe logic consumed by multiple CTNH modules (3 Java files).

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Shared constants | `api/CTNHValues.java` |
| Cross-parallel recipe logic | `api/CrossParallelRecipeLogic.java`, `api/ICrossParallelRecipeLogicMachine.java` |

## CONVENTIONS
- API surfaces here are consumed by feature modules; keep them stable and dependency-free.
- `CrossParallelRecipeLogic` implements shared parallel recipe behavior used by machine trait implementations (e.g., Core's `SimpleComputationContainer`).

## RECIPE LOGIC BOUNDARY
`CrossParallelRecipeLogic` 是 `RecipeLogic` 子类，被多个模块的机器复用。约束以 `docs/_architecture/AGENTS.md` §6/§7 为准：

- 遍历 recipe 内容统一走 `ContentListMap.forEachEntry`；不要遍历 `asMap().entrySet()` 再手排。顺序基准是 `RecipeCapability.COMPARATOR`（按 `sortIndex`），底层容器是插入序的 `Reference2ObjectArrayMap`，**不要假定 map 迭代序等于 capability 序**。
- 输出内容的解释归各 `RecipeCapability`；`RecipeLogic` 不加 capability 类型判断。
- 泛型擦除集中在 `ContentListMap` 内部，调用方用泛型 `EntryConsumer`，不要新增 `rawtypes`/`unchecked` helper。

## ANTI-PATTERNS
- Do not add module-specific constants to `CTNHValues`; put them in the owning module.

## SCOPE
Applies to `src/main/java/tech/vixhentx/mcmod/ctnhlib/api`.

## READ WHEN
- Adding shared values or cross-parallel recipe behavior used by multiple modules.

## SOURCE OF TRUTH
- `api/CrossParallelRecipeLogic.java` and its machine interface contract.

## WORKFLOW
1. Confirm the value/logic is used by more than one module.
2. Check consumers in Core/Energy/Bio before changing signatures.
3. Run `:modules:CTNH-Lib:build`.
