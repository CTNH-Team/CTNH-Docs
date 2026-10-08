# CTNH-LIB CLIENT DOMAIN

## OVERVIEW
客户端共享基础设施（33 个 Java 文件）：`ClientProxy` 引导、方块高亮渲染、共享 Ponder 框架（场景基类 / lang 抽取 / tag 助手 / 机器 UI 栈 / 思索内「查看 UI 详情」按钮）。

## STRUCTURE
```text
client/
├── ClientProxy.java
├── ponder/                    # ButtonRow, CTNHPonderLang, CTNHPonderSceneBuilder, CTNHPonderTagHelper,
│   │                          # FrameGuard, PonderUiButtons
│   ├── machine/               # MachineEdit, MachineEditInstruction, MachineEdits, CoverChange,
│   │                          # AutoOutputChange, WorkingModelChange, ParallelChange, MaintenanceChange
│   └── ui/                    # MachineUI, MachineUiPlacement, MachineUiStart, MachineUiAnchor, MachineUiElement,
│                              # MachineUiOverlay, MachineUiPanel, MachineUiPanelBuilder, MachineUiInteraction,
│                              # MachineUiWrites, RecipeFiller, ConfiguratorTabs, CircuitSlots,
│                              # ShowMachineUiInstruction, StackWrite
└── render/                    # ColorData
    └── highlight/             # HighlightHandler, HighlightRender
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| 客户端引导 | `client/ClientProxy.java` |
| 高亮状态与渲染钩子 | `client/render/highlight/HighlightHandler.java`（`highlight(...)` / `expire()` / `getBlockData()` / `HighlightData`）、`HighlightRender.java`（`hook(RenderLevelStageEvent)`） |
| Ponder 场景基类 | `client/ponder/CTNHPonderSceneBuilder.java` |
| Ponder lang 抽取 | `client/ponder/CTNHPonderLang.java` |
| Ponder tag 助手 | `client/ponder/CTNHPonderTagHelper.java` |
| 机器 UI 门面与摆放 API | `client/ponder/ui/MachineUI.java`（`of(...)` / `showFullUI()` / `scale()` / `fitToPanel()` / `showCircuit()` / `forceMultiblockActivated()` / `in(SceneBuilder)`）、`MachineUiPlacement.java`（`at` / `machinePos` / `scale` / `pointing` / `slot` / `tank` / `recipe` / `outline*` / `show`） |
| 机器 UI 面板 / 写入 / 点击 / 配方填充 | `client/ponder/ui/MachineUiPanelBuilder.java`, `MachineUiWrites.java`, `MachineUiInteraction.java`, `RecipeFiller.java`, `MachineUiElement.java`, `MachineUiOverlay.java`, `ConfiguratorTabs.java`, `CircuitSlots.java`, `ShowMachineUiInstruction.java`, `StackWrite.java` |
| 机器编辑指令 | `client/ponder/machine/{MachineEdit, MachineEditInstruction, MachineEdits, CoverChange, AutoOutputChange, WorkingModelChange, ParallelChange, MaintenanceChange}.java` |
| 思索「查看 UI 详情」按钮 | `client/ponder/PonderUiButtons.java`（`attach` / `beforeRender` / `afterRender` / `clickPanel` / `tick`，挂到 `PonderUI` 控件表）、`ButtonRow.java`（底部按钮锚点判定）、`FrameGuard.java`（一帧只处理一次的标记） |
| 颜色数据 | `client/render/ColorData.java` |

## CONVENTIONS
- `ClientProxy extends CommonProxy`，标注 `@Mod.EventBusSubscriber(modid = CTNHLib.MODID, bus = FORGE, value = Dist.CLIENT)`；`onRenderLevel(RenderLevelStageEvent)` 转调 `HighlightRender.hook(event)`。`ClientProxy.init()` 为空实现。
- 高亮状态由 `HighlightHandler.highlight(pos, dim, expireTime, color[, ...])` 写入、`expire()` 清理；`BlockHighlightPacket` 以 `System.currentTimeMillis() + 10000` 与 `ColorData.RED` 触发 10 秒高亮。
- `CTNHPonderSceneBuilder extends CreateSceneBuilder`：提供 `init5x5` / `init7x7` / `init9x9` / `initAll` 底板与缩放、`rotateAround(duration)` 四向环绕、双语 `title(sceneId, en, cn)` 与 `title(sceneId, headerEn, headerCn, titleEn, titleCn)`、`showText(duration, en, cn)` 与 `showText(duration, Lang)`。
- 场景 lang key 形如 `<modId>.ponder.<sceneId>.<title|header|text_N>`；双语注册经构造参数传入的 `LangRegistrar`（默认 `NOOP`），未提供 modId 时 `sceneLangKey` 抛 `IllegalStateException`。
- `CTNHPonderLang.init(PonderPlugin plugin)`：注册插件 → `PonderIndex.registerAll()` → lang access 为 `PonderLocalization` 时调 `generateSceneLang()`。
- `CTNHPonderTagHelper.registerTag(...)` 用 `CNRegistrate.genLang` 写 tag 名与描述，key 为 `<namespace>.ponder.tag.<path>` 与 `<...>.description`。
- 机器 UI 入口 `CTNHPonderSceneBuilder.showUI(MachineUI)` 返回起点态 `MachineUiStart`；`MachineUI.of(MachineDefinition)` / `of(Block)` 建门面，`showFullUI()` / `hideTitleBar()` / `hideSideTabs()` / `showPlayerInventory()` / `showConfigurators()` / `showCircuit()` / `showNavigationButtons()` 调界面形态，`forceMultiblockActivated()` 让控制器在思索里按成型显示（只调 `onStructureFormed()`，不跑结构校验），`scale(float)` / `fitToPanel(float)` 定尺寸。
- 三段式摆放 API（编译期强制给机器位置）：`MachineUiStart`（`showUI` 的返回值，只有 `at(BlockPos)` 一步到位 / `at(Vec3)` 只定箭头 / `scale` / `pointing`）→ `at(Vec3)` 得到 `MachineUiAnchor`（只有 `machinePos(BlockPos)` / `scale` / `pointing`）→ 拿到 `MachineUiPlacement` 后才能链 `slot` / `tank` / `recipe` / `outline*` / `show(ticks)`；写入 `slot(int).withItem(ItemStack[, delayTicks])`、`tank(int).withFluid(FluidStack[, delayTicks])`；配方 `recipe(String[, delayTicks])`；红框具名方法 `outlineSlot` / `outlineTank` / `outlineProgress` / `outlineCircuit` / `outlinePowerToggle` / `outlineAutoOutput` / `outlineCircuitButton` / `outlineDistinct` / `outlineButton(index)`，或通用入口 `outline(Part, index[, delayTicks])`（`Part` 是红框控件的公开扩展点）；最后 `show(int ticks)` 落地。
- `MachineUiInteraction` 维护当前帧的面板视图（`publish` / `beginFrame` / `hasPanel` / `hasFullPanel`）、转发面板点击（`click`，只放行页签与配置器页签）、给冻住的场景继续 `tickPanels`；`enabled()` / `setEnabled(boolean)` 表示「查看 UI 详情」开关状态，开启时记下电源 / 自动输出 / 电路的开关值、关闭时还原并收起配置器；`PonderUIMixin` 在 `tick` / `getPartialTicks` 里读它来冻结场景。
- `MachineEdits` 提供按机器坐标施加与还原的指令（`add` / `placeCover` / `setWorkingModel` / `setItemOutput` / `setFluidOutput` / `setAutoOutput` / `setParallel` / `fixMaintenance` / `fixMaintenanceWithoutTape`），`MachineEdit` 的 `apply` / `revert` 由 `CoverChange`、`AutoOutputChange`、`WorkingModelChange`、`ParallelChange`、`MaintenanceChange` 实现；`redraw(PonderScene)` 强制场景方块重画，`requestRebuild()` / `rebuildGeneration()` 用递增代际让每块面板各自重建一次。
- `MachineUiWrites` 是一次摆放的写入时间线：数量在 `FILL_TICKS`（20 tick）内从 0 叠到目标值，摆放自带的写入排在配方追加的写入之前，面板收起或场景回退时按写入前的内容还原；空流体的取空规则集中在 `StackWrite.normalized(...)`。
- `RecipeFiller` 按配方 id 找配方（`byId` 是唯一取配方链条，内部 `runtime(Recipe)` 同时接受 `GTRecipeDefinition` 与 `GTRecipe`；`needsCircuit` 预判配方是否要编程电路），按 GT 的 `IngredientIO` 标签把入料写进输入槽 / 输入储罐，配方里的编程电路经 `CircuitSlots` 摘进机器的电路槽，进度条走完后把成品写进输出槽 / 输出储罐，并在运行与待机之间切机器模型；时间线为入料 1 秒 → 进度条 1 秒 → 成品 1 秒。
- `PonderUiButtons` 把「查看 UI 详情」按钮挂进 `PonderUI` 自己的控件表，随底部一排淡入淡出、被派发点击；按钮锚点（该排第一个不贴边、在左半边的按钮）由 `ButtonRow.anchor(...)` 判定，「一帧只处理一次」由 `FrameGuard` 保证；点击转 `MachineUiInteraction`，`PonderUIMixin` 在 `init` / `renderWindow` / `mouseClicked` / `tick` / `getPartialTicks` 上接线。
- 思索编辑模式（`PonderIndex.editingModeActive()`）下，`MachineUiOverlay` 把悬停槽位 / 储罐 / 机器页按钮在机器里的真实序号加到 tooltip 首行，供 `slot(index)` / `tank(index)` / `outlineButton(index)` 对齐。
- 消费方：Core、Energy、Bio、Mana、CTPP 各自的 `client/ponder/*SceneBuilder` + `*PonderTags`，在其 `CommonProxy` 中接线；机器 UI 栈的使用示例见 CTNH-Core `client/ponder/example/ChemicalReactorUi`。

## ANTI-PATTERNS
- 把模块专属 Ponder 场景 / tag / 插件或 Energy 的 AE2 线缆助手搬进 Lib。
- 在 Lib 里加模块专属 GUI 逻辑；客户端域只承载共享基础设施。
- 在功能模块内另起一套机器 UI 面板 / 写入 / 配方回放实现；统一走 Lib 的 `client/ponder/ui` 栈。

## SCOPE
适用于 `src/main/java/tech/vixhentx/mcmod/ctnhlib/client` 及其子包。

## READ WHEN
- 改高亮渲染、共享 Ponder 场景基类 / lang 抽取 / tag 注册助手。
- 改机器 UI 栈（`MachineUI` / `MachineUiPlacement` / 面板构建 / 写入 / 配方回放）或思索「查看 UI 详情」按钮。

## SOURCE OF TRUTH
- `client/ClientProxy.java`（引导）、`client/ponder/CTNHPonderSceneBuilder.java`（场景契约）、`client/render/highlight/HighlightHandler.java`。
- `client/ponder/ui/MachineUI.java` / `MachineUiPlacement.java`（机器 UI 门面与摆放契约）、`client/ponder/PonderUiButtons.java`（按钮接线）。

## WORKFLOW
1. 先确认改动确实跨模块共享，再动 Lib 客户端代码。
2. 检查受影响消费方（Core / Energy / Bio / Mana / CTPP 的 Ponder 适配与高亮调用点）。
3. 跑 `:modules:CTNH-Lib:build` 与最小消费模块任务。
