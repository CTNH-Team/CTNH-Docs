# CTNH-MANA REGISTRY DOMAIN

## OVERVIEW
Registrate surface for Mana (27 Java files): items, blocks, block entities, entities, machines, multiblocks, materials, elements, tag prefixes, recipe types, effects, sounds, and particles.

## STRUCTURE
```text
registry/
|-- CMRegistrate.java, CMBlockEntities.java, CMBlocks.java, CMCreativeModeTabs.java, CMElements.java, CMEntities.java
|-- CMGuiTextures.java, CMItems.java, CMMachines.java, CMMaterials.java, CMMobEffects.java, CMModelLayers.java
|-- CMMultiblockMachines.java, CMParticleTypes.java, CMRecipeConditions.java, CMRecipeTypes.java, CMRegistrate.java, CMTagPrefixes.java, CMTags.java, GTMaterialAddon.java
|-- items/                    # CMFuelItems
|-- multiblock/               # 5: BloodMagic, Botania, ManaMachine, Misc, ZenithMachine
`-- sounds/                   # CMSoundDefinitionsProvider, CMSoundEvent
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Registrate/root | `registry/CMRegistrate.java` |
| Items | `registry/CMItems.java`, `registry/items/CMFuelItems.java` |
| Blocks/block entities/entities | `registry/CMBlocks.java`, `registry/CMBlockEntities.java`, `registry/CMEntities.java` |
| Machines/multiblocks | `registry/CMMachines.java`, `registry/CMMultiblockMachines.java`, grouped files under `registry/multiblock/` (BloodMagic, Botania, ManaMachine, Misc, ZenithMachine) |
| Materials/elements/tag prefixes | `registry/CMMaterials.java`, `CMElements.java`, `CMTagPrefixes.java`, `GTMaterialAddon.java` |
| Recipe types/conditions | `registry/CMRecipeTypes.java`, `CMRecipeConditions.java` |
| Effects/sounds/particles | `CMMobEffects.java`, `CMParticleTypes.java`, `registry/sounds/`, `CMModelLayers.java`, `CMGuiTextures.java` |

## CONVENTIONS
- Registry classes use the `CM` prefix.
- `CTNHManaGTAddon.initializeAddon()` initializes items, blocks, and block entities; `registerTagPrefixes()` and `registerElements()` initialize Mana tag/material data; `removeRecipes()` delegates to `RecipeRemoval`.

## ANTI-PATTERNS
- Do not register the same entry from both registry and EventHandler paths.

## SCOPE
Applies to `src/main/java/com/moguang/ctnhmana/registry` and its child packages.

## READ WHEN
- Adding or changing Mana items, blocks, machines, multiblocks, materials, or recipe types.

## SOURCE OF TRUTH
- `registry/CMRegistrate.java` and `CTNHManaGTAddon.java` / `event/EventHandler.java` hook order.

## WORKFLOW
1. Identify the registry class group for the entry.
2. Check GT addon hook order and EventHandler registration.
3. Run `:modules:CTNH-Mana:runData` when data is affected.
