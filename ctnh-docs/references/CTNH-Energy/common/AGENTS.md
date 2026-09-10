# CTNH-ENERGY COMMON DOMAIN

## OVERVIEW
`common/` 是 CTNH-Energy 的实现核心（60 个 Java 文件）：ME 机器与仓室（能源仓 / 输入输出仓 / 仓储仓 / 样板缓冲）、EU 存储与键类型、电路样板与样板署名、量子计算机多块、能量分配服务，以及物品 / 流体 / EU 三套存储 handler。

## STRUCTURE
```
common/
├─ CESettings.java, CommonProxy.java
├─ block/           QuantumComputerCasingBlock
├─ circuit/         CircuitPatternData, CircuitPatternService
├─ item/            DynamoCardItem, EUCellItem, EUCellStats, IEUCell, MaintainingCardItem
├─ machine/         ITagFilter, MEPartMachine
│  ├─ energyhatch/  MEEnergyInputConfigurator, MEEnergyPartMachine, MESubstationHatch
│  ├─ gui/          AEConfigSlotWidget, AmountSetWidget, AutoPullAmountConfigurator,
│  │                ConfigWidget, MEDualOutputConfigurator, TagFilterConfigurator
│  ├─ handler/      MEStorageEUHandler, MEStorageFluidHandler, MEStorageItemHandler
│  ├─ iohatch/      MEInputMachine, MEOutputMachine, MEStokingInputMachine
│  ├─ patternbuffer/ MEPatternBuffer
│  └─ utils/        GenericStackHandler, StockingConfigHandler
├─ me/              GenericStackEUStorage, MEMachineEUHandler
│  ├─ cell/         EUCellInventory, EuCellHandler
│  ├─ key/          EUKey, EUKeyType, VoltageKey, VoltageKeyType
│  ├─ parts/p2p/    EUP2PTunnelPart
│  ├─ service/      EnergyDistributeService, IEnergyDistributor
│  └─ strategy/     EUContainerItemStrategy, context/ (CarriedContextEU, PlayerInvContextEU)
├─ multi/           PowerSubstationMachine
├─ pattern/         DynamicProcessingPattern, PatternAuthorData
├─ quantumcomputer/ cpu/     ElapsedTimeTracker, ExecutingCraftingJob, QuantumComputerCluster,
│  │                        VirtualCraftingCPU, VirtualCraftingCPULogic
│  │               gui/     InfoBar, QuantumComputerMenu, QuantumComputerScreen,
│  │                        QuantumCpuSelectionList
│  │               machine/ QuantumComputerMultiblockMachine
│  │               port/    QuantumComputerMENetworkPortBlock, ...BlockEntity
└─ stats/           CEStats
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| 样板署名与编码时间写入 | common/pattern/PatternAuthorData（`addAuthorLore` / `addEncodedTimeLine`） |
| 动态处理样板 | common/pattern/DynamicProcessingPattern, PatternAuthorData |
| 电路样板数据与服务 | common/circuit/CircuitPatternData, CircuitPatternService |
| ME 能源仓配置 | common/machine/energyhatch/MEEnergyInputConfigurator, MESubstationHatch |
| 机器网络端口 | common/machine/MEPartMachine, iohatch/MEInputMachine, MEOutputMachine |
| 样板缓冲 | common/machine/patternbuffer/MEPatternBuffer |
| 仓室 GUI 控件 | common/machine/gui/*Configurator, ConfigWidget, AmountSetWidget |
| 配置缓存（拉取量等） | common/machine/utils/StockingConfigHandler, GenericStackHandler |
| EU 存储/键 | common/me/GenericStackEUStorage, me/key/EUKey, VoltageKey |
| 单元物品 | common/item/EUCellItem, IEUCell, EUCellStats; me/cell/EUCellInventory |
| 能量分配 | common/me/service/EnergyDistributeService, IEnergyDistributor |
| 容器/玩家 EU 上下文 | common/me/strategy/EUContainerItemStrategy, strategy/context/ |
| 量子计算机 | common/quantumcomputer/{machine,cpu,gui,port} |
| 统计 | common/stats/CEStats |

## CONVENTIONS
- `PatternAuthorData.addAuthorLore(stack, playerName)` 是“改写”而非“追加”：重复调用会把署名与编码时间改成当前调用者，并先移除旧署名行，因此同一玩家重复编码也不会在 Lore 中堆叠多条署名。修改已有样板必须走这条路径。
- 署名行以组件 JSON 字符串存入 `display.Lore`；判断/去重前需先反序列化为纯文本再比较（见 `plainText`），不要直接比较 JSON 字符串。
- ME 网络交互统一经 `me/` 下的 handler 与存储类完成，机器类不直接操作 AE2 内部容器。
- 机器数值配置统一用 `machine/utils/StockingConfigHandler` 与 `machine/gui/*Configurator` 组合，不各自实现配置读写。

## ANTI-PATTERNS
- 在 Lore 中直接追加署名行而不清理旧行，导致出现多条“由 X 编码”。
- 在 `common/` 内用物品/方块 ID 字符串反查注册对象，而非 `CEItems.*` / `CEBlocks.*` 等静态对象。
- 绕过 `PatternAuthorData` 自行写 `AUTHOR` / `ENCODE_TIME` / `LORE` 标签。
- 在机器类中硬编码 AE2 网络实现细节，而非使用 `common/me/` 的 handler 或 `api/` 契约。

## SCOPE
`modules/CTNH-Energy/src/main/java/tech/luckyblock/mcmod/ctnhenergy/common/` 下全部子包。

## READ WHEN
- 修改机器 / 仓室 / 总线的行为或 GUI
- 修改 EU 存储、键类型、单元物品或能量分配
- 修改样板署名、电路样板、样板提供者逻辑
- 修改量子计算机 CPU / GUI / 端口

## SOURCE OF TRUTH
`modules/CTNH-Energy/src/main/java/tech/luckyblock/mcmod/ctnhenergy/common/`。注册对象定义以 `registry/` 为准，跨域接口以 `api/` 为准。

## WORKFLOW
1. 定位子包 → 改实现；新注册对象回到 `registry/`；跨域契约回到 `api/`。
2. 样板相关改 `common/pattern/PatternAuthorData`（署名）或 `common/circuit/`（电路样板），不要复制逻辑到 mixin 或客户端。
3. `:modules:CTNH-Energy:build` 编译；涉及 ME 行为在游戏内验证。
