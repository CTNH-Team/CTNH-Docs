# CREATE-ENOUGH-ITEMS MODULE

## OVERVIEW
Create-Enough-Items（`cei`）是 CTNH 的 EMI 体验模块，包根 `com.ctnh.cei`，31 个 Java 文件。覆盖 EMI 侧栏折叠组（含成员数量与 Alt+左键切换提示）、配方页过滤（精选/回收、Create 派生重复配方、GTCEu 电压区间）与刷新时保留聚焦页、关联搜索与标签展开、拖拽物品名填充搜索框、作弊模式流体容器填充、EMI 居中搜索栏禁用，以及静态 EMI 规则资源。命名空间为 `com.ctnh.cei`（不是 `com.moguang.cei`）。

## STRUCTURE
源码根 `modules/Create-Enough-Items/src/main/java/com/ctnh/cei/`（括号内为该域 Java 文件数）

```
cei/
├── CreateEnoughItems.java   # mod 入口 @Mod("cei")，持有 MODID / LOGGER / REGISTRATE
├── client/   (1)            # ClientProxy：客户端代理，构造期提前加载折叠组规则
├── common/   (1)            # CommonProxy：注册 registrate、datagen 与 GTCEu 监听占位
├── data/     (1)            # CEIDatagen：仅挂 lang processor
├── event/    (1)            # ForgeClientEventHandler：客户端 tick 驱动 tooltip 烘焙队列
├── mixin/    (12)           # accessor/、create/、emi/(8)、emi/accessor/、tmrv/
├── registry/ (1)            # CEIRegistrate：CTNH-Lib CNRegistrate 的薄封装
└── utils/    (13)           # emi/ 及 collapsible/duplicate/featured/search/voltage 子包
```

`mixin/` 12 个：`accessor/EditBoxAccessor`、`create/CreateJEIMixin`（含内部类 `CategoryBuilderMixin`）、`emi/` 8 个、`emi/accessor/GTEmiRecipeAccessor`、`tmrv/RecipeManagerMixin`。

`utils/` 13 个：`emi/TooltipBakeQueue`；`emi/collapsible/`(1)、`emi/duplicate/`(2)、`emi/featured/`(2)、`emi/search/`(5)、`emi/voltage/`(2)。

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| mod 入口 | `CreateEnoughItems.java` |
| 代理 | `client/ClientProxy.java`, `common/CommonProxy.java` |
| Registrate | `registry/CEIRegistrate.java` |
| Datagen 钩子 | `data/CEIDatagen.java` |
| EMI mixin | `mixin/emi/`（8）, `mixin/emi/accessor/GTEmiRecipeAccessor.java` |
| 流体堆栈给予 / 居中搜索栏禁用 | `mixin/emi/EmiScreenManagerMixin.java`（流体堆栈 → GT `FLUID_CELL`、光标容器填充、`EmiConfig.centerSearchBar` 强制关闭） |
| 折叠组 G 按钮与分组 tooltip | `mixin/emi/EmiScreenManagerInputMixin.java`（搜索框左侧绘制 G 按钮，追加分组数量/切换提示行） |
| 配方页按钮（精选 / 关联搜索 / 重复） | `mixin/emi/EmiScreenManagerInputMixin.java` + `mixin/emi/RecipeScreenMixin.java`（绘制与点击处理；`cei$toggleFeaturedRecipes` / `cei$toggleAssociatedSearch` / `cei$toggleDuplicateRecipes`） |
| 电压过滤按钮与重置 | `mixin/emi/EmiScreenManagerInputMixin.java` + `mixin/emi/RecipeScreenMixin.java`（最小值/最大值/重置按钮；`cei$resetVoltageFilter`） |
| 配方页过滤刷新 | `mixin/emi/RecipeScreenMixin.java`（应用 CEI 过滤器，恢复聚焦分类/页码而非回到 tab 0） |
| 折叠组侧栏投影与绘制 | `mixin/emi/EmiScreenManagerScreenSpaceMixin.java` |
| EMI 搜索加速与 tooltip 烘焙 | `mixin/emi/EmiSearchMixin.java`, `utils/emi/TooltipBakeQueue.java` |
| 标签展开 / 关联搜索入口 | `mixin/emi/EmiApiTagExpandMixin.java`, `utils/emi/search/CEIAssociatedSearch.java`, `utils/emi/search/TagRelationGraph.java` |
| 快速配方索引 | `mixin/emi/EmiRecipesMixin.java`, `utils/emi/search/FastRecipeManager.java` |
| Create JEI mixin | `mixin/create/CreateJEIMixin.java`（含 `CategoryBuilderMixin` 内部类） |
| TMRV mixin | `mixin/tmrv/RecipeManagerMixin.java` |
| EditBox accessor | `mixin/accessor/EditBoxAccessor.java` |
| EMI 功能实现 | `utils/emi/`（collapsible/, duplicate/, featured/, search/, voltage/） |
| 静态规则 JSON | `src/main/resources/assets/cei/emi/emi_collapsible_groups.json`, `emi_featured_recipes.json` |
| 语言与资源 | `src/main/resources/assets/cei/lang/`, `META-INF/mods.toml`, `cei.mixins.json` |

## ARCHITECTURE CONTRACT
机器 / trait / capability / Jade 的所有权边界、字段同步与持久化规则、Jade 数据最小化原则和迁移步骤在 `references/_architecture/AGENTS.md`。改动机器、trait、recipe capability 或 Jade 代码前先读它；本文件只描述本模块的落点。

## DOMAIN GUIDE ROUTING
| Source area | Guide | Read before |
|-------------|-------|-------------|
| `client/**` | `ctnh-docs/references/Create-Enough-Items/client/AGENTS.md` | 改动客户端启动与折叠组规则加载时机 |
| `common/**` | `ctnh-docs/references/Create-Enough-Items/common/AGENTS.md` | 改动启动流程、注册与 GTCEu 监听占位 |
| `data/**` | `ctnh-docs/references/Create-Enough-Items/data/AGENTS.md` | 新增 datagen 输出或语言处理 |
| `event/**` | `ctnh-docs/references/Create-Enough-Items/event/AGENTS.md` | 新增 Forge 事件监听（尤其客户端 tick） |
| `mixin/**` | `ctnh-docs/references/Create-Enough-Items/mixin/AGENTS.md` | 改写 EMI / Create JEI / TMRV 行为或 accessor |
| `registry/**` | `ctnh-docs/references/Create-Enough-Items/registry/AGENTS.md` | 改动 registrate 或新增注册内容 |
| `utils/**` | `ctnh-docs/references/Create-Enough-Items/utils/AGENTS.md` | 改动折叠组、过滤器、搜索等 EMI 功能实现 |

## CONVENTIONS
- **命名空间**：包根 `com.ctnh.cei`，前缀 `cei`，类名前缀 `CEI`；mod id 与 `CreateEnoughItems.MODID` 均为 `cei`。
- **依赖边界**：仅通过 `dependencies.gradle` 依赖 `:modules:CTNH-Lib`（`modImplementation(project(":modules:CTNH-Lib"))`），不依赖 CTNH-Core。`mods.toml` 强制依赖 `forge`、`minecraft`、`gtceu`（`[1.6,)`）与 `emi`（`[1.1,)`，`side="CLIENT"`）。
- **注册对象优先**：引用物品/方块/流体**必须**用静态注册对象（如 `GTItems.FLUID_CELL`、`Items.AIR`），**禁止** `ResourceLocation` 字符串解析 + `ForgeRegistries` 查找；字符串 ID 仅限无注册对象的场景（配方 ID、配方类别 ID、tag key、分组 GUID），`utils/emi/duplicate/CEIDuplicateRecipes` 与 `utils/emi/featured/CEIFeaturedRecipes` 的规则匹配即属此类。
- **GT 配方来源**：本模块无 `*GTAddon`、无 GT 配方注册，`CEIDatagen.init()` 只挂 lang processor，模块内不存在 `src/generated`。GT/GMT 配方由 GTCEu 与 CTNH-Core 经 `*GTAddon.addRecipes()` 注册为运行时动态数据包，`runData` 对其**不产出 JSON**；CEI 只在运行时经 EMI 读取这些配方，验证靠游戏内。
- **状态分家**：用户开关与展开状态存 `config/cei/*.json`（`collapsible_emi_groups.json`、`featured_emi_recipes.json`、`duplicate_emi_recipes.json`、`voltage_emi_recipes.json`、`associated_emi_search.json`）；内置默认值只放 `src/main/resources/assets/cei/emi/` 下的静态 JSON。
- **界面行为归 mixin**：侧栏、搜索框、配方页的差异化行为由 `mixin/emi/**` 直接改写 EMI 内部状态实现，属代码固有行为，不是配置项；改动前先核对上游 EMI 目标成员。
- **规则 JSON 语法**：接受物品 ID、tag（`#`）、Forge 矿石前缀（`$`）、正则（`regex:` / `r/.../`）、取反（`!`）、分组 OR（`|`）与 AND（空白分隔），以及 `recipe:` / `recipe_regex:` / `category:` / `category_regex:` / `input:` / `output:` / `catalyst:` / `item:` 选择器。

## ANTI-PATTERNS
- 把 EMI UI 行为挪到 CTNH-Core；EMI 侧栏/搜索/配方页定制属于 CEI。
- 在 `mixin/emi/EmiScreenManagerMixin.java` 之外处理 EMI 作弊模式容器填充；这是 CEI 拥有的 screen-manager 行为。
- 改运行时 `config/cei/*.json` 来改默认值；应改 `src/main/resources/assets/cei/emi/` 下的静态规则文件。
- 把电压过滤当通用 EMI 过滤；它只处理 GTCEu `GTEmiRecipe` 路径。
- 不改 `cei.mixins.json` 与上游 EMI/GTCEu 目标成员就直接改 mixin accessor 签名。
- 重新引入 `RecipeScreenMixin` 旧的“过滤刷新回到 tab 0 / page 0”行为；CEI 保留聚焦的配方页。
- 用字符串 ID + `ForgeRegistries` 查找代替已存在的静态注册对象。

## COMMANDS
```bash
./gradlew :modules:Create-Enough-Items:build           # 编译 + 校验
./gradlew :modules:Create-Enough-Items:runData         # 数据生成（本模块只产出 lang）
./gradlew :modules:Create-Enough-Items:spotlessCheck   # 格式化校验
```

## SCOPE
适用于 `modules/Create-Enough-Items` 及其子模块仓库。它是通过根路由表加载的参考指南，不是额外的源码树指令文件。

## READ WHEN
- 改动 EMI 侧栏、搜索、配方页或 screen-manager 的给予/填充行为。
- 改动 EMI/Create/TMRV mixin 目标或静态规则 JSON。
- 改动折叠组 G 按钮、侧栏投影绘制或分组 tooltip 渲染。
- 改动配方页过滤按钮（精选/关联搜索/重复/电压）或过滤刷新行为。

## SOURCE OF TRUTH
- 注册与生命周期：`CreateEnoughItems.java`、`common/CommonProxy.java`。
- EMI 功能实现：`utils/emi/` 各功能类。
- EMI screen-manager 行为：`mixin/emi/EmiScreenManagerMixin.java`、`mixin/emi/EmiScreenManagerInputMixin.java`。
- 配方页过滤刷新：`mixin/emi/RecipeScreenMixin.java`。
- 静态规则：`src/main/resources/assets/cei/emi/` 下的 JSON。

## WORKFLOW
1. 把改动的符号映射到域，先读对应域文档（见 DOMAIN GUIDE ROUTING）。
2. 改行为前先核对 EMI mixin 目标与 accessor 对齐情况。
3. 跑最窄的 Gradle 任务；EMI 界面改动在运行时验证。
4. 若改动引入新的模块边界，回头复核根路由表。
