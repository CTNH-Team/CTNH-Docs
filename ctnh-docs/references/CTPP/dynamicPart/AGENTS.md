# CTPP DYNAMICPART DOMAIN

## OVERVIEW
动态 contraption 支持（10 个 Java 文件）：旋转魔杖、移动/旋转 contraption 与其实体、渲染器，以及四元数旋转状态。

## STRUCTURE
```text
dynamicPart/
|-- QuaternionRotationState.java, RotationWandItem.java
|-- SimpleBearingContraption.java, SimpleContraptionEntityRenderer.java
|-- moving/                    # SimpleMovingContraption
`-- rotation/                  # FixedAxisRotatingContraptionEntity, IContraptionMultiblock,
                               RubiksCubeContraptionEntity, SimpleRotatingContraption, SimpleRotatingContraptionEntity
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| 移动 contraption | `dynamicPart/moving/SimpleMovingContraption.java` |
| 旋转逻辑与多方块接口 | `dynamicPart/rotation/`（5 个类；`IContraptionMultiblock` 由 `KineticGeneratorMachine` 实现） |
| 旋转魔杖 | `dynamicPart/RotationWandItem.java`（物品条目在 `registry/CTPPItems.java`，当前被注释掉） |
| 旋转状态 | `dynamicPart/QuaternionRotationState.java` |
| 实体注册 | `CTPPEntityTypes.java`（`simple_contraption`、`rubiks_cube_contraption`） |
| 实体渲染器 | `dynamicPart/SimpleContraptionEntityRenderer.java` |

## CONVENTIONS
- Create 动能行为由 Mixin 与 dynamic contraption 类共同打补丁；改旋转或移动方块行为需同时看两处（`mixin/create/`）。
- `IContraptionMultiblock` 是机器与旋转 contraption 的契约：实现方提供装配枢轴与旋转轴，`KineticGeneratorMachine` 在结构成型/失效时装配或拆解。
- 实体经 `CTPPEntityTypes` 的 `contraption(...)` 助手注册（`MobCategory.MISC`、附带 `ContraptionVisual`）。

## ANTI-PATTERNS
- 改旋转行为却不检查对应的 `mixin/create/` 补丁。
- 绕过 `CTPPEntityTypes` 自行注册 contraption 实体。

## SCOPE
适用于 `src/main/java/com/mo_guang/ctpp/dynamicPart` 及其子包。

## READ WHEN
- 改动旋转魔杖、移动/旋转 contraption 或旋转状态。
- 改动使用旋转 contraption 的机器（如应力发电机）。

## SOURCE OF TRUTH
- `dynamicPart/` 各类与 `mixin/create/` 的对应补丁。
- `CTPPEntityTypes.java` 的实体注册。

## WORKFLOW
1. 同时核对 dynamic contraption 类与 Create Mixin 补丁。
2. 跑 `:modules:CTPP:build`；有条件时进游戏验证装配与旋转表现。
