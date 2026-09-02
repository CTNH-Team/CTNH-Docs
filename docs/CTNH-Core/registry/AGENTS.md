# CTNH-CORE REGISTRY DOMAIN

## OVERVIEW
Registrate surface for Core (50 Java files): items, blocks, block entities, creative tabs, tags, models, recipe types/modifiers/conditions, GTCEu machines and multiblocks, materials, ores, fluid veins, worldgen layers, sound events, and Jade providers.

## STRUCTURE
```text
registry/
|-- CTNHRegistrate.java        # registrate root
|-- CTNHRegistration.java      # registration entry (coexists with CTNHRegistrate)
|-- CTNHItems.java / CTNHBlocks.java / CTNHBlockEntities.java
|-- CTNHCreativeModeTabs.java / CTNHTags.java / CTNHModels.java / CTNHModelLayers.java / CTNHRenders.java
|-- CTNHRecipeTypes.java / CTNHRecipeModifiers.java / CTNHRecipeConditions.java / CTNHRecipeCategories.java / CTNHRecipes.java
|-- CTNHChanceLogic.java / CTNHGuiTextures.java
|-- CTNHDamageTypes.java / CTNHDimensionMarkers.java / CTNHWorlds.java
|-- CTNHElements.java / CTNHMaterialFlags.java (registry-level)
|-- CTNHFluidVeins.java / CTNHOres.java / CTNHTagPrefixes.java / CTNHWorldgenLayers.java
|-- CTNHTemperatureModifierRegister.java
|-- adventure/                 # CTNHEnchantments
|-- jade/                      # CTNHJadePlugin
|-- machines/                  # CTNHMachines, GTMachineModify
|   `-- multiblock/            # GTNNMultiblocks, HyperPlasmaTurbineRegister, Mechanical, MultiblocksA/B/C, WindPowerArrayRegister
|-- material/                  # CTNHMaterialBlocks, CTNHMaterialFlags, CTNHMaterials, GTMaterialAddon
`-- sound/                     # CTNHSoundEvents (easter_egg_clown)
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Registrate/root | `registry/CTNHRegistrate.java`, `registry/CTNHRegistration.java` |
| Items/blocks/block entities | `registry/CTNHItems.java`, `registry/CTNHBlocks.java`, `registry/CTNHBlockEntities.java` |
| Creative tabs/tags/models | `registry/CTNHCreativeModeTabs.java`, `registry/CTNHTags.java`, `registry/CTNHModels.java`, `registry/CTNHModelLayers.java` |
| GTCEu machines | `registry/machines/CTNHMachines.java`; multiblocks under `registry/machines/multiblock/` (GTNNMultiblocks, MultiblocksA/B/C) plus `registry/CTNHMultiblockMachines.java` |
| Materials/worldgen | `registry/material/CTNHMaterials.java`, `registry/material/GTMaterialAddon.java`, `registry/CTNHTagPrefixes.java`, `registry/CTNHOres.java`, `registry/CTNHFluidVeins.java`, `registry/CTNHWorldgenLayers.java` |
| Recipe types/modifiers/conditions | `registry/CTNHRecipeTypes.java`, `registry/CTNHRecipeModifiers.java`, `registry/CTNHRecipeConditions.java`, `registry/CTNHRecipeCategories.java` |
| Enchantments | `registry/adventure/CTNHEnchantments.java` |
| Jade | `registry/jade/CTNHJadePlugin.java` |
| Sound events | `registry/sound/CTNHSoundEvents.java` |

## CONVENTIONS
- Registry classes use the `CTNH` prefix.
- Large multiblock registry files use `spotless:off/on`; preserve the local formatting boundary.
- `CTNHCoreGTAddon.initializeAddon()` initializes items, blocks, block entities, and block maps; later hooks register tag prefixes, elements, ore/fluid veins, worldgen layers, recipes, and recipe removals.
- `CTNHRegistrate` and `CTNHRegistration` coexist; treat `CTNHRegistration` as the entry that wires the registrate, not a duplicate.
- Sound events are registered via `CTNHSoundEvents.SOUND_EVENTS` in `CommonProxy.init()`; the corresponding `sounds.json` and audio assets live under `src/main/resources/assets/ctnhcore/`.

## ANTI-PATTERNS
- Do not manually reformat huge multiblock registry sections protected by Spotless toggles.
- Do not register the same entry from both registry and CommonProxy paths.

## SCOPE
Applies to `src/main/java/io/github/cpearl0/ctnhcore/registry` and its child packages.

## READ WHEN
- Adding or changing items, blocks, machines, recipe types, materials, sound events, or worldgen registrations in Core.

## SOURCE OF TRUTH
- `registry/CTNHRegistrate.java`, `registry/CTNHRegistration.java`, and `CTNHCoreGTAddon.java` hook order.
- Generated data: providers in `data/` plus `src/generated/resources`.
- Sound events: `registry/sound/CTNHSoundEvents.java` and `src/main/resources/assets/ctnhcore/sounds.json`.

## WORKFLOW
1. Identify the registry class group for the entry (items, machines, materials, recipe types, sound events, ...).
2. Check GT addon hook order and any datagen references.
3. Run `:modules:CTNH-Core:runData` when data is affected, then `spotlessCheck`.