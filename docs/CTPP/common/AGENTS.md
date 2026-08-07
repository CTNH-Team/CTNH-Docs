# CTPP COMMON DOMAIN

## OVERVIEW
Shared implementation for CTPP (58 Java files): CommonProxy, blocks, block entities, kinetic machine logic, fan processing, toolbox system, and recipe builders.

## STRUCTURE
```text
common/
|-- CommonProxy.java
|-- block/                     # CTPPToolboxBlock, GeneratorCoilBlock, KineticMachineBlock, MagnetBlock, MagnetPlacementHelper
|-- blockentity/               # CTPPToolboxBlockEntity, GeneratorCoilBlockEntity, IKineticBlockEntityExtension, KineticMachineBlockEntity
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
`-- toolbox/                   # 13: CTPPToolboxBinding(s), CTPPToolboxBlockRegistry, CTPPToolboxEvents, CTPPToolboxInventory, CTPPToolboxOperations, CTPPToolboxSavedData, CTPPToolboxService, CTPPToolboxSnapshot, CTPPToolboxSounds, CTPPToolboxSourceId, CTPPToolboxStackData
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

## CONVENTIONS
- `common/CommonProxy.java` initializes config, creative tabs, registrate, datagen, fan-processing deferred registers, machine/recipe listeners, Create arm interaction point type, materials, and client Ponder lang extraction.
- `CTPPGTAddon.initializeAddon()` initializes `CTPPBlocks` and `CTPPBlockMaps`; `registerRecipeCapabilities()` initializes stress capabilities; `registerRecipeKeys()` exposes KubeJS `SU_IN` / `SU_OUT`; `registerMultiblockPreviewHighlighters()` adds kinetic/upgrade ability colors.
- Recipe builders live in `data/recipe/` (top-level), not under `common/`; fan-processing types are in `data/recipe/fanprocessing/`.

## ANTI-PATTERNS
- Do not change kinetic/electric machine tiers without checking both registry code and generated models/recipes.

## SCOPE
Applies to `src/main/java/com/mo_guang/ctpp/common` and its child packages.

## READ WHEN
- Implementing kinetic machines, fan processing, the toolbox system, or CommonProxy wiring in CTPP.

## SOURCE OF TRUTH
- `common/CommonProxy.java` and `CTPPGTAddon.java` hook order.

## WORKFLOW
1. Check `CommonProxy` init order before adding behavior.
2. Verify recipe capability registration for stress I/O.
3. Run `:modules:CTPP:build`.
