# CTNH-CORE CLIENT DOMAIN

## OVERVIEW
客户端引导、模型、渲染器，以及 Core 自有的 Create Ponder 场景、tags 与插件（26 个 Java 文件）。

## STRUCTURE
```text
client/
|-- ClientProxy.java           # 客户端引导（extends CommonProxy）
|-- ClientUtil.java
|-- model/                     # ModelBase, ModelDefinition, TemplateModel, TurbineRotorModel
|-- ponder/                    # CTNHCorePonderPlugin, CTNHCorePonderSceneBuilder, CTNHCorePonderScenes, CTNHCorePonderTags
|   |-- Electric/              # GregTechMultiblocks, NeutronActivator, ChemicalPlant
|   |-- Kinetic/               # Meadow, MechanicalExporter
|   |-- Misc/                  # Drum
|   |-- machine/               # NeutronSensorChange（反射改中子传感器门限/输出反转）
|   `-- example/               # ChemicalReactorUi（机器界面 Ponder 示例）
|-- renderer/                  # ArcBlockRender, AstralPlanetSpecialEffects, DynamicCasingRender, HyperPlasmaTurbineRender, MartialMoralityEyeRender, TurbineRotorRender
|-- renderer/utils/            # RenderUtils
`-- util/                      # SnowOverlayQuadOffset
```
- 流体渲染由服务端 trait `MultiblockFluidRendererTrait` 承担（在 `LargeBottleMachine` 中 attach）；本域不放 `LargeBottleRender` 这类自定义 `DynamicRender` 子类。

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| 客户端引导 | `client/ClientProxy.java`, `client/ClientUtil.java` |
| Ponder 插件/场景/tags | `client/ponder/CTNHCorePonderPlugin.java`, `CTNHCorePonderScenes.java`, `CTNHCorePonderTags.java` |
| Core Ponder 场景 | `client/ponder/Kinetic/`（Meadow, MechanicalExporter）, `client/ponder/Electric/`（GregTechMultiblocks, NeutronActivator, ChemicalPlant）, `client/ponder/Misc/`（Drum）, `client/ponder/machine/`（NeutronSensorChange） |
| 机器界面 Ponder 示例 | `client/ponder/example/ChemicalReactorUi.java`（LV 化学反应釜，用 Lib 的 `MachineUI`/`MachineUiPlacement` 演示槽位、储罐、配方与配置器开关） |
| Ponder 适配构建器 | `client/ponder/CTNHCorePonderSceneBuilder.java` |
| 模型 | `client/model/`（ModelBase, ModelDefinition, TemplateModel, TurbineRotorModel） |
| 渲染器 | `client/renderer/`（ArcBlockRender, DynamicCasingRender, HyperPlasmaTurbineRender, TurbineRotorRender, AstralPlanetSpecialEffects） |
| 客户端工具 | `client/util/SnowOverlayQuadOffset.java` |

## CONVENTIONS
- Ponder 场景用 `scene.title(sceneId, headerEn, headerCn, titleEn, titleCn)`（仅要标题时用 `title(sceneId, en, cn)`）/ `scene.showText(tick, en, cn)`，文案直接内嵌在场景文件里。
- `CTNHCorePonderSceneBuilder` 只是 Lib 共享构建器之上的 Core 适配层；可复用的构建器/文本行为留在 CTNH-Lib。
- 机器界面 Ponder 用 CTNH-Lib 的 `MachineUI`（`MachineUI.of(机器)`）与 `MachineUiPlacement` 链：`scene.showUI(MY_MACHINE_UI).at(anchor).machinePos(pos).slot(0).withItem(stack).show(200)`；`CTNHPonderSceneBuilder.showUI(MachineUI)` 转 `ui.in(this)`，`MachineUI.in(SceneBuilder)` 返回起点态 `MachineUiStart`。`ChemicalReactorUi` 是覆盖槽位、储罐、配方、输出口与配置器开关红框的完整示例。
- 一个 storyboard 可注册到多个组件：`drum/common` 经 `GTMachines` 的 8 种桶（木 / 青铜 / 钢 / 铝 / 不锈钢 / 金 / 钛 / 钨钢）共用 `Drum::Common`；`chemical_plant/common` 绑定 `GTNNMultiblocks.CHEMICAL_PLANT` 的 7x7x7 塔体，绑定组件与 storyboard 一一对应。
- Ponder 注册发生在 `ClientProxy.onClientSetupEvent()`；客户端 datagen 的语言提取在 `CommonProxy.gatherData()` 中经 `CTNHPonderLang.init(new CTNHCorePonderPlugin())` 完成。
- 引用物品/方块/流体**必须**使用静态注册对象，**禁止** `ResourceLocation` 字符串解析 + `ForgeRegistries` 查找，除非该对象不存在。

## ANTI-PATTERNS
- 把 Core 的 Ponder 场景/tags/插件搬进 CTNH-Lib；只有共享构建器属于 Lib。
- 让仅客户端类从 common 构造路径可达。
- 重新引入 `LargeBottleRender`；应使用 `MultiblockFluidRendererTrait`。

## SCOPE
适用于 `src/main/java/io/github/cpearl0/ctnhcore/client` 及其子包。

## READ WHEN
- 新增或修改 Core Ponder 场景、tags 或客户端渲染管线。
- 改动 Core 模型/图层注册。

## SOURCE OF TRUTH
- `client/ClientProxy.java`（引导）、`client/ponder/CTNHCorePonderPlugin.java`（场景/tag 注册）。
- Ponder 语言提取：CTNH-Lib `CTNHPonderLang`，由 `common/CommonProxy.gatherData()` 接线。

## WORKFLOW
1. 写场景前先读 `references/CTNH-Lib/client/AGENTS.md` 的共享 Ponder 构建器指南。
2. 在插件里加场景/tag 注册；可复用文本辅助留在 Lib。
3. Ponder 文案改动后跑 `:modules:CTNH-Core:runData`，再跑 `spotlessCheck`。
