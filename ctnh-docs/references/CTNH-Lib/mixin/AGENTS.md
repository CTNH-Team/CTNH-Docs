# CTNH-LIB MIXIN DOMAIN

## OVERVIEW
面向 GTM 与 `RecipeManager` 的字节码补丁（4 个 Java 文件）。配置 `src/main/resources/ctnhlib.mixins.json`。

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| 数据包配方剔除 | `RecipeManagerApplyMixin.java`：`@Mixin(value = RecipeManager.class, priority = 1100)`、`@Inject(method = "apply*", at = @At("HEAD"))`、`map.keySet().removeIf(...)` + `RemoveFilter.matches` |
| 静态过滤表清理 | `GTRecipesMixin.java`：`@Mixin(value = GTRecipes.class, remap = false)`，在 `recipeRemoval` HEAD 调 `DataFilterPack.FILTERED.clear()` |
| 机器构建器 lang 注入 | `MachineBuilderMixin.java`：`@Redirect` 拦 `MachineBuilder.register()` 内的 `BlockBuilder.register()`，实例实现 `ICNBuilder` 且 `getCNLangValue()` 非空时用 `ProviderTypes.CNLANG` 写入 descriptionId |
| TMRV 配方 id 保留 | `TMRVMixin.java`：`@Redirect` 拦 `RecipeManager.Category.Recipe.getID` 内的 `ResourceLocation.fromNamespaceAndPath`，改返回 `getOriginalID()` |
| 注册 | `ctnhlib.mixins.json`：`mixins=[GTRecipesMixin, MachineBuilderMixin, RecipeManagerApplyMixin, TMRVMixin]`，`client` 数组为空 |

## CONVENTIONS
- 新增 mixin 类必须登记到 `ctnhlib.mixins.json` 的 `mixins`（客户端专用进 `client`）数组，否则不会加载。
- 顺序敏感时显式写 `priority`（`RecipeManagerApplyMixin` = 1100）。
- mixin 只读 Lib 自身状态（`RecipeRemovalHelper.getFilters()`、`DataFilterPack.FILTERED`），不引用任何功能模块。
- 过滤器列表为空时提前 return（`RecipeManagerApplyMixin`）。
- 目标类在 GTCEu 等非 MC 包下时加 `remap = false`（`GTRecipesMixin`、`MachineBuilderMixin`、`TMRVMixin`）。

## ANTI-PATTERNS
- 加了 mixin `.java` 却不登记 `ctnhlib.mixins.json`。
- 在 mixin 里解析配方内容；这里只剔 map 键，解析留给 `RecipeManager`。
- 在这里处理动态 GT 配方。
- 在 mixin 内直接引用功能模块的类，破坏 Lib 的独立性。

## SCOPE
仅 Lib 自有的 bytecode 补丁。不放游戏逻辑。

## READ WHEN
- 新增或修改任何 `ctnhlib` mixin 与 `ctnhlib.mixins.json`。

## SOURCE OF TRUTH
- `tech.vixhentx.mcmod.ctnhlib.mixin` 源代码与 `src/main/resources/ctnhlib.mixins.json`。

## WORKFLOW
1. 加类 → 在 `ctnhlib.mixins.json` 登记 → 确认注入点（HEAD / Redirect 目标签名）与委托逻辑。
2. 跑 `:modules:CTNH-Lib:build`，进游戏验证注入未失败（`defaultRequire: 1`）。
