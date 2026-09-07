# CTNH-CORE DATA DOMAIN

## OVERVIEW
Datagen source for `src/generated/resources` (152 Java files): recipe generators split by age/chain/domain, tags, materials (26 sets including BauxiteProcessingMaterials renamed sodium aluminate), and worldgen providers.

## STRUCTURE
```text
data/
|-- CTNHCoreDatagen.java          # datagen entry
|-- CTNHMaterialFlags.java
|-- CreateRecipeTypes.java        # FIX: mechanicalTier Math.min(tier,5) not *2
|-- item/                         # CrystalItems
|-- machines/                     # GTNNMachines
|-- materials/                    # 26 sets: BauxiteProcessingMaterials (IMPURE_SODIUM_ALUMINATE_SOLUTION/PURE_SODIUM_ALUMINATE_SOLUTION renamed from ALUMINIUM_HYDROXIDE, RED_MUD/TITANYL_SULFATE formula updates), BoronChainMaterials NEW, GoldChainMaterials RENAMED, NaquadahMaterials, PlatinumLineMaterials, ...
|-- tags/                         # CTNHBiomeTagsProvider, CTNHEntityTypeTagsProvider, CTNHExtraBlockTagsProvider, CTNHExtraFluidTagsProvider, CTNHExtraItemTagsProvider, ItemTags, StoneTags, TagClearHelper
|-- worldgen/                     # CTNHBiomeModifiers
`-- recipe/
    |-- CTNHCoreRecipeAddition.java  # addRecipes() dispatch root
    |-- RecipeRemoval.java           # ID-only removal filters
    |-- WaferRecipes.java            # precision circuit wafer masking
    |-- (35 top-level classes)
    |-- age/                      # 10: LV..ZPM, PrimitiveKinetic
    |-- chain/                    # 30: AlumiumChain (Al/Ti yield & HCl tuning, VA[HV/MV]), BoronChain NEW, BrineChain, ...
    |-- cogniassembly/            # WetwareCircuit
    |-- create/                   # CafeRecipes, CreateOreExcavationRecipes, CreateRecipeJsonHelper, CreateRecipes, CreateVintageRecipe, DieselGeneratorRecipes
    |-- generated/                # HyperRotorRecipes
    |-- immersiveaircraft/        # ImmersiveAircraftRecipes
    |-- mana/                     # DigesterRecipes, MiscManaRecipes, TwistedFusionRecipes
    |-- migrated/                 # AE2ScriptRecipe, AvaritiaScriptRecipes, BioScriptRecipes, GtceuScriptRecipes
    |-- modmodify/                # EIORecipes
    |   `-- omnicells/            # QuantumOmniRecipes
    |-- multiblock/               # 11: AcceleratorRecipes, AstronomicalObservatoryRecipes, NaquadahReactorRecipes, ...
        |-- utils/                    # ComputationModifier, KeepIngredientRecipeHelper, NuclearComposition
    `-- wood/                     # WoodMachineRecipes, WoodTypeEntries, WoodTypeEntry
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Datagen entry | `data/CTNHCoreDatagen.java` |
| Recipe dispatch root | `data/recipe/CTNHCoreRecipeAddition.java` |
| Bauxite chain | `data/materials/BauxiteProcessingMaterials.java` (IMPURE/PURE_SODIUM_ALUMINATE_SOLUTION, RED_MUD, TITANYL_SULFATE formula updates), `data/recipe/chain/AlumiumChain.java` (Ti/Al yields, HCl reduction) |
| Boron chain | `data/materials/BoronChainMaterials.java`, `data/recipe/chain/BoronChain.java` |
| Gold chain rename | `data/materials/GoldChainMaterials.java` (was CrudeGoldRefiningMaterials) |
| Wafer/precision circuits | `data/recipe/WaferRecipes.java` |
| Create kinetic conversion | `data/CreateRecipeTypes.java` (tier scaling fix) |
| Age-based recipes | `data/recipe/age/` (LV..ZPM, PrimitiveKinetic) |
| Processing chains | `data/recipe/chain/` (30 chains) |
| Create/addon recipes | `data/recipe/create/`, `data/recipe/immersiveaircraft/`, `data/recipe/multiblock/` |
| Wood machine recipes | `data/recipe/wood/` |
| Migrated/script recipes | `data/recipe/migrated/` |
| Mod-modify recipes | `data/recipe/modmodify/`, `data/recipe/modmodify/omnicells/` |
| Mana bridge recipes | `data/recipe/mana/` |
| Generated recipe Java | `data/recipe/generated/` |
| Recipe helpers | `data/recipe/utils/` |
| Materials | `data/materials/` (26 sets), `data/CTNHMaterialFlags.java` |
| Tags/worldgen | `data/tags/`, `data/worldgen/` |

## CONVENTIONS
- `src/generated/resources` is produced by `:modules:CTNH-Core:runData`; never hand-edit generated JSON.
- GT/GMT recipes registered through `CTNHCoreGTAddon.addRecipes()` are runtime dynamic-pack data (`GTDynamicPackContents` / CTNH-Lib `CTNHDynamicDataPack`): `runData` produces NO JSON for them, and their absence from `src/generated/resources` is expected, not a failure. See the root AGENTS.md CONVENTIONS for the full statement.
- Recipe generators are split by age, chain, Create/addons, migrated scripts, mod modifies, mana bridge, multiblock, and wood domains.
- Recipe removal/filtering: `data/recipe/RecipeRemoval.java` registers ID-only filters; `mixin/mc/RecipeManagerApplyMixin.java` removes matching datapack entries at `RecipeManager.apply()` HEAD. Dynamic recipes are intentionally not filtered.
- When referencing items/blocks/fluids, MUST use direct registration objects (static field references like `GTMaterials.Iron`, `CTNHBlocks.MY_BLOCK`, `TagPrefix.ingot`, `AEItems.X`); never `ResourceLocation` string parsing + `ForgeRegistries` lookups except where no registration object exists. See root AGENTS.md CONVENTIONS.
- `CreateRecipeTypes` mechanicalTier scaling is `Math.min(GTUtil.getTierByVoltage(EUt),5)` for MECHANICAL_PRESSOR/MIXER/CENTRIFUGE/SIFTER/LATHE; `*2` was removed.
- Bauxite materials: `IMPURE_SODIUM_ALUMINATE_SOLUTION` formula `(TiO2)(?)+4NaAl(OH)4+nH2O` (was Aluminium Hydroxide), `PURE_SODIUM_ALUMINATE_SOLUTION` `Al(OH)3+NaOH+H2O`, `RED_MUD` `(TiO2)(Fe(OH)3)(?)+nH2O`, `SODIUM_HYDROXIDE_BAUXITE` `(TiO2)(?)(Al2O3)2+4NaOH+nH2O` etc; lang keys `impure/pure_sodium_aluminate_solution` replaced `aluminium_hydroxide_solution`.
- AlumiumChain tuning: GreenSapphire/Sapphire/Ruby centrifuge now `VA[HV]`, silicon/magnesium `VA[MV]`, Ti yield slightly up, Al yield slightly down, HCl usage reduced.

## ANTI-PATTERNS
- Do not hand-edit `src/generated/resources`; change datagen Java then run `runData`.
- Do not add broad cross-mod recipes to feature modules; Core is the aggregator.
- Do not create a new chain without registering it in the dispatch root (`CTNHCoreRecipeAddition`).

## SCOPE
Applies to `src/main/java/io/github/cpearl0/ctnhcore/data` and its child packages.

## READ WHEN
- Adding or changing recipes, tags, materials, or worldgen providers in Core.
- Tracing why a generated resource differs from datagen output.

## SOURCE OF TRUTH
- `data/CTNHCoreDatagen.java`, `data/recipe/CTNHCoreRecipeAddition.java`, and providers under `data/recipe/`.
- Generated output: `src/generated/resources`.

## WORKFLOW
1. Find the matching recipe domain (age/chain/create/migrated/modmodify/mana/multiblock/wood).
2. Edit the generator, then run `:modules:CTNH-Core:runData`.
3. Inspect generated-resource diffs; run `spotlessCheck` after datagen.
