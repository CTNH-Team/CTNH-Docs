# CTNH-CORE DATA DOMAIN

## OVERVIEW
Datagen source for `src/generated/resources` (152 Java files): recipe generators split by age/chain/domain, tags, materials (26 sets including new BoronChainMaterials), and worldgen providers.

## STRUCTURE
```text
data/
|-- CTNHCoreDatagen.java          # datagen entry
|-- CTNHMaterialFlags.java
|-- CreateRecipeTypes.java        # FIX: mechanicalTier Math.min(tier,5) not *2 for pressor/mixer/centrifuge/sifter/lathe
|-- item/                         # CrystalItems
|-- machines/                     # GTNNMachines
|-- materials/                    # 26 material sets: BoronChainMaterials NEW, GoldChainMaterials RENAMED (was CrudeGoldRefiningMaterials), NaquadahMaterials, PlatinumLineMaterials, RareEarthMaterials, AdastraMaterials, AeCrystalScienceMaterials, AeOmniMaterials, EnderIOMaterials, WetWareLineMaterials, ZrHfSeparationMaterials, NewExplosivesProductionMaterials (Boric Acid now dust H3BO3), ...
|-- tags/                         # CTNHBiomeTagsProvider, CTNHEntityTypeTagsProvider, CTNHExtraBlockTagsProvider, CTNHExtraFluidTagsProvider, CTNHExtraItemTagsProvider, ItemTags, StoneTags, TagClearHelper
|-- worldgen/                     # CTNHBiomeModifiers
`-- recipe/
    |-- CTNHCoreRecipeAddition.java  # addRecipes() dispatch root - now also BoronChain.init() + WaferRecipes.init()
    |-- RecipeRemoval.java           # ID-only removal filters - now gtceu:electrolyzer/decomposition_electrolyzing_borax + wildcard engrave_ram_*/lpic_*/ssoc_*
    |-- WaferRecipes.java            # NEW: precision circuit wafer masking (rubber-masked wafers -> BSC/LPIC/RAM/SSOC)
    |-- (34->35 top-level classes: AdAstraRecipes, CTNHCraftingComponents, ScalableReservoirComputingRecipes, UHVPartsRecipe, ...)
    |-- age/                      # 10: LVRecipes, EVRecipes, HVRecipes, IVRecipes, LuVRecipes, MVRecipes, UHVRecipes, UVRecipes, ZPMRecipes, PrimitiveKineticAgeRecipes
    |-- chain/                    # 30: AlumiumChain, BoronChain NEW, BrineChain, CementChain, ChromiteChain, CoalChain, ColorfulsocChain, FuelChain, FuelRefiningChain, GeyanChain, GoldChain, GraphiteChain, IodineChain, NaquadahLine, PlatinumLine, RareearthBastnasiteChain, RareearthChain, ...
    |-- cogniassembly/            # WetwareCircuit
    |-- create/                   # CafeRecipes, CreateOreExcavationRecipes, CreateRecipeJsonHelper, CreateRecipes, CreateVintageRecipe, DieselGeneratorRecipes
    |-- generated/                # HyperRotorRecipes (generated recipe Java)
    |-- immersiveaircraft/        # ImmersiveAircraftRecipes
    |-- mana/                     # DigesterRecipes, MiscManaRecipes, TwistedFusionRecipes
    |-- migrated/                 # AE2ScriptRecipe, AvaritiaScriptRecipes, BioScriptRecipes, GtceuScriptRecipes (KJS-migrated)
    |-- modmodify/                # EIORecipes
    |   `-- omnicells/            # QuantumOmniRecipes
    |-- multiblock/               # 11: AcceleratorRecipes, AstronomicalObservatoryRecipes, NaquadahReactorRecipes, PhotovoltaicStationRecipes, SinteringRecipes, SlaughterHouseRecipes, UnderfloorHeatingSystemRecipes, WaterPowerStationRecipes, ...
        |-- utils/                    # ComputationModifier, KeepIngredientRecipeHelper, NuclearComposition
    `-- wood/                     # WoodMachineRecipes, WoodTypeEntries, WoodTypeEntry
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Datagen entry | `data/CTNHCoreDatagen.java` |
| Recipe dispatch root | `data/recipe/CTNHCoreRecipeAddition.java` |
| Boron chain datagen | `data/materials/BoronChainMaterials.java` (BORAX_ACID_SOLUTION, BORON_TRIOXIDE), `data/recipe/chain/BoronChain.java` |
| Gold chain rename | `data/materials/GoldChainMaterials.java` (was CrudeGoldRefiningMaterials) |
| Wafer/precision circuits | `data/recipe/WaferRecipes.java` (rubber-masked silicon/BSC/LPIC/RAM/SSOC wafers) |
| Create kinetic conversion | `data/CreateRecipeTypes.java` (tier scaling fix) |
| Age-based recipes | `data/recipe/age/` (LV..ZPM, PrimitiveKinetic) |
| Processing chains | `data/recipe/chain/` (30 chains) |
| Create/addon recipes | `data/recipe/create/`, `data/recipe/immersiveaircraft/`, `data/recipe/multiblock/` |
| Wood machine recipes | `data/recipe/wood/` (WoodMachineRecipes, WoodTypeEntries, WoodTypeEntry) |
| Migrated/script recipes | `data/recipe/migrated/` (KJS-migrated) |
| Mod-modify recipes | `data/recipe/modmodify/`, `data/recipe/modmodify/omnicells/` |
| Mana bridge recipes | `data/recipe/mana/` |
| Generated recipe Java | `data/recipe/generated/` |
| Recipe helpers | `data/recipe/utils/` |
| Materials | `data/materials/` (26 sets), `data/CTNHMaterialFlags.java` |
| Tags/worldgen | `data/tags/`, `data/worldgen/` |
| Create recipe types | `data/CreateRecipeTypes.java` |

## CONVENTIONS
- `src/generated/resources` is produced by `:modules:CTNH-Core:runData`; never hand-edit generated JSON.
- GT/GMT recipes registered through `CTNHCoreGTAddon.addRecipes()` are runtime dynamic-pack data (`GTDynamicPackContents` / CTNH-Lib `CTNHDynamicDataPack`): `runData` produces NO JSON for them, and their absence from `src/generated/resources` is expected, not a failure. See the root AGENTS.md CONVENTIONS for the full statement.
- Recipe generators are split by age, chain, Create/addons, migrated scripts, mod modifies, mana bridge, multiblock, and wood domains.
- Recipe removal/filtering: `data/recipe/RecipeRemoval.java` registers ID-only filters; `mixin/mc/RecipeManagerApplyMixin.java` removes matching datapack entries at `RecipeManager.apply()` HEAD. Dynamic recipes are intentionally not filtered. Now removes `gtceu:electrolyzer/decomposition_electrolyzing_borax` and uses wildcards `gtceu:laser_engraver/engrave_ram_*`, `engrave_lpic_*`, `engrave_ssoc_*` (previously explicit silicon/phosphorus/naquadah/neutronium variants).
- When referencing items/blocks/fluids, MUST use direct registration objects (static field references like `GTMaterials.Iron`, `CTNHBlocks.MY_BLOCK`, `TagPrefix.ingot`, `AEItems.X`); never `ResourceLocation` string parsing + `ForgeRegistries` lookups except where no registration object exists. See root AGENTS.md CONVENTIONS.
- `CreateRecipeTypes` mechanicalTier scaling is `Math.min(GTUtil.getTierByVoltage(EUt),5)` for MECHANICAL_PRESSOR/MIXER/CENTRIFUGE/SIFTER/LATHE; `*2` was removed. Stress remains `EUt * config.pressorStressRequirement` etc.
- Boron materials: `BORAX_ACID_SOLUTION` liquid formula 2NaCl+4H3BO3+5H2O color 0xE8E8E8, `BORON_TRIOXIDE` dust B2O3 color 0xE8E8F0 DISABLE_DECOMPOSITION; `BORIC_ACID` now dust+liquid components H3BO3 DISABLE_DECOMPOSITION.
- Wafer flow: `RUBBER_MASKED_SILICON_WAFER` (uses gtceu naquadah_wafer texture) + `BSC_WAFER_RUBBER_MASKED`, `LPIC_WAFER_RUBBER_MASKED`, `RAM_WAFER_RUBBER_MASKED`, `SSOC_WAFER_RUBBER_MASKED` replace old `*_masked` names; lang and models updated accordingly.

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
