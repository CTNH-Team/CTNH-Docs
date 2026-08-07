# CTPP API DOMAIN

## OVERVIEW
Public API surfaces for CTPP (13 Java files): recipe capabilities, multiblock builder, predicates, parallel logic, and kinetic machine definitions.

## STRUCTURE
```text
api/
|-- CTPPModifierFunction.java, CTPPMultiblockBuilder.java, CTPPParallelLogic.java, CTPPPartAbility.java, CTPPPredicates.java
|-- CTPPRecipeCapabilities.java, CTPPRecipeConditions.java
|-- IBlockStressValues.java, KineticMachineDefinition.java, StressRecipeCapability.java
`-- pattern/                   # CTPPBlockMaps, FactoryStaticBlockPattern, StaticBlockPattern
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

## CONVENTIONS
- `StressRecipeCapability` (`"su"` key, Float) drives kinetic stress I/O and parallel calculation in `KineticWorkableMultiblockMachine` / `KineticOutputMachine`.
- `CTPPRecipeBuilder` (in `data/recipe/builder/`) extends `GTRecipeBuilder` with `.rpm(float)`, `.tier(int)`, `.inputStress(float)`, `.outputStress(float)`, `.noEUt()`.

## ANTI-PATTERNS
- Do not add stress I/O by raw JSON keys alone; use `StressRecipeCapability`, KubeJS recipe keys, and `CTPPRecipeBuilder` together.

## SCOPE
Applies to `src/main/java/com/mo_guang/ctpp/api` and its child packages.

## READ WHEN
- Exposing kinetic/electric machine APIs or recipe capability surfaces.

## SOURCE OF TRUTH
- `api/` contracts and `api/CTPPRecipeCapabilities.java` wiring.

## WORKFLOW
1. Confirm the surface is genuinely shared before adding it to `api/`.
2. Check registry wiring for capabilities and conditions.
3. Run `:modules:CTPP:build`.