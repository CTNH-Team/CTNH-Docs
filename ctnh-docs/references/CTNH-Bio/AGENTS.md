# CTNH-BIO MODULE

## OVERVIEW
CTNH-Bio（包 `com.moguang.ctnhbio`，mod id `ctnhbio`）是 CTNH 的生物机械模块：Biomancy 风格的活体机器（宿主实体 + 活体多方块）、生物 recipe capability（实体 / 模型 / 营养 / Cogni 物品）、生物配方与资源生成、意识装配机 Ponder 思索场景，以及针对上游 mod 的 Mixin 兼容补丁。共 177 个 Java 文件。入口类：`CTNHBio`（mod 主类）、`CTNHBioGTAddon`（GT addon：配方 capability / 元素 / 配方 / 配方移除）、`CBConfig`（配置）；代理为 `CommonProxy` / `ClientProxy`。

## STRUCTURE
源码根 `modules/CTNH-Bio/src/main/java/com/moguang/ctnhbio/`（括号内为该域 Java 文件数）

```
ctnhbio/
├─ CTNHBio.java / CTNHBioGTAddon.java / CBConfig.java   入口 / GT addon / 配置
├─ api/         (61) 活体机器基类与 block / blockentity / entity / item 层级、recipe capability、
│                   实体与模型原料、属性算子、营养序列化
├─ client/      (19) ClientProxy，model/（7），renderer/（5），ponder/（5），Text/ModelOutputLine
├─ common/      (7)  CommonProxy，condition/，item/，recipe/，serum/
├─ data/        (28) CBDatagen、CBElements，lang/，loot/，materials/，recipe/，tags/
├─ event/       (3)  EventHandler、ForgeEventHandler、TransformManager
├─ integration/ (7)  emi/，jade/，jei/，xei/
├─ machine/     (7)  braininavat/，bioobservation/，greatflesh/，multiblock/（含 part/）
├─ mixin/       (18) ali/，biomancy/，create/，emi/，gtm/，hostilenetworks/
├─ registry/    (17) CBRegistrate、CBItems、CBBlocks、CBEntities、CBMachines、CBMultiblocks、
│                   CBMaterials、CBMaterialItems、CBMobEffects、CBSerums、CBSoundEntries、
│                   CBTags、CBRecipeTypes、CBRecipes、CBRecipeCapabilities、
│                   CBRecipeConditions、CBCreativeModeTabs
└─ utils/       (7)  CBMachineNames、CBRecipeModifiers、DecomposingRecipeHandler、DespoilLootHelper、
                     IKeyPressedWithCoord、RandomUtils、VialCraftingRemainingItem
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| mod 入口 / 生命周期 | `CTNHBio.java`, `common/CommonProxy.java`, `client/ClientProxy.java` |
| 配置 | `CBConfig.java` |
| GT addon 钩子 | `CTNHBioGTAddon.java`（`initializeAddon` / `registerRecipeCapabilities` / `addRecipes` / `removeRecipes` / `registerElements`） |
| 活体机器契约 | `api/machine/BasicLivingMachine.java`, `api/machine/multiblock/WorkableLivingMultiblockMachine.java`, `api/ILivingMachine.java` |
| 活体机器实现 | `machine/braininavat/`, `machine/bioobservation/`, `machine/greatflesh/`, `machine/multiblock/` |
| 生物 recipe capability | `api/capability/recipe/`（CogniItem / Entity / Model / Nutrient），注册在 `registry/CBRecipeCapabilities.java` |
| 实体 / 模型原料与属性匹配 | `api/recipe/ingredient/`, `api/recipe/matcher/PropertyOperators.java` |
| 注册对象 | `registry/`（`CBItems`, `CBBlocks`, `CBEntities`, `CBMachines`, `CBMultiblocks`, `CBMaterials`, `CBRecipeTypes` 等） |
| 配方与数据生成 | `data/recipe/`, `data/CBDatagen.java` |
| 磨碎配方 | `common/recipe/MobCrushingRecipe.java`, `common/recipe/MobCrushingRecipeManager.java`, `integration/jei/MobCrushingCategory.java` |
| 集成 | `integration/`（EMI / Jade / JEI / XEI） |
| 客户端思索（Ponder） | `client/ponder/`（`CTNHBioPonderPlugin` / `CTNHBioPonderScenes` / `CTNHBioPonderTags` / `CTNHBioPonderSceneBuilder` / `CogniAssembler`） |
| Mixin 补丁 | `mixin/`；配置 `src/main/resources/ctnhbio.mixins.json` |
| 通用工具 | `utils/` |

## DOMAIN GUIDE ROUTING
| Source area | Guide | Read before |
|-------------|-------|-------------|
| `api/**` | `ctnh-docs/references/CTNH-Bio/api/AGENTS.md` | 改 recipe capability / 实体与模型原料 / 机器 API 面 |
| `client/**` | `ctnh-docs/references/CTNH-Bio/client/AGENTS.md` | 改渲染器 / 模型 / 客户端文本 / Ponder 场景 |
| `common/**` | `ctnh-docs/references/CTNH-Bio/common/AGENTS.md` | 改 CommonProxy 装配 / 条件 / 通用物品 / 磨碎配方 / 血清 |
| `data/**` | `ctnh-docs/references/CTNH-Bio/data/AGENTS.md` | 改配方生成器 / lang / 掉落 / 材料 / tag |
| `event/**` | `ctnh-docs/references/CTNH-Bio/event/AGENTS.md` | 改数据生成钩子 / Forge 事件订阅 / 血肉转换 |
| `integration/**` | `ctnh-docs/references/CTNH-Bio/integration/AGENTS.md` | 改 EMI / Jade / JEI / XEI 集成 |
| `machine/**` | `ctnh-docs/references/CTNH-Bio/machine/AGENTS.md` | 改活体机器实现 |
| `mixin/**` | `ctnh-docs/references/CTNH-Bio/mixin/AGENTS.md` | 改 Biomancy / HNN / EMI / Create / GTCEu 补丁 |
| `registry/**` | `ctnh-docs/references/CTNH-Bio/registry/AGENTS.md` | 新增或修改任何注册对象 |
| `utils/**` | `ctnh-docs/references/CTNH-Bio/utils/AGENTS.md` | 复用工具类而非另起实现 |

## CONVENTIONS
- 命名空间 `com.moguang.ctnhbio`，注册对象统一 `CB` 前缀（`CBItems`, `CBBlocks`, `CBMachines` 等）。
- **GTM 动态包**：GT/GMT 配方经 `CTNHBioGTAddon.addRecipes()` 注册为运行时动态数据包（`GTDynamicPackContents` / CTNH-Lib `CTNHDynamicDataPack`），`runData` 对其**不产出 JSON**；静态 `src/generated/resources` 只含 tags/lang/models/loot_tables/非 GT 配方；验证方式为游戏内或 `ConfigHolder.dev.dumpRecipes`。
- **注册对象优先**：引用物品/方块/流体**必须**使用静态注册对象（`CBItems.X`, `CBBlocks.X`, `GTMaterials.X`, `TagPrefix.ingot`, `AEItems.X`, `CEItems.X`, `CMItems.X`, `CABlocks.X`, `CTPPBlocks.X`），**禁止** `ResourceLocation` 字符串解析 + `ForgeRegistries` 查找；字符串 ID 仅限无注册对象的场景（上游 mod 专属 ID、配方 ID、tag key、维度 ID）。
- 手写静态配方/数据 JSON 位于 `src/main/resources/data/ctnhbio/`（`mob_crushing_recipes/` 6 个生物磨碎配方，`loot_categories/despoil_loot.json`）；`src/generated/resources` 由 `:modules:CTNH-Bio:runData` 生成，不要手改。
- Mixin 覆盖 Biomancy、Hostile Neural Networks、EMI/ALI、Create、GTCEu 内部；一律按兼容补丁对待，不当通用工具使用。
- 机器 / trait / capability / Jade 的所有权边界与字段规则以 `ctnh-docs/references/_architecture/AGENTS.md` 为准（§1 边界、§2 字段、§4 capability 分层），改动机器、trait、recipe capability 或 Jade 前先读它；本文件只描述落点。

## ANTI-PATTERNS
- 把生物 recipe capability 合并进 Core；活体机器抽象归本模块所有。
- 假定所有配方 JSON 都是生成的；先确认文件在 `src/main/resources` 还是 `src/generated/resources`。
- 新增实体/模型配方匹配时绕过 `PropertyOperators` / `EntityProperties`；这两个注册表在 `CommonProxy.init()` 中显式初始化。
- despoil 战利品催化剂展示由 CTNH-Core 的 `CTNHExtraEmiPlugin` 处理（`ctnhbio:despoil_loot`）；本模块不加 `mixin/ali/EmiCompatibilityMixin`。
- 期望 `runData` 产出 GT 配方 JSON 并据此验证配方。

## COMMANDS
```
./gradlew :modules:CTNH-Bio:build
./gradlew :modules:CTNH-Bio:runData
./gradlew :modules:CTNH-Bio:spotlessCheck
```

## SCOPE
`modules/CTNH-Bio` 及其源码与资源目录：`src/main/java/com/moguang/ctnhbio/`、`src/main/resources/`、`src/generated/resources/`。

## READ WHEN
- 新增或修改活体机器、生物 recipe capability 或实体/模型原料。
- 修改 Bio 的数据生成 provider、静态数据 JSON 或 Mixin 补丁。
- 新增 Bio 注册对象（物品 / 方块 / 实体 / 机器 / 配方类型）。
- 调整 EMI / Jade / JEI / XEI 集成。
- 新增或修改客户端 Ponder 思索场景、tag 与双语文案。

## SOURCE OF TRUTH
- 注册与生命周期：`CTNHBio.java`, `CTNHBioGTAddon.java`, `common/CommonProxy.java`。
- Forge 元数据与 Mixin：`src/main/resources/META-INF/mods.toml`, `src/main/resources/ctnhbio.mixins.json`。
- 静态数据：`data/` 下的 provider 与 `src/generated/resources`，以及手写 JSON `src/main/resources/data/ctnhbio/`。
- 本目录层级文档：`ctnh-docs/references/CTNH-Bio/**`。

## WORKFLOW
1. 定位改动所属域 → 先读对应域 `AGENTS.md`（见 DOMAIN GUIDE ROUTING）。
2. 改动落在正确域：注册 → `registry/`，机器实现 → `machine/`（契约在 `api/`），配方 → `data/recipe/`，渲染 → `client/renderer/`，上游补丁 → `mixin/`。
3. 检查 GT addon 钩子顺序、`CommonProxy.init()`，以及 `PropertyOperators` / `EntityProperties` 的初始化时机。
4. 跑最窄的 Gradle 任务（`runData` 管数据、`build` 管编译），涉及运行时行为在游戏内验证。
