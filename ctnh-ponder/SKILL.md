---
name: ctnh-ponder
description: >-
  CTNH 模组的 Create Ponder（思索）场景开发与排障指南。覆盖 CTNH-Lib 共享构建器
  （CTNHPonderSceneBuilder / CTNHPonderLang / CTNHPonderTagHelper）、CTNH-Core /
  CTNH-Energy / CTNH-Mana / CTPP 各自的 Plugin-Scenes-Tags 适配层、
  assets/模块 id/ponder/场景路径.nbt storyboard 资源，以及双语 lang 的 datagen 规则。
  新增或修改思索场景、调整 PonderTag、给模块补齐 Ponder 适配层、按上游 Create/GTCEu 补场景、
  或排查场景不显示 / 文案显示成 lang key 时使用。Triggers: Ponder, 思索, pondering, storyboard,
  CTNHPonderSceneBuilder, PonderTag, addStoryBoard, ponder nbt, 场景不显示
---

# CTNH Ponder

CTNH 的思索（Ponder）不是 Create 原生写法的直接复制：**共享能力在 CTNH-Lib，场景与注册在所属模块，
文案双语内嵌且只能经 registrate 走 datagen**。本 skill 描述这条链路的做法、边界与排障。

## 何时使用

- 给某台机器/方块新增一个思索场景。
- 要把**机器自己在游戏里的那套界面**画进思索、并按真实槽位序号写入（`MachineUI`，见工作流 E）。
- 修改或扩展已有场景（文案、步骤、镜头、结构展示）。
- 新增或调整 PonderTag，或把组件挂到 tag 上。
- 给一个还没有 Ponder 的模块补齐适配层。
- 为上游 Create / GTCEu 的对象补场景（含 Mixin 注入注册）。
- 排查：场景不出现、文案显示成 `<modid>.ponder.xxx.title`、场景是空结构、注册期报错。

## 动手之前

1. 先按 ctnh-docs 技能读对应模块指南：
   - 共享构建器改动 → `references/CTNH-Lib/AGENTS.md` + `references/CTNH-Lib/client/AGENTS.md`
   - 场景/注册改动 → `references/<Module>/client/AGENTS.md`（Core / Energy / Mana / CTPP）
   - 涉及机器/trait/能力 → 先读 `references/_architecture/AGENTS.md`
2. 版本事实（本 skill 所依据的现场，改动前重新核对）：
   - 上游 Create 提供 `com.simibubi.create.foundation.ponder.CreateSceneBuilder`，CTNH 共享构建器继承它；
   - 版本（`CTNH-Modules/gradle/ctnh.versions.toml`）：Create `6.0.8-291`、Ponder-Forge 1.20.1 `1.0.78`，
     运行时包名为 `net.createmod.ponder`；
   - 现有 storyboard 注册条数：Core 5、Energy 24、Mana 6、CTPP 7（含 `kinetic_generator`），另有 CTPP 对 Create 的 Mixin 注入。

## 证据阶梯与时间预算（硬纪律）

本 skill 的绝大多数返工来自**证据获取顺序错误**，而不是知识不足。按下面的阶梯取证据，
**能用上层结论就不要去下层试错**：

| 优先级 | 证据来源 | 成本 | 适用 |
|--------|---------|------|------|
| 1 | **框架源码**（`BlockPattern.setActualRelativeOffset`、`PonderSceneBuilder`、`MetaMachineBlock`） | 一次 `read` | 一切"映射/语义/行为"问题——**默认从这里开始** |
| 2 | **机器注册代码**（`.pattern(...)`、`.rotationState(...)`、`.where(...)`） | 一次 `read` | 结构、朝向、属性、方块 id |
| 3 | **运行时注册日志**（`modules/<M>/run/logs/debug.log` 的 `Registered <id>`） | 一次 `grep` | 只有拿不准注册 id 时 |
| 4 | **反查已有 storyboard / 生成物** | 数次 `read` + 脚本 | **仅当上层都没有答案时**——对称结构反查不出方向，极易空耗 |

**禁止的循环**：拿"直觉映射"生成一版 → 与已有文件比对 → 不一致 → 换一种猜测再比对。
这是猜测驱动的循环，收敛慢且结论不可信。**一旦发现自己在做第二次"试一种再比一比"，
立刻停下来去读第 1 层的源码。**

**时间预算（单个新场景）**：查证事实 ≤ 总时长的一半，写代码与验证占另一半。
如果一直在 grep/read 而没有产出任何文件，就是已经跑偏了——此时必须立刻
**问用户要结构，或直接读框架源码下结论**，不要继续扩大搜索面。

**另一条**：不确定的细节要**问**，不要靠搜索堆证据。玩家手上的实际摆放、
sceneId 的取名习惯、要讲的步骤，这些本来就不在代码里，搜多久都搜不出来。

**第三条——按需读取，不要整文件吞**：本 skill 涉及的类（`CTNHPonderSceneBuilder`、
`PonderLocalization`、工厂 pattern、机器类）都不大，但**一次只读你要用的那一段**。
判断"这个类的行为"时读它的方法签名与关键分支即可；把整个类读完再动手，
是"过度查询"最常见的形态。**读文件是有明确问题的**——写下你要回答的问题，
读完就回答它，不要顺手读别的。

**第四条——注释写给维护者，不写给自己**。代码注释只放：这个场景的坐标事实、
非显然的耦合（"文案里的百分比为什么写成文字"这类若确实必要，一句话，且应当
已经进了本 skill 排障表）。**不要**在代码里留"这里容易写错""注意不要用 X"
这类给自己看的便条——那是本 skill 的内容，不是源码的内容。
写完自问：**这段注释是写给下一个改这个文件的人，还是写给我自己看的？**
后者一律删掉，并把信息搬进本 skill 的排障表。

## 三层结构（唯一所有权）

| 层 | 位置 | 职责 |
|----|------|------|
| 共享栈 | CTNH-Lib `client/ponder/` | `CTNHPonderSceneBuilder`（双语标题/正文、底板与缩放、`rotateAround`）、`CTNHPonderLang`（lang 抽取）、`CTNHPonderTagHelper`（tag lang）；**机器 UI 层**在 `ui/`（`MachineUI`、`MachineUiPlacement`、`MachineUiElement`、`MachineUiOverlay`、`MachineUiPanel`、`MachineUiPanelBuilder`、`MachineUiWrites`、`RecipeFiller`、`ConfiguratorTabs`、`MachineUiInteraction`、`CircuitSlots`）与 `machine/`（`MachineEdit` 指令体系与 `MachineEdits`）；思索界面按钮在 `PonderUiButtons` + `mixin/PonderUIMixin` |
| 模块适配层 | `<Module>/client/ponder/` | 每模块一个 `*PonderPlugin` / `*PonderScenes` / `*PonderTags` / `*PonderSceneBuilder` + 场景类 |
| 资源与文案 | `src/main/resources/assets/<modid>/ponder/**/*.nbt`、`src/generated/resources/assets/<modid>/lang/{en_us,zh_cn}.json` | storyboard 结构；lang 由 datagen 生成，禁止手改 |

四个模块的落点：

| 模块 | 包 | 场景分组 |
|------|----|----------|
| CTNH-Core | `io.github.cpearl0.ctnhcore.client.ponder` | `Electric/`、`Kinetic/`、`Misc/`（不属于前两类的通用内容，如桶）、`example/`（机器 UI 示例：`ChemicalReactorUi`，八段覆盖画界面/写入/配方/机器状态/整套 UI 红框） |
| CTNH-Energy | `tech.luckyblock.mcmod.ctnhenergy.client.ponder` | `ae2/` |
| CTNH-Mana | `com.magicbee.ctnhmana.client.ponder` | `mana/`（含 `PonderParticleUtil`） |
| CTPP | `com.mo_guang.ctpp.client.ponder` | `electric/`、`kinetic/` |

## CTNH 定制改写（硬约束，违反即返工）

1. **必须走 CTNH 封装 API。** 场景标题与正文用 `CTNHPonderSceneBuilder.title(...)` /
   `showText(...)` 的双语重载。不要绕过它在 `overlay().showText().text("硬编码")` 里写死文案，
   也不要复刻 `CTNHPonderSceneBuilder` 的底板/缩放/环绕逻辑。
2. **文案双语内嵌，只能经 registrate 生成。** 场景文案写在场景类里（`title(sceneId, headerEn, headerCn, titleEn, titleCn)`、
   `showText(ticks, en, cn)`），不写进资源文件、不手写 lang json。
   lang key 固定为 `<modId>.ponder.<sceneId>.<title|header|text_N>`，`text_N` 从 1 递增。
   模块适配层必须提供 `registerLang` 回调，并且**只用 `GTCEu.isDataGen()` 门控**：
   ```java
   private static void registerLang(String key, String en, String cn) {
       if (GTCEu.isDataGen()) {
           REGISTRATE.genLang(key, en, cn);
       }
   }
   ```
3. **验证只认 datagen。** 改完跑 `:modules:<Module>:runData`，检查
   `src/generated/resources/assets/<modid>/lang/en_us.json` 与 `zh_cn.json` 中同一批 key **成对出现**。
   禁止手改 `src/generated/resources`。Ponder 没有运行时输出，datagen 产物就是可核验的回归面。
4. **模块边界不可越。** 可复用构建器/文本助手只能留在 CTNH-Lib；场景、tag、插件、模块专属助手
   （如 Energy 的 `AE2CablePonderHelper`、Mana 的 `PonderParticleUtil`）必须留在所属模块。
5. **客户端隔离。** 场景类、`*PonderPlugin`、`*PonderSceneBuilder` 只活在 client 侧，
   插件经 `ClientProxy` 在 `FMLClientSetupEvent` 里用 `PonderIndex.addPlugin(...)` 注册；
   语言抽取经 `CommonProxy.gatherData()` 的 `includeClient()` 分支调 `CTNHPonderLang.init(...)`。
   `common/` 不得引用 ponder 客户端类。
6. **地板与朝向是约定，不是自由发挥。** y=0 铺满地板（机械时代安山机壳 / 电力时代列车机壳），
   尺寸为结构水平外接矩形每边外扩 1 格；主方块及所有朝向类方块写 `facing=north`（+ `upwards_facing=north`），
   默认镜头下正面朝玩家。例外要写理由，不要默默改。
7. **引用注册对象，不用字符串 id。** Java 侧用静态注册对象及其 `getId()`
   （`MultiblocksA.MEADOW.getId()`、`GTMultiMachines.COKE_OVEN.getId()`、`CTPPMultiblockMachines.BIG_DAM.getId()`）。
   字符串 id 只允许出现在 storyboard NBT 与外部 mod 目标（例：Core 组合
   `ResourceLocation.fromNamespaceAndPath("jackseconomy", "mechanical_exporter")`）中，且要注明来源 mod。
8. **机器 UI 场景只用 Lib 的封装。** 画面板、写入、配方、红框、机器状态指令一律走 `MachineUI` + 构建器的 `scene.showUI(...)` + `MachineEdits`；
   不要在场景里自己搭控件树、自己摆「查看 UI 详情」按钮，也不要绕过 `MachineUiElement` 直接画。
   这条同时保证每段结束的还原（物品/流体/开关）与冻结后的点击转发仍然有效。

## 经验证的场景设计经验（跨机器通用）

这些经验用于同一台机器的多个相关思索，也适用于之后新增的其他机器；不要把某一台机器的部件名称或配方术语当成通用规则。

### 1. 先还原真实触发链

- 先读目标机器的 recipe type、recipe logic、输入 capability 和 UI，再决定场景文案。机器有 UI 不等于玩家在 UI 中选择配方；配方可能由物品、流体、能源、实体或其他能力自动匹配。
- 场景必须展示实际触发配方的设备和输入来源。若配方选择由输入物品触发，就展示输入设备和匹配过程，不要编造一个不存在的“打开主方块界面选择配方”步骤。
- 能力限制要限定到真实的配方类型或工作模式，不要把某个配方的限制写成整台机器的绝对限制。
- 场景中的方块、部件和物品都从注册对象取得；显示名称、配方名称和注册 id 不能互相推断。

### 2. 用 tick 控制阅读和动作节奏

- `20 tick = 1 秒`，所以半秒间隔是 `idle(10)`。中文文案较长时通常给 `140–180` tick，并让下一段 `showText` 在前一段结束后再出现，避免文字重叠。
- 一段说明需要演示多个位置时，让同一条文字保持可读，再按顺序执行 `world().setBlock(...)`、`overlay().showControls(..., 10)`（或轮廓高亮）和 `idle(10)`，把指向和替换放在同一时间线上。
- `showControls(...).rightClick().withItem(...)` 只用于确实存在的放置或操作；只是强调位置时用 `pointAt` 或 `showOutline`，避免画面暗示错误的交互方式。
- 运行时替换结构中的部件前，确认坐标属于要展示的结构选区；后续清理结构时，明确这些临时部件是否也应被移除。

### 3. 侧面目标要同时处理镜头和坐标

- 侧面或背面的目标必须先用 `rotateCameraY(...)` 暴露，等待 `idle(20–40)` 让镜头完成旋转，再展示控制和文案；步骤结束后旋回原视角。只改 `pointAt` 不会让被遮挡的面自动可见。
- 修改结构主方块位置或朝向时，要同时核对 NBT 的 controller 坐标、Java 中的选区和所有 `pointAt` 坐标。用蓝图脚本的 `--print`、NBT `--check` 和实际镜头确认屏幕上的左右顺序，不要只凭世界坐标判断“左边”。
- 朝向类方块应按其真实 `RotationState` 设置属性；不要给没有朝向属性的方块强行写 `facing`。

### 4. 同一机器的相关思索保持同源、分场景

同一机器的多个相关思索可以放在一个场景 Java 类中，用不同的静态方法、sceneId、注册路径和 NBT 文件分别承载。这样可以共享坐标和叙事约定，同时保持每个 storyboard 独立可校验；不要为了复用而把不同步骤硬塞进一个过长场景。

### 5. 文案、资源和验证必须一起更新

- 插入或删除 `showText` 会让后续 `text_N` 整体重排；只改 Java 后必须重跑 datagen，并检查当前 scene 前缀下的 `header`、`title`、`text_1..N`。全局语言文件可能有历史遗留差异，验收时先比较当前 scene 的 key 集合，并确认旧文案已消失。
- 生成流程通过后，再运行模块的 `compileJava`、`spotlessCheck`，并对每个 storyboard NBT 执行 `--check`。编译成功只能证明 Java 正确，不能证明资源路径、结构边界或镜头可读。
- 项目脚本还提供 scene 级语言检查：
  `python CTNH-Docs/ctnh-ponder/scripts/check_ponder_lang.py <lang-dir> --namespace <modid> --scene <sceneId>`。

## 工作流 A：给机器新建一个思索场景

输入：目标组件（方块/机器注册对象）、场景要讲的步骤、机器是否为多方块（决定要不要读 `pattern(...)`）。

1. **确定锚点与 sceneId。** 锚点必须有 Ponder 组件身份——`getId()` 可直接取自注册对象。
   sceneId 用稳定的蛇形名（`neutron_activator_building`、`coke_oven_building`、`meadow_common`），
   因为 sceneId 同时决定 lang key 与 storyboard 文件名。
2. **自动生成 storyboard NBT。** 不要手搭、更不要手写二进制：先写一份 JSON 蓝图，
   再用零依赖脚本产出 `.nbt`。完整规范见
   [references/storyboard-nbt.md](references/storyboard-nbt.md)，样例蓝图见
   [assets/storyboard-blueprint.template.json](assets/storyboard-blueprint.template.json)。
   - 位置：`src/main/resources/assets/<modid>/ponder/<path>.nbt`。
     `addStoryBoard("a/b", ...)` 把命名空间取为插件 modId，路径解析成
     `assets/<modid>/ponder/a/b.nbt`（相对真实资源路径再加一级 `ponder/`，扩展名自动补 `.nbt`）。
     不匹配时日志报 `Ponder schematic missing: <ns>:ponder/<path>.nbt`，且场景**不报错但为空**。
   - **地板**：y=0 铺满，机械时代用 `create:andesite_casing`（安山机壳），
     电力时代用 `create:railway_casing`（列车机壳）。
     尺寸 = 结构水平外接矩形**每边各外扩 1 格**（每轴 +2）：结构 3x3 → 地板 5x5。
   - **机器**：单方块只放那一个方块；多方块要先去读机器定义的 `pattern(...)`，
     按 `aisle(...)` 还原（`FactoryBlockPattern.start()` = LEFT/UP/FRONT：字符→x、行→y、aisle→z；
     `Predicates.air()` 的符号不放方块），再套地板。
   - **朝向**：主方块写 `facing=north` + `upwards_facing=north`，在默认镜头下正面正对玩家
     （已按 Ponder 相机数学验算：默认可见面为 NORTH/WEST/UP）。脚本会自动补这两个属性。
   - 命令：
     ```bash
     python CTNH-Docs/ctnh-ponder/scripts/build_storyboard_nbt.py my_blueprint.json --print   # 干跑核对
     python CTNH-Docs/ctnh-ponder/scripts/build_storyboard_nbt.py my_blueprint.json           # 落盘 .nbt
     python CTNH-Docs/ctnh-ponder/scripts/build_storyboard_nbt.py --check <path>.nbt          # 校验已有文件
     ```
3. **写场景类。** 一个场景一个类，静态方法作为 `PonderStoryBoard`。骨架见
   [assets/scene-template.java.txt](assets/scene-template.java.txt)。要点：
   - 用模块适配层构建器：`new CTNHCorePonderSceneBuilder(builder)`（各模块前缀不同）；
   - 开头 `title(...)`，结尾 `markAsFinished()`；`idle(ticks)` 控制节奏（20 tick = 1 秒）；
   - 步骤切换处 `attachKeyFrame()`，让玩家能跳步；
   - 展示结构用 `world().showSection(util.select()...)` / `setBlock(...)` /
     `modifyBlockEntityNBT(...)`；引导操作用 `overlay().showControls(...)`；
   - **不要**在场景里重新推导结构或从字符串查方块。
4. **注册场景。** 在模块的 `*PonderScenes.register(helper)` 中加一条
   `helper.forComponents(<锚点>.getId()).addStoryBoard("<path>", <Scene>::<Method>, <Tags>.XXX);`
   模板见 [assets/scenes-registration-template.java.txt](assets/scenes-registration-template.java.txt)。
5. **挂 tag（可选但推荐）。** 见工作流 C；标签会进 index 并高亮。
6. **跑 datagen 并核验。**
   ```
   ./gradlew :modules:<Module>:runData
   ```
   在 `zh_cn.json` / `en_us.json` 中确认 `<modid>.ponder.<sceneId>.header`、`.title`、`.text_1..N` 齐全且双语一致。
   再运行：
   ```bash
   python CTNH-Docs/ctnh-ponder/scripts/check_ponder_lang.py \
       modules/<Module>/src/generated/resources/assets/<modid>/lang \
       --namespace <modid> --scene <sceneId>
   ```
7. **游戏内确认（有条件必做）。** `/ponder <sceneId>` 直接打开；`/ponder index`、`/ponder tags`、
   `/ponder reload` 用于索引与热重载。开启 Ponder 客户端的 `editingMode` 会显示缺失文案与场景调试信息。

**验收**：组件能触发场景；场景能开到 `markAsFinished`；每一段文案中英文都能显示（不是 key）；datagen 产物包含全部 key。

## 工作流 B：修改或扩展已有场景

1. 先读该场景类与它的注册行，确认锚点、sceneId、storyboard 路径。
2. **加步骤**：在合适位置插入 `showText(...)` + `attachKeyFrame()`，并用 `idle(...)` 留出阅读时间。
   若插在中间，后面的 `text_N` 序号会整体后移——这是正常的，但**必须重跑 `runData`**，
   否则旧 lang 里的 `text_N` 会与新序号错位。
3. **改文案**：只改场景类中的英文/中文参数，不碰生成的 json。
4. **改结构展示**：优先调整 NBT 与 `showSection` 选区，不要在场景里堆坐标魔法数字。
5. **删除步骤**：同步删掉对应 `showText`，否则会留下无意义的一步并让后续 key 空洞。
6. 重跑 `runData` 并核验 key 数量变化。

**验收**：场景步骤与文案自洽；`zh_cn.json` 与 `en_us.json` 的 key 集合完全一致；没有遗留孤立的 `text_N`。

## 工作流 C：新增或调整 PonderTag

1. 在模块 `*PonderTags` 中声明 `ResourceLocation` 常量：
   `ResourceLocation.tryBuild(<MODID>, "<tag_path>")`。
2. 用共享助手注册并写 tag 名与描述的双语：
   ```java
   CTNHPonderTagHelper.registerTag(REGISTRATE, helper, <tag>,
           "English name", "中文名",
           "English description", "中文描述")
           .addToIndex()
           .item(<代表物品>, true, false)
           .register();
   ```
   lang key 由助手生成为 `<namespace>.ponder.tag.<path>` 与 `...` + `.description`。
   `addToIndex()` 决定它是否出现在索引里；`item(item, true, false)` 的第一个布尔是当图标，第二个是当主物品。
3. 用 `helper.addToTag(<tag>).add(...)` 批量挂组件；`addStoryBoard(..., tags...)` 的重载可让场景自带 tag 高亮。
4. 重跑 `runData`，确认 tag 名与描述在两种语言里都在。

**验收**：`/ponder tags` 能看到该 tag；tag 图标显示正常；描述不显示为 key；空 tag（没有成员）要么补成员要么不要 `addToIndex()`。

## 工作流 D：排障

按症状查表，不要猜。

| 症状 | 可能原因 | 动作 |
|------|----------|------|
| 组件完全不显示 Ponder 提示 | 场景没注册；插件没在客户端 setup 注册；注册发生在注册期结束后 | 检查 `*PonderScenes.register` 的这一行与 `ClientProxy` 的 `PonderIndex.addPlugin(...)`；注册期结束会抛 `IllegalStateException("Registration Phase has already ended!")` |
| 场景能开但是**空世界** | storyboard 路径与文件不匹配 | 看日志 `Ponder schematic missing: <ns>:ponder/<path>.nbt`，按命名空间/路径/扩展名逐段对齐 |
| 文案显示成 `xxx.ponder.yyy.title` | lang 未生成或被覆盖 | 把模块加进 `CommonProxy.gatherData()` 的 `includeClient()` 分支调 `CTNHPonderLang.init(...)`，再跑 `runData` |
| 只有中文/只有英文 | 只改了一侧或手改了生成物 | 改场景类，重跑 `runData`，禁止直接补 json |
| 改完文案没变化 | 忘记 datagen；或用了 `showText(ticks, Lang)` 走了注解文案 | 重跑 `runData`；确认该处用的是 `(en, cn)` 重载 |
| 步骤顺序/文案对不上 | 插删步骤后未重生成 lang | 重跑 `runData`，核对 `text_N` 序号 |
| 场景下标越界/看不到方块 | `util.grid().at(...)` 坐标与 NBT 结构不一致 | 用 `util.select().fromTo(...)` 选区与 NBT 对齐；先 `showSection` 再操作 |
| tag 不出现 | 没 `addToIndex()`，或没 `register()` | 补齐调用链，重跑 `runData` |
| 场景里结构错位/悬空 | 蓝图的 `pos` 与 `pattern` 还原不一致，或忘了套地板 | 用 `--print` 看 footprint 与控制器坐标，再和 `aisle` 对照 |
| **场景里机器左右镜像**（仓室/控制器开口在错误一侧） | 只翻转了 y，没按 `setActualRelativeOffset` 同时翻转 x/z | 读 [references/storyboard-nbt.md](references/storyboard-nbt.md) 3.1；`x = -i`、`y = +j`、`z = -k` |
| **文案显示 `Format error:` 后跟原文** | 文案里写了字面 `%`。Ponder 文案走 `I18n`/`Component` 格式化，裸 `%` 抛 `UnknownFormatConversionException` | 百分比改写"个百分点"等文字，或转义成 `%%`。**这是文案层问题，与 datagen 无关**——`runData` 照常通过 |
| 讲解某个仓室时**看不到它**（默认镜头只露 NORTH/WEST） | 仓室在背面（EAST/SOUTH 面），没转镜头 | 讲背面的部件前 `scene.rotateCameraY(180)`，讲完再 `-180` 转回。别为了镜头去改仓室朝向 |
| `rotateSection` 转的不是该转的东西 | 把"机器外壳"当成旋转体。真实旋转体由机器自己决定 | 读机器的 `getContraptionRotationAxis()` / `getAssemblyPivot()`（或 `IContraptionMultiblock`）确定是哪批方块、绕哪根轴 |
| 生成时报"没有 controller"或"y=0 保留" | 蓝图漏标主方块，或结构压到了地板层 | 给主方块加 `"controller": true`；结构 y 从 1 起 |
| 管道在场景里是**一根光柱、没连上** | GT 管道的连接存在 BE 的 `connections` 位掩码里，Ponder 不跑 tick 不会自动连 | 在蓝图该方块的 `nbt` 里写 `"connections"`（竖直贯通 = 3）；见 [references/storyboard-nbt.md](references/storyboard-nbt.md) 第 6 节 |
| 桶/储罐等 `RotationState.NONE` 机器被补了 `facing` | 脚本默认给 controller 补朝向，但这类机器 blockstate 没有该属性 | 蓝图里写 `"controller_props": false`；见 [references/storyboard-nbt.md](references/storyboard-nbt.md) 第 4.1 节 |
| 同一方块要在不同步骤"换位置" | 用坐标魔法数字或准备两份 NBT | `showIndependentSection` + `moveSection`，见 [references/api-cheatsheet.md](references/api-cheatsheet.md) |
| 机器 UI 面板没出现 | 这一段没调 `scene.showUI(...)`，或 `show(ticks)` 太短 | 面板是**逐段**登记的：每段都要自己 `scene.showUI(ui)`；`show(...)` 按演示内容留够时间 |
| **画了 `showUI` 但面板完全不出现** | 整段只写了 `.at(...)` 没写 `.machinePos(pos)`；或者 `machinePos(pos)` 指的坐标上不是那台机器（storyboard 里主方块常与场景文案惯用的坐标差一格）。现在不再兜底猜锚点所在的那一格，而是一行 error 且这一段什么都不画 | 按日志分三种情况：`this UI segment has no machine position …` 说明缺机器坐标，补 `.machinePos(pos)`；`no block entity at <坐标> …` 说明那一格没有方块实体（多半是代码 `setBlock` 摆的机器，要写进 storyboard）；`the block at <坐标> (<方块>) produced no panel …` 说明坐标对了但建不出面板。对着日志里的坐标去 storyboard 的 palette+blocks 查主方块真实位置 |
| 面板里的数字框/文本框**是空的** | 那个控件没开 client-side：LDLib `TextFieldWidget` 只在 client-side 模式下每帧从 `textSupplier` 取文本（构造函数不初始化文本） | Lib 的面板构建器已给槽位、储罐、进度条、文本框统一打开这个开关；**自己新建控件容器时要照做** |
| 改了机器字段，面板上的数字**不跟着变** | 直接 `modifyBlockEntityNBT` 不会请求面板重建，控件读的还是旧值 | 写成 `MachineEdit` 用 `MachineEdits.add(...)` 挂上时间线，落地后会自动重建面板 |
| 两块面板叠在一起，或反而不该同时出现 | 按先后写了两条 `showUI`，或两块锚点挨太近 | `showUI` 是非阻塞的，连续两条本来就会同屏：用 `.pointing(...)` 往不同侧推，挤不开就分成两段 |
| 日志 `there is no GT recipe with this id` | 配方 id 在本包里不存在；或把配方形态认错了 | 用 JEI 里那条配方的 id；本仓库的 fork 往 `RecipeManager` 里放的是 `GTRecipeDefinition`，要先 `toRuntime()` 再当 `GTRecipe` 用（`RecipeFiller.runtime(...)` 就是干这个的） |
| 配方填了但槽位/储罐对不上 | 机器的 `IngredientIO` 标签与预期不符 | 输入/输出槽位由 GT 自己打的标签决定，不要手工猜顺序；用 `outlineSlot` / `outlineTank` 核对序号 |
| 配置器里的开关点了没反应 | 思索里没有 LDLib 容器，`Toggle` 的 `isPressed` 缓存没人刷新 | `ConfiguratorTabs.syncConfigurators(...)` 每 tick 调一次 `detectAndSendChange`（Lib 已封装） |
| 点编程电路的格子没反应 | `ClickData` 的 `isRemote` 恒为 true，格子回调只在非远程时改本地槽位 | `MachineUiInteraction` 用反射造 `isRemote=false` 的 `ClickData` 直接调按钮回调，不要在场景里自己转发 |
| 「查看 UI 详情」按钮位置不对、或多出一个 | 锚点每帧重算、只有贴好那一刻才可见；重挂后旧对象要收起 | 交给 Lib 的 `PonderUiButtons`，场景里不要自己摆按钮 |
| 关掉详情后机器开关没还原 | 开关备份取的是**上一帧**登记的面板 | 面板必须每段都经 `MachineUiElement` 渲染登记；没有登记就无从还原 |
| 改了 Lib 的 UI 类，游戏里没变化 | 客户端还在跑旧类 | `:modules:CTNH-Lib:compileJava` 后**完整重启**客户端（退出重进思索界面不够） |
| `runData` 报 `fml.toml` 的 `Not enough data available` | 模块 `run/config/fml.toml` 被截断或填成零字节，属于可再生的运行目录文件 | 删除对应模块的 `run/config` 后重新运行 `runData`，不要为此修改源码或生成的语言文件 |

## 工作流 E：把 GT 机器界面画进思索（MachineUI）

共享栈里已经带了机器 UI 层：面板不是贴图，而是这台机器**真实的 fancy UI**（把 GT 的控件树直接搭出来再画），
因此槽位序号、储量、配置器、页签都是真的。能力由 Lib 提供，模块侧只写场景调用，不要自己搭控件、不要自己摆按钮。

### 场景侧写法（Core 的 `example/ChemicalReactorUi` 是完整范例）

```java
private static final MachineUI LV_UI = MachineUI.of(GTMachines.CHEMICAL_REACTOR[GTValues.LV]).scale(0.6f);
private static final MachineUI FULL_UI = MachineUI.of(GTMachines.CHEMICAL_REACTOR[GTValues.LV]).showFullUI().scale(0.6f);

scene.showUI(LV_UI).at(machinePos).show(120);                                  // 只画界面
scene.showUI(LV_UI).at(machinePos)
        .slot(1).withItem(new ItemStack(Items.GRASS_BLOCK, 64), 20)          // 按实机序号写入，1 秒内 0→目标值
        .tank(0).withFluid(new FluidStack(Fluids.WATER, 1000), 20)
        .outlineSlot(1, 20).outlineProgress(20)                             // 红框，可带延迟
        .show(160);
scene.showUI(FULL_UI).at(machinePos)
        .outlinePowerToggle(20).outlineAutoOutput(20).outlineCircuitButton(20)
        .show(160);
```

- 定义面板：`MachineUI.of(MachineDefinition | Block)`，可链式 `.scale(f)` / `.fitToPanel(f)` / `.showFullUI()` /
  `.showCircuit()` / `.showPlayerInventory()` / `.showConfigurators()` / `.showNavigationButtons()`。
  默认只画标题栏、页签与机器页；`showFullUI()` 一次画出原版整套 UI（配置器、提示面板、玩家背包都不裁）。
- 摆放：面板由**构建器**登记——`CTNHPonderSceneBuilder.showUI(MachineUI)` 返回摆放对象，再链 `.at(pos)` /
  `.at(vec)` / `.machinePos(pos)` / `.at(pos)` / `.pointing(Pointing.DOWN)` / `.scale(f)`；
  缩放要么写在定义上（`.scale(f)` / `.fitToPanel(f)`），要么写在摆放这一步。写入与红框见上面的链式调用。
- 配方：`.recipe("<配方 id>", 起始 tick)` 之后，入料、编程电路（配方带 `circuitMeta(n)` 时）、进度条、成品全自动；
  机器与配方对不上（不是配方机器、id 不存在、配方类型不符、面板没有对应槽位）只报一行 error 并跳过这一段。
- 机器状态（与界面无关，独立指令）：`MachineEdits.placeCover(scene, pos, side, item|CoverDefinition[, delay])`、
  `setWorkingModel(scene, pos, boolean[, delay])`、`setItemOutput` / `setFluidOutput` / `setAutoOutput(scene, pos, side[, delay])`；
  每一段演完与场景回退都会还原。要看输出面就把镜头转过去（`scene.rotateCameraY(180)`）。
- **要改机器自己的字段，就写一个 `MachineEdit`，不要直接 `modifyBlockEntityNBT`。** 模块专属的变更类放本模块的
  `client/ponder/machine/`：实现 `apply` / `revert`（机器不是预期那台、能力不支持时记一行 error 就返回，不要抛），
  用 `MachineEdits.add(scene, pos, edit[, delay])` 挂上时间线。落地后 Lib 会自动重画机器并 `requestRebuild()`，
  **画着这台机器的面板下一次 tick 重建**，控件才读得到新值——直接写 NBT 不会触发重建，面板上还是旧的。
- **连续变化（"一秒内递增"那类）**：`MachineEditInstruction` 同样是非阻塞的，而 `PonderScene.tick()` 会并行 tick
  所有非阻塞指令、只在遇到阻塞指令时停下，所以按 `1..N` tick 的延迟排 N 条变更就能得到逐帧爬升；
  时长跟面板里槽位/储罐的写入对齐（20 tick = 1 秒）。代价是 N 次面板重建与重画，档位可以调粗。
- **面板演过的事，不要再叠一条操作提示。** 面板已经把"往仓室里灌东西 / 填数值"演出来了，同一处的
  `showControls(...).rightClick().withItem(...)` 就删掉——同一件事说两遍反而互相打架；
  没有对应面板的动作（终端一键放置、给机器贴覆盖板等）才留提示。

### 时序：面板不占时间线

`showUI(...).show(ticks)` 走 `FadeInOutInstruction`（`TickingInstruction(false, ticks + 10)`），**非阻塞**：

- 面板与紧随其后的 `showText(...)`、`idle(...)` **并行**——想让文字与面板同屏，就照这个顺序写；
- 连续两条 `showUI(...)` 会**同时在屏上**，可以一次摆出两块面板（两种产物、两个仓室各一块）；
  要错开就 `.pointing(...)` 把它们往不同侧推，别指望时间线帮你分先后；
- 真正占时间线的是 `idle(ticks)`。`show(ticks)` 只决定面板什么时候淡出：给少了会出现"字还在、面板先没了"。
- 落点会被 `clampOffset` 拉回屏幕内，锚点贴近屏幕边缘不会被裁；但两块面板**是不是互相压住只能游戏内看**。

### 画面板之前要确认的两件事

- **哪些方块画得出来**：目标机器要实现 `IUIMachine`。多方块的仓室与总线天然满足
  （`IMultiPart extends IFancyUIMachine`）；单方块机器看它自己的实现（`MetaMachine` 本身不是 `IUIMachine`），
  不满足的那一段面板会被跳过，只在日志里留一行。
- **序号怎么定**：`slot(i)` / `tank(i)` 就是实机 UI 里**可见**控件按机器 `createUIWidget()` 添加顺序收集出来的序号。
  `LargeStackSlotWidget` 也算 `SlotWidget`；储罐同时认 GT 与 LDLib 两种 `TankWidget`。
  拿不准就用 `outlineSlot(i)` / `outlineTank(i)` 在游戏里打框确认，不要猜。

### 仓室选型：总成优先，装不下就升等级

要展示的配方**同时要物品和流体**时，优先用**输入 / 输出总成**（`GTMachines.DUAL_IMPORT_HATCH` /
`DUAL_EXPORT_HATCH`）：一块方块上就带物品格与储罐，面板也只占一块，比"物品总线 + 流体仓"少一块方块、
少一块面板，`.slot(i)` 与 `.tank(i)` 可以在同一段里一起写。总成只到 `LV..UHV`
（`GTMachineUtils.DUAL_HATCH_TIERS`）；只有物品或只有流体的场合，用对应的总线 / 仓就够。

**先数需求再挑等级**——槽位与容量都随等级走，别让演示用的仓室装不下自己引用的配方：

| 要数的东西 | 从哪来 |
|------------|--------|
| 物品格数 | `ItemBusPartMachine.INVENTORY_SIZE[tier]`：ULV 1 / LV 4 / MV 6 / HV 8 … |
| 物品每格堆叠倍率 | `ItemBusPartMachine.getSlotMultiplier(tier)`（tooltip 的 item_storage_multiplier） |
| 储罐个数 | `FluidHatchPartMachine.TANKS[tier]`：LV 2 / MV 3 / HV 4 …，总成用同一张表 |
| 单罐容量 | `FluidHatchPartMachine.getTankCapacity(8000, tier)` = `8000 × (1 << 2 × tier)`：LV 32000、MV 128000 |

输出侧同样按证据挑：**配方真的产出流体**才值得上输出总成，否则那块储罐永远是空的，用物品输出总线更贴实情
（只出物品的配方就是这种情况）。

总成的面板里**物品格在前、储罐在后**：`DualHatchPartMachine#createUIWidget()` 先 `addItemGrid` 再
`addTankGrid`，所以 `slot(0..n-1)` 是物品、`tank(0..)` 是流体，序号互不串。
只给**真有槽位或储罐**的仓室挂面板：动能仓、能源仓没有可画的槽位，给它们画面板只会得到默认的方块预览页。

### 交互：「查看 UI 详情」按钮

按钮由 Lib 的 `PonderUiButtons` + `mixin/PonderUIMixin` 挂在思索界面底部，**场景不需要做任何接线**。
它只在当前这一段是 `showFullUI()` 时出现（裁剪版不显示），点开后冻结场景，把左下配置器整列转发给 GT 原版
（开关、页签、电路设置都能点），关闭时把观众拨过的开关与展开的配置器还原。
它的位置跟着「显示方块名称」按钮走、每帧重算，锚点限定在左半边；不要自己再摆一个按钮，也不要改 Ponder 自己的按钮。

### 与本仓库 fork 的对齐（照官方 GTCEu 写会踩的坑）

| 官方 GTCEu 写法 | 本仓库 fork 的实际形态 | Lib 里的处理 |
|-----------------|------------------------|--------------|
| `RecipeManager` 里就是 `GTRecipe` | 放的是 `GTRecipeDefinition`（同样是原版 `Recipe`，带 id/inputs/outputs/duration/tier） | `RecipeFiller.runtime(...)` 认两种形态，遇到定义就 `toRuntime()` |
| `RecipeHelper.getInputItems(recipe)` | 多了 `boolean simulate` 参数 | 调用处传 `false` |
| `machine instanceof IHasCircuitSlot` | 编程电路是 `ProgrammableCircuitSlotTrait` 这个 trait | `CircuitSlots` 反射取 trait 里的 `storage`，拿不到就报一行 error 并跳过电路 UI |
| `IAutoOutputItem` / `IAutoOutputFluid` | 物品与流体都在 `AutoOutputTrait` 里 | 用 `machine.getTrait(AutoOutputTrait.class)` 加 `hasAutoOutputItem()` / `hasAutoOutputFluid()` 守卫 |

### 验证纪律

- 改 Lib 的 UI 类之后跑 `:modules:CTNH-Lib:compileJava`，然后**完整重启客户端**：类被换掉了，重启思索界面不够。
- 场景里的配方 id 必须在本包里真实存在（用 JEI 复制）；填不上时日志会写 `there is no GT recipe with this id`，
  先确认 id 再怀疑代码。
- 面板每段结束都会把写进去的物品/流体还原，所以**不要**靠上一段的残留来做下一段，每段都要自己写。
## 上游 Ponder 改动边界

需要给上游对象（Create 方块、GTCEu 多方块）加场景时，**默认只读**：在模块的 `*PonderScenes` 里
`helper.forComponents(<上游 id>)` 注册即可，不改上游代码。

确有必要向上游注册流程注入（CTPP 先例：`mixin/create/AllCreatePonderScenesMixin` 在
`AllCreatePonderScenes.register` 的 `@At("TAIL")` 追加场景）时：

- Mixin 放 `mixin/<targetmod>/`，并在 `<modid>.mixins.json` 登记；
- 上游类通常不需要 remap（`@Mixin(value = ..., remap = false)`），照现有先例写；
- 注入的场景同样要走 CTNH 双语构建器，不要在 Mixin 里硬编码文案；
- 这是例外而非常规，能量/核心模块用 `forComponents` 就够了。

## 输入与不可推断的事实

- **需要**：目标注册对象、sceneId、要讲的步骤顺序、机器结构（多方块要能读到 `pattern(...)`）。
- **不要凭空推断**：NBT 里到底摆了哪些方块、机器朝向与正面、上游 mod 的内部实现。
  这些必须来自文件、源码或玩家的实际摆放；不确定就标注为待确认。
- **不要把 UI 当成配方来源的证据**：必须从 recipe logic、输入 capability 或实际配方代码确认配方是由 UI、输入物品、流体还是其他能力选择的。
- **不要把世界坐标直接当成屏幕左右**：镜头旋转和默认可见面会改变视觉顺序；侧面步骤要在对应镜头下验证。
- **不要假装验证过**。编译通过 + `runData` 成功，只证明"代码能编译、lang 能生成"，
  **对场景是否可用几乎零信息量**。按下面的分界老实话说什么验过了：

  | 能静态验证 | 必须游戏内 `/ponder <sceneId>` 看 |
  |-----------|-----------------------------------|
  | 编译通过、lang key 成对生成 | 结构是否显示、位置是否与讲解一致 |
  | NBT 几何（尺寸/越界/地板空洞/连接掩码） | 镜头能不能看见被讲解的方块 |
  | 场景坐标与 NBT 逐格一致 | 旋转体转得对不对、朝向观感 |
  | 文案无裸 `%`（可 grep 生成物） | 文案长度是否溢出、时序是否够读完 |
  | | 部件遮挡、箭头指向、淡入淡出 |

  交付时**逐条写明哪一格验过、哪一格没验**。把"编译通过"说成"验证完成"，等于让用户
  替你做验收——本 skill 的返工大多是这样产生的。
- **上游方块 id 要落到证据上，不要靠拼名字猜。** 常见来源，按可靠度排序：
  1. 游戏注册日志——跑过一次 `runClient`/`runData` 后，`modules/<Module>/run/logs/debug.log`
     里有 `Registered <id> to registry minecraft:block`，这是运行时真值；
  2. 生成物——`src/generated/resources/assets/<mod>/blockstates/<name>.json`、`models/`；
  3. 注册代码——例如 GT 管道是 `"%s_%s_fluid_pipe".formatted(material.getName(), pipeType.name)`
     （→ `bronze` + `normal` = `gtceu:bronze_normal_fluid_pipe`）。
  注意上游 mod 的 `langValue` 显示名（"Normal Bronze Fluid Pipe"）**不等于**注册 id，别直接转换。

## 本仓库的构建环境事实（datagen 前置）

跑 `runData` 前先确认这三件事，否则会在构建系统上报错而不是在 Ponder 上报错：

1. **JDK**：项目目标 Java 17，但机器上可能只有 JDK 21（`~/.gradle/jdks/eclipse_adoptium-21-*`），
   21 可以跑构建。
2. **Gradle 版本**：仓库 wrapper 锁 9.1.0；但根 `settings.gradle` 的
   `org.gradle.toolchains.foojay-resolver-convention` 若为 `0.5.0`，在 Gradle 9 上会直接抛
   `JvmVendorSpec does not have member field 'IBM_SEMERU'`。临时调到 `1.0.0` 可解，
   **验证完必须还原**（它属于根仓库，不属于本模块改动）。
3. **Gradle 8.x 不可用**：`modules/GregTech-Modern/gradle/scripts/moddevgradle.gradle` 用了
   `failOnNoDiscoveredTests`，8.14 没有该属性；不要靠降版本绕。

命令模板：

```bash
JAVA_HOME=~/.gradle/jdks/eclipse_adoptium-21-amd64-windows.2 ./gradlew :modules:<Module>:runData --console=plain
```

**spotlessCheck 的红灯要先归因**：Windows 检出下 CRLF 与仓库 LF 不一致会让 spotless 报
几百个**既有**文件违规。用 `| Select-String <你的文件名>` 过滤——你的文件不在列表里就说明
不是你的问题，不要为此重排整个仓库的换行。

## 何时提问、停止或拒绝

- 锚点不是注册对象、或组件没有任何可指向的 id → 先问用哪个对象，不要编造 id。
- sceneId 会决定 lang key 与 NBT 路径，用户已有约定时按用户的；没有时给出建议再确认。
- 结构与步骤描述不足以决定 NBT → 停下来说明缺少什么，不要凭想象写坐标。
- 要求"直接改 `src/generated/resources` 的 json"→ 拒绝并改走 datagen。
- 要求手工拼 `.nbt` 二进制或手搭结构 → 改走脚本生成；脚本报错先修蓝图，不要绕开校验。
- 要求把模块专属场景搬进 CTNH-Lib → 拒绝，说明模块边界。
- 要求改动 vendored `GregTech-Modern` 内部 → 除非任务明确指向 GTCEu 内部，否则拒绝。

## 配套文件

- API 速查（构建器/注册助手/lang 规则/接线站点）：[references/api-cheatsheet.md](references/api-cheatsheet.md)
- storyboard NBT 格式、地板/尺寸/朝向规则与自动生成：[references/storyboard-nbt.md](references/storyboard-nbt.md)
- 落地检查清单与本 skill 自测请求：[references/checklist.md](references/checklist.md)
- 模板：场景类 [assets/scene-template.java.txt](assets/scene-template.java.txt)、
  场景注册 [assets/scenes-registration-template.java.txt](assets/scenes-registration-template.java.txt)、
  tag 注册 [assets/tags-registration-template.java.txt](assets/tags-registration-template.java.txt)、
  模块适配层 [assets/module-adapter-templates.java.txt](assets/module-adapter-templates.java.txt)、
  机器 UI 场景 [assets/machine-ui-scene-template.java.txt](assets/machine-ui-scene-template.java.txt)
