# CTNH-Mana data DOMAIN

## OVERVIEW
Datagen + static data + GT recipe registration source for Mana. ~55 Java files: `CMDatagen`, `ManaData`, `lang(3)`, `materials(1)`, `recipe(35+builder11+utils1)`, `tags(2)`.

## WHERE TO LOOK
| Concern | Location |
|---|---|
| Recipe removal (lib-based) | `recipe/ManaRecipeRemoval.java` (final, `REMOVED_RECIPE_IDS: List<String>`, `init()` no-arg via `RecipeRemovalHelper.remove(new RemoveFilter().id(...))`) |
| GTAddon removal entry | `../CTNHManaGTAddon.java#removeRecipes(ignoredConsumer)` -> calls `ManaRecipeRemoval.init()` + `RemoveFilter().type/idRegex` for `bloodmagic:altar`, `botania:petal_apothecary/runic_altar/terra_plate`, `extrabotany:petal_apothecary`, `mythicbotany:.*_runic_altar`, `bloodmagic:soulforge` |
| Deleted legacy | `recipe/RecipeRemoval.java` REMOVED (old `removePaths: List<String>` + `init(Consumer<ResourceLocation>)` loop); do not restore |
| GT/machine recipes | `recipe/ManaRecipes`, `MachineRecipes`, `ManaMachineRecipes`, `ManaReactorRecipes`, `BeamsRecipes`, `HellForgeRecipes`, `ZenithRecipes`, etc. (35 files) |
| Cross-mod builders | `recipe/builder/botania(7)`, `bloodmagic(2)`, `apotheosis(2)`: `ManaInfusion/ElvenTrade/RuneAltar/TerraPlate`, `BloodAltar/TartaricForge`, `GemCutting/SalvagingRecipeBuilder` + `recipe/utils/BotaniaIngredients` |
| Conditions/custom logic | `api/recipe/condition/*` (`BloodAltar/HellForge/InfusionCellCasting/ZenithCondition`), `api/recipe/customlogic/*` (`EternalGardenLogic`, `IndustrialGemSublimatorLogic`, etc.) used by data recipes |
| Tags/lang/materials | `tags/ItemTags`, `FluidTypeTags`; `lang/EnglishLangHandler`, `ChineseLangHandler`, `AHCCRuneLang`; `materials/BotaniaMaterials`; `CMDatagen`, `ManaData` |

## CONVENTIONS
- Follow parent MODULE CONVENTIONS for dynamic-pack and registry-object rules.
- Removal only via `RecipeRemovalHelper.RemoveFilter`: `.id(String)` for exact IDs, `.type(String)` for `modid:type`, `.idRegex(String)` for patterns; batch exact IDs in `ManaRecipeRemoval.REMOVED_RECIPE_IDS`.
- Keep apotheosis salvaging removals (`apotheosis:salvaging/*`) co-located in `ManaRecipeRemoval` (re-registered under `ctnhmana:salvaging/*` elsewhere).

## ANTI-PATTERNS
- No `DataFilterPack.removeRecipeType/removeRecipe`; no `Consumer<ResourceLocation>` removal loop.
- No string recipe-ID removal outside `ManaRecipeRemoval` + `CTNHManaGTAddon.removeRecipes`; no hard-coded `ResourceLocation.parse` for registry objects.
- No expecting `runData` JSON for GT/dynamic recipes.

## SCOPE
Data-only; logic lives in `api/recipe/*` and `common/multiblock/*`; registry defs in `registry/*`.

## READ WHEN
Editing `data/recipe/*`, `ManaRecipeRemoval`, builders, tags/lang.

## SOURCE OF TRUTH
`com.magicbee.ctnhmana.data` tree; commit 72b5b88 (`RecipeRemoval` -> `ManaRecipeRemoval` + lib helper).

## WORKFLOW
Update this guide when `data/recipe/*` add/delete or removal rules change; keep class names in sync with tree.
