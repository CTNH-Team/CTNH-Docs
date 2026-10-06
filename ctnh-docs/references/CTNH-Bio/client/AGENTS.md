# CTNH-BIO CLIENT DOMAIN

## OVERVIEW
Bio 的客户端渲染、模型与 Ponder 思索场景（20 个 Java 文件）：活体机器实体渲染、可染色渲染器族、基于 GeckoLib 的模型注册表、Create Ponder 插件与场景，以及客户端代理。

## STRUCTURE
```
client/
├─ ClientProxy.java           # 客户端代理：Ponder 插件注册
├─ Text/                      # ModelOutputLine（模型输出行文本）
├─ model/                     # BioelectricForgeModel, BioReactorModel, CBModels, DecomposerModel,
│                             #   DigesterModel, GreatFleshModel, VatModel
├─ ponder/                    # CTNHBioPonderPlugin, CTNHBioPonderSceneBuilder,
│                             #   CTNHBioPonderScenes, CTNHBioPonderTags,
│                             #   CogniAssembler, GreatFlesh
└─ renderer/                  # BasicLivingMachineEntityRenderer, ColorableEntityRenderer,
                              #   ColorableMachineBlockEntityRenderer, ColorableMachineItemRenderer,
                              #   LivingMetaMachineBERProvider
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| 客户端代理 | `client/ClientProxy.java`（`FMLClientSetupEvent` 中 `PonderIndex.addPlugin(new CTNHBioPonderPlugin())`） |
| 实体渲染 | `client/renderer/BasicLivingMachineEntityRenderer.java` |
| 可染色渲染 | `client/renderer/ColorableEntityRenderer.java`, `ColorableMachineBlockEntityRenderer.java`, `ColorableMachineItemRenderer.java` |
| 模型按名分发 | `client/renderer/LivingMetaMachineBERProvider.java`（`CBModels.MODELS.get(name)`） |
| 模型定义 | `client/model/CBModels.java` 及各 `*Model` 类 |
| 客户端文本 | `client/Text/ModelOutputLine.java` |
| Ponder 插件 | `client/ponder/CTNHBioPonderPlugin.java`（`registerScenes` → `CTNHBioPonderScenes`；`registerTags` → `CTNHBioPonderTags`） |
| Ponder 场景注册 | `client/ponder/CTNHBioPonderScenes.java`：`CBMultiblocks.COGNI_ASSEMBLER` 绑定 `cogni_assembler/common`；`CBMultiblocks.GREAT_FLESH` 绑定 `great_flesh/growth` 与 `great_flesh/differentiation`；均挂 `CTNHBioPonderTags.BioMultiblock` |
| Ponder 场景类 | `client/ponder/CogniAssembler.java`（`common`）、`client/ponder/GreatFlesh.java`（`growth` / `differentiation`） |
| Ponder 机器界面 | `client/ponder/CogniAssembler.java`、`client/ponder/GreatFlesh.java`（CTNH-Lib `MachineUI`：意识装配机演 I 位数据模型接口、LV 输入总成与 LV 物品输出总线；巨型肉块分化演 MV 输入总成） |
| Ponder tag | `client/ponder/CTNHBioPonderTags.java`（`BioMultiblock` = `ctnhbio:bio_multiblock`，经 `CTNHPonderTagHelper` 注册并加入 `COGNI_ASSEMBLER` / `GREAT_FLESH`） |
| Ponder 场景适配器 | `client/ponder/CTNHBioPonderSceneBuilder.java`（继承 CTNH-Lib `CTNHPonderSceneBuilder`，构造传入 `CTNHBio.MODID`，datagen 时经 `REGISTRATE.genLang` 产出 lang） |

## CONVENTIONS
- 可染色渲染器族服务于可染色的活体机器内容：实体 / 方块实体 / 物品三种渲染器共用同一套模型与颜色参数。
- `LivingMetaMachineBERProvider` 是机器与模型的唯一绑定入口，模型按 key 从 `CBModels.MODELS` 取；新增机器模型在 `CBModels` 注册，不要在机器类里直接 new 渲染器。
- `ClientProxy` 只在客户端分发路径构造（`CTNHBio` 经 `DistExecutor.unsafeRunForDist` 选择 `ClientProxy` / `CommonProxy`），客户端专属类不得进入 common 构造路径。
- Ponder 场景文案用 `scene.title(..., en, cn)` / `scene.showText(..., en, cn)` 双语直接内联在场景类里；datagen 时由 `CTNHBioPonderSceneBuilder.registerLang` 经 `REGISTRATE.genLang(key, en, cn)` 写入 lang（仅 `GTCEu.isDataGen()` 时）。
- Ponder 机器界面经 CTNH-Lib `MachineUI` 摆放：`scene.showUI(ui).at(anchor).machinePos(pos)` 把面板绑定到 `pos` 处的机器方块；`at(Vec3)` 后必须补 `machinePos(pos)`，`MachineUiAnchor` 在编译期强制（缺了无法调 `slot` / `show`）。面板常量以 `MachineUI.of(机器).scale(0.6f)` 的静态字段声明。
- Ponder 插件注册在 `ClientProxy.onClientSetup(FMLClientSetupEvent)`；思索 lang 抽取在 `common/CommonProxy.gatherData()` 调 CTNH-Lib `CTNHPonderLang.init(new CTNHBioPonderPlugin())`。场景 / tag / 插件均属 Bio 专属，不放 CTNH-Lib。

## ANTI-PATTERNS
- 把渲染逻辑写进机器实现类（`machine/`、`api/machine/`）。
- 绕过 `CBModels` / `LivingMetaMachineBERProvider` 直接构造模型或渲染器。
- 把 Bio 的 Ponder 场景 / tag / 插件搬进 CTNH-Lib（只有共享构建器属于 Lib）。
- 在场景类里硬编码单语文本，或在非 datagen 路径调用 `genLang`。

## SCOPE
`src/main/java/com/moguang/ctnhbio/client` 及其全部子包。

## READ WHEN
- 修改活体机器渲染器、可染色渲染或模型。
- 新增机器模型或调整模型-机器绑定。
- 新增或修改 Bio 的 Ponder 场景、tag、双语文案。

## SOURCE OF TRUTH
- `client/renderer/` 与 `client/model/` 的实现，以及实体 / 机器的渲染注册点（`api/item/LivingMetaMachineItem.java` 与 `client/renderer/LivingMetaMachineBERProvider.java`）。
- `client/ponder/CTNHBioPonderPlugin.java` 与 `client/ponder/CTNHBioPonderScenes.java` 的场景 / tag 登记；共享 Ponder 构建器以 `ctnh-docs/references/CTNH-Lib/client/AGENTS.md` 为准。

## WORKFLOW
1. 先看 `LivingMetaMachineBERProvider` 与 `CBModels` 的现有绑定，再决定模型 key。
2. 写 Ponder 场景前先读 CTNH-Lib 的共享 Ponder 构建器指南；场景实现放 `client/ponder/`，登记在 `CTNHBioPonderScenes` / `CTNHBioPonderTags`。
3. Ponder 文案改动后跑 `:modules:CTNH-Bio:runData` 刷新 lang，再跑 `:modules:CTNH-Bio:build`；渲染改动需在客户端运行中目视验证。
