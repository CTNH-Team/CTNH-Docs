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

## 四个模块的接线点

| 模块 | ClientProxy 注册 | gatherData lang 抽取 | 适配层 |
|------|------------------|----------------------|--------|
| CTNH-Core | `ClientProxy.onClientSetupEvent` → `PonderIndex.addPlugin(new CTNHCorePonderPlugin())` | `CommonProxy.gatherData` `includeClient()` → `CTNHPonderLang.init(new CTNHCorePonderPlugin())` | `CTNHCorePonderSceneBuilder` + `REGISTRATE.genLang` |
| CTNH-Energy | `ClientProxy` → 同上 | 同上 | `CTNHEnergyPonderSceneBuilder` |
| CTNH-Mana | `ClientProxy` → 同上 | 同上 | `CTNHManaPonderSceneBuilder` |
| CTPP | `ClientProxy.onClientSetup` → 同上 | 同上 | `CTPPPonderSceneBuilder` + `CTPPRegistration.REGISTRATE` |

## 调试命令（Ponder 自带）

`/ponder`（打开 tags）、`/ponder index`、`/ponder tags`、`/ponder <scene id>`、
`/ponder reload`；客户端配置 `editingMode` 打开后会显示更多调试信息（含未注册文案占位）。
