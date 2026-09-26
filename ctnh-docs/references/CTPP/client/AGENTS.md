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
|   `-- kinetic/               # BigDam, KineticGenerator, KineticHatch, SmashingFactory, WindmillControlCenter
|-- renderer/                  # CTPPBeamRenderTypes, CTPPToolboxCurioRenderer, CTPPToolboxRenderer, CTPPWireRenderTypes,
|                              EmitterBeamRenderer, GTWireCutterRenderer, VoltageTerminalRenderer
|-- terminal/                  # TerminalClientSelection, TerminalClientSelectionEvents
`-- toolbox/                   # CTPPToolboxClientState, CTPPToolboxKeyHandler, CTPPToolboxOverlay,
                               CTPPToolboxRadialScreen, CTPPToolboxScreen
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| 客户端代理 | `client/ClientProxy.java` |
| Ponder 插件 / 场景 / 标签 | `client/ponder/`（10 个类；`electric/` + `kinetic/` 两组场景） |
| 渲染器 | `client/renderer/`（7 个：工具箱、线剪、接线柱、发射器光束，以及两套 RenderType 常量） |
| 顶层 Visual / 渲染 | `client/{CarbonBrushesRenderer, CarbonBrushesVisual, GeneratorCoilRenderer, GeneratorCoilVisual, SplitShaftVisual}` |
| 方块实体渲染 | `client/KineticMachineBlockEntityRenderer.java` |
| 工具箱 UI | `client/toolbox/`（5 个类：客户端状态、按键、叠加层、轮盘界面、主界面） |
| 接线柱客户端选线 | `client/terminal/{TerminalClientSelection, TerminalClientSelectionEvents}.java` |
| 提示 tooltip | `client/MagnetTooltipHandler.java`, `client/TerminalWireTooltipHandler.java` |
| 部件模型 | `client/CTPPPartialModels.java` |

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
