# CTPP REGISTRY DOMAIN

## OVERVIEW
CTPP 的 Registrate 注册面（12 个 Java 文件）：物品、方块、方块实体、机器、多方块、菜单、网络通道、配方类型与修饰符，以及 Create 材料与 GT 材料扩展。

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Registrate 根 | `registry/CTPPRegistration.java`, `registry/CTPPRegistrate.java` |
| 物品 | `registry/CTPPItems.java`（`BASIC_MECHANISM`、`STEEL_MECHANISM` 与半成品、`DOUBLE_BLAZE_CAKE`、`CONTRAPTION_LOCATOR` / `CONTRAPTION_ASSEMBLER` / `CONTRAPTION_DISASSEMBLER`） |
| 方块 | `registry/CTPPBlocks.java`（钢机壳、重型钢机壳、发电机线圈、反射镜、16 色工具箱、ULV–UHV 接线柱） |
| 方块实体 | `registry/CTPPBlockEntities.java` |
| 机器 | `registry/CTPPMachines.java`（`CARBON_BRUSHES`、`PLACEABLE_EMITTER[TIER_COUNT]` 等） |
| 多方块 | `registry/CTPPMultiblockMachines.java`（`SMASHING_FACTORY`、`KINETIC_GENERATOR`、`KINETIC_STEAM_TURBINE`、`SEAWEED_FARM`、`WINDMILL_CONTROL_CENTER`、`BOOM_OF_CREATE`、`BIG_DAM`；除 `BIG_DAM` 外均走 `CTPPRegistration.conditionalRegistration`） |
| 配方类型 | `registry/CTPPRecipeTypes.java`（8 个 GT 类型；明细见模块主文档 RECIPE TYPES） |
| 配方修饰符 | `registry/CTPPRecipeModifiers.java`（`KINETIC_PARALLEL`, `KINETIC_PERFECT_PARALLEL`） |
| 菜单 | `registry/CTPPMenus.java` |
| 网络通道 | `registry/CTPPNetwork.java`（经 `GTNetwork.register` 注册 11 个包） |
| 创造栏 | `registry/CTPPCreativeModeTabs.java` |
| 材料 | `registry/CreateMaterials.java`（AndesiteAlloy、RefinedRadiance、ShadowSteel、SLAG、ASURINE / CRIMSITE / OCHRUM / VERIDIUM 及其 slurry）；`registry/GTMaterialAddon.java` |
| 实体 | `CTPPEntityTypes.java`（顶层；`simple_contraption`、`rubiks_cube_contraption`） |

## CONVENTIONS
- 注册类统一 `CTPP` 前缀；注册入口集中在 `CTPPRegistration.REGISTRATE`。
- `CTPP.java` 构造函数经 `DistExecutor.unsafeRunForDist` 分流 `ClientProxy` / `CommonProxy`，随后调用 `CTPPEntityTypes.init()`。
- `CTPPRegistration.REGISTRATE.registerRegistrate()` 在 `common/CommonProxy.init()` 中调用；机器、配方类型、配方条件分别经 `GTCEuAPI.RegisterEvent` 泛型监听器（`registerMachines` / `registerRecipeTypes` / `registerRecipeConditions`）注册。
- `CTPPGTAddon.initializeAddon()` 初始化 `CTPPBlocks`、`CTPPBlockEntities`、`CTPPBlockMaps`，并注册 `MagnetPlacementHelper` 放置助手。
- `CTPPRecipeTypes.init()` 目前只启用 `MACERATOR_RECIPES` → `SMASHING_FACTORY_RECIPES` 的自动转换；`MIXER_RECIPES` → `KINETIC_MIXER_RECIPES` 的挂钩已注释掉。
- `CTPPRecipeModifiers` 的两个修饰符只作用于 `KineticWorkableMultiblockMachine`，其他机器返回 `null`。
- 材料走两条事件：`MaterialRegistryEvent` 创建 `ctpp` 材料注册表，`MaterialEvent` 调用 `CreateMaterials.init()`。

## ANTI-PATTERNS
- 同一条目同时从 `registry/` 与 `CommonProxy` 两条路径注册。
- 在 `common/machine/**` 内直接调用注册 API（应回到 `registry/`）。
- 用字符串 ID + `ForgeRegistries` 查找代替静态注册对象。

## SCOPE
适用于 `src/main/java/com/mo_guang/ctpp/registry`，以及顶层的 `CTPPEntityTypes.java`。

## READ WHEN
- 新增或修改 CTPP 的物品、方块、BE、机器、多方块、材料或创造栏。
- 新增配方类型、配方条件或配方修饰符。
- 新增网络包注册或菜单注册。

## SOURCE OF TRUTH
- `registry/CTPPRegistrate.java`、`registry/CTPPRegistration.java` 与 `CTPPGTAddon.java` 的挂钩顺序。
- 生命周期以 `CTPP.java` 与 `common/CommonProxy.java` 为准。

## WORKFLOW
1. 定位该条目所属的注册类分组。
2. 核对 GT addon 挂钩顺序与 datagen 引用。
3. 影响数据时跑 `:modules:CTPP:runData`，编译跑 `:modules:CTPP:build`。
