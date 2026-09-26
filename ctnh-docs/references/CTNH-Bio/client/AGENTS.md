# CTNH-BIO CLIENT DOMAIN

## OVERVIEW
Bio 的客户端渲染、模型与思索场景（19 个 Java 文件）：活体机器实体渲染、可染色渲染器族、基于 GeckoLib 的模型注册表、意识装配机 Ponder 思索场景，以及客户端代理。

## STRUCTURE
```
client/
├─ ClientProxy.java
├─ Text/                     # ModelOutputLine（模型输出行文本）
├─ model/                    # BioelectricForgeModel, BioReactorModel, CBModels, DecomposerModel,
│                            #   DigesterModel, GreatFleshModel, VatModel
├─ ponder/                   # CTNHBioPonderPlugin, CTNHBioPonderSceneBuilder,
│                            #   CTNHBioPonderScenes, CTNHBioPonderTags, CogniAssembler
└─ renderer/                 # BasicLivingMachineEntityRenderer, ColorableEntityRenderer,
                             #   ColorableMachineBlockEntityRenderer, ColorableMachineItemRenderer,
                             #   LivingMetaMachineBERProvider
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| 客户端代理 | `client/ClientProxy.java` |
| 实体渲染 | `client/renderer/BasicLivingMachineEntityRenderer.java` |
| 可染色渲染 | `client/renderer/ColorableEntityRenderer.java`, `ColorableMachineBlockEntityRenderer.java`, `ColorableMachineItemRenderer.java` |
| 模型按名分发 | `client/renderer/LivingMetaMachineBERProvider.java`（`CBModels.MODELS.get(name)`） |
| 模型定义 | `client/model/CBModels.java` 及各 `*Model` 类 |
| 客户端文本 | `client/Text/ModelOutputLine.java` |
| Ponder 插件 | `client/ponder/CTNHBioPonderPlugin.java`（`getModId` / `registerScenes` / `registerTags`） |
| Ponder 场景 / tag 登记 | `client/ponder/CTNHBioPonderScenes.java`, `client/ponder/CTNHBioPonderTags.java`（tag `BioMultiblock` = `ctnhbio:bio_multiblock`） |
| Ponder 场景适配器 | `client/ponder/CTNHBioPonderSceneBuilder.java`（继承 CTNH-Lib `CTNHPonderSceneBuilder`） |
| 意识装配机思索场景 | `client/ponder/CogniAssembler.java`（`common(SceneBuilder, SceneBuildingUtil)`，`cogni_assembler` 剧本） |

## CONVENTIONS
- 可染色渲染器族服务于可染色的活体机器内容：实体 / 方块实体 / 物品三种渲染器共用同一套模型与颜色参数。
- `LivingMetaMachineBERProvider` 是机器与模型的唯一绑定入口，模型按 key 从 `CBModels.MODELS` 取；新增机器模型在 `CBModels` 注册，不要在机器类里直接 new 渲染器。
- `ClientProxy` 只在客户端分发路径构造（`CTNHBio` 经 `DistExecutor.unsafeRunForDist` 选择 `ClientProxy` / `CommonProxy`），客户端专属类不得进入 common 构造路径。
- Ponder 接线：`ClientProxy.onClientSetup(FMLClientSetupEvent)` 在 `event.enqueueWork` 中把 `CTNHBioPonderPlugin` 注册进 `PonderIndex`；`CommonProxy.gatherData(GatherDataEvent)` 在 `event.includeClient()` 时调 CTNH-Lib `CTNHPonderLang.init(new CTNHBioPonderPlugin())` 抽取思索 lang。
- `CTNHBioPonderScenes.register` 把 `CBMultiblocks.COGNI_ASSEMBLER` 绑定到剧本 `cogni_assembler/common`（资源 `assets/ctnhbio/ponder/cogni_assembler/common.nbt`），场景实现为 `CogniAssembler::common`，tag 为 `CTNHBioPonderTags.BioMultiblock`。
- `CTNHBioPonderTags.register` 经 CTNH-Lib `CTNHPonderTagHelper.registerTag` 注册 `ctnhbio:bio_multiblock`（英文 `Biological Multiblocks` / 中文 `生物多方块机器`）并 `.addToIndex()`，用 `CBMultiblocks.COGNI_ASSEMBLER.getItem()` 作条目，随后 `helper.addToTag(BioMultiblock).add(CBMultiblocks.COGNI_ASSEMBLER.getId())`。
- 场景文案用 `scene.title(sceneId, en, cn, ...)` / `scene.showText(duration, en, cn)` 双语内联在场景类里；datagen 时由 `CTNHBioPonderSceneBuilder.registerLang` 经 `CTNHBio.REGISTRATE.genLang(key, en, cn)` 产出 lang 条目（仅 `GTCEu.isDataGen()` 时写入），场景使用 `scene.init7x7(util)` 布局。

## ANTI-PATTERNS
- 把渲染逻辑写进机器实现类（`machine/`、`api/machine/`）。
- 绕过 `CBModels` / `LivingMetaMachineBERProvider` 直接构造模型或渲染器。
- 在场景类里硬编码单语文本，或在非 datagen 路径调用 `genLang`。
- 把 Bio 专属的 Ponder 插件 / 场景 / tag 搬到 CTNH-Lib；共享的场景构建器只放 CTNH-Lib。

## SCOPE
`src/main/java/com/moguang/ctnhbio/client` 及其全部子包。

## READ WHEN
- 修改活体机器渲染器、可染色渲染或模型。
- 新增机器模型或调整模型-机器绑定。
- 新增或修改 Bio 的 Ponder 场景、tag 与双语文案。

## SOURCE OF TRUTH
- `client/renderer/` 与 `client/model/` 的实现，以及实体 / 机器的渲染注册点（`api/item/LivingMetaMachineItem.java` 与 `client/renderer/LivingMetaMachineBERProvider.java`）。
- `client/ponder/` 的实现，以及思索注册点 `client/ClientProxy.java` 与 `common/CommonProxy.java`。

## WORKFLOW
1. 先看 `LivingMetaMachineBERProvider` 与 `CBModels` 的现有绑定，再决定模型 key。
2. Ponder 场景在 `CTNHBioPonderScenes` / `CTNHBioPonderTags` 登记，场景实现放 `client/ponder/`；文案改动后跑 `:modules:CTNH-Bio:runData` 刷新 lang。
3. 跑 `:modules:CTNH-Bio:build`；渲染与思索改动需在客户端运行中目视验证。
