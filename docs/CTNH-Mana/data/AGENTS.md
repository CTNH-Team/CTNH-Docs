# CTNH-MANA DATA DOMAIN

## OVERVIEW
Datagen source for `src/generated/resources` (47 Java files): recipe generators (30), lang, materials, and tags.

## STRUCTURE
```text
data/
|-- CMDatagen.java, ManaData.java
|-- lang/                      # AHCCRuneLang, ChineseLangHandler, EnglishLangHandler
|-- materials/                 # BotaniaMaterials
|-- recipe/
|   |-- 30 top-level classes: ManaReactorRecipes, HellForgeRecipes, WishingWillRecipes, BloodAltarRecipes, BotaniaRecipes, ElvenTradeRecipes, ManaCondenserRecipes, MeteorCapturerRecipes, DemonWillGeneratorRecipes, GaiaReactorRecipes, RuneAltarRecipes, TerraPlateRecipes, ZenithRecipes, TwistCollapseRecipes, ManaHatchRecipes, ManaMachineUpgradeRecipes, BeamsRecipes, RitualMechanicalRecipes, RecipeRemoval, ...
|   |-- builder/
|   |   |-- bloodmagic/        # BloodAltarRecipeBuilder, TartaricForgeRecipeBuilder
|   |   `-- botania/           # ElfPlateRecipeBuilder, ElvenTradeRecipeBuilder, ManaInfusionRecipeBuilder, PetalRecipeBuilder, RuneAltarRecipeBuilder, RuneRitualRecipeBuilder, TerraPlateRecipeBuilder
|   `-- utils/                 # BotaniaIngredients
`-- tags/                      # FluidTypeTags, ItemTags
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Datagen entry | `data/CMDatagen.java` |
| Recipe generation | `data/recipe/` (30 classes, dispatched from `CTNHManaGTAddon.addRecipes()`) |
| Blood Magic builders | `data/recipe/builder/bloodmagic/` (BloodAltarRecipeBuilder, TartaricForgeRecipeBuilder) |
| Botania builders | `data/recipe/builder/botania/` (7 builders) |
| Botania ingredients | `data/recipe/utils/BotaniaIngredients.java` |
| Lang | `data/lang/` (incl. AHCCRuneLang) |
| Materials | `data/materials/BotaniaMaterials.java` |
| Tags | `data/tags/` (FluidTypeTags, ItemTags) |

## CONVENTIONS
- `src/generated/resources` is produced by `:modules:CTNH-Mana:runData`; do not hand-edit generated JSON.
- GT/GMT recipes via `CTNHManaGTAddon.addRecipes()` are runtime dynamic-pack data: `runData` produces NO JSON for them. See root AGENTS.md CONVENTIONS.
- Keep magic-only recipes here; broad cross-module recipes go to Core.
- Ponder scene language extraction happens during client datagen in `event/EventHandler.gatherData()` via CTNH-Lib's `CTNHPonderLang`.

## ANTI-PATTERNS
- Do not hand-edit `src/generated/resources`.

## SCOPE
Applies to `src/main/java/com/moguang/ctnhmana/data` and its child packages.

## READ WHEN
- Adding Mana recipes, lang, materials, or tags.

## SOURCE OF TRUTH
- `data/CMDatagen.java` and `CTNHManaGTAddon.addRecipes()` dispatch in `data/recipe/**`.

## WORKFLOW
1. Edit the matching provider, then run `:modules:CTNH-Mana:runData`.
2. Inspect generated-resource diffs; run `spotlessCheck`.
