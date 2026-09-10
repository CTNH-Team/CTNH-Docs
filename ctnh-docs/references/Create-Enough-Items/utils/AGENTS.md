# CREATE-ENOUGH-ITEMS UTILS DOMAIN

## OVERVIEW
`utils/` 是 CEI 的 EMI 功能实现域（13 个 Java 文件）：侧栏折叠组、精选/回收配方过滤、Create 派生重复配方过滤、关联搜索、快速配方索引、拖拽搜索填充，以及 GTCEu 电压区间过滤（含一键重置）。

## STRUCTURE
```
utils/emi/
├── TooltipBakeQueue.java
├── collapsible/    # CEICollapsibleGroups
├── duplicate/      # CEIDuplicateRecipeScreen, CEIDuplicateRecipes
├── featured/       # CEIFeaturedRecipeScreen, CEIFeaturedRecipes
├── search/         # 5: CEIAssociatedSearch, CEIAssociatedSearchRecipeScreen,
│                   #    CEIEmiDragSearchFill, FastRecipeManager, TagRelationGraph
└── voltage/        # CEIVoltageRecipeFilter, CEIVoltageRecipeScreen
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| 折叠组（规则、状态、tooltip 查询） | `utils/emi/collapsible/CEICollapsibleGroups.java` |
| 精选/回收配方过滤 | `utils/emi/featured/CEIFeaturedRecipes.java`, `utils/emi/featured/CEIFeaturedRecipeScreen.java` |
| 重复配方过滤（Create 派生） | `utils/emi/duplicate/CEIDuplicateRecipes.java`, `utils/emi/duplicate/CEIDuplicateRecipeScreen.java` |
| 关联搜索开关与上下文 | `utils/emi/search/CEIAssociatedSearch.java`, `utils/emi/search/CEIAssociatedSearchRecipeScreen.java` |
| 快速配方索引 | `utils/emi/search/FastRecipeManager.java` |
| 标签关系图 | `utils/emi/search/TagRelationGraph.java` |
| 拖拽填搜索框 | `utils/emi/search/CEIEmiDragSearchFill.java` |
| 电压区间过滤（含重置） | `utils/emi/voltage/CEIVoltageRecipeFilter.java`, `utils/emi/voltage/CEIVoltageRecipeScreen.java` |
| tooltip 烘焙队列 | `utils/emi/TooltipBakeQueue.java` |

## CONVENTIONS
- `CEICollapsibleGroups` 读取内置规则 `/assets/cei/emi/emi_collapsible_groups.json`（实际文件含 214 个分组），把展开/折叠状态持久化到 `config/cei/collapsible_emi_groups.json`；`loadRules()` 由 `ClientProxy` 构造函数提前调用。
- 折叠组只有成员数 ≥ 2 才算有效分组（`totalGroupCount` / `hasGroups` / `collapseAll` 均以此为准）。
- `EmiScreenManagerInputMixin` 用 `CEICollapsibleGroups.getGroup(ingredient)` 追加 `cei.emi.collapsible.group.count` 与 `cei.emi.collapsible.group.toggle` 两行 tooltip；`EmiScreenManagerScreenSpaceMixin` 用 `project()` / `projectReload()` 得到 `ProjectResult`（列表 + `GroupBuf` 折叠位置链表）完成侧栏投影。
- `CEIFeaturedRecipes`、`CEIDuplicateRecipes`、`CEIVoltageRecipeFilter` 依次套在 `RecipeScreenMixin.cei$applyRecipeFilters()` 中，驱动配方页过滤。
- `CEIFeaturedRecipes.apply()` 需 `enabled` 为真且规则非空才过滤，隐藏匹配规则的配方；规则来源为 `/assets/cei/emi/emi_featured_recipes.json`（3 组 GTCEu 回收类别），开关状态存 `config/cei/featured_emi_recipes.json`（默认关闭）。
- `CEIFeaturedRecipes.ItemIdRule` 容忍“物品不存在”的写法：同命名空间下若该 ID 未注册，则按路径前缀匹配。
- `CEIDuplicateRecipes` 硬编码 Create 派生类别黑名单：`create:automatic_shaped`、`automatic_shapeless`、`automatic_brewing`、`automatic_packing`、`block_cutting`、`fan_smoking`、`fan_blasting`，外加 `vintageimprovements:unpacking`（Create Vintage 振动台自动生成的“震动解包”配方，与机械动力的压缩配方重复）。ID 由 `createId()` / `vintageImprovementsId()` 经 `ResourceLocation.tryBuild` 构造，不用 `ForgeRegistries`。
- `CEIDuplicateRecipes` 还会过滤 Create `spout_filling` 类别下 `fill_` 前缀与 `potions` 配方，以及 `draining` 类别下 `empty_` 前缀与 `potions` 配方；隐藏开关存 `config/cei/duplicate_emi_recipes.json`（默认显示）。
- `CEIVoltageRecipeFilter` 只读 `GTEmiRecipe`：经 `GTEmiRecipeAccessor.cei$getRecipe()` 取 `GTRecipeDefinition` 的 `tier`；非 GT 配方与取不到 tier 的配方一律保留。
- `CEIVoltageRecipeFilter` 区间默认 `GTValues.ULV` 到 `GTValues.MAX`，超出边界时环绕（`cycleTier`），状态存 `config/cei/voltage_emi_recipes.json`；`reset()` 重新加载状态后把 `minTier`/`maxTier` 复位并保存。
- `CEIVoltageRecipeScreen` 声明 6 个按钮坐标访问器与 `cei$adjustVoltageMinTier` / `cei$adjustVoltageMaxTier` / `cei$resetVoltageFilter`，由 `RecipeScreenMixin` 实现。
- `CEIAssociatedSearch` 的开关（默认开启）存 `config/cei/associated_emi_search.json`，并记录当前配方页的查询对象与模式（`RECIPES`/`USES`）供 `refreshCurrentLookup()` 重放。
- `TagRelationGraph` 只存标签前缀的对称关系；`EmiApiTagExpandMixin` 注册 `ingots`/`nuggets`/`hot_ingots` 与 `dusts`/`small_dusts`/`tiny_dusts` 两组。
- `FastRecipeManager` 实现 `EmiRecipeManager`，按类别/输入/输出/ID 建索引，输入索引同时纳入催化剂（`getCatalysts()`），输出去重，并填充 `EmiRecipes.byWorkstation`。
- `CEIEmiDragSearchFill` 通过 `EditBoxAccessor` 读取 `bordered` 计算可视区域，对 AE2 `AETextField` 额外留出内边距与光标宽度；拖拽时用 `0x8000FF00` 高亮可落点搜索框。
- 规则 JSON 通用语法：物品 ID、tag（`#`）、Forge 前缀（`$`）、正则（`regex:` / `r/.../`）、取反（`!`）、OR（`|`）与 AND（空白分隔），以及`recipe:` / `recipe_regex:` / `category:` / `category_regex:` / `input:` / `output:` / `catalyst:` / `item:` 选择器。
- 折叠组规则条目支持 `key`/`rules`、`priority`（非负，负数整组作废）与 `expanded` 字段。
- 本域的 `ForgeRegistries` 用法限于规则字符串 ID 匹配（如 `ItemRegexRule` / `ItemIdRule` 反查物品 ID），不用于物品解析。

## ANTI-PATTERNS
- 改运行时 `config/cei/*.json` 来改默认值；应改 `src/main/resources/assets/cei/emi/` 下的静态规则文件。
- 把电压过滤当通用 EMI 过滤；它只处理 GTCEu `GTEmiRecipe` 路径。
- 用 `ForgeRegistries` 去解析 `CEIDuplicateRecipes` 的 ID 黑名单；保持硬编码的 `ResourceLocation` 列表。
- 不经 `loadState()`/`saveState()` 直接改 `minTier`/`maxTier` 来实现电压重置；应走 `CEIVoltageRecipeFilter.reset()`。
- 在折叠组之外重复实现侧栏投影或分组 tooltip 查询。

## SCOPE
适用于 `src/main/java/com/ctnh/cei/utils` 及其子包。

## READ WHEN
- 改动 EMI 侧栏/搜索/配方页功能行为。
- 改动折叠组 tooltip 内容、分组规则查找或侧栏投影。
- 改动重复配方 ID 黑名单（Create / Vintage Improvements 或其他上游配方 ID）。
- 改动电压过滤重置行为或 `CEIVoltageRecipeScreen` 接口。

## SOURCE OF TRUTH
- `utils/emi/` 下的类与 `src/main/resources/assets/cei/emi/` 下的静态规则 JSON。
- 重复配方过滤以 `utils/emi/duplicate/CEIDuplicateRecipes.java` 的 ID 黑名单为准。
- 电压过滤/重置以 `utils/emi/voltage/CEIVoltageRecipeFilter.java` 与 `utils/emi/voltage/CEIVoltageRecipeScreen.java` 为准。

## WORKFLOW
1. 改行为前先看对应功能类。
2. 新增黑名单条目前，先核对该上游配方 ID 真实存在。
3. 规则 JSON 需符合上述选择器语法。
4. 电压重置相关改动保持 `CEIVoltageRecipeScreen` 接口与 `RecipeScreenMixin` 实现同步。
5. 跑 `:modules:Create-Enough-Items:build`；EMI 界面改动在运行时验证。
