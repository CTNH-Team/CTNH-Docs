# CTNH-CORE DATA DOMAIN

## OVERVIEW
Datagen source for `src/generated/resources` (141 Java files, the second-largest Core domain): recipe generators split by age/chain/domain, tags, materials (25 sets), and worldgen providers.

## STRUCTURE
```text
data/
|-- CTNHCoreDatagen.java          # datagen entry
|-- CTNHMaterialFlags.java
|-- CreateRecipeTypes.java
|-- item/                         # CrystalItems
|-- machines/                     # GTNNMachines
|-- materials/                    # 25 material sets: NaquadahMaterials, PlatinumLineMaterials, RareEarthMaterials, AdastraMaterials, AeCrystalScienceMaterials, AeOmniMaterials, EnderIOMaterials, WetWareLineMaterials, ZrHfSeparationMaterials, ...
|-- tags/                         # CTNHBiomeTagsProvider, CTNHEntityTypeTagsProvider, CTNHExtraBlockTagsProvider, CTNHExtraFluidTagsProvider, CTNHExtraItemTagsProvider, ItemTags, StoneTags, TagClearHelper
|-- worldgen/                     # CTNHBiomeModifiers
`-- recipe/
    |-- CTNHCoreRecipeAddition.java  # addRecipes() dispatch root
    |-- RecipeRemoval.java           # ID-only removal filters
    |-- (32 top-level classes: AdAstraRecipes, CTNHCraftingComponents, ScalableReservoirComputingRecipes, UHVPartsRecipe, EUCellRecipes, MachinesRecipes, ...)
    |-- age/                      # 10: LVRecipes, EVRecipes, HVRecipes, IVRecipes, LuVRecipes, MVRecipes, UHVRecipes, UVRecipes, ZPMRecipes, PrimitiveKineticAgeRecipes
    |-- chain/                    # 25: AlumiumChain, BrineChain, CementChain, ChromiteChain, CoalChain, FuelChain, FuelRefiningChain, GoldChain, GraphiteChain, IodineChain, NaquadahLine, PlatinumLine, RareearthChain, SiliconChain, SpaceFabric, StonedustChain, TiChain, WoodChain, ZirconChain, ...
    |-- cogniassembly/            # WetwareCircuit
    |-- create/                   # CafeRecipes, CreateOreExcavationRecipes, CreateRecipeJsonHelper, CreateRecipes, CreateVintageRecipe, DieselGeneratorRecipes
    |-- generated/                # HyperRotorRecipes (generated recipe Java)
    |-- immersiveaircraft/        # ImmersiveAircraftRecipes
    |-- mana/                     # DigesterRecipes, MiscManaRecipes, TwistedFusionRecipes
    |-- migrated/                 # AE2ScriptRecipe, AvaritiaScriptRecipes, BioScriptRecipes, GtceuScriptRecipes (KJS-migrated)
    |-- modmodify/                # EIORecipes
    |   `-- omnicells/            # QuantumOmniRecipes
    |-- multiblock/               # 11: AcceleratorRecipes, AstronomicalObservatoryRecipes, NaquadahReactorRecipes, PhotovoltaicStationRecipes, SinteringRecipes, SlaughterHouseRecipes, UnderfloorHeatingSystemRecipes, WaterPowerStationRecipes, ...
    |-- tconstruct/               # EMPTY leftover directory
    |-- utils/                    # ComputationModifier, KeepIngredientRecipeHelper, NuclearComposition
    `-- wood/                     # WoodMachineRecipes, WoodTypeEntries, WoodTypeEntry
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Datagen entry | `data/CTNHCoreDatagen.java` |
| Recipe dispatch root | `data/recipe/CTNHCoreRecipeAddition.java` |
| Age-based recipes | `data/recipe/age/` (LV..ZPM, PrimitiveKinetic) |
| Processing chains | `data/recipe/chain/` (25 chains) |
| Create/addon recipes | `data/recipe/create/`, `data/recipe/immersiveaircraft/`, `data/recipe/multiblock/` |
| Wood machine recipes | `data/recipe/wood/` (WoodMachineRecipes, WoodTypeEntries, WoodTypeEntry) |
| Migrated/script recipes | `data/recipe/migrated/` (KJS-migrated) |
| Mod-modify recipes | `data/recipe/modmodify/`, `data/recipe/modmodify/omnicells/` |
| Mana bridge recipes | `data/recipe/mana/` |
| Generated recipe Java | `data/recipe/generated/` |
| Recipe helpers | `data/recipe/utils/` |
| Materials | `data/materials/` (25 sets), `data/CTNHMaterialFlags.java` |
| Tags/worldgen | `data/tags/`, `data/worldgen/` |
| Create recipe types | `data/CreateRecipeTypes.java` |

## CONVENTIONS
- `src/generated/resources` is produced by `:modules:CTNH-Core:runData`; never hand-edit generated JSON.
- GT/GMT recipes registered through `CTNHCoreGTAddon.addRecipes()` are runtime dynamic-pack data (`GTDynamicPackContents` / CTNH-Lib `CTNHDynamicDataPack`): `runData` produces NO JSON for them, and their absence from `src/generated/resources` is expected, not a failure. See the root AGENTS.md CONVENTIONS for the full statement.
- Recipe generators are split by age, chain, Create/addons, migrated scripts, mod modifies, mana bridge, multiblock, and wood domains.
- Recipe removal/filtering: `data/recipe/RecipeRemoval.java` registers ID-only filters; `mixin/mc/RecipeManagerApplyMixin.java` removes matching datapack entries at `RecipeManager.apply()` HEAD. Dynamic recipes are intentionally not filtered.
- When referencing items/blocks/fluids, MUST use direct registration objects (static field references like `GTMaterials.Iron`, `CTNHBlocks.MY_BLOCK`, `TagPrefix.ingot`, `AEItems.X`); never `ResourceLocation` string parsing + `ForgeRegistries` lookups except where no registration object exists. See root AGENTS.md CONVENTIONS.
- `data/recipe/tconstruct/` is an empty leftover directory; do not add files there without first checking where TConstruct recipes actually live.
- Recent recipe changes: PrimitiveKineticAgeRecipes now includes cinnabar/realgar/pyrite/chalcopyrite centrifugation; CreateRecipes now crushes GT ingots to dust (not vanilla ingots) and removes Create silver/brass recipes; OreProcessingRecipes melts PreciousAlloy to liquid gold; GoldChain now uses fluid copper chloride and adds sodium cyanide production; `MachinesRecipes` overrides `gtceu:shaped/ulv_machine_hull` to use `minecraft:planks` tag.

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
