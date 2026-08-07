# CTNH-CORE COMMON DOMAIN

## OVERVIEW
Shared (client+server) implementation for Core: CommonProxy, blocks, block entities, capabilities, enchantments, entities, GUIs, items, machines, recipes, and world handling. This is the largest domain (119 Java files), dominated by the multiblock machine hierarchy.

## STRUCTURE
```text
common/
|-- CommonProxy.java              # registration hub
|-- block/                        # CoilType, PhotovoltaicBlock, TurbineRotorBlock, CTNHFusionCasingType, SpaceStructuralFramework
|   `-- blockdata/                # IPBData, ISSFData, PlanetMinerData (block data attachments)
|-- blockentity/                  # TurbineRotorBE
|-- capability/                   # EIOCapacitorProvider (EIO capacitor capabilities, namespace/remap helpers)
|-- enchantment/                  # TemperatureEnchantment
|-- entity/monster/               # astralslime/AstralSlime, sightseerspitter/SightSeerSpitter
|-- gui/                          # WPAAcceleratorGui, MachineModeFancyConfiguratorTest (legacy leftover)
|   |-- terminal/                 # TerminalInputWidget
|   `-- widget/                   # SimpleNumberInputWidget
|-- item/                         # ArkOfHomoItem, AstronomyCircuitItem, MEAdvancedTerminalItem, SnowCitySwordItem, ThrowableSummoner, TurbineRotorItem, ConnectTerminalItem, ProgramItem, MultiblockHelper, SingleItemHandler, TagPrefixBehavior, CatalystBehavior, IThrowableItem, IDroneItem, IDataItem
|   `-- debug/                    # ReloadItem
|-- machine/
|   |-- cover/                    # CreativeEnergyCover
|   |-- multiblock/               # KineticElectricMultiblockMachine, LargeBottleMachine, MultiblockComputationMachine, SlaughterHouseMachine, UnderfloorHeatingMachine
|   |   |-- electric/             # 33 machines: WideParticleAccelerator, NeutronActivatorMachine, PlanetMiner, LargeDigitalMinerMachine, VoidMinerProcessingMachine (+VoidMinerRecipeLogic), INFFluidDrillMachine (+INFFluidDrillLogic), MegaLCRMachine, NeuroMatrixCompiler, ScalableReservoirComputingMachine, Superconducting_Penning_Trap, ...
|   |   |   `-- multithread/      # CNCAlloySmelter
|   |   |-- generator/            # 12 machines: Arc_Generator, Arc_Reactor, ChemicalGeneratorMachine, HyperPlasmaTurbineMachine, LargeNaquadahReactorMachine, MegaTurbineMachine, NanoscaleTriboelectricGenerator, NaqReactorMachine, PhotoVoltaicDroneStation, PhotovoltaicPowerStationMachine, WaterPowerStationMachine, WindPowerArrayMachine
|   |   |-- kinetic/              # IndustrialPrimitiveBlastFurnaceMachine, MeadowMachine, NoEnergyMachine
|   |   |-- part/                 # 12 parts: CTNHPartAbility, CatalystHatchPartMachine, CircuitBusPartMachine, CompilerMachine, CreativeEnergyHatchPartMachine, CreativeInputBusPartMachine, CreativeInputHatchPartMachine, CreativeLaserHatchPartMachine, DroneHolderMachine, HighSpeedPipeBlock, NeutronAcceleratorMachine, NeutronSensorMachine
|   |   `-- quantum/              # quantum_core
|   |-- simple/                   # DigitalMiner, EfficiencyGeneratorMachine, HighPerformanceComputerMachine, SimpleComputationMachine
|   `-- trait/                    # ScalableReservoirComputingLogic, SimpleComputationContainer
|       `-- providable_net/       # IProviableNetHandlerMachine, ProvidableNetHandler, ProvidableNetInfo, ProviderInfo
|-- recipe/                       # KeepIngredientShapedRecipe, NeutronActivatorCondition, PlantCasingCondition, TierCasingCondition
|   `-- builder/                  # CTNHRecipeBuilder
`-- world/                        # CTNHChunkLoading
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Common proxy | `common/CommonProxy.java` |
| Blocks/block data | `common/block/`, `common/block/blockdata/` |
| Block entities | `common/blockentity/` |
| Capabilities | `common/capability/` |
| Enchantments | `common/enchantment/` |
| Entities | `common/entity/monster/` |
| GUIs | `common/gui/`, `common/gui/terminal/`, `common/gui/widget/` |
| Items | `common/item/`, `common/item/debug/` |
| Electric multiblocks | `common/machine/multiblock/electric/` (33) |
| Generator multiblocks | `common/machine/multiblock/generator/` (12) |
| Kinetic multiblocks | `common/machine/multiblock/kinetic/` (3) |
| Machine parts | `common/machine/multiblock/part/` (12) |
| Simple machines | `common/machine/simple/` (4) |
| Machine traits | `common/machine/trait/`, `common/machine/trait/providable_net/` |
| Recipe builders | `common/recipe/`, `common/recipe/builder/` |
| World | `common/world/CTNHChunkLoading.java` |

## CONVENTIONS
- `CommonProxy.java` registers config, registrate, recipe conditions, machines, recipe types, datagen, creative tabs, and client/server setup listeners.
- Machine implementations live here; their registrate entries live in `registry/machines/` and `registry/CTNHMachines.java`.
- Electric multiblocks follow `*Machine` naming (some legacy files use `*_old` or snake_case); parts implement `CTNHPartAbility`.

## ANTI-PATTERNS
- Do not bypass `CommonProxy` registration order; registry dependencies are deliberate.
- Do not put client-only rendering in common machine classes.
- Do not treat `WPA_old.java` or `MachineModeFancyConfiguratorTest` as current implementation; both are legacy leftovers.

## SCOPE
Applies to `src/main/java/io/github/cpearl0/ctnhcore/common` and its child packages.

## READ WHEN
- Implementing blocks, machines, items, capabilities, or entities in Core.
- Changing CommonProxy registration or Forge event wiring.

## SOURCE OF TRUTH
- `common/CommonProxy.java` (registration), `registry/` (entries), `event/ForgeEventHandler.java` (runtime hooks).

## WORKFLOW
1. Confirm the behavior belongs in Core rather than a feature module.
2. Check `CommonProxy` registration and any GT addon hooks that reference the new content.
3. Run the narrowest Gradle task; regenerate data when datagen inputs changed.
