# CTNH Ponder 落地检查清单

逐条打勾；任一条不满足就不要声称完成。

## 新建场景

- [ ] storyboard 由蓝图 + `scripts/build_storyboard_nbt.py` 生成，没有手工拼二进制
- [ ] y=0 铺满地板，材质按时代选（`create:andesite_casing` / `create:railway_casing`）
- [ ] 地板尺寸 = 结构水平外接矩形每边外扩 1 格（每轴 +2）
- [ ] 多方块结构逐条对照机器定义的 `pattern(...)` 还原，`Predicates.air()` 的符号未放方块
- [ ] 主方块标了 `"controller": true`；朝向类方块为 `facing=north` + `upwards_facing=north`
- [ ] 不对称结构的 K/E 等能力符号已按 `BlockPattern` 映射核对，未发生左右镜像或能力仓错位
- [ ] 场景中新放置的朝向类仓室显式设置了 `FACING`；`facing`、`pointAt` 面与当前镜头可见面一致
- [ ] 不同能力仓使用不同 outline 颜色，并逐个确认文案目标不是相邻的另一仓室
      （`RotationState.NONE` 的机器如桶/储罐例外：写 `"controller_props": false`，不带朝向属性）
- [ ] 若结构里有 GT 管道，该方块的 `nbt` 写了 `connections` 位掩码（竖直贯通 = 3）；
      否则场景里会是一根没连上的光柱
- [ ] `--print` 的 footprint 与 `aisle` 一致，`--check` 无 warning
- [ ] 锚点是注册对象，用 `<RegistryObject>.getId()`，没有字符串拼 id
- [ ] sceneId 稳定、蛇形、与 storyboard 文件名语义一致
- [ ] storyboard 位于 `src/main/resources/assets/<modid>/ponder/<path>.nbt`，与 `addStoryBoard("<path>")` 完全对应
- [ ] 场景类使用模块 `*PonderSceneBuilder`（继承 `CTNHPonderSceneBuilder`），文案全走双语重载
- [ ] 场景以 `title(...)` 开头、`markAsFinished()` 结尾，步骤间有 `idle` 与 `attachKeyFrame`
- [ ] 同一机器的多个相关思索可共用一个 Java 类，但各自有独立静态方法、sceneId、注册路径和 NBT
- [ ] 文案描述的配方触发方式来自 recipe logic / capability 证据，没有把不存在的 UI 操作写进场景
- [ ] 连续动作的节奏按 tick 设计（20 tick = 1 秒；半秒间隔 = `idle(10)`），没有连续 `showText` 重叠
- [ ] 注册写入 `*PonderScenes.register`，带 tag（若非刻意不加）
- [ ] 无硬编码方块/物品 id；结构展示来自 NBT 与 `util.select()`，场景坐标与生成的 NBT 一致
- [ ] 未新增仅客户端类到 `common/` 引用链
- [ ] 讲"两种布局/两种接法"时用 `showIndependentSection` + `moveSection` 表达，没有为同一方块准备两份 NBT
- [ ] 粒子/流动效果用 `effects().emitParticles(...)`，锚点取方块中心，且不阻塞后续步骤

## 修改/扩展场景

- [ ] 插入或删除步骤后重跑 `runData`
- [ ] `zh_cn.json` 与 `en_us.json` 的 ponder key 集合完全一致
- [ ] 没有孤立的 `text_N`（不存在对应 `showText`）
- [ ] 关键帧位置仍能覆盖新步骤

## PonderTag

- [ ] tag `ResourceLocation` 常量在模块 `*PonderTags` 中声明，命名空间为模块 modId
- [ ] 名称与描述走 `CTNHPonderTagHelper.registerTag`（双语），没有手写 lang key
- [ ] 调用链以 `.register()` 收尾；是否 `addToIndex()` 有明确理由
- [ ] 通过 `helper.addToTag(...)` 或 `addStoryBoard(..., tags)` 与组件关联，不是空 tag

## datagen 与验证

- [ ] `:modules:<Module>:runData` 通过
- [ ] `src/generated/resources/assets/<modid>/lang/en_us.json` 与 `zh_cn.json` 中 `.ponder.` 条目成对
- [ ] 用 `scripts/check_ponder_lang.py` 按 scene 前缀检查 `header`、`title` 和连续的 `text_N`
- [ ] 未手工修改 `src/generated/resources`
- [ ] 有条件时游戏内用 `/ponder <sceneId>` 验证观感与节奏（编译通过 ≠ 可用）
- [ ] `spotlessCheck` 通过

## 边界与纪律

- [ ] 共享能力没有下沉到 CTNH-Lib，模块专属助手没有上移到 Lib
- [ ] 未改 vendored `GregTech-Modern`
- [ ] 上游注入（如有）放在 `mixin/<targetmod>/` 且登记进 `<modid>.mixins.json`
- [ ] 未触碰 `build/`、`run/`、`src/generated/resources`

## 本 skill 的自测请求

用下列请求检验触发与产出；前四类必须命中，第五类必须不命中。

1. **直接**：「给 CTNH-Core 的 XX 多方块加一个思索场景，讲怎么搭建。」
   → 应命中：读 Core client 指南、走 `CTNHPonderSceneBuilder`、产出场景类 + 注册行 + NBT 落位 + `runData` 核验。
2. **间接**：「这机器玩家老不会搭，做个 Create 那种演示。」
   → 应命中同一流程（"演示/教学/Ponder/思索" 都算触发）。
3. **信息不全**：「随便加个场景吧。」
   → 应提问：锚点组件、sceneId、要讲的步骤、结构 NBT 来源；不得编造 id 与坐标。
4. **排障**：「场景能打开但是空世界 / 文案显示成 ctnhcore.ponder.xxx.title。」
   → 应给出 storyboard 路径与 lang datagen 两条定位路径，而不是泛泛而谈。
5. **生成 NBT**：「给土高炉做个 3x3x4 的思索结构。」
   → 应读 `PRIMITIVE_BLAST_FURNACE` 的 `pattern(...)`、还原结构、机械时代铺安山机壳地板、
   结构 3x3 → 地板 5x5、主方块 `facing=north`，并用脚本产出并 `--check`。
6. **不该触发**：「给这台机器加个 Jade 显示 / 加个 EMI 分类 / 改 GT 配方。」
   → 不应触发本 skill（走 ctnh-docs 对应模块指南与 `_architecture/AGENTS.md`）。
