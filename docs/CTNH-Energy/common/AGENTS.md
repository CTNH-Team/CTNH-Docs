# CTNH-ENERGY COMMON DOMAIN

## OVERVIEW
Shared implementation for Energy (60 Java files): CommonProxy, AE2/EU logic, machines, quantum computer, items, and pattern machinery.

## STRUCTURE
```text
common/
|-- CommonProxy.java, CESettings.java
|-- me/                        # AE2/EU core logic
|   |-- GenericStackEUStorage.java, MEMachineEUHandler.java
|   |-- cell/                  # EUCellInventory, EuCellHandler
|   |-- key/                   # EUKey, EUKeyType, VoltageKey, VoltageKeyType
|   |-- parts/p2p/             # EUP2PTunnelPart
|   |-- service/               # EnergyDistributeService, IEnergyDistributor
|   `-- strategy/              # EUContainerItemStrategy
|       `-- context/           # CarriedContextEU, PlayerInvContextEU
|-- machine/
|   |-- ITagFilter.java, MEPartMachine.java   # circuitInventory is @DescSynced
|   |-- energyhatch/           # MEEnergyInputConfigurator, MEEnergyPartMachine, MESubstationHatch
|   |-- gui/                   # AEConfigSlotWidget, AmountSetWidget, AutoPullAmountConfigurator, ConfigWidget, MEDualOutputConfigurator, TagFilterConfigurator
|   |-- handler/               # MEStorageEUHandler, MEStorageFluidHandler, MEStorageItemHandler
|   |-- iohatch/               # MEInputMachine, MEOutputMachine, MEStokingInputMachine
|   |-- patternbuffer/         # MEPatternBuffer
|   `-- utils/                 # GenericStackHandler, StockingConfigHandler
|-- quantumcomputer/
|   |-- cpu/                   # ElapsedTimeTracker, ExecutingCraftingJob, QuantumComputerCluster, VirtualCraftingCPU, VirtualCraftingCPULogic
|   |-- gui/                   # InfoBar, QuantumComputerMenu, QuantumComputerScreen, QuantumCpuSelectionList
|   |-- machine/               # QuantumComputerMultiblockMachine
|   `-- port/                  # QuantumComputerMENetworkPortBlock, QuantumComputerMENetworkPortBlockEntity
|-- block/                     # QuantumComputerCasingBlock
|-- item/                      # DynamoCardItem, EUCellItem, EUCellStats, IEUCell, MaintainingCardItem
|-- multi/                     # PowerSubstationMachine
`-- pattern/                   # DynamicProcessingPattern
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Common proxy | `common/CommonProxy.java` |
| Settings | `common/CESettings.java` |
| AE2/EU keys/cells/P2P | `common/me/key/`, `common/me/cell/`, `common/me/parts/p2p/` |
| Energy distribution | `common/me/service/` (EnergyDistributeService, IEnergyDistributor) |
| Container strategy | `common/me/strategy/` (+ `context/`) |
| Machine EU handler | `common/me/MEMachineEUHandler.java` |
| Pattern buffer | `common/machine/patternbuffer/MEPatternBuffer.java` |
| Circuit inventory sync | `common/machine/MEPartMachine.java` (`@DescSynced` on `circuitInventory`) |
| Energy hatches | `common/machine/energyhatch/` (MEEnergyPartMachine, MESubstationHatch) |
| I/O hatches | `common/machine/iohatch/` (MEInputMachine, MEOutputMachine, MEStokingInputMachine) |
| Storage handlers | `common/machine/handler/` (EU/fluid/item) |
| Machine GUI widgets | `common/machine/gui/` (6 widgets) |
| Quantum computer | `common/quantumcomputer/` (cpu/, gui/, machine/, port/) |
| Items | `common/item/` (EUCellItem, EUCellStats, DynamoCardItem, MaintainingCardItem) |

## CONVENTIONS
- `CommonProxy.init()` initializes config, registrate, AE menus, networking, datagen, gatherData listener, creative tabs, and AE key type registration.
- Common setup registers `EnergyDistributeService`, EU container strategy, EU cell handler/upgrades, pattern-provider upgrade cards, and EU P2P attunement.
- `CommonProxy.attachCapabilities()` adds `generic_eu_wrapper` through `common/me/MEMachineEUHandler.java`.
- `MEPartMachine.circuitInventory` is `@DescSynced`; circuit slot contents are pushed from the server part to the client so GUI slots stay synchronized.
- Do not register EU key/cell behavior only in item code; AE2 key types, storage cell handler, container strategy, upgrades, and P2P attunement are separate CommonProxy hooks.
- `MaintainingCardItem` implements `api/IMaintainingContext` and provides right-click configuration for stocking amount.

## TRAIT OWNERSHIP
Energy 侧 trait 落点：`MEStorageEUHandler` / `MEStorageFluidHandler` / `MEStorageItemHandler`（`NotifiableRecipeHandlerTrait<T>`，前者同时实现 `IEnergyContainer`）、`PowerStationEnergyBank extends MachineTrait`。`MEMachineEUHandler` 只实现 `IEnergyContainer`，不是 trait —— 它由 trait 或机器持有，不要当作 trait 挂载。

约束以 `docs/_architecture/AGENTS.md` 为准，本域重点：

- EU/AE2 状态一份一个所有者：AE key 类型、存储单元 handler、容器策略、升级与 P2P attunement 是各自独立的 CommonProxy 挂载点，不要在物品代码里重复登记（见本文件 ANTI-PATTERNS）。
- 能量容器由 tiered machine 的工厂创建；子类特殊容器需要额外参数时用构造时传入的工厂闭包，让父类调用 `createEnergyContainer` 时保留子类参数，禁止延迟绑定绕开构造参数。
- 量子计算机与 pattern buffer 的 UI 进度属客户端同步状态：`@DescSynced` 已覆盖的字段禁止再写进 Jade NBT。


## ANTI-PATTERNS
- Do not treat quantum computer/menu updates as server-only; UI progress sync is part of the module.

## SCOPE
Applies to `src/main/java/tech/luckyblock/mcmod/ctnhenergy/common` and its child packages.

## READ WHEN
- Implementing AE2/EU behavior, pattern buffer, quantum computer logic, or machine circuit-slot sync.

## SOURCE OF TRUTH
- `common/CommonProxy.java` and `common/me/` contracts.

## WORKFLOW
1. Check `CommonProxy.init()` / common setup hook order before adding behavior.
2. Verify AE key types, container strategy, and P2P attunement wiring.
3. Run `:modules:CTNH-Energy:build`.