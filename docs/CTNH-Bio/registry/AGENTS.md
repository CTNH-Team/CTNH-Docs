# CTNH-BIO REGISTRY DOMAIN

## OVERVIEW
Registrate surface for Bio (17 Java files): items, blocks, entities, materials, effects, serums, sounds, tags, machines, multiblocks, and recipe types.

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Registrate/root | `registry/CBRegistrate.java` |
| Items/blocks/entities | `registry/CBItems.java`, `registry/CBBlocks.java`, `registry/CBEntities.java`, `registry/CBMaterialItems.java` |
| Machines/multiblocks | `registry/CBMachines.java`, `registry/CBMultiblocks.java` |
| Materials/effects/serums/sounds/tags | `registry/CBMaterials.java`, `CBMobEffects.java`, `CBSerums.java`, `CBSoundEntries.java`, `CBTags.java` |
| Recipe types/recipes/capabilities/conditions | `registry/CBRecipeTypes.java`, `CBRecipes.java`, `CBRecipeCapabilities.java`, `CBRecipeConditions.java` |
| Creative tabs | `registry/CBCreativeModeTabs.java` |
| Recipe modifiers | `utils/CBRecipeModifiers.java` (see utils domain) |

## CONVENTIONS
- Registry classes use the `CB` prefix.
- `CTNHBioGTAddon.initializeAddon()` initializes items/blocks and registers `ModelIngredient` map ingredients; `registerRecipeCapabilities()` initializes `CBRecipeCapabilities`; `registerRecipeKeys()` exposes nutrient KubeJS keys `NU_IN` / `NU_OUT`.

## ANTI-PATTERNS
- Do not register the same entry from both registry and CommonProxy paths.

## SCOPE
Applies to `src/main/java/com/moguang/ctnhbio/registry`.

## READ WHEN
- Adding or changing Bio items, blocks, entities, machines, recipes, or materials.

## SOURCE OF TRUTH
- `registry/CBRegistrate.java` and `CTNHBioGTAddon.java` hook order.

## WORKFLOW
1. Identify the registry class group for the entry.
2. Check GT addon hook order and datagen references.
3. Run `:modules:CTNH-Bio:runData` when data is affected.
