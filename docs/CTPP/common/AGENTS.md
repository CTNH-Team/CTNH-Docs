# CTPP COMMON DOMAIN

## OVERVIEW
Shared implementation for CTPP (71 Java files): CommonProxy, blocks, block entities, kinetic machine logic, fan processing, toolbox system, placeable emitter/mirror/beam, and terminal wire hazard.

## STRUCTURE
```text
common/
|-- CommonProxy.java
|-- block/                     # GeneratorCoilBlock, KineticMachineBlock, MagnetBlock, MagnetPlacementHelper, VoltageTerminalBlock, MirrorBlock, CTPPToolboxBlock
|-- blockentity/               # CTPPToolboxBlockEntity, GeneratorCoilBlockEntity, IKineticBlockEntityExtension, KineticMachineBlockEntity, VoltageTerminalBlockEntity
|-- beam/                      # BeamChunkIndex, EmitterBeam, EmitterBeamTracker, IBeamRedirector (mirror reflection)
|-- command/                   # CTPPToolboxCommands, CTPPTerminalCommands (wire_damage_debug on/off)
|-- condition/                 # MechanicalTierCondition (now GTValues.VNF), RPMCondition
|-- data/                      # GTArmInteractionPointTypes
|   `-- model/                 # CTPPMachineModels
|-- gui/widget/                # EmitterAngleDialWidget
|-- item/                      # CTPPToolboxItem, GTHammerItem, GTWireCutterItem
|   `-- debug/                 # ContraptionDebugToolItem
|-- kinetic/fan/
|   |-- acidwashing/           # AcidWashingProcessingType, AcidwashingRecipe
|   |-- breathing/             # BreathingFanProcessingType, BreathingRecipe
|   `-- oiling/                # OilingRecipe
|-- machine/                   # IKineticMachine, NotifiableStressTrait, SimpleKineticElectricWorkableMachine
|   |-- multiblock/            # BigDamMachine, ComplexRotatingMachine, KineticGeneratorMachine (maxKineticInputTier + tier penalty), KineticMultiblockMachine, KineticOutputMachine, KineticTurbineMachine, KineticWorkableMultiblockMachine
|   |   |-- part/              # KineticPartMachine, MechanicalUpgradePartMachine
|   |   `-- windmillController/ # WindMillControlMachine, WindmillManager, WindmillSavedData
|   `-- simple/                # CarbonBrushesGeneratorMachine, ElectricGearBoxMachine, PlaceableEmitterMachine (zenith/azimuth managed fields, no manual markDirty)
|-- menu/                      # CTPPToolboxHostSlot, CTPPToolboxMenu, CTPPToolboxSlot
|-- terminal/                  # TerminalNetwork, TerminalWirePayment, TerminalWireHazardManager, TerminalWireDamageDebug
`-- toolbox/                   # 13: CTPPToolboxBinding(s), CTPPToolboxBlockRegistry, CTPPToolboxEvents, CTPPToolboxInventory, CTPPToolboxItemCapability, CTPPToolboxOperations, CTPPToolboxSavedData, CTPPToolboxService, CTPPToolboxSnapshot, CTPPToolboxSounds, CTPPToolboxSourceId, CTPPToolboxStackData
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Common proxy | `common/CommonProxy.java` |
| Kinetic machines | `common/machine/`, `common/machine/multiblock/` (KineticGeneratorMachine tier penalty logic) |
| Fan processing | `common/kinetic/fan/` (acidwashing/, breathing/, oiling/) |
| Toolbox system | `common/toolbox/` (13 classes) |
| Toolbox menus | `common/menu/` |
| Machine models | `common/data/model/CTPPMachineModels.java` |
| Arm interaction | `common/data/GTArmInteractionPointTypes.java` |
| Conditions | `common/condition/` (RPMCondition, MechanicalTierCondition — now `GTValues.VNF[tier]`) |
| Voltage terminal | `common/block/VoltageTerminalBlock.java`, `common/blockentity/VoltageTerminalBlockEntity.java` (registers wires to `TerminalWireHazardManager`), `common/terminal/` |
| Mirror/beam | `common/block/MirrorBlock.java`, `common/beam/EmitterBeam.java` + `IBeamRedirector.java` |
| Placeable emitter | `common/machine/simple/PlaceableEmitterMachine.java` (managed fields `zenith`/`azimuth`/`transferDisabled`/`consumptionAmps`) |
| Terminal wire hazard | `common/terminal/TerminalWireHazardManager.java`, `api/terminal/TerminalWireGeometry.java` |
| Terminal debug | `common/terminal/TerminalWireDamageDebug.java`, `common/command/CTPPTerminalCommands.java` (`/ctpp wire_damage_debug on/off`) |
| Terminal wire payment | `common/terminal/TerminalWirePayment.java` |

## CONVENTIONS
- `common/CommonProxy.java` initializes config, creative tabs, registrate, datagen, fan-processing deferred registers, machine/recipe listeners, Create arm interaction point type, materials, and client Ponder lang extraction.
- `CTPPGTAddon.initializeAddon()` initializes `CTPPBlocks` and `CTPPBlockMaps`; `registerRecipeCapabilities()` initializes stress capabilities; `registerRecipeKeys()` exposes KubeJS `SU_IN` / `SU_OUT`; `registerMultiblockPreviewHighlighters()` adds kinetic/upgrade ability colors.
- Recipe builders live in `data/recipe/` (top-level), not under `common/`; fan-processing types are in `data/recipe/fanprocessing/`.
- `CTPPToolboxItem.initCapabilities()` provides `CTPPToolboxItemCapability` for capability access.
- `TerminalWirePayment` builds an all-or-nothing fine-wire extraction plan; `TerminalNetwork.handleUse()` uses it instead of direct stack shrink.
- Kinetic multiblock machines require all kinetic inputs to run at the same rotation speed; `RPMCondition` uses `Math.abs(controller.speed)`.
- `KineticGeneratorMachine` now tracks `maxKineticInputTier` from `KineticPartMachine` parts (IO.IN) and applies `getTierPenalty() = (tier-MV)*0.1` when `tier>=HV` (min efficiency 10%); display adds `info4` (Kinetic Hatch Tier Penalty). `onStructureFormed()`/`onStructureInvalid()` reset tier.
- `PlaceableEmitterMachine` managed fields rely on LDLib ref-update for sync/dirty; do not call `markDirty()` manually in `adjustAngle()`/`setAngles()` etc.
- `VoltageTerminalBlockEntity` registers each link to `TerminalWireHazardManager` on `addLink()` and on first `serverTick()` (`terminalWiresRegistered` guard); removal unregisters.

## TRAIT / CAPABILITY LAYERING
动能应力的分层落点（约束以 `docs/_architecture/AGENTS.md` §4 为准）：

| 层 | 实现 |
|----|------|
| Recipe capability | `api/StressRecipeCapability`（`"su"`, Float），并行上限经 `getMaxParallelByInput`；`CTPPRecipeCapabilities.SU` 是其别名 |
| Machine trait | `NotifiableStressTrait extends NotifiableRecipeHandlerTrait<Float> implements ICapabilityTrait` 持有应力 I/O 状态 |
| RecipeLogic | `KineticRecipeLogic`（`KineticMultiblockMachine` 内） |
| Machine 子类 | 只放动能机器特有规则（RPM/tier 判定、结构约束） |

- 应力 I/O 不要用裸 JSON 键拼；`StressRecipeCapability` + KubeJS `SU_IN`/`SU_OUT` + `CTPPRecipeBuilder` 三者配套使用。
- 并行计算属 recipe capability 与 `CTPPParallelLogic`，不要在机器子类里重算。
- 机器字段与 trait 字段禁止并存形成双重所有权。

## ANTI-PATTERNS
- Do not change kinetic/electric machine tiers without checking both registry code and generated models/recipes.
- Do not bypass `TerminalWirePayment` for wire extraction; use the plan to ensure atomicity.
- Do not manually `markDirty()` in `PlaceableEmitterMachine` angle/consumption setters.
- Do not duplicate `TerminalWireGeometry` math in `VoltageTerminalRenderer` or `TerminalWireHazardManager`.

## SCOPE
Applies to `src/main/java/com/mo_guang/ctpp/common` and its child packages.

## READ WHEN
- Implementing kinetic machines, fan processing, the toolbox system, or CommonProxy wiring in CTPP.
- Modifying voltage terminal, terminal wire hazard, mirror/beam, or placeable emitter logic.

## SOURCE OF TRUTH
- `common/CommonProxy.java` and `CTPPGTAddon.java` hook order.
- `common/terminal/TerminalWirePayment.java` and `common/terminal/TerminalNetwork.java`.
- `common/machine/multiblock/KineticGeneratorMachine.java` for tier penalty.
- `common/machine/simple/PlaceableEmitterMachine.java` for managed fields.

## WORKFLOW
1. Check `CommonProxy` init order before adding behavior.
2. Verify recipe capability registration for stress I/O.
3. Run `:modules:CTPP:build`.
