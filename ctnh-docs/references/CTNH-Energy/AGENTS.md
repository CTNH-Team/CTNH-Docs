# CTNH-ENERGY MODULE

## OVERVIEW
CTNH-Energy（包 `tech.luckyblock.mcmod.ctnhenergy`）是 CTNH 的 AE2 × GT 能源桥接模块：把 EU 接入 ME 网络（EU 键类型与存储单元、EU P2P、量子计算机虚拟 CPU、ME 能源仓与能量分配），并扩展 AE2 样板编码（样板署名、电路样板、样板提供者逻辑）。共 187 个 Java 文件。入口类：`CTNHEnergy`（mod 主类）、`CTNHEnergyGTAddon`（GT addon）、`CEConfig`（配置）；代理为 `CommonProxy` / `ClientProxy`。

## STRUCTURE
源码根 `modules/CTNH-Energy/src/main/java/tech/luckyblock/mcmod/ctnhenergy/`（括号内为该域 Java 文件数）

```
ctnhenergy/
├─ CTNHEnergy.java / CTNHEnergyGTAddon.java / CEConfig.java   入口 / GT addon / 配置
├─ api/          (8)   跨域接口：EUItemContext, ICircuitPattern, IMaintainingContext,
│                      IPatternProviderLogic, IUpgradeableMenu, IAutoMultiplyCPU,
│                      IGhostKeyTarget, CEPredicates
├─ client/       (21)  ClientProxy, render/EUKeyRenderHandler,
│                      ponder/（CTNHEnergyPonderPlugin/SceneBuilder/Scenes/Tags）
│                      ponder/ae2/（14 个 AE2 思索场景 + AE2CablePonderHelper）
├─ common/       (60)  实现核心 → common/AGENTS.md
├─ data/         (3)   CEDatagen, lang/（ChineseLangHandler, EnglishLangHandler）
├─ event/        (2)   ForgeEventHandler, ForgeClientEventHandler
├─ integration/  (9)   emi/ (4), jade/ (4), ldlib/ (1)
├─ mixin/        (59)  上游 AE2 系列 / GTM / Omni 补丁 → mixin/AGENTS.md
├─ network/      (2)   packets/QCOpenCPUMenuPacket, syncdata/AEKeyPayLoad
├─ registry/     (9)   AEMenus, CEBlocks, CEItems, CEMachines, CEMultiblock,
│                      CENetWorking, CERecipeTypes, CECreativeModeTabs, CERegistrate
└─ utils/        (11)  CEUtil, CEDrawHelper, CEPatternProviderTarget, MEConfigUtil,
                       ProviderRecord, FakeSizedIntList, TempColorSprayBehaviour, button/
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| mod 入口 / 代理 | `CTNHEnergy`, `CommonProxy`, `ClientProxy` |
| GT addon 与注册时机 | `CTNHEnergyGTAddon.initializeAddon()`（只做 `CEBlocks.init()` / `CEItems.init()`） |
| 配置 | `CEConfig.java`, `common/CESettings.java` |
| EU 键类型 / 存储 | `common/me/key/{EUKey, EUKeyType, VoltageKey, VoltageKeyType}`, `common/me/GenericStackEUStorage` |
| EU 存储单元 | `common/item/{EUCellItem, IEUCell, EUCellStats}`, `common/me/cell/{EUCellInventory, EuCellHandler}` |
| ME 能源仓 / 变电站 | `common/machine/energyhatch/{MEEnergyPartMachine, MEEnergyInputConfigurator, MESubstationHatch}` |
| ME 输入 / 输出 / 仓储仓 | `common/machine/iohatch/{MEInputMachine, MEOutputMachine, MEStokingInputMachine}` |
| 机器-网络 EU 交互 | `common/me/MEMachineEUHandler`, `common/machine/handler/MEStorageEUHandler` |
| 能量分配 | `common/me/service/{EnergyDistributeService, IEnergyDistributor}` |
| 样板提供者目标 / 记录 | `utils/CEPatternProviderTarget`, `utils/ProviderRecord`; `common/machine/MEPartMachine` |
| 样板署名 / 编码时间 | `common/pattern/PatternAuthorData` |
| 电路样板 | `common/circuit/{CircuitPatternData, CircuitPatternService}`; `api/ICircuitPattern` |
| 样板缓冲 | `common/machine/patternbuffer/MEPatternBuffer` |
| 量子计算机 | `common/quantumcomputer/{port,cpu,gui}`（虚拟 CPU 集群由 `common/quantumcomputer/port/QuantumComputerMENetworkPortBlockEntity` 创建，经 `mixin/ae2/cpu/CraftingServiceMixin` 接入 AE2）；多方块定义 `CEMultiblock.JIUZHANG_QUANTUM_COMPUTER` 与 `common/quantumcomputer/machine/QuantumComputerMultiblockMachine` 当前为整文件注释、未注册 |
| 大型机器 | `common/multi/PowerSubstationMachine`（注册于 `registry/CEMultiblock.POWER_SUBSTATION`） |
| 注册表 | `registry/{AEMenus, CEBlocks, CEItems, CEMachines, CEMultiblock, CENetWorking, CERecipeTypes, CECreativeModeTabs, CERegistrate}` |
| 客户端 / 思索 | `client/ClientProxy`, `client/ponder/CTNHEnergyPonderPlugin` |
| EMI / Jade / LDLib 集成 | `integration/emi/CEEMIPlugin`, `integration/jade/CTNHEnergyJadePlugin`, `integration/ldlib/CELDLibPlugin` |
| 数据生成 | `data/CEDatagen` |
| 网络包 | `network/packets/QCOpenCPUMenuPacket`, `network/syncdata/AEKeyPayLoad` |

## DOMAIN GUIDE ROUTING
| Source area | Guide | Read before |
|-------------|-------|-------------|
| `api/**` | `ctnh-docs/references/CTNH-Energy/api/AGENTS.md` | 新增或修改跨 `common/` 与 `mixin/` 的契约接口、多方块谓词 |
| `client/**` | `ctnh-docs/references/CTNH-Energy/client/AGENTS.md` | 新增 Ponder 场景 / tag、客户端渲染或界面注册 |
| `common/**` | `ctnh-docs/references/CTNH-Energy/common/AGENTS.md` | 改动机器 / 仓室 / EU 存储 / 样板逻辑 |
| `data/**` | `ctnh-docs/references/CTNH-Energy/data/AGENTS.md` | 新增 lang 键或 datagen 产物 |
| `event/**` | `ctnh-docs/references/CTNH-Energy/event/AGENTS.md` | 新增 Forge 事件监听 |
| `integration/**` | `ctnh-docs/references/CTNH-Energy/integration/AGENTS.md` | 对接 EMI / Jade / LDLib |
| `mixin/**` | `ctnh-docs/references/CTNH-Energy/mixin/AGENTS.md` | 改动任何 AE2 系列或 GTM / Omni 补丁 |
| `network/**` | `ctnh-docs/references/CTNH-Energy/network/AGENTS.md` | 新增网络包或同步载荷 |
| `registry/**` | `ctnh-docs/references/CTNH-Energy/registry/AGENTS.md` | 新增任何注册对象（物品 / 方块 / 机器 / 菜单 / 配方类型） |
| `utils/**` | `ctnh-docs/references/CTNH-Energy/utils/AGENTS.md` | 复用工具类而非另起实现 |

## CONVENTIONS
- **GTM 动态包**：GT/GMT 配方经 `*GTAddon.addRecipes()` 注册为运行时动态数据包（`GTDynamicPackContents` / CTNH-Lib `CTNHDynamicDataPack`），`runData` 对其**不产出** JSON；静态 `src/generated/resources` 只含 lang/models/blockstates/loot_tables/tags 等非 GT 产物。`CTNHEnergyGTAddon` 未覆写 `addRecipes()`（`IGTAddon` 默认空实现），本模块不自建 GT 配方；验证方式为游戏内或 `ConfigHolder.dev.dumpRecipes`。
- **注册对象优先**：引用物品/方块/流体**必须**使用静态注册对象（`CEItems.X`, `CEBlocks.X`, `GTMaterials.Iron`, `TagPrefix.ingot`, `AEItems.X` 等），**禁止** `ResourceLocation` 字符串解析 + `ForgeRegistries` 查找；字符串 ID 仅限无注册对象的场景（上游 mod 专属 ID、配方 ID、tag key、维度 ID）。
- 模块自有类统一前缀 `CE` / `ME` / `EU`；注册对象只在 `registry/` 声明、初始化与注册，其他包只引用。
- 跨域契约放 `api/`（如 `ICircuitPattern`, `IPatternProviderLogic`, `IUpgradeableMenu`），实现放 `common/` 或 `mixin/`；对上游 AE2 系列的侵入式修改一律走 `mixin/`，不复制上游类。
- Mixin 自有成员用 `ctnhenergy$` 或 `CE$` 前缀，目标成员用 `@Shadow` 访问。

## ANTI-PATTERNS
- 用 `new ResourceLocation(...)` + `ForgeRegistries`/`BuiltInRegistries` 反查已有注册对象。
- 在 `common/` 内直接操作 AE2 内部结构而绕过 `me/` 下的 handler 与 `api/` 契约。
- 在 `registry/` 之外声明/注册物品、方块、菜单、网络包或配方类型。
- 期望 `runData` 产出 GT/GTM 配方 JSON。
- 新增 mixin 目标而不在 `src/main/resources/ctnhenergy.mixins.json` 中登记。

## COMMANDS
```bash
./gradlew :modules:CTNH-Energy:build              # 编译 + 校验
./gradlew :modules:CTNH-Energy:spotlessApply      # 格式化（提交前必跑）
./gradlew :modules:CTNH-Energy:runData            # 数据生成（不含 GT 动态配方）
./gradlew :modules:CTNH-Energy:runClient          # 游戏内验证机器 / 样板 / Ponder
```

## SCOPE
`modules/CTNH-Energy/src/main/java` 下全部包，以及同模块资源目录（`src/main/resources/ctnhenergy.mixins.json`、lang 等）。

## READ WHEN
- 修改 ME↔EU 存储、能源仓、能量分配、量子计算机虚拟 CPU 或样板逻辑
- 新增机器、仓室、菜单、网络包或注册表条目
- 调整客户端思索、EMI / Jade / LDLib 集成
- 新增或修改对上游 AE2 系列 / GTM / Omni 的 Mixin 补丁

## SOURCE OF TRUTH
源码：`modules/CTNH-Energy/src/main/java/tech/luckyblock/mcmod/ctnhenergy/`。文档与代码冲突时以代码为准。

## WORKFLOW
1. 定位所属域 → 先读对应域 `AGENTS.md`（见 DOMAIN GUIDE ROUTING）。
2. 新注册对象加到 `registry/`；跨域契约加到 `api/`；实现放 `common/` 或 `mixin/`。
3. `:modules:CTNH-Energy:build` 编译；`spotlessApply` 格式化；`runData` 校验非 GT 静态资源。
4. GT 配方与 AE2 运行时行为在游戏内验证，或使用 `ConfigHolder.dev.dumpRecipes`。
