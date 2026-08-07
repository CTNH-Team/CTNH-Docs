# CTNH-ASTRAL DATA DOMAIN

## OVERVIEW
Astral data registration (38 Java files): materials, elements, tag prefixes, recipes, lang, and worldgen (biomes, dimensions, density/noise/surface rules, structures, features).

## STRUCTURE
```text
data/
|-- CAElements.java, CAEnchantments.java, CAMaterials.java, CARecipes.java, CATagPrefixes.java, GTMateralAdjust.java
|-- lang/                      # ChineseLangHandler, EnglishLangHandler
`-- worldgen/
    |-- CABiomes.java, CADensityFunctions.java, CADimensionTypes.java, CADimensions.java
    |-- CANetherRegion.java, CANoiseSetting.java, CAOverworldRegion.java, CASurfaceRuleData.java
    |-- biome/                 # AstralBiomes, BiomeParameters, MoonBiomes, NetherBiomes
    |-- feature/               # AcidPoolFeature, CAConfiguredFeatures, CAFeatures, CAPlacements, MarsDeadVolcanoFeature
    `-- structure/             # 12: AstralMeteorStructure(+Piece/Placer), CAStructureSets, CAStructures, MarsResearchGraveyardStructure(+Piece), MarsStargateRuinsStructure(+Piece), MoonAbandonedOutpostStructure, MoonCraterStructure(+Piece/Placer)
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Core data | `data/CAElements.java`, `CAMaterials.java` (incl. Seawater), `CATagPrefixes.java`, `CARecipes.java` |
| Worldgen root | `data/worldgen/` (CABiomes, CADimensions, CADimensionTypes, CANoiseSetting, CASurfaceRuleData, CAOverworldRegion, CANetherRegion, CADensityFunctions) |
| Biomes | `data/worldgen/biome/` (AstralBiomes, MoonBiomes, NetherBiomes, BiomeParameters) |
| Features | `data/worldgen/feature/` (5) |
| Structures | `data/worldgen/structure/` (12) |
| Lang | `data/lang/` |
| Enchantments | `data/CAEnchantments.java`, `common/enchantment/VacuumSealEnchantment.java` |

## CONVENTIONS
- Worldgen classes are concentrated under `data/worldgen`; dimension classes live directly in the `worldgen` root (no `dimension/` subpackage).
- Datagen output is mostly dynamic registry/sound provider driven; don't infer missing JSON means missing worldgen.
- This module has `src/generated/resources` (lang, blockstates, noise settings); many material model JSON files are static resources under `src/main/resources`.
- `CAMaterials.Seawater` is the Astral seawater fluid (replaces `GTMaterials.SaltWater`); `GTMateralAdjust` no longer adjusts SaltWater block/textures. Moon dimension default fluid uses `CAMaterials.Seawater` (see `CANoiseSetting`).

## ANTI-PATTERNS
- Do not edit one worldgen registry without checking related biome/source/dimension/noise classes.

## SCOPE
Applies to `src/main/java/com/ctnh/ctnhastral/data` and its child packages.

## READ WHEN
- Adding astral materials, fluids, worldgen, dimensions, or lang.

## SOURCE OF TRUTH
- `data/` classes and `CommonProxy.gatherData()` bootstraps.

## WORKFLOW
1. Check related worldgen registries as a group before editing.
2. Run `:modules:CTNH-Astral:runData` when datagen is affected.
