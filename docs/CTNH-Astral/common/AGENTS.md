# CTNH-ASTRAL COMMON DOMAIN

## OVERVIEW
Shared bootstrap and implementation for Astral (19 Java files): CommonProxy, blocks, enchantments, entities, machines, and the oxygen/atmosphere environment system.

## STRUCTURE
```text
common/
|-- CommonProxy.java
|-- block/                     # AstralFlowerBlock, AstralGrass, AstralGrassBlock, AstralSaplingBlock, AstralTallGrassBlock, MarsSaplingBlock, SiliconBuddingBlock
|-- enchantment/               # VacuumSealEnchantment
|-- entity/                    # RocketContraptionEntity
|-- event/                     # RocketDimensionTravelHandler
|-- machine/
|   |-- multiblock/            # RocketAssemblyPlatformMachine
|   `-- simple/                # OxygenEnricherMachine
|-- oxygen/                    # AtmosphereType, OxygenAreaSource, OxygenEnvironment, OxygenEnvironmentService, OxygenMachineRules
`-- recipe/                    # OxygenCondition
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Common proxy | `common/CommonProxy.java` |
| Oxygen/atmosphere | `common/oxygen/` (OxygenEnvironmentService, OxygenEnvironment, OxygenAreaSource, OxygenMachineRules, AtmosphereType) |
| Rocket entities | `common/entity/RocketContraptionEntity.java`, `common/event/RocketDimensionTravelHandler.java` |
| Machines | `common/machine/multiblock/RocketAssemblyPlatformMachine.java`, `common/machine/simple/OxygenEnricherMachine.java` |
| Blocks | `common/block/` (astral grass/sapling/flower, Mars sapling, silicon budding) |
| Recipes/conditions | `common/recipe/OxygenCondition.java` |

## CONVENTIONS
- `CommonProxy.registerMaterials()` also calls `CAMaterials.tagPrefixIgnore()`.
- `CommonProxy.commonSetup()` registers `CAOverworldRegion`, `CANetherRegion`, and overworld/nether surface rules (TerraBlender).
- `CommonProxy.gatherData()` bootstraps biome, configured/placed feature, dimension type, level stem, noise settings, structure, structure set, and density function registries.
- The oxygen system pairs with the OxygenEnricherMachine and the Ad Astra oxygen mixins.

## ANTI-PATTERNS
- Do not bypass CommonProxy registration order.

## SCOPE
Applies to `src/main/java/com/ctnh/ctnhastral/common`.

## READ WHEN
- Changing Astral bootstrap, structures, sounds, enchantments, rockets, or oxygen system registration.

## SOURCE OF TRUTH
- `common/CommonProxy.java` and `CTNHAstral.java`.

## WORKFLOW
1. Check `CommonProxy` registration order before adding hooks.
2. Run `:modules:CTNH-Astral:build`.
