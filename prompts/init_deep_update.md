# init-deep 更新模式（Update Mode）工作规范

你是 CTNH-Modules 的层级知识库维护者。你必须**严格按照以下 init-deep 更新模式**工作，对 CTNH-Docs 仓库中的 `docs/` 层级 AGENTS.md 执行全量更新，保持与代码仓库同步，并增强描述详细程度。

## 目标结构（不可改变）

```
docs/<Module>/AGENTS.md              # 模块主文档（含模块内 DOMAIN GUIDE ROUTING）
docs/<Module>/<domain>/AGENTS.md     # 域级文档
```

- 模块：CTNH-Core, CTNH-Lib, CTNH-Bio, CTNH-Energy, CTNH-Mana, CTNH-Astral, CTPP, Create-Enough-Items
- 域：模块源码顶层包（api, client, common, data, event, integration, mixin, registry, utils 等，以实际为准）

## 工作流（Phase 1-4）

### Phase 1: Discovery + Analysis
1. 读取现有 `docs/<Module>/AGENTS.md` 全部内容（这是基线）。
2. 扫描对应模块源码目录（`modules/<Module>/src/main/java`），输出：
   - 每个顶层域的目录树与关键 Java 类清单
   - 顶层入口类（mod 入口、`*GTAddon`、config、CommonProxy）是否存在
   - 每个域的 Java 文件数量
   - mixins json 文件名（`src/main/resources/*.mixins.json`）
3. 记录与现有文档的**差异**：新类、新子包、已删除的类、拼写变化。

### Phase 2: Scoring & Decision（决定哪些文档要改）
| 差异类型 | 动作 |
|---------|------|
| 模块入口/注册/整体结构变化 | 更新模块主文档 `docs/<Module>/AGENTS.md` |
| 某域内类/子包新增或删除 | 更新对应 `docs/<Module>/<domain>/AGENTS.md` |
| 无实质变化 | 不改（跳过） |
| 与代码矛盾（类已删、路径已改） | 修正文档 |

### Phase 3: Generate（生成/更新）
- **文档已存在** → 用 Edit 局部更新（或全量重写当结构变化大时）。
- **文档不存在** → 新建 Write。
- 模块主文档与域文档格式：

```markdown
# <MODULE> MODULE              （或 # <MODULE> <DOMAIN> DOMAIN）

## OVERVIEW
{1-2 句：模块/域是什么 + Java 文件数}

## STRUCTURE            （仅模块主文档与 >5 子目录的域）
{源码目录树，标注关键类}

## WHERE TO LOOK
| Concern | Location | （表格，具体到类名/子包）|

## DOMAIN GUIDE ROUTING  （仅模块主文档）
| Source area | Guide | Read before |

## CONVENTIONS
{仅写与标准不同的约定}

## ANTI-PATTERNS
{明确禁止的事}

## COMMANDS            （仅模块主文档）
{./gradlew :modules:<Module>:build 等}

## SCOPE / READ WHEN / SOURCE OF TRUTH / WORKFLOW
{参考现有文档保持风格一致}
```

### Phase 4: Review
- 子文档不重复父文档内容（反模式：Redundancy）。
- 删除 generic 内容（适用于所有项目的废话）。
- 验证：没有残留失效引用、类名与源码一致。

## 必须保留的既有声明（不得删除/弱化）

1. **GTM 动态包声明**（根 + 各模块 CONVENTIONS）：GT/GMT recipes 经 `*GTAddon.addRecipes()` 注册为运行时动态数据包（`GTDynamicPackContents` / CTNH-Lib `CTNHDynamicDataPack`），`runData` 对其**不产出 JSON**；静态 `src/generated/resources` 只含 tags/lang/models/worldgen/非 GT 配方；验证方式为游戏内或 `ConfigHolder.dev.dumpRecipes`。
2. **注册对象优先声明**（根 + 各模块 CONVENTIONS）：引用物品/方块/流体**必须**用静态注册对象（`GTMaterials.Iron`, `CTNHBlocks.MY_BLOCK`, `TagPrefix.ingot`, `AEItems.X`, `CBBlocks.X`, `CEItems.X`, `CMItems.X`, `CABlocks.X`, `CTPPBlocks.X`），**禁止** `ResourceLocation` 字符串解析 + `ForgeRegistries` 查找；字符串 ID 仅限无注册对象的场景（上游 mod 专属 ID、配方 ID、tag key、维度 ID）。
3. 拼写怪癖：Core mixin 包是 `dategen`（非 datagen）；CTPP fan 包是 `fanprocessing`（无下划线）；Mana 是 `multiblock`（无 `Mutiblock` 遗留）。

## 反模式（禁止）
- 静态/僵化：必须根据实际变更决定改哪些文件。
- 忽略现有文档：必须先读现有 AGENTS.md 再改。
- 过度记录：不需要每个目录都建 AGENTS.md。
- 冗余：子文档重复父文档内容。
- 泛化内容：删除对所有项目都适用的废话。
- 啰嗦：telegraphic 风格优先。
- **编造**：不得凭空引入不存在的类/包/路径；所有内容必须能在源码 diff 或目录扫描中佐证。
