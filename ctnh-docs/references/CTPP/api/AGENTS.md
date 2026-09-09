# CTPP API DOMAIN

## OVERVIEW
Public API surfaces for CTPP (17 Java files): recipe capabilities, multiblock builder, predicates, parallel logic, kinetic machine definitions, and terminal wire geometry.

## STRUCTURE
```text
api/
|-- CTPPModifierFunction.java, CTPPMultiblockBuilder.java, CTPPParallelLogic.java, CTPPPartAbility.java, CTPPPredicates.java
|-- CTPPRecipeCapabilities.java, CTPPRecipeConditions.java
|-- IBlockStressValues.java, KineticMachineDefinition.java, StressRecipeCapability.java, IEnergyTransferHandler.java, CTPPRecipeCapabilities.java
|-- pattern/                   # CTPPBlockMaps, FactoryStaticBlockPattern, StaticBlockPattern
`-- terminal/                  # TerminalLinkState, TerminalProperties, TerminalWireGeometry (shared catenary + collision)
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Stress capability | `api/StressRecipeCapability.java` (`"su"` key, Float) |
| Recipe capabilities | `api/CTPPRecipeCapabilities.java` |
| Recipe conditions | `api/CTPPRecipeConditions.java` (public interface); concrete conditions in `common/condition/` (RPMCondition, MechanicalTierCondition) |
| Multiblock builder | `api/CTPPMultiblockBuilder.java` |
| Parallel logic | `api/CTPPParallelLogic.java` |
| Kinetic definitions | `api/KineticMachineDefinition.java`, `api/IBlockStressValues.java` |
| Predicates | `api/CTPPPredicates.java`, `api/pattern/` (CTPPBlockMaps, FactoryStaticBlockPattern, StaticBlockPattern) |
| Terminal geometry | `api/terminal/TerminalWireGeometry.java` — `points()`, `bounds()`, `radius()`, `segmentCount()` used by both `client/renderer/VoltageTerminalRenderer` and `common/terminal/TerminalWireHazardManager` |

## CONVENTIONS
- `StressRecipeCapability` (`"su"` key, Float) drives kinetic stress I/O and parallel calculation in `KineticWorkableMultiblockMachine` / `KineticOutputMachine`. Lang keys migrated to `ctpp.stressrecipecapability.*`.
- `CTPPRecipeBuilder` (in `data/recipe/builder/`) extends `GTRecipeBuilder` with `.rpm(float)`, `.tier(int)`, `.inputStress(float)`, `.outputStress(float)`, `.noEUt()`.
- `TerminalWireGeometry` is the single source for catenary sag (`sag = min(2.5, length*0.08)`) and radius (`0.035*sqrt(multiplier)`); do not duplicate math in renderer or hazard manager.

## ANTI-PATTERNS
- Do not add stress I/O by raw JSON keys alone; use `StressRecipeCapability`, KubeJS recipe keys, and `CTPPRecipeBuilder` together.
- Do not fork wire geometry; always call `TerminalWireGeometry.points()` / `bounds()`.

## SCOPE
Applies to `src/main/java/com/mo_guang/ctpp/api` and its child packages.

## READ WHEN
- Exposing kinetic/electric machine APIs or recipe capability surfaces.
- Changing terminal wire rendering or collision.

## SOURCE OF TRUTH
- `api/` contracts and `api/CTPPRecipeCapabilities.java` wiring.
- `api/terminal/TerminalWireGeometry.java` for wire math.

## WORKFLOW
1. Confirm the surface is genuinely shared before adding it to `api/`.
2. Check registry wiring for capabilities and conditions.
3. Run `:modules:CTPP:build`.
