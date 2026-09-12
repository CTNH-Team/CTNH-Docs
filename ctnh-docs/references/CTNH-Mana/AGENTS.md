# CTNH-MANA MODULE

## OVERVIEW
CTNH-Mana 是 CTNH 的魔法内容模块，包根 `com.magicbee.ctnhmana`，mod id `ctnhmana`，333 个 Java 文件。承载 Botania / Blood Magic / Ars Nouveau / Apotheosis 集成、魔力驱动的 GTCEu 多方块、血魔法仪式适配、自定义物品与生物效果、客户端 Caduceus 轮盘 UI，以及「虚境(Zenith)」入侵事件系统。入口类：`CTNHMana`（`@Mod`）、`CTNHManaGTAddon`（`@GTAddon`，`addRecipes` / `removeRecipes`）、`CMConfig`；代理为 `common/CommonProxy` 与 `client/ClientProxy`（`ClientProxy extends CommonProxy`）。

## STRUCTURE
源码根 `modules/CTNH-Mana/src/main/java/com/magicbee/ctnhmana/`（括号内为该域 Java 文件数）

```
com.magicbee.ctnhmana/                        # 333 个 Java 文件
├── CTNHMana / CTNHManaGTAddon / CMConfig     # mod 入口、GT addon、配置
├── api/        (35)  效果(16)、配方条件(4)、自定义配方逻辑(6)、图案、机器 trait(3)、Botania 网络扩展
├── client/     (41)  代理、轮盘(4)、模型(8)、Ponder(4+3)、渲染(17+1)、Zenith 客户端镜像
├── common/     (125) 代理、多方块(31)、物品(8 子包)、实体(5+ai8+nav2+proj3)、GUI(7)、仓室(5+3)、仪式(2+6)
├── data/       (55)  CMDatagen、ManaData、配方(35)、builder(11)、lang(3)、tags(2)、materials(1)
├── event/      (16)  EventHandler(MOD 总线空标记) + 13 个 Forge 处理器 + 按键绑定 + Boss 池
├── integration/(3)   emi(1)、jade(2)
├── mixin/      (18)  ae2(2)、ars(4)、bloodmagic(4)、botania(6)、emi(1)、minecraft(1)
├── networking/ (7)   CMNetworking + 6 个包
├── registry/   (27)  19 个根类、items(1)、multiblock(5)、sounds(2)
└── utils/      (3)   CTNHManaUtils、EnvUtils、ModUtils
```

细则：
- `common/` 子包：`blockentity/{flower(7), machine(1)}`、`blocks(5)`、`capability(1)`、`entity/{ai(8), navigation(2), projectile(3)}`、`event/zenith(5)`、`gui(7)`、`item/{bloodmagicjade, bosssummoner, caduceus, dungeon, equipment, manafuelstick, manamachineupgrade, rune}`、`machine(3)`、`multiblock(31)`、`parts/{ManaHatches(3)}`、`ritual(2)`、`ritualtypes(6)`。
- `data/recipe/` 顶层 35 个文件 = `CTNHManaGTAddon.addRecipes()` 直接调用的 33 个配方类 + `ManaRecipeRemoval` + 由 `SalvagingRecipes` 间接调用的 `RuneSalvagingRecipes`。
- Mixin 配置 `src/main/resources/ctnhmana.mixins.json`：17 条目，refmap `mixins.ctnhmana.refmap.json`；`mixin/ars/StoredItemStackMixin` 源码已整体注释、未注册。

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| mod 入口 / GT addon / 配置 | `CTNHMana.java`, `CTNHManaGTAddon.java`, `CMConfig.java` |
| 生命周期与注册编排 | `common/CommonProxy.java`（机器/配方类型/条件泛型监听、材质、物品/方块/BE、创造栏、粒子、音效、网络、datagen、配置） |
| 客户端编排 | `client/ClientProxy.java`（动态渲染注册、shader、物品属性、Ponder 插件） |
| GT 配方增删 | `CTNHManaGTAddon.addRecipes()` → `data/recipe/*`；`removeRecipes()` → `data/recipe/ManaRecipeRemoval` + CTNH-Lib `RecipeRemovalHelper` |
| 注册对象 | `registry/CM*`（`CMRegistrate`, `CMItems`, `CMBlocks`, `CMBlockEntities`, `CMEntities`, `CMMachines`, `CMMultiblockMachines`, `CMRecipeTypes`, `CMRecipeConditions`, `CMMobEffects`, `CMMaterials`, `CMTags`, `GTMaterialAddon` ...） |
| 多方块与机器 | `common/multiblock/*`（31：`ManaMultiBlockMachine`, `BaseManaMultiBlockMachine`, `ManaReactor`, `HellForgeMachine`, `MysticSpire`, `ZenithMatrixMachine`, `EternalGarden` ...）、`common/machine/*`、`common/parts/*`、`registry/multiblock/*` |
| 机器 trait 契约 | `api/machine/trait/{BTManaContainerTrait, MysticSpireManaTrait, ExtendedControlBusCircuitTrait}` |
| 数据生成 / 静态数据 | `data/CMDatagen.java`, `data/ManaData.java`, `data/recipe/*`, `data/tags/*`, `data/lang/*` |
| 客户端渲染 / 模型 / Ponder | `client/render/*`, `client/model/*`, `client/ponder/*` |
| 网络与集成 | `networking/packets/CMNetworking.java`, `integration/{emi, jade}/*` |
| Mixin 补丁 | `mixin/*` + `api/mixin/IBloodAltarLogic.java` |

## DOMAIN GUIDE ROUTING
| Source area | Guide | Read before |
|-------------|-------|-------------|
| `api/**` | `ctnh-docs/references/CTNH-Mana/api/AGENTS.md` | 新增效果 / 配方条件 / 自定义配方逻辑 / 机器 trait |
| `client/**` | `ctnh-docs/references/CTNH-Mana/client/AGENTS.md` | 改动渲染、模型、轮盘界面或 Ponder 场景 |
| `common/**` | `ctnh-docs/references/CTNH-Mana/common/AGENTS.md` | 新增或修改多方块、机器、仓室、物品、实体、GUI、仪式 |
| `data/**` | `ctnh-docs/references/CTNH-Mana/data/AGENTS.md` | 改动任意 `data/recipe/*`、配方移除、builder、tags 或 lang |
| `event/**` | `ctnh-docs/references/CTNH-Mana/event/AGENTS.md` | 新增 Forge 事件处理器或效果副作用 |
| `integration/**` | `ctnh-docs/references/CTNH-Mana/integration/AGENTS.md` | 对接 EMI / Jade |
| `mixin/**` | `ctnh-docs/references/CTNH-Mana/mixin/AGENTS.md` | 打补丁到 Botania / Blood Magic / Ars Nouveau / AE2 / EMI / MC |
| `networking/**` | `ctnh-docs/references/CTNH-Mana/networking/AGENTS.md` | 新增或修改数据包 |
| `registry/**` | `ctnh-docs/references/CTNH-Mana/registry/AGENTS.md` | 新增任何注册对象（物品/方块/BE/机器/配方类型/效果/音效） |
| `utils/**` | `ctnh-docs/references/CTNH-Mana/utils/AGENTS.md` | 复用或新增工具类 |

## CONVENTIONS
- **GTM 动态包**：GT/GMT 配方经 `CTNHManaGTAddon.addRecipes()` 注册为运行时动态数据包（`GTDynamicPackContents` / CTNH-Lib `CTNHDynamicDataPack`），`runData` 对其**不产出 JSON**；静态 `src/generated/resources` 只含 tags/lang/models/worldgen/非 GT 配方。验证方式为游戏内或 `ConfigHolder.dev.dumpRecipes`。
- **注册对象优先**：引用物品/方块/流体**必须**用静态注册对象（`CMItems.X`, `CMBlocks.X`, `CMMaterials.X`, `GTMaterials.*`, `TagPrefix.ingot`, `AEItems.X`, `CBBlocks.X`, `CEItems.X`, `CABlocks.X`, `CTPPBlocks.X`），**禁止** `ResourceLocation` 字符串解析 + `ForgeRegistries` 查找；字符串 ID 仅限无注册对象的场景（上游 mod 专属 ID、配方 ID、tag key、维度 ID）。
- **命名空间**：包名固定 `com.magicbee.ctnhmana`（不是 `com.moguang.ctnhmana`），注册对象统一 `CM` 前缀。
- **配方移除走 CTNH-Lib**：`ManaRecipeRemoval.init()` 用 `RecipeRemovalHelper.remove(new RemoveFilter().id(...))` 批量删除精确 ID；类型/正则删除写在 `CTNHManaGTAddon.removeRecipes(Consumer<ResourceLocation>)` 内；本模块不得自建 `Consumer<ResourceLocation>` 删除循环或 `DataFilterPack`。
- **重注册改命名空间**：被删除配方即使重新注册也会被过滤，需经 `CTNHManaGTAddon.changeId(...)` 把 ID 改到 `ctnhmana` 命名空间。
- **双语文本**：所有文案走 CTNH-Lib lang provider（`com.ctnhlang.CN` / `com.ctnhlang.EN` 注解或 `Lang#translate()`），不得硬编码中文文案。
- **魔改四面同步**：改动 Blood Magic / Botania / Ars Nouveau / Apotheosis 集成面时，同时检查配方 builder（`data/recipe/builder/<mod>/`）、mixin（`mixin/<mod>/`）、集成（`integration/`）、客户端包四处。
- **注册编排集中**：全部注册流程写在 `common/CommonProxy` 与各 `CM*` 注册类；`event/EventHandler` 只是 MOD 总线空标记类，不承载注册逻辑。

## ANTI-PATTERNS
- 恢复 `data/recipe/RecipeRemoval` 或使用 `DataFilterPack.removeRecipe*` / `Consumer<ResourceLocation>` 删除循环。
- 在已有静态注册对象时用 `ResourceLocation.parse` + `ForgeRegistries` 查找。
- 期望在 `src/generated/resources` 下找到 `addRecipes()` 产出的 GT 配方 JSON。
- 把生命周期/注册编排塞回 `event/EventHandler`（空标记类）或 `CTNHMana` 入口类。
- 在魔力容器上重新引入 BlockEntity 侧魔力字段，或让 `ManaMultiBlockMachine` 自己持有 `BTManaContainerTrait`（仓室 `ManaHatch` 才是归属方）。
- 手改 `src/generated/resources`、`build/`、run 目录产物。

## COMMANDS
```bash
./gradlew :modules:CTNH-Mana:build           # 编译 + 校验
./gradlew :modules:CTNH-Mana:spotlessApply   # 格式化（提交前必跑）
./gradlew :modules:CTNH-Mana:runData         # 数据生成（lang/tags/models/sounds；不含 GT 动态配方）
./gradlew :modules:CTNH-Mana:spotlessCheck   # 仅校验格式
```
GT 配方与配方移除必须在游戏内验证，或用 `ConfigHolder.dev.dumpRecipes` 转储。

## SCOPE
仅覆盖 Mana 的魔法系统、多方块/机器、物品与实体、效果、集成与兼容 Mixin。核心 GT/registrate 基础设施与跨模块共享工具归 CTNH-Core / CTNH-Lib。

## READ WHEN
- 改动 `CTNHManaGTAddon`（增删配方、移除规则、tag prefix、element）
- 改动 `data/recipe/*`、`data/recipe/builder/*`、`data/tags/*`、`data/lang/*`
- 新增注册对象、多方块、机器、仓室、物品、实体或效果
- 改动任意 `mixin/<mod>/`、`integration/` 或 `networking/packets/`
- 改动机器 trait（魔力容器、尖塔魔力、扩展总成电路）

## SOURCE OF TRUTH
- 源码：`modules/CTNH-Mana/src/main/java/com/magicbee/ctnhmana/`
- 资源与 mixin 配置：`modules/CTNH-Mana/src/main/resources/`（`ctnhmana.mixins.json`、`META-INF/mods.toml`）
- 生成物：`modules/CTNH-Mana/src/generated/resources/`
- 本目录层级文档：`ctnh-docs/references/CTNH-Mana/**`

## WORKFLOW
1. 先读本文件与对应域的 `AGENTS.md`（见 DOMAIN GUIDE ROUTING）。
2. 改动落在正确域：注册 → `registry/`，机器/多方块 → `common/multiblock/`，配方 → `data/recipe/`，渲染 → `client/render/`，事件 → `event/`。
3. 新增 GT 配方时先在 `CTNHManaGTAddon.addRecipes()` 接线，被删配方的重注册走 `changeId(...)`。
4. 修改后跑 `spotlessApply` 与 `:modules:CTNH-Mana:build`；datagen/lang/Ponder 改动跑 `runData`。
5. GT 配方与配方移除改动在游戏内验证，不要依赖 `runData` 产物。
6. 结构变化（新增/删除类、新子包、mixin 条目增减、文件数变化）时同步更新本文件与对应域文档。