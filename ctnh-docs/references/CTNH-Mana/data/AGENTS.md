# CTNH-MANA DATA DOMAIN

## OVERVIEW
Datagen source for `src/generated/resources` (55 Java files): recipe generators (35), lang, materials, tags, and builders.

## STRUCTURE
```text
data/
|-- CMDatagen.java, ManaData.java
|-- lang/                      # AHCCRuneLang, ChineseLangHandler, EnglishLangHandler
|-- materials/                 # BotaniaMaterials
|-- recipe/
|   |-- 35 top-level classes: BeamsRecipes, BloodAltarRecipes, BotaniaRecipes, DemonWillGeneratorRecipes, ElvenTradeRecipes, EternalGardenRecipes, EternalGardenSpecialRecipes, EternalWosRecipes, GaiaReactorRecipes, GemCuttingRecipes, HellForgeRecipes, MachineRecipes, ManaCircuitRecipes, ManaCondenserRecipes, ManaHatchRecipes, ManaMachineBlockRecipes, ManaMachineRecipes, ManaMachineUpgradeRecipes, ManaPoolRecipes, ManaReactorRecipes, ManaRecipes, ManaTransformerRecipes, MeteorCapturerRecipes, MeteorRitualGuideRecipes, RecipeRemoval, RitualMechanicalRecipes, RuneAltarRecipes, RuneSalvagingRecipes, SalvagingRecipes, TerraPlateRecipes, TwistCollapseRecipes, WishingWillRecipes, ZenithRecipes, runeRitualRecipes
|   |-- builder/
|   |   |-- apotheosis/        # GemCuttingRecipeBuilder, SalvagingRecipeBuilder
|   |   |-- bloodmagic/        # BloodAltarRecipeBuilder, TartaricForgeRecipeBuilder
|   |   `-- botania/           # ElfPlateRecipeBuilder, ElvenTradeRecipeBuilder, ManaInfusionRecipeBuilder, PetalRecipeBuilder, RuneAltarRecipeBuilder, RuneRitualRecipeBuilder, TerraPlateRecipeBuilder
|   `-- utils/                 # BotaniaIngredients
`-- tags/                      # FluidTypeTags, ItemTags
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Datagen entry | `data/CMDatagen.java` |
| Recipe generation | `data/recipe/` (35 classes, dispatched from `CTNHManaGTAddon.addRecipes()`) |
| Gem cutting recipes | `data/recipe/GemCuttingRecipes.java` |
| Mana transformer recipe | `data/recipe/ManaTransformerRecipes.java` |
| Blood Magic builders | `data/recipe/builder/bloodmagic/` (BloodAltarRecipeBuilder, TartaricForgeRecipeBuilder) |
| Botania builders | `data/recipe/builder/botania/` (7 builders) |
| Apotheosis builders | `data/recipe/builder/apotheosis/` (GemCuttingRecipeBuilder, SalvagingRecipeBuilder) |
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
Applies to `src/main/java/com/magicbee/ctnhmana/data` and its child packages.

## READ WHEN
- Adding Mana recipes, lang, materials, or tags.

## SOURCE OF TRUTH
- `data/CMDatagen.java` and `CTNHManaGTAddon.addRecipes()` dispatch in `data/recipe/**`.

## WORKFLOW
1. Edit the matching provider, then run `:modules:CTNH-Mana:runData`.
2. Inspect generated-resource diffs; run `spotlessCheck`.