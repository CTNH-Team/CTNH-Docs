---
name: ctnh-ponder
description: >-
  CTNH 模组的 Create Ponder（思索）场景开发与排障指南。覆盖 CTNH-Lib 共享构建器
  （CTNHPonderSceneBuilder / CTNHPonderLang / CTNHPonderTagHelper）、CTNH-Core /
  CTNH-Energy / CTNH-Mana / CTPP 各自的 Plugin-Scenes-Tags 适配层、
  assets/<modid>/ponder/<path>.nbt storyboard 资源，以及双语 lang 的 datagen 规则。
  新增或修改思索场景、调整 PonderTag、给模块补齐 Ponder 适配层、按上游 Create/GTCEu 补场景、
  或排查场景不显示 / 文案显示成 lang key 时使用。Triggers: Ponder, 思索, pondering, storyboard,
  CTNHPonderSceneBuilder, PonderTag, addStoryBoard, ponder nbt, 场景不显示
---

# CTNH Ponder

CTNH 的思索（Ponder）不是 Create 原生写法的直接复制：**共享能力在 CTNH-Lib，场景与注册在所属模块，
文案双语内嵌且只能经 registrate 走 datagen**。本 skill 描述这条链路的做法、边界与排障。

## 何时使用

- 给某台机器/方块新增一个思索场景。
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
   - 现有 storyboard 注册条数：Core 5、Energy 24、Mana 6、CTPP 6，另有 CTPP 对 Create 的 Mixin 注入。

## 三层结构（唯一所有权）

| 层 | 位置 | 职责 |
|----|------|------|
| 共享栈 | CTNH-Lib `client/ponder/` | `CTNHPonderSceneBuilder`（双语标题/正文、底板与缩放、`rotateAround`）、`CTNHPonderLang`（lang 抽取）、`CTNHPonderTagHelper`（tag lang） |
| 模块适配层 | `<Module>/client/ponder/` | 每模块一个 `*PonderPlugin` / `*PonderScenes` / `*PonderTags` / `*PonderSceneBuilder` + 场景类 |
| 资源与文案 | `src/main/resources/assets/<modid>/ponder/**/*.nbt`、`src/generated/resources/assets/<modid>/lang/{en_us,zh_cn}.json` | storyboard 结构；lang 由 datagen 生成，禁止手改 |

四个模块的落点：

| 模块 | 包 | 场景分组 |
|------|----|----------|
| CTNH-Core | `io.github.cpearl0.ctnhcore.client.ponder` | `Electric/`、`Kinetic/`、`Misc/`（不属于前两类的通用内容，如桶） |
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
| 生成时报"没有 controller"或"y=0 保留" | 蓝图漏标主方块，或结构压到了地板层 | 给主方块加 `"controller": true`；结构 y 从 1 起 |
| 管道在场景里是**一根光柱、没连上** | GT 管道的连接存在 BE 的 `connections` 位掩码里，Ponder 不跑 tick 不会自动连 | 在蓝图该方块的 `nbt` 里写 `"connections"`（竖直贯通 = 3）；见 [references/storyboard-nbt.md](references/storyboard-nbt.md) 第 6 节 |
| 桶/储罐等 `RotationState.NONE` 机器被补了 `facing` | 脚本默认给 controller 补朝向，但这类机器 blockstate 没有该属性 | 蓝图里写 `"controller_props": false`；见 [references/storyboard-nbt.md](references/storyboard-nbt.md) 第 4.1 节 |
| 同一方块要在不同步骤"换位置" | 用坐标魔法数字或准备两份 NBT | `showIndependentSection` + `moveSection`，见 [references/api-cheatsheet.md](references/api-cheatsheet.md) |

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
- **不要假装验证过**：`runData` 只证明 lang；场景的观感、镜头、时序需要在游戏内确认。
  只编译通过不等于场景可用。
- **上游方块 id 要落到证据上，不要靠拼名字猜。** 常见来源，按可靠度排序：
  1. 游戏注册日志——跑过一次 `runClient`/`runData` 后，`modules/<Module>/run/logs/debug.log`
     里有 `Registered <id> to registry minecraft:block`，这是运行时真值；
  2. 生成物——`src/generated/resources/assets/<mod>/blockstates/<name>.json`、`models/`；
  3. 注册代码——例如 GT 管道是 `"%s_%s_fluid_pipe".formatted(material.getName(), pipeType.name)`
     （→ `bronze` + `normal` = `gtceu:bronze_normal_fluid_pipe`）。
  注意上游 mod 的 `langValue` 显示名（"Normal Bronze Fluid Pipe"）**不等于**注册 id，别直接转换。

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
  模块适配层 [assets/module-adapter-templates.java.txt](assets/module-adapter-templates.java.txt)
