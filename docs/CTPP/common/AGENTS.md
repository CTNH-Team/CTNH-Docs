# CTPP COMMON DOMAIN

## OVERVIEW
Shared implementation for CTPP (73 Java files): CommonProxy, blocks, block entities, kinetic machine logic, fan processing, toolbox system, and recipe builders.

## STRUCTURE
```text
common/
|-- CommonProxy.java
|-- block/                     # CTPPToolboxBlock, GeneratorCoilBlock, KineticMachineBlock, MagnetBlock, MagnetPlacementHelper, VoltageTerminalBlock
|-- blockentity/               # CTPPToolboxBlockEntity, GeneratorCoilBlockEntity, IKineticBlockEntityExtension, KineticMachineBlockEntity, VoltageTerminalBlockEntity
|-- command/                   # CTPPToolboxCommands
|-- condition/                 # MechanicalTierCondition, RPMCondition
|-- data/                      # GTArmInteractionPointTypes
|   `-- model/                 # CTPPMachineModels
|-- item/                      # CTPPToolboxItem, GTHammerItem, GTWireCutterItem
|   `-- debug/                 # ContraptionDebugToolItem
|-- kinetic/fan/
|   |-- acidwashing/           # AcidWashingProcessingType, AcidwashingRecipe
|   |-- breathing/             # BreathingFanProcessingType, BreathingRecipe
|   `-- oiling/                # OilingRecipe
|-- machine/                   # IKineticMachine, KineticWorkableTieredMachine, NotifiableStressTrait, SimpleKineticElectricWorkableMachine, SimpleKineticWorkableMachine
|   |-- multiblock/            # BigDamMachine, ComplexRotatingMachine, KineticGeneratorMachine, KineticMultiblockMachine, KineticOutputMachine, KineticTurbineMachine, KineticWorkableMultiblockMachine
|   |   |-- part/              # KineticPartMachine, MechanicalUpgradePartMachine
|   |   `-- windmillController/ # WindMillControlMachine, WindmillManager, WindmillSavedData
|   `-- simple/                # CarbonBrushesGeneratorMachine, ElectricGearBoxMachine
|-- menu/                      # CTPPToolboxHostSlot, CTPPToolboxMenu, CTPPToolboxSlot
|-- terminal/                  # TerminalNetwork, TerminalWirePayment
`-- toolbox/                   # 13: CTPPToolboxBinding(s), CTPPToolboxBlockRegistry, CTPPToolboxEvents, CTPPToolboxInventory, CTPPToolboxItemCapability, CTPPToolboxOperations, CTPPToolboxSavedData, CTPPToolboxService, CTPPToolboxSnapshot, CTPPToolboxSounds, CTPPToolboxSourceId, CTPPToolboxStackData
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Common proxy | `common/CommonProxy.java` |
| Kinetic machines | `common/machine/`, `common/machine/multiblock/` |
| Fan processing | `common/kinetic/fan/` (acidwashing/, breathing/, oiling/) |
| Toolbox system | `common/toolbox/` (13 classes) |
| Toolbox menus | `common/menu/` |
| Machine models | `common/data/model/CTPPMachineModels.java` |
| Arm interaction | `common/data/GTArmInteractionPointTypes.java` |
| Conditions | `common/condition/` (RPMCondition, MechanicalTierCondition) |
| Voltage terminal | `common/block/VoltageTerminalBlock.java`, `common/blockentity/VoltageTerminalBlockEntity.java`, `common/terminal/` |
| Terminal wire payment | `common/terminal/TerminalWirePayment.java` |

## CONVENTIONS
- `common/CommonProxy.java` initializes config, creative tabs, registrate, datagen, fan-processing deferred registers, machine/recipe listeners, Create arm interaction point type, materials, and client Ponder lang extraction.
- `CTPPGTAddon.initializeAddon()` initializes `CTPPBlocks` and `CTPPBlockMaps`; `registerRecipeCapabilities()` initializes stress capabilities; `registerRecipeKeys()` exposes KubeJS `SU_IN` / `SU_OUT`; `registerMultiblockPreviewHighlighters()` adds kinetic/upgrade ability colors.
- Recipe builders live in `data/recipe/` (top-level), not under `common/`; fan-processing types are in `data/recipe/fanprocessing/`.
- `CTPPToolboxItem.initCapabilities()` provides `CTPPToolboxItemCapability` for capability access.
- `TerminalWirePayment` builds an all-or-nothing fine-wire extraction plan; `TerminalNetwork.handleUse()` uses it instead of direct stack shrink.
- Kinetic multiblock machines require all kinetic inputs to run at the same rotation speed; `RPMCondition` uses `Math.abs(controller.speed)`.

## ANTI-PATTERNS
- Do not change kinetic/electric machine tiers without checking both registry code and generated models/recipes.
- Do not bypass `TerminalWirePayment` for wire extraction; use the plan to ensure atomicity.

## SCOPE
Applies to `src/main/java/com/mo_guang/ctpp/common` and its child packages.

## READ WHEN
- Implementing kinetic machines, fan processing, the toolbox system, or CommonProxy wiring in CTPP.
- Modifying voltage terminal or terminal wire payment logic.

## SOURCE OF TRUTH
- `common/CommonProxy.java` and `CTPPGTAddon.java` hook order.
- `common/terminal/TerminalWirePayment.java` and `common/terminal/TerminalNetwork.java`.

## WORKFLOW
1. Check `CommonProxy` init order before adding behavior.
2. Verify recipe capability registration for stress I/O.
3. Run `:modules:CTPP:build`.