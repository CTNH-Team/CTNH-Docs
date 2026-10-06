# CTPP CLIENT DOMAIN

## OVERVIEW
CTPP 的客户端侧（34 个 Java 文件）：`ClientProxy`、Ponder 插件/场景/标签、方块与实体渲染器、工具箱 UI、接线柱选线，以及顶层 Visual 类。

## STRUCTURE
```text
client/
|-- ClientProxy.java, CTPPPartialModels.java
|-- CarbonBrushesRenderer.java, CarbonBrushesVisual.java, GeneratorCoilRenderer.java, GeneratorCoilVisual.java
|-- KineticMachineBlockEntityRenderer.java, MagnetTooltipHandler.java, SplitShaftVisual.java
|-- TerminalWireTooltipHandler.java
|-- ponder/                    # CTPPPonderPlugin, CTPPPonderSceneBuilder, CTPPPonderScenes, CTPPPonderTags
|   |-- electric/              # CarbonBrushes
|   `-- kinetic/               # BigDam（bigdam/common：Common + Work）, KineticGenerator, KineticHatch, SmashingFactory, WindmillControlCenter
|-- renderer/                  # CTPPBeamRenderTypes, CTPPToolboxCurioRenderer, CTPPToolboxRenderer, CTPPWireRenderTypes,
|                              EmitterBeamRenderer, GTWireCutterRenderer, VoltageTerminalRenderer
|-- terminal/                  # TerminalClientSelection, TerminalClientSelectionEvents
`-- toolbox/                   # CTPPToolboxClientState, CTPPToolboxKeyHandler, CTPPToolboxOverlay,
                               CTPPToolboxRadialScreen, CTPPToolboxScreen
```
- storyboard 按绑定组件注册，一个 storyboard 可提供多段场景方法（`bigdam/common` 含 `Common` 与 `Work`）；映射见 PONDER SCENES。

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| 客户端代理 | `client/ClientProxy.java` |
| Ponder 插件 / 场景 / 标签 | `client/ponder/`（10 个类；`electric/` 与 `kinetic/` 两组场景） |
| Ponder 场景注册（storyboard → 场景方法 + tag） | `client/ponder/CTPPPonderScenes.java`, `client/ponder/CTPPPonderTags.java` |
| 机器界面演示（`MachineUI`） | `client/ponder/kinetic/`：流体输入仓（`BigDam` / `KineticGenerator` / `WindmillControlCenter`）与物品输入/输出总线（`SmashingFactory`） |
| 风车控制中心结构与规则 | `client/ponder/kinetic/WindmillControlCenter.java`, `common/machine/multiblock/windmillController/WindMillControlMachine.java` |
| 渲染器 | `client/renderer/`（7 个：工具箱、线剪、接线柱、发射器光束，以及两套 RenderType 常量） |
| 顶层 Visual / 渲染 | `client/{CarbonBrushesRenderer, CarbonBrushesVisual, GeneratorCoilRenderer, GeneratorCoilVisual, SplitShaftVisual}` |
| 方块实体渲染 | `client/KineticMachineBlockEntityRenderer.java` |
| 工具箱 UI | `client/toolbox/`（5 个类：客户端状态、按键、叠加层、轮盘界面、主界面） |
| 接线柱客户端选线 | `client/terminal/{TerminalClientSelection, TerminalClientSelectionEvents}.java` |
| 提示 tooltip | `client/MagnetTooltipHandler.java`, `client/TerminalWireTooltipHandler.java` |
| 部件模型 | `client/CTPPPartialModels.java` |

## PONDER SCENES
storyboard 位于 `src/main/resources/assets/ctpp/ponder/<scene>/common.nbt`；`CTPPPonderScenes.register()` 把 storyboard 绑到机器/方块组件与 tag，`PonderIndex.addPlugin(new CTPPPonderPlugin())` 在 `ClientProxy.onClientSetup()` 注册，客户端 lang 提取经 `CommonProxy.gatherData()` 的 `CTNHPonderLang.init(new CTPPPonderPlugin())`。

| Storyboard | 绑定组件 | 场景方法 | 演示要点 |
|------------|----------|----------|----------|
| `bigdam/common` | `CTPPMultiblockMachines.BIG_DAM` | `BigDam::Common`、`BigDam::Work` | 主方块、终端一键放置、12 组水车、应力输出仓数量、流体输入仓灌润滑油 |
| `smashing_factory/common` | `CTPPMultiblockMachines.SMASHING_FACTORY` | `SmashingFactory::Common` | 主方块、终端放置、粉碎轮朝向修正、应力接入、机械升级仓、物品输入/输出总线 |
| `kinetic_generator/common` | `CTPPMultiblockMachines.KINETIC_GENERATOR` | `KineticGenerator::Common` | 主方块、磁铁与线圈、应力输入仓、机械升级仓、流体输入仓灌润滑油、能量输出仓 |
| `windmill_control_center/common` | `CTPPMultiblockMachines.WINDMILL_CONTROL_CENTER` | `WindmillControlCenter::Common` | 自带风车轴承与转子、流体输入仓灌润滑油、应力输出仓、机械升级仓、周围风车轴承、冲突检测 |
| `kinetic_hatch/common` | 全部 `CTPPMachines.KINETIC_INPUT_BOX` / `KINETIC_OUTPUT_BOX` 等级 | `KineticHatch::Common` | 等级与每级 4 倍应力 |
| `carbonbrushes/common` | `CTPPMachines.CARBON_BRUSHES` + `CTPPBlocks.GENERATOR_COIL` | `CarbonBrushes::ponder` | 碳刷与发电线圈 |

- 机器界面演示经 CTNH-Lib `MachineUI.of(...)` 建门面；`scene.showUI(ui).at(anchor).machinePos(pos)` 指定界面展示位置与对应机器，再链式写入流体 `tank(0).withFluid(stack, delay)` 或物品 `slot(0).withItem(stack, delay)`，以 `show(ticks)` 落地。
- `BigDam` / `KineticGenerator` / `WindmillControlCenter` 共用 `MachineUI.of(GTMachines.FLUID_IMPORT_HATCH[GTValues.LV]).scale(0.6f)` 演示流体输入仓：`tank(0).withFluid(new FluidStack(GTMaterials.Lubricant.getFluid(), 1000), 20)`。
- `SmashingFactory` 用 `MachineUI.of(GTMachines.ITEM_IMPORT_BUS[GTValues.LV])` 与 `MachineUI.of(GTMachines.ITEM_EXPORT_BUS[GTValues.LV])`，`slot(0).withItem(...)` 演示入料与取成品。
- `WindmillControlCenter` storyboard size `[21, 27, 19]`：主方块 `(10,1,7)`、外壳 `x5..15 y1..5 z7..17`、屋顶风车轴承 `(10,5,12)`、转子（线性底盘 + 羊毛）`x5..15 y6..26 z7..17` 绕 `(10,5,12)` 竖直轴旋转；示范风车轴承 `(3,1,3)` 与 `(17,1,3)`，5x5 十字叶片在 `y2..3`。
- `WindMillControlMachine` 规则：`getMaxControlledSize() = tier * 4 + 4`（机械升级仓决定 `tier`）；主方块 32 格半径内的风车轴承按 `|generatedSpeed| × 512 su` 累加进 `TotalOutput`，`efficiency = min(windmillAround.size(), getMaxControlledSize())`；`LEGAL_DISTANCE = 64` 内存在另一个控制中心时 `hasConflictingController`，配方输出与转速归零；转速取 `min(sqrt((512 + TotalOutput) × efficiency / 512), AllConfigs.server().kinetics.maxRotationSpeed)`。
- `WindmillControlRecipes`：润滑油输入 25 mB、`duration(200)`（10 秒）、`outputStress(512)`。

## CONVENTIONS
- 客户端类不得进入 common 的构造路径；`CTPP.java` 经 `DistExecutor` 只在客户端创建 `ClientProxy`。
- Ponder 场景经 `CTNHPonderLang.init(new CTPPPonderPlugin())` 在 `CommonProxy.gatherData()` 的 `includeClient()` 分支做 lang 提取。
- 方块实体渲染注册在 `registry/CTPPBlockEntities.java` 的对应条目上，不在 `client/` 内自行注册。
- 接线柱线缆几何必须调用 `api/terminal/TerminalWireGeometry`，渲染器内不重复实现。

## ANTI-PATTERNS
- 把渲染逻辑写进机器实现类。
- 在客户端渲染器中重算线缆下垂/半径，而非调用 `TerminalWireGeometry`。
- 在 `client/` 中直接引用 `common/` 的服务端专用入口（`CommonProxy`、`CTPPRegistration`）。

## SCOPE
适用于 `src/main/java/com/mo_guang/ctpp/client` 及其子包。

## READ WHEN
- 改动 CTPP 的 Ponder 场景、标签、渲染器、tooltip 或工具箱 UI。
- 改动接线柱客户端的选线与预览。

## SOURCE OF TRUTH
- `client/ponder/` 各类与其注册站点（`CTPPPonderPlugin`）。
- `client/renderer/` 各类与 `registry/CTPPBlockEntities.java` 中的渲染器绑定。

## WORKFLOW
1. 先确认 Ponder / 渲染器的注册连线（`CTPPPonderPlugin`、方块实体注册）。
2. 跑 `:modules:CTPP:build`；有条件时进游戏验证观感与交互。
