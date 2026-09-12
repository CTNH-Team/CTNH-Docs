# CTPP MIXIN DOMAIN

## OVERVIEW
CTPP 的补丁集（21 个 Java 文件）：Create 旋转/动能修复、部署器与序列装配修复、Create Diesel 与 JEI 修补、GT 工具类型、GT 桶与多方块状态钩子，以及一个 Minecraft 选取方块钩子。

## STRUCTURE
```text
mixin/
|-- BlockPatternMixin, GTBucketItemMixin, RotationPropagatorMixin, SmartBlockEntityMixin
|-- create/                    # AllCreatePonderScenesMixin, KineticBlockEntityMixin, Matrix3dMixin,
|                              ToolboxHandlerClientMixin, WindmillBearingBlockMixin
|   |-- diesel/                # BasinFermentingCategoryMixin, BasinRecipeMixin, CDGJEIMixin, DistillationTankBlockEntityMixin
|   |-- fix/                   # DeployerApplicationRecipeMixin（json 中以 6 个内部类分别登记）, SequencedAssemblyCategoryMixin
|   `-- jei/                   # RecipeSlotBuilderMixin, SequencedAssemblyCategoryMixin,
|                              SequencedAssemblySubCategoryMixin, TMRVSlotWidgetMixin
|-- gtm/                       # GTToolTypeMixin
`-- mc/                        # MinecraftPickBlockMixin
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Create 补丁 | `mixin/create/`（顶层 5：`KineticBlockEntityMixin`、`Matrix3dMixin`、`WindmillBearingBlockMixin`，以及客户端的 `AllCreatePonderScenesMixin`、`ToolboxHandlerClientMixin`） |
| Create Diesel 补丁 | `mixin/create/diesel/`（4） |
| 部署器 / 序列装配修复 | `mixin/create/fix/`（2 个类） |
| Create JEI 补丁 | `mixin/create/jei/`（4） |
| GT 补丁 | `mixin/gtm/GTToolTypeMixin.java` |
| Minecraft 补丁 | `mixin/mc/MinecraftPickBlockMixin.java`（client 段） |
| 顶层通用补丁 | `mixin/{BlockPatternMixin, GTBucketItemMixin, RotationPropagatorMixin, SmartBlockEntityMixin}.java` |
| Mixin 配置 | `src/main/resources/ctpp.mixins.json`（`mixins` 段 21 项、`client` 段 6 项，`compatibilityLevel: JAVA_17`） |

## CONVENTIONS
- Mixin 配置与包结构必须同步：新增类要同时加进 `ctpp.mixins.json` 的 `mixins` 或 `client` 段，并按目标 mod 分组放置。
- Create 动能行为由 Mixin 与 `dynamicPart/` 的 contraption 类共同打补丁；改旋转或移动方块行为需同时看两处。
- 客户端专用补丁（Ponder、工具箱客户端、选取方块）必须登记在 `client` 段。
- 转子支架（rotor holder）行为由 GTM 原生处理，本模块不加相关 Mixin。

## ANTI-PATTERNS
- 改注入点却不核对上游目标成员（Create / GT / MC 版本）。
- 重新引入转子支架 Mixin。
- 把客户端补丁登记进 `mixins` 段（或反之），导致加载失败。

## SCOPE
适用于 `src/main/java/com/mo_guang/ctpp/mixin` 与 `src/main/resources/ctpp.mixins.json`。

## READ WHEN
- 给 Create 的旋转/动能、部署器/序列装配、Create Diesel 或 JEI 打补丁。
- 给 GT 桶/多方块状态或 MC 本体打补丁。

## SOURCE OF TRUTH
- `src/main/resources/ctpp.mixins.json` 与 `mixin/` 下的类。
- 上游目标成员以当前 Create / GTCEu 依赖版本为准。

## WORKFLOW
1. 定位 Mixin 包与 json 条目。
2. 对照已加载的 Create / GT 版本核对目标成员。
3. 跑 `:modules:CTPP:build`；进游戏验证。
