# CREATE-ENOUGH-ITEMS MIXIN DOMAIN

## OVERVIEW
`mixin/` 是 CEI 的补丁域（12 个 Java 文件）：改写 EMI 的配方页按钮、侧栏折叠组投影、搜索加速、标签展开与配方管理器，替换 TMRV 的配方忽略判定，并修补 Create JEI 的配方注册；附带 2 个 accessor。

## STRUCTURE
```
mixin/
├── accessor/       # EditBoxAccessor
├── create/         # CreateJEIMixin（含 CategoryBuilderMixin 内部类）
├── emi/            # 8: EmiApiTagExpandMixin, EmiRecipesMixin, EmiScreenManagerInputMixin,
│                   #    EmiScreenManagerMixin, EmiScreenManagerScreenSpaceMixin, EmiSearchMixin,
│                   #    EmiTagsMixin, RecipeScreenMixin
├── emi/accessor/   # GTEmiRecipeAccessor
└── tmrv/           # RecipeManagerMixin
```
`src/main/resources/cei.mixins.json`：`mixins` 6 项（`accessor.EditBoxAccessor`、`create.CreateJEIMixin`、`create.CreateJEIMixin$CategoryBuilderMixin`、`emi.EmiScreenManagerMixin`、`emi.EmiTagsMixin`、`tmrv.RecipeManagerMixin`）；`client` 7 项（`emi.EmiApiTagExpandMixin`、`emi.EmiRecipesMixin`、`emi.EmiScreenManagerInputMixin`、`emi.EmiScreenManagerScreenSpaceMixin`、`emi.EmiSearchMixin`、`emi.RecipeScreenMixin`、`emi.accessor.GTEmiRecipeAccessor`）。

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| 流体堆栈给予 / 光标容器填充 / 居中搜索栏禁用 | `mixin/emi/EmiScreenManagerMixin.java` |
| 侧栏 G 按钮、配方页按钮、折叠组 tooltip、拖拽填搜索 | `mixin/emi/EmiScreenManagerInputMixin.java` |
| 配方页过滤按钮实现与过滤刷新 | `mixin/emi/RecipeScreenMixin.java` |
| 折叠组侧栏投影与绘制 | `mixin/emi/EmiScreenManagerScreenSpaceMixin.java` |
| 搜索加速与 tooltip 烘焙 | `mixin/emi/EmiSearchMixin.java` |
| 标签展开与关联搜索 | `mixin/emi/EmiApiTagExpandMixin.java` |
| 快速配方索引替换 | `mixin/emi/EmiRecipesMixin.java` |
| EMI tag 压缩修正 | `mixin/emi/EmiTagsMixin.java` |
| Create JEI 配方注册修补 | `mixin/create/CreateJEIMixin.java` |
| TMRV 配方忽略判定修补 | `mixin/tmrv/RecipeManagerMixin.java` |
| GTCEu 配方访问 | `mixin/emi/accessor/GTEmiRecipeAccessor.java` |
| EditBox 边框读取 | `mixin/accessor/EditBoxAccessor.java` |
| Mixin 配置 | `src/main/resources/cei.mixins.json` |

## CONVENTIONS
- 目标覆盖 EMI、Create JEI、TMRV 与 GTCEu 的 EMI 类；改注入点前先核对上游目标方法/字段名。多数文件为 `remap = false`。
- `EmiScreenManagerMixin` 目标是 `EmiScreenManager`：`Redirect` `give` 中的 `EmiStack.getItemStack()`，流体堆栈时经 `GTItems.FLUID_CELL` 填 1000mB 后返回（结果存 `@Share("realStack")`）；`Inject` 到 `mouseReleased` 的 `deleteCursor` 调用处以填充光标容器；`ModifyExpressionValue` 把 `EmiConfig.centerSearchBar` 强制为 `false`。
- `EmiScreenManagerMixin` 填充后除创造模式物品栏且 `instabuild` 外，都经 `CreateItemC2SPacket` 同步服务端；被处理的界面经 `EmiApi.getHandledScreen()` 获取，不 `@Shadow` `Minecraft client`。
- `EmiScreenManagerInputMixin` 在 `renderWidgets` 尾部绘制 4 组配方页按钮与拖拽高亮，G 按钮位于 `search.getX() - TOGGLE_BUTTON_SIZE(16) - TOGGLE_BUTTON_GAP(4)`，Y 取 `search.getY()`。
- `EmiScreenManagerInputMixin` 在 `mouseClicked` 头部依次处理精选（56×16）、关联搜索（56×16）、重复（56×16）、电压（最小/最大 32×16、重置 56×16）按钮；随后左键 G 按钮 `toggleAll(false)`（智能：存在折叠组则展开全部）、右键 `toggleAll(true)`（强制折叠），Alt+左键 `toggleGroup` 单个分组；`mouseScrolled` 在电压最小/最大按钮上调节区间。
- `EmiScreenManagerInputMixin` 用 `Redirect` 改写 `renderCurrentTooltip` 中的 `EmiIngredient.getTooltip()`，为分组成员追加 `cei.emi.collapsible.group.count` 与 `cei.emi.collapsible.group.toggle` 两行；`getSearchSource` 返回时按需重建分组，`toggleVisibility` 头部标记 dirty。
- `EmiScreenManagerInputMixin` 在 `mouseReleased` 头部调用 `CEIEmiDragSearchFill.dropNameIntoHoveredTextField()`，把拖拽的物品名填入落点搜索框。
- `RecipeScreenMixin` 实现 `CEIFeaturedRecipeScreen`、`CEIAssociatedSearchRecipeScreen`、`CEIDuplicateRecipeScreen`、`CEIVoltageRecipeScreen` 四个接口，`@Shadow` `recipes`、`tabs`、`tabPageSize`、`tab`、`page`、`setPage`、`backgroundWidth`、`backgroundHeight`、`x`、`y`（不 `@Shadow` `tabPage`）。
- `RecipeScreenMixin` 在 `<init>` 中 `Redirect` `recipes` 的 `PUTFIELD`，先用 `CEIFeaturedRecipes.copyOf()` 备份原始列表到 `cei$allRecipes`，再套 `cei$applyRecipeFilters()`（顺序为 `CEIVoltageRecipeFilter.apply(CEIDuplicateRecipes.apply(CEIFeaturedRecipes.apply(recipes)))`）。
- `RecipeScreenMixin.cei$refreshFilteredRecipes()` 先记录聚焦分类与页码，重算过滤后 `Minecraft.getInstance().setScreen(this)`，再由 `cei$restoreFocusedPage()` 用 `setPage()` 还原；不会把 `tab`/`page` 归零。
- `RecipeScreenMixin` 按钮坐标：精选 `x + max(0,(backgroundWidth-56)/2)`、关联搜索 `x`、重复 `x + max(0, backgroundWidth-56)`，三者 Y 均为 `min(y + backgroundHeight + 4, height - 20)`；电压最小值 `x + max(0,(backgroundWidth-88)/2)`、最大值 = 最小值 X 加 56，Y 为 `min(关联搜索 Y + 18, height - 38)`；重置按钮 `x + max(0,(backgroundWidth-56)/2)`，Y 为电压按钮 Y + 18。
- `EmiScreenManagerScreenSpaceMixin` 只作用于 `EmiScreenManager.ScreenSpace` 的 `search && getType() == SidebarType.INDEX`：`getStacks` 返回时替换为折叠投影，折叠代表项跳过 EMI 原图标，`StackBatcher.draw()` 之后补画背景/边框/双层图标（GTNH NEI 风格：折叠背景 `0x335555EE`、边框 `0x995555EE`、后层偏移 `(1,-1)`、前层偏移 `(-2,2)`；展开成员背景 `0x44113377`、边框 `0xCC3344AA`，相邻同组格子省略共享边）。
- `EmiSearchMixin`：`Redirect` `bake` 中的 `EmiStack.getTooltipText()` 返回 `null`，`bake` 尾部标记折叠组 dirty 并重建 `TooltipBakeQueue`；`@Overwrite` `search(String)` 走快速路径（只接受单堆栈且已烘焙命中的 ingredient）。
- `EmiApiTagExpandMixin`：`displayRecipes`/`displayUses` 头部记录关联搜索上下文；启用时把 Forge 前缀关系组（`ingots`/`nuggets`/`hot_ingots`、`dusts`/`small_dusts`/`tiny_dusts`）展开成额外堆栈，并补 `forge:<suffix>` 与 `forge:molten_<suffix>` 流体条目，结果缓存于 `cei$tagCache`。
- `EmiRecipesMixin` `@Overwrite` `EmiRecipes.bake()`，用 `FastRecipeManager` 建索引并记录耗时。
- `EmiTagsMixin` 在 `EmiTags.getIngredient` 中拦截“含 NBT 的流体被错误压成 tag”的情况，直接返回 `ListEmiIngredient`。
- `CreateJEIMixin` `@Overwrite` 掉 `registerExtraIngredients`；内部类 `CategoryBuilderMixin` 对 `MILLING`/`SMELTING` 强制全量注册、对 `BLASTING` 跳过，并重写 `removeRecipes` 按首槽物品排除。
- `RecipeManagerMixin` 修补 TMRV `RecipeManager.addRecipe` 的忽略判定（对应 TooManyRecipeViewers issue #24：鼓风机只显示非原版配方）。
- accessor 仅暴露读取：`EditBoxAccessor.cei$isBordered()`、`GTEmiRecipeAccessor.cei$getRecipe()`；保持名字与 mixin 目标一致，并与 `cei.mixins.json` 包路径同步。

## ANTI-PATTERNS
- 未核对 `cei.mixins.json` 与上游 EMI/GTCEu 目标成员就改 mixin accessor 签名。
- 绕过 `mouseReleased` 填充路径中的创造模式 `instabuild` 跳过，直接发 `CreateItemC2SPacket`。
- 在 `EmiScreenManagerMixin` 里重新引入 `@Shadow Minecraft client`；应使用 `EmiApi.getHandledScreen()`。
- 把折叠组 G 按钮挪回搜索框右侧；当前行为是紧邻搜索框左侧。
- 让 `RecipeScreenMixin` 的过滤刷新把 `tabPage`/`tab`/`page` 归零；必须保留聚焦分类与页码。
- 把电压重置按钮放到最小/最大值按钮上方或与之重叠；它画在其下方（`cei$getVoltageMinButtonY() + 18`）。

## SCOPE
适用于 `src/main/java/com/ctnh/cei/mixin` 与 `src/main/resources/cei.mixins.json`。

## READ WHEN
- 修补 EMI 配方页、侧栏、搜索、标签展开、配方管理器、screen-manager 给予/填充，或 Create JEI、TMRV 行为。
- 改动折叠组 tooltip 渲染、G 按钮位置或侧栏投影绘制。
- 改动电压过滤按钮或配方页过滤刷新行为。

## SOURCE OF TRUTH
- `src/main/resources/cei.mixins.json` 与 `mixin/` 下的 mixin/accessor 类，尤其是 `mixin/emi/EmiScreenManagerMixin.java`、`mixin/emi/EmiScreenManagerInputMixin.java`、`mixin/emi/EmiScreenManagerScreenSpaceMixin.java`、`mixin/emi/RecipeScreenMixin.java`。

## WORKFLOW
1. 定位 mixin 包与其 JSON 条目。
2. 对照实际加载的 EMI/GTCEu/Create/TMRV 版本核对目标成员。
3. 跑 `:modules:Create-Enough-Items:build`；EMI 界面改动在运行时验证。
