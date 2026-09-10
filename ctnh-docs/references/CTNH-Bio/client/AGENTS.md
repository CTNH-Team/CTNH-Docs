# CTNH-BIO CLIENT DOMAIN

## OVERVIEW
Bio 的客户端渲染与模型（14 个 Java 文件）：活体机器实体渲染、可染色渲染器族、基于 GeckoLib 的模型注册表，以及客户端代理。

## STRUCTURE
```
client/
├─ ClientProxy.java
├─ Text/                     # ModelOutputLine（模型输出行文本）
├─ model/                    # BioelectricForgeModel, BioReactorModel, CBModels, DecomposerModel,
│                            #   DigesterModel, GreatFleshModel, VatModel
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

## CONVENTIONS
- 可染色渲染器族服务于可染色的活体机器内容：实体 / 方块实体 / 物品三种渲染器共用同一套模型与颜色参数。
- `LivingMetaMachineBERProvider` 是机器与模型的唯一绑定入口，模型按 key 从 `CBModels.MODELS` 取；新增机器模型在 `CBModels` 注册，不要在机器类里直接 new 渲染器。
- `ClientProxy` 只在客户端分发路径构造（`CTNHBio` 经 `DistExecutor.unsafeRunForDist` 选择 `ClientProxy` / `CommonProxy`），客户端专属类不得进入 common 构造路径。

## ANTI-PATTERNS
- 把渲染逻辑写进机器实现类（`machine/`、`api/machine/`）。
- 绕过 `CBModels` / `LivingMetaMachineBERProvider` 直接构造模型或渲染器。

## SCOPE
`src/main/java/com/moguang/ctnhbio/client` 及其全部子包。

## READ WHEN
- 修改活体机器渲染器、可染色渲染或模型。
- 新增机器模型或调整模型-机器绑定。

## SOURCE OF TRUTH
- `client/renderer/` 与 `client/model/` 的实现，以及实体 / 机器的渲染注册点（`api/item/LivingMetaMachineItem.java` 与 `client/renderer/LivingMetaMachineBERProvider.java`）。

## WORKFLOW
1. 先看 `LivingMetaMachineBERProvider` 与 `CBModels` 的现有绑定，再决定模型 key。
2. 跑 `:modules:CTNH-Bio:build`；渲染改动需在客户端运行中目视验证。
