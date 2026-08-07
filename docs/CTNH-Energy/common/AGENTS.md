# CTNH-ENERGY COMMON DOMAIN

## OVERVIEW
Shared implementation for Energy (55 Java files): CommonProxy, AE2/EU logic, machines, quantum computer, items, and pattern machinery.

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
|   |-- ITagFilter.java, MEPartMachine.java
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
|-- item/                      # DynamoCardItem, EUCellItem, EUCellStats, IEUCell
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
| Container strategy | `common/me/strategy/` (+ context/) |
| Machine EU handler | `common/me/MEMachineEUHandler.java` |
| Pattern buffer | `common/machine/patternbuffer/MEPatternBuffer.java` |
| Energy hatches | `common/machine/energyhatch/` (MEEnergyPartMachine, MESubstationHatch) |
| I/O hatches | `common/machine/iohatch/` (MEInputMachine, MEOutputMachine, MEStokingInputMachine) |
| Storage handlers | `common/machine/handler/` (EU/fluid/item) |
| Machine GUI widgets | `common/machine/gui/` (6 widgets) |
| Quantum computer | `common/quantumcomputer/` (cpu/, gui/, machine/, port/) |
| Items | `common/item/` (EUCellItem, EUCellStats, DynamoCardItem) |

## CONVENTIONS
- `CommonProxy.init()` initializes config, registrate, AE menus, networking, datagen, gatherData listener, creative tabs, and AE key type registration.
- Common setup registers `EnergyDistributeService`, EU container strategy, EU cell handler/upgrades, pattern-provider upgrade cards, and EU P2P attunement.
- `CommonProxy.attachCapabilities()` adds `generic_eu_wrapper` through `common/me/MEMachineEUHandler.java`.
- Do not register EU key/cell behavior only in item code; AE2 key types, storage cell handler, container strategy, upgrades, and P2P attunement are separate CommonProxy hooks.

## ANTI-PATTERNS
- Do not treat quantum computer/menu updates as server-only; UI progress sync is part of the module.

## SCOPE
Applies to `src/main/java/tech/luckyblock/mcmod/ctnhenergy/common` and its child packages.

## READ WHEN
- Implementing AE2/EU behavior, pattern buffer, or quantum computer logic.

## SOURCE OF TRUTH
- `common/CommonProxy.java` and `common/me/` contracts.

## WORKFLOW
1. Check `CommonProxy.init()` / common setup hook order before adding behavior.
2. Verify AE key types, container strategy, and P2P attunement wiring.
3. Run `:modules:CTNH-Energy:build`.
