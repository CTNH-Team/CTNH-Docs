# CTNH Ponder API 速查

以本仓库现场为准（Ponder-Forge 1.20.1 / Create 1.20.1 / CTNH 四模块）。改动前可重新核对源码。

## CTNH-Lib 共享构建器

`tech.vixhentx.mcmod.ctnhlib.client.ponder.CTNHPonderSceneBuilder extends CreateSceneBuilder`

| 成员 | 签名 | 说明 |
|------|------|------|
| 构造 | `CTNHPonderSceneBuilder(SceneBuilder)` | modId 与 lang 注册器缺省（写作时 `sceneLangKey` 会抛 `IllegalStateException`） |
| 构造 | `CTNHPonderSceneBuilder(SceneBuilder, String modId, LangRegistrar)` | 模块适配层用这一支 |
| 底板 | `init5x5(util)` / `init7x7` / `init9x9` / `initAll` | 设底板大小 + `scaleSceneView` + 显示第 0 层 |
| 环绕 | `rotateAround(int duration)` | 拆成 4 段 `rotateCameraY(90)` + `idle` |
| 标题 | `title(String sceneId)` / `title(sceneId, String title)` / `title(sceneId, Lang)` | 只登记标题正文（`title` 是 header 的 display 值） |
| 标题 | `title(sceneId, String en, String cn)` | 同时把 `title` 与 `header` 登记为同一文案 |
| 标题 | `title(sceneId, String headerEn, String headerCn, String titleEn, String titleCn)` | 页眉与标题分开 |
| 正文 | `showText(int duration, String en, String cn)` | 递增 `text_N` 并登记双语 |
| 正文 | `showText(int duration, Lang lang)` | 用注解 Lang（`@EN`/`@CN`）的文案，**不进 ponder lang** |
| 取用 | `getSceneBuilder()` | 返回自身，便于需要 `CreateSceneBuilder` 的地方 |

lang key：`<modId>.ponder.<sceneId>.<entry>`，entry ∈ `title` | `header` | `text_1`、`text_2`…

### LangRegistrar

```java
@FunctionalInterface
public interface LangRegistrar {
    LangRegistrar NOOP = (key, en, cn) -> {};
    void register(String key, String en, String cn);
}
```

模块适配层把它接到 `REGISTRATE.genLang`，并**必须**用 `GTCEu.isDataGen()` 门控。

## CTNHPonderLang

```java
public static void init(PonderPlugin plugin) {
    PonderIndex.addPlugin(plugin);
    PonderIndex.registerAll();
    if (PonderIndex.getLangAccess() instanceof PonderLocalization localization) {
        localization.generateSceneLang();
    }
}
```

只在 `CommonProxy.gatherData()` 的 `includeClient()` 分支调用（Core / Energy / Mana / CTPP 均如此）。

## CTNHPonderTagHelper

```java
public static TagBuilder registerTag(CNRegistrate registrate,
                                     PonderTagRegistrationHelper<ResourceLocation> helper,
                                     ResourceLocation id,
                                     String en, String cn,
                                     String descriptionEn, String descriptionCn)
public static String tagKey(ResourceLocation id)            // <ns>.ponder.tag.<path>
public static String tagDescriptionKey(ResourceLocation id) // 上者 + .description
```

拿到 `TagBuilder` 后链式：`addToIndex()` / `item(ItemLike, useAsIcon, useAsMainItem)` / `icon(...)` / `register()`。

## 注册助手（上游 API，CTNH 已消费的部分）

`PonderSceneRegistrationHelper<ResourceLocation>`：

- `forComponents(ResourceLocation...)` / `forComponents(Iterable)` → `MultiSceneBuilder`
- `asLocation(String path)` → `new ResourceLocation(插件 modId, path)`
- `addStoryBoard(component, schematicPath, storyBoard, tags...)` → `StoryBoardEntry`

`MultiSceneBuilder`：`addStoryBoard(String schematicPath, PonderStoryBoard, ResourceLocation... tags)`、
以及 `addStoryBoard(..., PonderStoryBoard, Consumer<StoryBoardEntry> extras)`。

`StoryBoardEntry`：`orderBefore(...)` / `orderAfter(...)`（含跨 mod 重载）、`highlightTag(s)`。

`PonderTagRegistrationHelper<ResourceLocation>`：`registerTag(ResourceLocation|String)`、
`addToTag(tag).add(component)`、`addToComponent(component).add(tag)`、`addTagToComponent(...)`。

## storyboard 解析规则

> 生成方式（蓝图 JSON → .nbt 脚本、地板/尺寸/朝向规则、NBT 载荷格式）见
> [storyboard-nbt.md](storyboard-nbt.md)。

`PonderSceneRegistry.loadSchematic`：`path = "ponder/" + location.getPath() + ".nbt"`，
命名空间取 `asLocation` 的命名空间，即插件的 modId。文件实际落在
`src/main/resources/assets/<modid>/ponder/<path>.nbt`。

缺失时记 `Ponder schematic missing: <ns>:ponder/<path>.nbt`，返回空 `StructureTemplate`（空场景，不抛异常）。

## 场景常用调用（既有场景里已验证）

```java
scene.showBasePlate();
scene.idle(10);
scene.world().showSection(util.select().layer(0), Direction.UP);
scene.world().showSection(util.select().position(3, 1, 1), Direction.DOWN);
scene.world().showSection(util.select().fromTo(1, 1, 5, 5, 6, 1), Direction.DOWN);
scene.world().setBlock(util.grid().at(x, y, z), blockState, true);
scene.world().modifyBlockEntityNBT(util.select().position(x, y, z), BlockEntity.class, tag -> {...}, true);
scene.overlay().showControls(util.vector().blockSurface(util.grid().at(x, y, z), Direction.UP),
        Pointing.LEFT, 40).rightClick().withItem(stack).whileSneaking();
scene.effects().emitParticles(vec, (world, x, y, z) -> {...}, countPerTick, duration);
scene.markAsFinished();
```

文案链式：`scene.showText(...).pointAt(vec).attachKeyFrame();`

### 让同一个方块"换位置"（讲两种布局）

讲"先贴在一起、再插一格管道"这类对照时，不要让同一坐标显示两种结构，而是把该方块
**独立成一个 section**，后续用 `moveSection` 平移它：

```java
// 1) 独立 section：从基座 world section 里摘出来，可以单独动
ElementLink<WorldSectionElement> drumLink =
        scene.world().showIndependentSection(util.select().position(1, 3, 1), Direction.DOWN);

// 2) 平移（offset 是相对位移，不是目标坐标；duration 是 tick 数）
scene.world().moveSection(drumLink, new Vec3(0, -1, 0), 10);   // 下落一格，底面贴住下方容器
scene.world().moveSection(drumLink, new Vec3(0, 1, 0), 10);    // 升回去，腾出中间一格放管道

// 3) 整个 section 淡出
scene.world().hideSection(util.select().position(1, 1, 1), Direction.DOWN);
```

要点：

- `showIndependentSection` 返回的 link 必须存下来；`moveSection` / `rotateSection` /
  `hideIndependentSection` 都按 link 操作。
- 平移量与`showSection` 的淡入可以并行安排时间；平移本身是**阻塞**的 ticking instruction，
  后面接 `idle(...)` 才有停顿感。
- 结构 NBT 里只需要一种摆放；"另一种布局"用移动表达，比准备两份 NBT 更好维护。

### 镜头：默认只看得见 NORTH / WEST / UP

默认相机在场景的 `(-x, +y, -z)` 象限，**可见面只有 NORTH、WEST、UP**，
正对视线的是 NORTH。这意味着：**摆在 EAST / SOUTH 面（或机体东侧、南侧）的部件，
在默认镜头下完全看不见**——写了讲解文案等于白写，玩家只看到一堵墙。

仓室摆放与镜头必须一起设计，二选一：

```java
// 方案 1：讲背面部件的段落前把镜头转过去，讲完转回来
scene.rotateCameraY(180);
scene.idle(40);
scene.world().setBlock(util.grid().at(6, 2, 4), CTPPMachines.MECHANICAL_UPGRADE_BUS[GTValues.LV]
        .defaultBlockState(), true);
scene.showText(80, "...", "...")
        .pointAt(util.vector().blockSurface(util.grid().at(6, 2, 4), Direction.SOUTH))  // 面也要跟着改
        .attachKeyFrame();
scene.idle(90);
// ...讲完
scene.rotateCameraY(-180);
scene.idle(40);
```

方案 2：把仓室放在西侧/北侧这些可见面上（前提是结构允许）。

注意 `pointAt` 的面要和当前镜头一致——转了 180° 之后还指 `Direction.WEST`，箭头会穿到机体后面。

### `rotateSection`：转哪个方块由机器决定，不是由你挑

表现"机器运转"时，**不要凭直觉挑一组方块去转**。真机里哪些方块是旋转体、
绕哪根轴，都写在机器代码里：

```java
// KineticGeneratorMachine
private Direction.Axis getContraptionRotationAxis() {
    return getFrontFacing().getAxis() == Direction.Axis.Z ? Direction.Axis.X : Direction.Axis.Z;
}
@Override public BlockPos getAssemblyPivot() { return MachineUtils.getOffset(this, 2, 0, 1); }
```

实现 `IContraptionMultiblock` 的机器还会有 `assembleFromPattern(pivot, rotationAxis)`，
把 pattern 里标为 dynamic part 的方块打包成旋转体。**去读这两个方法，再照着挑方块和轴。**

用法（`x,y,z` 是**角度**，单位度，按 tick 匀速补间）：

```java
ElementLink<WorldSectionElement> link = scene.world().showIndependentSection(magnets, Direction.DOWN);
scene.world().moveSection(link, PARK, 20);                       // 先挪到一边单独讲
scene.world().moveSection(link, PARK.scale(-1d), 20);            // 归位
scene.world().rotateSection(link, 360, 0, 0, 200);               // 绕 X 轴整圈，200 tick
```

`rotateSection` 的旋转中心是**该 section 的几何中心**，不是 pivot 坐标；如果旋转体
不对称、中心与真机 pivot 不一致，观感会和游戏内对不上。

### 文案：字面 `%` 会渲染成 `Format error:`

Ponder 文案最终走 `I18n.get(...)` → `Component` 的格式化路径，**裸 `%` 会抛
`UnknownFormatConversionException`**，屏幕上显示成：

```text
Format error:
<你写的原文>
```

两种写法：

```java
scene.showText(80, "each tier adds 10 percentage points of efficiency", "每提升一级效率增加 10 个百分点");
// 或者真的需要百分号时转义
scene.showText(80, "10%% faster", "快 10%%");
```

**这个错误 `runData` 抓不到**：lang 会正常生成，`%s`、`%d` 这类占位符更是会被
原样写出（GT 的机器 tooltip 用的就是 `%d%%`，那是另一套格式化路径，可以照写）。
所以 `.ponder.` 的文案里出现 `%` 时，必须游戏内确认。

### 粒子（表现流体/能量流动）

```java
scene.effects().emitParticles(
        Vec3.atLowerCornerOf(util.grid().at(x, y, z)).add(0.5, 0.0, 0.5),   // 锚点=方块中心
        scene.effects().simpleParticleEmitter(ParticleTypes.FALLING_WATER,   // 粒子类型
                new Vec3(0, -0.15, 0)),                                      // 初速度
        2f,      // 每 tick 生成个数（小数部分按概率取整）
        20);     // 持续 tick 数
```

- `simpleParticleEmitter` = 精确锚点；`particleEmitterWithinBlockSpace` = 锚点所在方块内随机散布。
- 锚点用 `Vec3.atLowerCornerOf(pos).add(.5, 0, .5)` 取方块中心；直接传 `util.vector().centerOf(...)` 亦可。
- 这两个 emit 调用是**非阻塞**的，会与后续 `idle`/`modifyBlockEntityNBT` 重叠，适合做持续流动感。

## 四个模块的接线点

| 模块 | ClientProxy 注册 | gatherData lang 抽取 | 适配层 |
|------|------------------|----------------------|--------|
| CTNH-Core | `ClientProxy.onClientSetupEvent` → `PonderIndex.addPlugin(new CTNHCorePonderPlugin())` | `CommonProxy.gatherData` `includeClient()` → `CTNHPonderLang.init(new CTNHCorePonderPlugin())` | `CTNHCorePonderSceneBuilder` + `REGISTRATE.genLang` |
| CTNH-Energy | `ClientProxy` → 同上 | 同上 | `CTNHEnergyPonderSceneBuilder` |
| CTNH-Mana | `ClientProxy` → 同上 | 同上 | `CTNHManaPonderSceneBuilder` |
| CTPP | `ClientProxy.onClientSetup` → 同上 | 同上 | `CTPPPonderSceneBuilder` + `CTPPRegistration.REGISTRATE` |

## 机器 UI（CTNH-Lib `client/ponder/ui`）

定义面板（`MachineUI`）：

| 调用 | 说明 |
|------|------|
| `MachineUI.of(MachineDefinition \| Block)` | 用注册对象取界面定义，不要在场景里按字符串 id 查 |
| `.scale(f)` / `.fitToPanel(fraction)` | 固定缩放 / 按 Ponder 面板宽度自适应 |
| `.showFullUI()` | 一次画出原版整套 UI（配置器、提示面板、玩家背包都在），一个部件都不裁 |
| `.showCircuit()` | 常开编程电路 UI（默认只在配方带 `circuitMeta(n)` 时出现） |
| `.showPlayerInventory()` / `.showConfigurators()` / `.showNavigationButtons()` | 逐个打开默认裁掉的部件 |
| `.hideTitleBar()` / `.hideSideTabs()` | 反过来藏掉标题栏与左侧页签（把面板压到最小） |

两条与"画不画得出来"有关的前提：

- 目标机器要实现 `IUIMachine`。多方块的仓室与总线都满足（`IMultiPart extends IFancyUIMachine`）；
  单方块机器看它自己的实现（`MetaMachine` 本身不是 `IUIMachine`），不满足时这一段面板被跳过，只留一行日志。
- `.slot(i)` / `.tank(i)` 的序号 = 实机 UI 里**可见**控件按机器 `createUIWidget()` 添加顺序收集的序号。
  `LargeStackSlotWidget` 也是 `SlotWidget`；储罐同时认 GT 与 LDLib 两种 `TankWidget`。不确定就先用红框核对。
- **仓室选型**：配方同时要物品和流体就用输入 / 输出总成（`GTMachines.DUAL_IMPORT_HATCH` /
  `DUAL_EXPORT_HATCH`，LV..UHV），一块面板上 `.slot(i)` 与 `.tank(i)` 一起写；装不下就升等级。
  容量表与选型流程见 [../SKILL.md](../SKILL.md) 工作流 E〈仓室选型〉。

摆放、写入与红框（`CTNHPonderSceneBuilder.showUI(MachineUI)` 返回的摆放对象上的链式调用）：

| 调用 | 说明 |
|------|------|
| `MachineUiStart.at(BlockPos)` 一步到位；`MachineUiStart.at(Vec3)` → `MachineUiAnchor.machinePos(BlockPos)` 分开指定 | 三段式由类型强制：`showUI` 返回 `MachineUiStart`，`at(Vec3)` 返回 `MachineUiAnchor`，拿到 `MachineUiPlacement` 才能链 `slot` / `tank` / `show` 等。忘写 `machinePos` 是**编译错误**，不再依赖运行期日志 |
| `.pointing(Pointing.DOWN)` | 面板落在指向点的哪一侧，默认 DOWN |
| `.scale(f)` | 覆盖定义上的缩放 |
| `.slot(i).withItem(stack, startTick)` / `.tank(i).withFluid(fluidStack, startTick)` | 第 i 个槽位/储罐，`startTick` 之后开始写，写入固定 1 秒，从 0 涨到目标值 |
| `.recipe(recipeId, startTick)` | 入料 → 进度条 → 成品；配方带 `circuitMeta(n)` 时自动写电路 |
| `.outlineSlot(i[, delay])` / `.outlineTank(i[, delay])` / `.outlineProgress([delay])` / `.outlineCircuit([delay])` | 面板内控件的红框 |
| `.outlineButton(i[, delay])` | **机器页里**第 i 个按钮/开关的红框，序号按 `createUIWidget()` 的添加顺序；标题栏、页签、配置器那一列都不算在内（LDLib 里 `SwitchWidget` 与 `ButtonWidget` 都算按钮） |
| `.outlinePowerToggle()` / `.outlineAutoOutput()` / `.outlineCircuitButton()` / `.outlineDistinct()` | 配置器那一列按钮的红框（这一段需要 `showFullUI()`） |
| `.outline(Part, i[, delay])` | 上面这些的底层入口；`Part` 是公开的扩展点 |
| `.show(ticks)` | 这一段持续多久；**非阻塞**（不占时间线，与后续 `showText`/`idle` 并行）。连续两条 `showUI` 会同时在屏上，用 `.pointing(...)` 错开；面板淡出时把这一段写进去的东西还原 |

写 `slot(i)` / `tank(i)` / `outlineButton(i)` 的 `i` 不用猜：**ponder 编辑模式**下把鼠标停在控件上，
tooltip 第一行就是它在机器里的真实序号（槽位 / 储罐 / 按钮都有，用的是和场景 API 同一份收集清单）；
按钮自己的悬停提示（模式名那类）现在也会一并显示。

带索引的红框（`SLOT` / `TANK` / `BUTTON`）身份由**收集顺序**决定：改机器 `createUIWidget()` 里的添加顺序会让编号整体平移，
所以这类红框要和「按实机 UI 核对序号」一样对待。`Part` 枚举是公开的扩展点——新增一类可框控件要三处一起动：
在 `Part` 里加值、在 `MachineUiPanelBuilder` 里收集、在 `MachineUiPanel#parts` 里解析。

机器状态（`machine/MachineEdits`，与面板无关，独立指令）：

```java
MachineEdits.placeCover(scene, pos, Direction.UP, GTItems.CONVEYOR_MODULE_LV.asStack(), 10);
MachineEdits.setWorkingModel(scene, pos, true, 20);        // 只换模型，不动配方逻辑
MachineEdits.setItemOutput(scene, pos, Direction.WEST, 10);
MachineEdits.setFluidOutput(scene, pos, Direction.SOUTH, 10);
MachineEdits.setAutoOutput(scene, pos, Direction.NORTH);    // 物品与流体一起设
```

delay 都可省略；机器不支持时每条报一行 error 并跳过，场景继续播，场景回退时一并还原。

| 调用 | 说明 |
|------|------|
| `MachineEdits.add(scene, pos, edit[, delay])` | 把模块自写的 `MachineEdit` 挂到时间线上 |
| `MachineEdits.redraw(scene)` / `requestRebuild()` | `MachineEditInstruction` 落地后自己会调，场景侧一般不用管 |

自己写变更类（放**本模块**的 `client/ponder/machine/`）：实现 `MachineEdit` 的 `apply` / `revert`；
机器不是预期那台或能力不支持时记一行 error 就返回、不要抛；`revert` 把改动前的值写回去。
**改机器字段就走它，别直接 `modifyBlockEntityNBT`**——只有 `MachineEditInstruction` 落地后才会
`redraw + requestRebuild()`，画着这台机器的面板下一次 tick 重建，控件才读得到新值。

连续变化（例如"一秒内递增"）：`MachineEditInstruction` 是非阻塞的，而 `PonderScene.tick()` 并行 tick 所有非阻塞
指令、遇到阻塞指令才停，所以按 `1..N` tick 的延迟排 N 条变更就是逐帧爬升；时长与面板里槽位/储罐的写入对齐
（20 tick = 1 秒）。排 N 条会有 N 次面板重建，档位可以调粗。

面板里的**文本框**（数字输入框那类）只有在 client-side 模式下才会每帧从 `textSupplier` 取回文本
（LDLib `TextFieldWidget` 的构造函数不初始化文本）。Lib 的面板构建器已经统一给槽位、储罐、进度条与文本框
打开这个开关；**自己新建控件容器时要照做**，否则数字框在思索里永远是空的，机器上的值改了也看不见。

**fork 形态差异**（照官方 GTCEu 写会踩）：配方在 `RecipeManager` 里是 `GTRecipeDefinition`（要 `toRuntime()`）、
编程电路是 `ProgrammableCircuitSlotTrait`、自动输出在 `AutoOutputTrait`、`RecipeHelper` 多一个 `simulate` 参数。
详见 [../SKILL.md](../SKILL.md) 工作流 E。

## 调试命令（Ponder 自带）

`/ponder`（打开 tags）、`/ponder index`、`/ponder tags`、`/ponder <scene id>`、
`/ponder reload`；客户端配置 `editingMode` 打开后会显示更多调试信息（含未注册文案占位）。
