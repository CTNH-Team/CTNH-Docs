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
| 旋转逻辑与多方块接口 | `dynamicPart/rotation/`（5 个类）；`IContraptionMultiblock` 的实现方：`KineticGeneratorMachine`、`BigDamMachine`、`WindMillControlMachine`（`SimpleRotatingContraptionEntity`）与 `ComplexRotatingMachine`（`RubiksCubeContraptionEntity`） |
| 可复用的旋转实体内核 | `dynamicPart/rotation/SimpleRotatingContraptionEntity.java`（`create(level, contraption, controller, pivot)`、`controllerPos`、`setRotationSpeed` / `setRotationSpeedRPM`、`setPivot`、`protected getController()`） |
| 固定轴定向旋转 | `dynamicPart/rotation/FixedAxisRotatingContraptionEntity.java`（`SimpleRotatingContraptionEntity` 子类；`setFixedRotationAxis` / `setTargetAngle` / `setRotateSpeed` / `stopSeekingTarget`） |
| 魔方式单层转动 | `dynamicPart/rotation/RubiksCubeContraptionEntity.java`（`RotationLayer` + `clockwise`；`create(...)` 额外需要 `frontFacing` 与 `pos`） |
| 旋转魔杖 | `dynamicPart/RotationWandItem.java`（物品条目在 `registry/CTPPItems.java`，当前被注释掉） |
| 旋转状态 | `dynamicPart/QuaternionRotationState.java` |
| 实体注册 | `CTPPEntityTypes.java`（`simple_contraption`、`rubiks_cube_contraption`） |
| 实体渲染器 | `dynamicPart/SimpleContraptionEntityRenderer.java`（`SimpleRotatingContraptionEntity` 与 `RubiksCubeContraptionEntity` 共用） |

## CONVENTIONS
- Create 动能行为由 Mixin 与 dynamic contraption 类共同打补丁；改旋转或移动方块行为需同时看两处（`mixin/create/`）。
- `IContraptionMultiblock<T extends SimpleRotatingContraptionEntity> extends IMultiController` 是机器与旋转 contraption 的契约：实现方提供 `assemble(BlockPos pivot)`、`getContraptionEntity()`、`setContraptionEntity(List)`，可选覆写 `getAssemblyPivot()`。默认助手 `assembleFromPattern(pivot, rotationAxis)`、`createAndAttachRotatingEntities(pivot, axis)`、`clearAndDisassembleRotatingEntities()`、`findAndReattachEntities()` 承担装配、拆解与区块重载后的重挂；`shouldIgnoreContraptionChange(pos, state)` 让 `StaticBlockPattern` 的动态部件在装配期间不使结构失效。
- `SimpleRotatingContraptionEntity` 是旋转实体内核：`create(Level, Contraption, IContraptionMultiblock, Vec3 pivot)` 记录 `controllerPos` 并置 `isRunning`；`tickContraption()` 每 tick 用 `getController()` 找回控制器并 `attach`（找不到机器时保留实体，交给结构失效路径清理）；`getController()` 为 `protected`，可覆写返回 `null` 让实体脱离控制器自由运行（CTNH-Astral 的 `RocketContraptionEntity` 即此用法）。改 `create(...)` 签名或 `controllerPos` 语义会同时打断下游。
- `SimpleRotatingContraption(partPos, anchor, rotationAxis)` 只搬运给定部件列表并按轴展开包围盒；`rotationAxis` 传 `null` 时按三轴展开（给运行时可换轴的装置用）。
- 实体经 `CTPPEntityTypes` 的 `contraption(...)` 助手注册（`MobCategory.MISC`、追踪范围 10、更新间隔 3、附带 `ContraptionVisual`）。

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
