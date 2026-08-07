# CTNH-CORE REGISTRY DOMAIN

## OVERVIEW
Registrate surface for Core (42 Java files): items, blocks, block entities, creative tabs, tags, models, recipe types/modifiers/conditions, GTCEu machines and multiblocks, materials, ores, fluid veins, worldgen layers, and Jade providers.

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
`-- material/                  # CTNHMaterialBlocks, CTNHMaterialFlags, CTNHMaterials, GTMaterialAddon
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
| Block names/lang | `registry/CTNHBlocks.java` (cnlang for block display names) |

## CONVENTIONS
- Registry classes use the `CTNH` prefix.
- Large multiblock registry files use `spotless:off/on`; preserve the local formatting boundary.
- `CTNHCoreGTAddon.initializeAddon()` initializes items, blocks, block entities, and block maps; later hooks register tag prefixes, elements, ore/fluid veins, worldgen layers, recipes, and recipe removals.
- `CTNHRegistrate` and `CTNHRegistration` coexist; treat `CTNHRegistration` as the entry that wires the registrate, not a duplicate.
- Block display names are registered through `createCasingBlock(..., cnlang)` in `CTNHBlocks`; keep block registration and lang in the same file rather than scattering raw lang JSON.
- When referencing items/blocks/fluids, MUST use direct registration objects (static field references like `GTMaterials.Iron`, `CTNHBlocks.MY_BLOCK`, `TagPrefix.ingot`, `AEItems.X`); never `ResourceLocation` string parsing + `ForgeRegistries` lookups except where no registration object exists. See root AGENTS.md CONVENTIONS.

## ANTI-PATTERNS
- Do not manually reformat huge multiblock registry sections protected by Spotless toggles.
- Do not register the same entry from both registry and CommonProxy paths.
- Do not hand-edit generated lang JSON for block names when the registrate `cnlang` is the source of truth.

## SCOPE
Applies to `src/main/java/io/github/cpearl0/ctnhcore/registry` and its child packages.

## READ WHEN
- Adding or changing items, blocks, machines, recipe types, materials, or worldgen registrations in Core.
- Changing block display names/language entries.

## SOURCE OF TRUTH
- `registry/CTNHRegistrate.java`, `registry/CTNHRegistration.java`, and `CTNHCoreGTAddon.java` hook order.
- Generated data: providers in `data/` plus `src/generated/resources`.

## WORKFLOW
1. Identify the registry class group for the entry (items, machines, materials, recipe types, ...).
2. Check GT addon hook order and any datagen references.
3. Run `:modules:CTNH-Core:runData` when data is affected, then `spotlessCheck`.
