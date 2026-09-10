# CTNH-ENERGY CLIENT DOMAIN

## OVERVIEW
CTNH-Energy 的客户端侧（21 个 Java 文件）：AE2 原生方块与部件的 Ponder 思索场景、思索 tag 注册、思索场景适配器、EU 键渲染，以及菜单/界面与物品属性注册。

## STRUCTURE
```
client/
├─ ClientProxy.java              # 客户端代理：菜单界面、EU 键渲染、Ponder 插件、物品属性
├─ render/                       # EUKeyRenderHandler
└─ ponder/
   ├─ CTNHEnergyPonderPlugin.java, CTNHEnergyPonderSceneBuilder.java,
   │  CTNHEnergyPonderScenes.java, CTNHEnergyPonderTags.java
   └─ ae2/                       # 15 个：AE2CablePonderHelper + 14 个场景
                                  # AnnihilationPlane, BuddingQuartz, Cable, Controller,
                                  # CraftingProcessUnit, CraftingSystem, FormationPlane,
                                  # ImportExportBus, Interface, IOPort, MolecularAssembler,
                                  # PatternProvider, QuantumNetworkBridge, StorageBus
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| 客户端代理与注册 | `client/ClientProxy`（`InitScreens.register` 注册 `QuantumComputerScreen`；`AEKeyRendering.register` 注册 `EUKeyRenderHandler`；`PonderIndex.addPlugin`；`ItemProperties.register` 注册 `cell_content` / `voltage` 属性） |
| Ponder 插件 | `client/ponder/CTNHEnergyPonderPlugin` |
| Ponder 场景 / tag | `client/ponder/CTNHEnergyPonderScenes`, `CTNHEnergyPonderTags`（tag `AEOriginal` = `ctnhenergy:ae_original`） |
| AE2 思索场景 | `client/ponder/ae2/`（14 个场景类） |
| Ponder 场景适配器 | `client/ponder/CTNHEnergyPonderSceneBuilder`（继承 CTNH-Lib `CTNHPonderSceneBuilder`） |
| AE2 线缆可视化辅助 | `client/ponder/ae2/AE2CablePonderHelper` |
| EU 键渲染 | `client/render/EUKeyRenderHandler` |

## CONVENTIONS
- 场景文案用 `scene.title(..., en, cn)` / `scene.showText(..., en, cn)` 双语直接内联在场景类里；datagen 时由 `CTNHEnergyPonderSceneBuilder.registerLang` 经 `REGISTRATE.genLang(key, en, cn)` 产出 lang 条目（仅 `GTCEu.isDataGen()` 时写入）。
- Ponder 插件注册在 `ClientProxy.onClientSetup`；思索 lang 抽取在 `common/CommonProxy.gatherData()` 调 CTNH-Lib `CTNHPonderLang.init(new CTNHEnergyPonderPlugin())`。
- `AE2CablePonderHelper` 维护 AE2 可连接方块白名单与线缆连接视觉，属于 AE2 专属可视化代码。

## ANTI-PATTERNS
- 把 `client/ponder/ae2/AE2CablePonderHelper` 或 Energy 的 Ponder 场景 / tag / 插件搬到 CTNH-Lib（它们是 AE2 与 Energy 专属）。
- 在场景类里硬编码单语文本，或在非 datagen 路径调用 `genLang`。
- 在 `client/` 内做注册表声明（应走 `registry/`）。

## SCOPE
`modules/CTNH-Energy/src/main/java/tech/luckyblock/mcmod/ctnhenergy/client/` 及其子包。

## READ WHEN
- 新增或修改 Energy 的 Ponder 场景、tag、双语文案
- 修改客户端菜单界面注册、EU 键渲染或物品属性

## SOURCE OF TRUTH
`client/ponder/CTNHEnergyPonderPlugin` 与 `client/ClientProxy` 的注册顺序；场景实现以 `client/ponder/ae2/` 为准。

## WORKFLOW
1. 先读 CTNH-Lib 的共享 Ponder 指南 `references/CTNH-Lib/client/AGENTS.md`。
2. 在 `CTNHEnergyPonderScenes` / `CTNHEnergyPonderTags` 中登记场景与 tag，场景实现放 `client/ponder/ae2/`。
3. 文案改动后跑 `:modules:CTNH-Energy:runData` 刷新 lang，再 `:modules:CTNH-Energy:build`。
