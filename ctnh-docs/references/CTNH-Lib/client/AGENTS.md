# CTNH-LIB CLIENT DOMAIN

## OVERVIEW
客户端共享基础设施（7 个 Java 文件）：`ClientProxy` 引导、方块高亮渲染、共享 Ponder 框架（场景基类 / lang 抽取 / tag 助手）。

## STRUCTURE
```text
client/
├── ClientProxy.java
├── ponder/                    # CTNHPonderLang, CTNHPonderSceneBuilder, CTNHPonderTagHelper
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
| 颜色数据 | `client/render/ColorData.java` |

## CONVENTIONS
- `ClientProxy extends CommonProxy`，标注 `@Mod.EventBusSubscriber(modid = CTNHLib.MODID, bus = FORGE, value = Dist.CLIENT)`；`onRenderLevel(RenderLevelStageEvent)` 转调 `HighlightRender.hook(event)`。`ClientProxy.init()` 为空实现。
- 高亮状态由 `HighlightHandler.highlight(pos, dim, expireTime, color[, ...])` 写入、`expire()` 清理；`BlockHighlightPacket` 以 `System.currentTimeMillis() + 10000` 与 `ColorData.RED` 触发 10 秒高亮。
- `CTNHPonderSceneBuilder extends CreateSceneBuilder`：提供 `init5x5` / `init7x7` / `init9x9` / `initAll` 底板与缩放、`rotateAround(duration)` 四向环绕、双语 `title(sceneId, en, cn)` 与 `title(sceneId, headerEn, headerCn, titleEn, titleCn)`、`showText(duration, en, cn)` 与 `showText(duration, Lang)`。
- 场景 lang key 形如 `<modId>.ponder.<sceneId>.<title|header|text_N>`；双语注册经构造参数传入的 `LangRegistrar`（默认 `NOOP`），未提供 modId 时 `sceneLangKey` 抛 `IllegalStateException`。
- `CTNHPonderLang.init(PonderPlugin plugin)`：注册插件 → `PonderIndex.registerAll()` → lang access 为 `PonderLocalization` 时调 `generateSceneLang()`。
- `CTNHPonderTagHelper.registerTag(...)` 用 `CNRegistrate.genLang` 写 tag 名与描述，key 为 `<namespace>.ponder.tag.<path>` 与 `<...>.description`。
- 消费方：Core、Energy、Mana、CTPP 各自的 `client/ponder/*SceneBuilder` + `*PonderTags`，在其 `CommonProxy` 中接线。

## ANTI-PATTERNS
- 把模块专属 Ponder 场景 / tag / 插件或 Energy 的 AE2 线缆助手搬进 Lib。
- 在 Lib 里加模块专属 GUI 逻辑；客户端域只承载共享基础设施。

## SCOPE
适用于 `src/main/java/tech/vixhentx/mcmod/ctnhlib/client` 及其子包。

## READ WHEN
- 改高亮渲染、共享 Ponder 场景基类 / lang 抽取 / tag 注册助手。

## SOURCE OF TRUTH
- `client/ClientProxy.java`（引导）、`client/ponder/CTNHPonderSceneBuilder.java`（场景契约）、`client/render/highlight/HighlightHandler.java`。

## WORKFLOW
1. 先确认改动确实跨模块共享，再动 Lib 客户端代码。
2. 检查受影响消费方（Core / Energy / Mana / CTPP 的 Ponder 适配与高亮调用点）。
3. 跑 `:modules:CTNH-Lib:build` 与最小消费模块任务。
