# CTNH-ENERGY REGISTRY DOMAIN

## OVERVIEW
CTNH-Energy 的注册中枢（9 个 Java 文件）：Registrate 根、物品与方块、GT 机器与多方块、配方类型、AE 菜单、LDLib 网络、创造栏。

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Registrate 根 | `registry/CERegistrate`（继承 CTNH-Lib `CNRegistrate`，提供 `addLang(type, id, en, cn)` 便捷重载）；实例为 `CTNHEnergy.REGISTRATE` |
| 物品 | `registry/CEItems`（`EU_CELL` 数组、`DYNAMO_CARD`、`PROGRAMMED_CIRCUIT_CARD`、`EU_CELL_HOUSING`、`EU_P2P`、`MAINTAINING_CARD`） |
| 方块 | `registry/CEBlocks`（`QUANTUM_COMPUTER_ME_NETWORK_PORT`、`QUANTUM_COMPUTER_CASING`、`STEADY_STATE_COMPUTING_MATRIX_SHELL`、`QUANTUM_POINTING_BLOCK`、`ASSEMBLER_MATRIX_FRAME/WALL`） |
| GT 机器 | `registry/CEMachines`（`me_input_bus` / `me_input_hatch` / `me_dual_input_hatch` / `me_stoking_input_bus` / `me_stoking_input_hatch` 等） |
| 多方块 | `registry/CEMultiblock`（`POWER_SUBSTATION` 已注册；`JIUZHANG_QUANTUM_COMPUTER` 定义整块注释、未注册） |
| 配方类型 | `registry/CERecipeTypes`（`QUANTUM_COMPUTER` = `ctnhenergy:quantum_computer`，基类 `GTRecipeTypes.ELECTRIC`） |
| AE 菜单 | `registry/AEMenus`（`DeferredRegister<MenuType<?>> DR`；`QUANTUM_COMPUTER` = `jiuzhang_quantum_computer`） |
| 网络 | `registry/CENetWorking`（`LDLNetworking.NETWORK.registerC2S`） |
| 创造栏 | `registry/CECreativeModeTabs` |

## CONVENTIONS
- 注册类统一 `CE` 前缀；所有注册对象只在此域声明与初始化，其他包只引用静态实例。
- 挂接顺序：`CTNHEnergyGTAddon.initializeAddon()` 只做 `CEBlocks.init()` 与 `CEItems.init()`；`common/CommonProxy.init()` 依次做 `REGISTRATE.registerRegistrate()`、`AEMenus.DR.register(eventBus)`、`CENetWorking.init()`、`CEDatagen.init()`、`CECreativeModeTabs.init()`、`CEStats.init()`，并挂 `GTRecipeType` / `MachineDefinition` 泛型监听。
- 机器与多方块分别由 `CommonProxy.registerMachines()`（`CEMachines.init()` + `CEMultiblock.init()`）与 `registerRecipeTypes()`（`CERecipeTypes.init()`）驱动，二者都是空壳 `init()`，真实定义写在字段初始化里。
- 创造栏归属由各注册类的静态块 `REGISTRATE.creativeModeTab(() -> CECreativeModeTabs.ITEM)` 指定。
- 引用注册对象必须用静态实例（`CEItems.X` / `CEBlocks.X`），不要用字符串 ID 反查。

## ANTI-PATTERNS
- 在 `registry/` 之外声明或注册物品、方块、菜单、网络包、配方类型。
- 同一条目在 `registry/` 与 `CommonProxy` 两条路径重复注册。
- 把机器实现或配方逻辑写进注册类（应放 `common/` 与 `data/`）。
- 通过 `ResourceLocation` 字符串 + `ForgeRegistries` 取用已在 `registry/` 中声明的对象。

## SCOPE
`modules/CTNH-Energy/src/main/java/tech/luckyblock/mcmod/ctnhenergy/registry/`。

## READ WHEN
- 新增或修改 Energy 的物品、方块、机器、多方块、配方类型、AE 菜单或创造栏条目

## SOURCE OF TRUTH
`registry/` 下的注册类，以及 `CTNHEnergyGTAddon` 与 `common/CommonProxy` 的挂接顺序。

## WORKFLOW
1. 找到条目所属的注册类（物品 → `CEItems`，方块 → `CEBlocks`，机器 → `CEMachines`，多方块 → `CEMultiblock`，配方类型 → `CERecipeTypes`，菜单 → `AEMenus`）。
2. 确认挂接时机：GT 侧走 addon 的 `initializeAddon()`，通用侧走 `CommonProxy.init()` 与其泛型监听。
3. `:modules:CTNH-Energy:build` 编译；`runData` 刷新 lang 与模型。