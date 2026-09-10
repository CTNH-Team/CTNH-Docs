# CTNH-LIB MODULE

## OVERVIEW
CTNH 全模块共享库，**两个包根**：`tech.vixhentx.mcmod.ctnhlib`（48 个 Java 文件）+ `com.ctnhlang`（11 个 Java 文件），合计 **59 个 Java 文件**。入口 `CTNHLib`（`@Mod("ctnhlib")`），代理 `common/CommonProxy` / `client/ClientProxy`。只放共享基础设施，无游戏内容；消费方为 CTNH-Core、CTNH-Energy、CTNH-Bio、CTNH-Mana、CTNH-Astral、CTPP、Create-Enough-Items。

## STRUCTURE
源码根 `modules/CTNH-Lib/src/main/java/`（括号内为该域 Java 文件数）

```text
com/ctnhlang/ (11)
├── CN, EN, Lang, LangFactory, Key, Prefix, Suffix, Domain, Category, IgnoreLang
└── langprovider/LangKeyBuilder
tech/vixhentx/mcmod/ctnhlib/ (48)
├── CTNHLib.java
├── api/         (3)  CTNHValues, CrossParallelRecipeLogic, ICrossParallelRecipeLogicMachine
├── client/      (7)  ClientProxy；ponder/{CTNHPonderLang, CTNHPonderSceneBuilder, CTNHPonderTagHelper}；
│                     render/ColorData；render/highlight/{HighlightHandler, HighlightRender}
├── command/     (3)  CTNHCommands, CTNHCommandChatHelper, CTNHCommandInspector
├── common/      (2)  CommonProxy, MultiblockHelper
├── data/        (3)  CTNHDynamicDataPack, DataFilterPack, recipe/RecipeRemovalHelper
├── langprovider/ (2) Lang, LangProcessor
├── mixin/       (4)  GTRecipesMixin, MachineBuilderMixin, RecipeManagerApplyMixin, TMRVMixin
├── network/     (1)  packets/BlockHighlightPacket
├── registrate/  (14) CNRegistrate, CTNHLibNetworking；builders/*（10）；data/ProviderTypes；lang/RegistrateCNLangProvider
└── utils/       (8)  AllBuilder2, ChunkList, CodecBuilder, EnvUtils, ExtendNbtUtils,
                     InfiniteMeteorTerrain, LockIdentityHashMap, MachineUtils
src/main/resources/ctnhlib.mixins.json
```

`jade/` 域已于 f9951f9「移除gt jade相关」删除（当前 0 个 Java 文件），不要在 Lib 内重建 Jade provider 排序。

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| mod 入口 / 代理 | `CTNHLib`, `common/CommonProxy`, `client/ClientProxy` |
| 跨并行配方逻辑与共享常量 | `api/CrossParallelRecipeLogic`, `api/ICrossParallelRecipeLogicMachine`, `api/CTNHValues` |
| 动态数据包 / 静态包过滤 / 配方移除 | `data/CTNHDynamicDataPack`, `data/DataFilterPack`, `data/recipe/RecipeRemovalHelper` |
| Mixin 补丁 | `mixin/{RecipeManagerApplyMixin, GTRecipesMixin, MachineBuilderMixin, TMRVMixin}` |
| Registrate 与构建器 | `registrate/CNRegistrate`, `registrate/builders/*` |
| 双语 lang 管线 | `com/ctnhlang/*`, `langprovider/{Lang, LangProcessor}`, `registrate/lang/RegistrateCNLangProvider`, `registrate/data/ProviderTypes` |
| 网络与方块高亮 | `registrate/CTNHLibNetworking`, `network/packets/BlockHighlightPacket`, `client/render/highlight/*` |
| 共享命令 | `command/CTNHCommands`, `command/CTNHCommandInspector`, `command/CTNHCommandChatHelper` |
| 客户端 Ponder 框架 | `client/ponder/{CTNHPonderSceneBuilder, CTNHPonderLang, CTNHPonderTagHelper}` |
| 通用工具 | `utils/*` |
| Mixin 配置 | `src/main/resources/ctnhlib.mixins.json` |

## DOMAIN GUIDE ROUTING
| Source area | Guide | Read before |
|-------------|-------|-------------|
| `api/**` | `ctnh-docs/references/CTNH-Lib/api/AGENTS.md` | 新增共享常量或跨并行配方逻辑 |
| `client/**` | `ctnh-docs/references/CTNH-Lib/client/AGENTS.md` | 改高亮渲染 / Ponder 场景基类 / tag 助手 |
| `command/**` | `ctnh-docs/references/CTNH-Lib/command/AGENTS.md` | 改 `/ctnh` 检查命令或 `showores` 开发工具 |
| `common/**` | `ctnh-docs/references/CTNH-Lib/common/AGENTS.md` | 改 Lib 引导、数据包注册或辅助物品 |
| `data/**` | `ctnh-docs/references/CTNH-Lib/data/AGENTS.md` | 改动态包 / 过滤 / 配方移除 |
| `com/ctnhlang/**`, `langprovider/**` | `ctnh-docs/references/CTNH-Lib/langprovider/AGENTS.md` | 改 lang 注解或注解处理器 |
| `mixin/**` | `ctnh-docs/references/CTNH-Lib/mixin/AGENTS.md` | 加改 mixin 或 mixins json |
| `network/**` | `ctnh-docs/references/CTNH-Lib/network/AGENTS.md` | 加改共享数据包 |
| `registrate/**` | `ctnh-docs/references/CTNH-Lib/registrate/AGENTS.md` | 加共享构建器 / registrate 助手 |
| `utils/**` | `ctnh-docs/references/CTNH-Lib/utils/AGENTS.md` | 复用共享工具而非另起实现 |

## CONVENTIONS
- **GTM 动态包**：GT/GMT 配方经 `*GTAddon.addRecipes()` 注册为运行时动态数据包（`GTDynamicPackContents` / CTNH-Lib `CTNHDynamicDataPack`），`runData` 对其**不产出 JSON**；静态 `src/generated/resources` 只含 tags/lang/models/worldgen/非 GT 配方。验证方式为游戏内或 `ConfigHolder.dev.dumpRecipes`。
- **注册对象优先**：引用物品/方块/流体**必须**使用静态注册对象（`GTMaterials.Iron`, `CTNHBlocks.MY_BLOCK`, `TagPrefix.ingot`, `AEItems.X`, `CBBlocks.X`, `CEItems.X`, `CMItems.X`, `CABlocks.X`, `CTPPBlocks.X`），**禁止** `ResourceLocation` 字符串解析 + `ForgeRegistries` 查找；字符串 ID 仅限无注册对象的场景（上游 mod 专属 ID、配方 ID、tag key、维度 ID）。
- **移除注册集中**：`data/recipe/RecipeRemovalHelper` 独占 `FILTERS`；`remove()` / `clear()` / `getFilters()` 是唯一入口，模块重载规则前先 `clear()`。
- **静态包过滤集中**：`data/DataFilterPack` 的 `FILTERED` 与 `removeRecipe/removeRecipeType/removeData` 是静态数据包剔除的唯一入口，由 `mixin/GTRecipesMixin` 在 `GTRecipes.recipeRemoval` HEAD 清空。
- **注册与 lang 统一走 `CNRegistrate`**：物品/方块/实体/机器/配方类型/材料全部经 `registrate/builders/*`；双语条目经 `com.ctnhlang` 注解 + `LangProcessor`，或 `CNRegistrate.genLang/addRawLang`。
- **`ProviderTypes.CNLANG` 的注册 id 必须是 `ctnhlib_cnlang`**（裸 `cnlang` 会被第三方 mod `ae2pw` 的同名拷贝顶掉，静默产出空 `zh_cn.json`）。
- **新增 mixin 必须登记** `src/main/resources/ctnhlib.mixins.json` 的 `mixins`（或 `client`）数组。
- **Lib 不做游戏内容**：模块专属命令、包、构建器、Ponder 场景、Jade provider 一律放所属模块。

## ANTI-PATTERNS
- 用字符串 ID + `ForgeRegistries` 查找代替已存在的静态注册对象。
- 期望 `runData` 产出 GT 动态配方 JSON 并据此验证配方。
- 在模块内重复实现 `RecipeRemovalHelper` / `DataFilterPack` 的移除逻辑。
- 在 Lib 内加模块专属命令、数据包、构建器或 Ponder 场景。
- 新增 mixin `.java` 却不登记 `ctnhlib.mixins.json`。
- 把已删除的 `jade/GTProvidersRegistrar` / `jade/JadePriorityManager` 重新加回 Lib。

## COMMANDS
```bash
./gradlew :modules:CTNH-Lib:build            # 编译 + 校验
./gradlew :modules:CTNH-Lib:spotlessApply    # 格式化（提交前必跑）
./gradlew :modules:CTNH-Lib:runData          # 数据生成；Lib 无 GatherDataEvent 入口，通常不产出内容
./gradlew :modules:CTNH-Lib:runClient        # 游戏内验证高亮 / Ponder / 命令
```
- 新增 mixin 后确认 `src/main/resources/ctnhlib.mixins.json` 已登记。
- lang 生成验证放到消费模块（其 `*Datagen` 调 `REGISTRATE.addLangProcessor()`）。

## SCOPE
仅 CTNH-Lib 共享代码。无游戏内容、无模块专属配方与注册对象。

## READ WHEN
- 改跨模块工具类、动态包、配方移除过滤或 Mixin。
- 加共享 registrate 构建器或双语 lang 条目。
- 判断某段逻辑该放 Lib 还是所属功能模块。

## SOURCE OF TRUTH
- 源码：`modules/CTNH-Lib/src/main/java`（`tech/vixhentx/mcmod/ctnhlib` + `com/ctnhlang`）
- 资源与 mixin 配置：`src/main/resources/`（`ctnhlib.mixins.json`、`assets/ctnhlib/lang/{en_us,zh_cn}.json`）
- 代码优先于文档。

## WORKFLOW
1. 先读本文件与对应域的 `AGENTS.md`（见 DOMAIN GUIDE ROUTING）。
2. 改动落在正确域：注册/构建器 → `registrate/`，配方过滤 → `data/`，字节码补丁 → `mixin/`，共享工具 → `utils/`。
3. 新增 mixin 类登记 `ctnhlib.mixins.json`。
4. 跑 `spotlessApply` 与 `:modules:CTNH-Lib:build`；行为改动在消费模块内验证。
5. 结构变化（新增/删除类、新子包）时同步更新本文件与对应域文档。
