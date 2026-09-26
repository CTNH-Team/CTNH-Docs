# CTNH-MANA CLIENT DOMAIN

## OVERVIEW
`client/` 是 CTNH-Mana 的客户端面（44 个 Java 文件）：ClientProxy 编排（动态渲染注册 / shader / 物品属性 / Ponder 插件 / 烘焙模型包装）、Caduceus 轮盘菜单、模型、Mana 自有 Ponder 插件与场景（4 个 `ponder/` 顶层类 + `ponder/mana/` 4 个场景类）、渲染器与粒子，以及虚境入侵的客户端镜像。

## STRUCTURE
```text
client/
├── ClientProxy.java, ZenithInvadeClient.java, ZenithMatrixEffect.java
├── gui/radial/                # CaduceusRadialMenu, RadialMenu, RadialMenuScreen, RadialMenuSlot
├── model/                     # 8: CMModels, GiantBeeModel, MagicCubeModel, ModelBase, ModelDefinition, RoyalServantBeeModel, StarCakeBlockModel, StarCakeItemModel
├── ponder/                    # CTNHManaPonderPlugin, CTNHManaPonderSceneBuilder, CTNHManaPonderScenes, CTNHManaPonderTags
│   └── mana/                  # IndustrialAltar, MagicRituals, MysticSpire, PonderParticleUtil
├── render/                    # 19: AntagonismRender, BeeNukeProjectileRenderer, DeltaSparkRenderer, DemonWillRender, EternalGardenRender, GiantBeeRenderer, MaliciousThermalilyProjectileRenderer, ManaCondenserRender, ManaReactorRender, OmegaSparkRenderer, RoyalServantBeeRenderer, ShroudGazingRender, StarCakeItemRender, StarCakeMachineBERProvider, StarCakeRender, UltraManaMistModel, UltraManaMistRenderType, WitherAconiteProjectileRenderer, ZenithMatrixRender
│   └── particle/              # IconParticle
└── utils/                     # RenderUtils
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| 客户端编排 | `client/ClientProxy.java`（`ClientProxy extends CommonProxy`） |
| 动态渲染注册 | `ClientProxy.init()`：`DynamicRenderManager.register` 注册 `zenith_laser`, `eternal_garden`, `mana_condenser`, `mana_reactor`, `demon_will_generator` 五个渲染类型 |
| shader | `ClientProxy.registerShaders()`：`zenith` 与 `zenith_beam`，经静态 getter 暴露 |
| 物品属性谓词 | `ClientProxy.onClientSetup()`：`CMItems.SABER_WAND` 的 `wand_status`（由 `SaberWandItem.getBindMode` 决定）、`CMItems.CADUCEUS` 的 `tool_type`（读 NBT `caduceus_type_index`，除以 12） |
| 粒子 / 模型层 | `ClientProxy.onRegisterParticleProviders()`（`CMParticleTypes.INDEX_TARGET` → `IconParticle.Provider`）、`onRegisterLayerDefinitions()`（`CMModelLayers.init()`） |
| Caduceus 轮盘 | `client/gui/radial/`（4 类）；按键触发在 `event/ForgeEventHandler.keyEvent` |
| Ponder 插件 | `client/ponder/CTNHManaPonderPlugin.java`（`getModId` → `CTNHMana.MODID`；注册 `CTNHManaPonderScenes` 与 `CTNHManaPonderTags`） |
| Ponder 场景/标签 | `client/ponder/CTNHManaPonderScenes.java`（`MysticSpire` 三幕 + `industrial_altar/common` + `blaze/common` + `rune_rituals/common` + `ritual_diviner/common`）、`CTNHManaPonderTags.java`（`ctnhmana:mana` 标签） |
| 尖塔 / 仪式场景 | `client/ponder/mana/`（`MagicRituals`, `MysticSpire`, `PonderParticleUtil`） |
| 工业血祭坛场景 | `client/ponder/mana/IndustrialAltar.java`：storyboard 存 4 级超集，按 box 露出/隐藏演示 2→3→4→3 级结构升降级与仓室替换；storyboard NBT 在 `src/main/resources/assets/ctnhmana/ponder/industrial_altar/common.nbt` |
| Ponder 构建器适配 | `client/ponder/CTNHManaPonderSceneBuilder.java` |
| 模型 | `client/model/`（8） |
| 渲染器 | `client/render/`（19）+ `render/particle/IconParticle` |
| 物品迷雾模型包装 | `ClientProxy.onModifyBakingResult(ModelEvent.ModifyBakingResult)`：把 `ultra_mana_ingot` 的 `ModelResourceLocation(CTNHMana.id("ultra_mana_ingot"), "inventory")` 烘焙模型替换为 `UltraManaMistModel` 包装；迷雾 pass 用 `UltraManaMistRenderType.mist()`，贴图取 `avaritia:misc/halo` 与 `avaritia:misc/halo_noise` |
| 虚境客户端镜像 | `client/ZenithInvadeClient.java`, `client/ZenithMatrixEffect.java` |

## CONVENTIONS
- `CTNHManaPonderSceneBuilder extends CTNHPonderSceneBuilder`（CTNH-Lib），只做薄适配：构造时传入 `CTNHMana.MODID` 与 `registerLang`，后者在 `GTCEu.isDataGen()` 时调 `REGISTRATE.genLang(key, en, cn)` 抽取文案。
- Ponder 场景文案内嵌在场景文件里，用 `scene.title(id, en, cn)` / `scene.showText(ticks, en, cn)` 三参形式（标题带两级文案时用 `title(id, en, cn, titleEn, titleCn)`），不走 lang key。
- 多级结构演出复用同一 storyboard：`IndustrialAltar` 依赖各级 pattern 还原到同一坐标系后的严格包含关系（base ⊂ L3 ⊂ L4 ⊂ L5 ⊂ L6，重叠处方块 id 一致），用 `showSection` / `hideSection` 切换 box 列表实现升级与降级，不换 NBT。
- Ponder 插件由 `ClientProxy.onClientSetup()` 经 `PonderIndex.addPlugin(new CTNHManaPonderPlugin())` 挂载；插件本身不含注册逻辑。
- 动态渲染类型必须在 `ClientProxy.init()` 注册，渲染类本身只提供 `TYPE`。
- Caduceus / Saber 的客户端行为由「网络包 + 物品属性谓词」两处共同决定，改动需成对检查。

## ANTI-PATTERNS
- 把 Mana 的 Ponder 场景/标签/插件搬到 CTNH-Core 或 CTNH-Lib（共享 builder 才归 Lib）。
- 在渲染器里复制 CTNH-Lib 已有的渲染或 lang 抽取逻辑，而非继承/复用。
- 改动 Caduceus / Saber 客户端行为时只改物品属性谓词或只改网络包其中一处。
- 在 `ClientProxy` 之外的客户端类里注册 shader、粒子 provider 或模型层。

## SCOPE
适用于 `src/main/java/com/magicbee/ctnhmana/client` 及其子包。

## READ WHEN
- 新增或修改 Mana Ponder 场景、标签或插件。
- 改动 Caduceus 轮盘菜单、模型或渲染器。
- 改动虚境入侵的客户端表现（天空裂缝、开场动画、shroud_whisper 循环）。
- 新增 shader、粒子类型或物品属性谓词。

## SOURCE OF TRUTH
- `client/ClientProxy.java`（注册与编排）、`client/ponder/CTNHManaPonderPlugin.java`。
- 共享 Ponder builder：`references/CTNH-Lib/client/AGENTS.md`。

## WORKFLOW
1. 写 Ponder 场景前先读 CTNH-Lib 的共享 builder 指南。
2. 场景/标签在插件里注册，文案用场景内嵌三参 API。
3. Ponder 文案或 lang 改动后跑 `:modules:CTNH-Mana:runData`。
4. 渲染/shader 改动在游戏内验证，跑 `:modules:CTNH-Mana:build`。