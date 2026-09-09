# CTNH-BIO DATA DOMAIN

## OVERVIEW
Datagen source for `src/generated/resources` (28 Java files): recipe generators, lang, loot, materials, and tags.

## STRUCTURE
```text
data/
|-- CBDatagen.java, CBElements.java
|-- lang/                      # ChineseLangHandler, EnglishLangHandler
|   `-- utils/                 # EntityPropertyLangUtil
|-- loot/                      # CBLootTableProvider
|-- materials/                 # CommonMaterials, OrganicMaterials
|-- recipe/
|   |-- CBRecipeBuilder.java, CBRecipeCategories.java, CogniRecipeBuilder.java
|   |-- CommonRecipes.java, CustomTags.java, LivingMachineRecipes.java, RecipeRemoval.java
|   |-- VanillaRecipeProvider.java, VanillaRecipes.java
|   |-- living/                # BasicLivingRecipes, BioReactorRecipes, BioelectricForgeRecipes, DecomposerRecipes, DigesterRecipes
|   `-- multi/                 # CogniRecipes, GreatFleshRecipes, HostileObservationRecipes
`-- tags/                      # BlockTags, FluidTags, ItemTags
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Datagen entry | `data/CBDatagen.java` |
| Recipe generation | `data/recipe/` (CommonRecipes, VanillaRecipes, LivingMachineRecipes, RecipeRemoval) |
| Living recipes | `data/recipe/living/` (BioReactor, BioelectricForge, Decomposer, Digester, BasicLiving) |
| Multi recipes | `data/recipe/multi/` (Cogni, GreatFlesh, HostileObservation) |
| Lang | `data/lang/`, `data/lang/utils/` |
| Loot | `data/loot/CBLootTableProvider.java` |
| Materials | `data/materials/` (CommonMaterials, OrganicMaterials) |
| Tags | `data/tags/` (BlockTags, FluidTags, ItemTags) |

## CONVENTIONS
- Keep Bio-specific living-machine recipes here; cross-module recipes usually go to Core.
- GT/GMT recipes via `CTNHBioGTAddon.addRecipes()` are runtime dynamic-pack data: `runData` produces NO JSON for them. See root AGENTS.md CONVENTIONS.
- `src/generated/resources` is produced by `:modules:CTNH-Bio:runData`; do not hand-edit generated JSON.
- Some recipe JSON is hand-authored under `src/main/resources/data/ctnhbio/recipes/decomposing`; check the source root before regenerating.

## ANTI-PATTERNS
- Do not assume all recipe JSON is generated; check whether it is under `src/main/resources` or `src/generated/resources`.

## SCOPE
Applies to `src/main/java/com/moguang/ctnhbio/data` and its child packages.

## READ WHEN
- Adding Bio recipes, lang, loot, materials, or tags.

## SOURCE OF TRUTH
- `data/CBDatagen.java` and providers under `data/recipe/`.

## WORKFLOW
1. Edit the matching provider, then run `:modules:CTNH-Bio:runData`.
2. Inspect generated-resource diffs; run `spotlessCheck`.
