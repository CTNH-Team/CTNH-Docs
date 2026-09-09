# CTNH-CORE MODULE

## OVERVIEW
CTNH-Core is the aggregate/core mod and CI release target (largest module). It hosts shared CTNH gameplay systems, GTCEu integration, large machine registries, generated data, Core-owned Ponder scenes, and cross-mod content.

## STRUCTURE
```text
src/main/java/io/github/cpearl0/ctnhcore/
|-- CTNHCore.java             # Forge mod initialization
|-- CTNHCoreGTAddon.java      # GTCEu addon hooks; addRecipes() dispatches data/recipe/**
|-- CTNHConfig.java           # module config
|-- api/                      # public APIs: multiblock builder, patterns, machine features (17 Java files)
|   |-- CTNHMultiblockBuilder.java
|   |-- Pattern/              # AsynBlockPattern, CTNHBlockMaps, CTNHBoilerFireboxType, CTNHPredicates (AsynBlockPattern null/empty guards for AE extract)
|   |-- data/material/        # icon sets/types, property keys, catalyst property
|   |-- gui/                  # CTNHGuiTextures
|   |-- jade/                 # multithread recipe/output/thread providers
|   |-- machine/feature/      # IDigitalMiner, IDynamicCasing (ICoilMachine removed -> CoilMachineTrait in GTCEu)
|   |-- machine/multiblock/   # UnlimitedItemStackTransfer
|   `-- recipe/               # DigitalMinerLogic
|-- client/                   # ClientProxy, models, renderers, Core Ponder (22 Java files)
|   |-- ClientProxy.java / ClientUtil.java
|   |-- model/                # ModelBase, ModelDefinition, TemplateModel, TurbineRotorModel
|   |-- ponder/               # plugin/scenes/tags + Electric/ and Kinetic/ scene groups
|   |-- renderer/             # ArcBlockRender, DynamicCasingRender, HyperPlasmaTurbineRender, MartialMoralityEyeRender, TurbineRotorRender, AstralPlanetSpecialEffects (+ utils/RenderUtils)
|   `-- util/                 # SnowOverlayQuadOffset
|-- common/                   # CommonProxy, blocks, machines, capabilities, items, entities (125 Java files)
|   |-- block/                # CoilType, PhotovoltaicBlock, TurbineRotorBlock, blockdata/
|   |-- capability/           # EIOCapacitorProvider
|   |-- entity/monster/       # AstralSlime, SightSeerSpitter
|   |-- gui/                  # WPAAcceleratorGui, terminal/widget widgets
|   |-- item/                 # ArkOfHomoItem, AstronomyCircuitItem, MEAdvancedTerminalItem, ...
|   |-- machine/cover/        # CreativeEnergyCover
|   |-- machine/multiblock/   # LargeBottleMachine (now delegates to MultiblockFluidRendererTrait), MultiblockComputationMachine (attachTrait NetworkedComputationContainer), SlaughterHouseMachine/FactoryMachine (attachTrait machineStorage)
|   |   |-- electric/         # BlazeBlastFurnaceMachine now getTraitOrThrow(CoilMachineTrait.class), 29 top-level + multithread/ + rareearth/
|   |   |-- generator/        # 12 machines
|   |   |-- kinetic/          # 5
|   |   |-- part/             # 12 parts
|   |   `-- quantum/          # quantum_core
|   |-- machine/simple/       # DigitalMiner, EfficiencyGeneratorMachine, ...
|   |-- machine/trait/        # ScalableReservoirComputingLogic, providable_net/
|   |-- recipe/               # KeepIngredientShapedRecipe, condition classes, CTNHRecipeBuilder
|   `-- world/                # CTNHChunkLoading
|-- data/                     # datagen: recipes, tags, materials, worldgen (152 Java files)
|   |-- CTNHCoreDatagen.java
|   |-- CreateRecipeTypes.java # mechanicalTier Math.min(tier,5)
|   |-- materials/            # 26 sets: BauxiteProcessingMaterials (IMPURE/PURE_SODIUM_ALUMINATE_SOLUTION renamed from ALUMINIUM_HYDROXIDE, formula updates TiO2/NaAl(OH)4), BoronChainMaterials NEW, GoldChainMaterials RENAMED
|   |-- recipe/               # 35 top-level + age/ chain/ create/ wood/ migrated/ modmodify/ multiblock/ ...
|   |   |-- CTNHCoreRecipeAddition.java # dispatches BoronChain.init() + WaferRecipes.init()
|   |   |-- WaferRecipes.java       # precision circuit wafer masking
|   |   `-- chain/               # AlumiumChain (Ti/Al yield/HCl tuning)
|   |-- tags/                 # biome/entity/block/fluid/item tag providers
|   `-- worldgen/             # CTNHBiomeModifiers
|-- event/                    # ForgeEventHandler, BuildTaskManager, DimensionFlightHandler
|-- integration/              # EMI, Create Diesel, Legendary Survival, FTB Essentials, CTPP
|-- mixin/                    # cross-mod mixins; mc/ RecipeManagerApplyMixin
|-- registry/                 # 50 root+child classes; adventure/ jade/ machines/ material/ ores/ sound/
|   `-- registry/machines/GTMachineModify.java # LARGE_ASSEMBLER now setMachineSupplier(MultiblockComputationMachine::new) + add PRECISION_ASSEMBLY_RECIPES
`-- utils/                    # CTNHCommonTooltips, CoilTierHelper, LayeredBiMap, ...
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Mod entry | `CTNHCore.java` |
| GT addon | `CTNHCoreGTAddon.java` |
| Config | `CTNHConfig.java` |
| Registries | `registry/` (50 root+child classes) |
| Precision assembly | `registry/machines/GTMachineModify.java` (LARGE_ASSEMBLER -> MultiblockComputationMachine, PRECISION_ASSEMBLY_RECIPES) |
| Bauxite/sodium aluminate | `data/materials/BauxiteProcessingMaterials.java` (IMPURE/PURE_SODIUM_ALUMINATE_SOLUTION), `data/recipe/chain/AlumiumChain.java` |
| Boron chain | `data/materials/BoronChainMaterials.java`, `data/recipe/chain/BoronChain.java` |
| Wafer/precision circuits | `data/recipe/WaferRecipes.java`, `registry/CTNHItems.java` |
| Recipe generation root | `data/recipe/CTNHCoreRecipeAddition.java` |
| Multiblocks (electric) | `common/machine/multiblock/electric/` |
| Multiblocks (generator) | `common/machine/multiblock/generator/` (12) |
| Multiblocks (parts) | `common/machine/multiblock/part/` (12) |
| Coil handling | `common/machine/multiblock/electric/BlazeBlastFurnaceMachine.java` via `CoilMachineTrait`, `FermentingTankMachine.java` |
| Fluid rendering | `common/machine/multiblock/LargeBottleMachine.java` via `MultiblockFluidRendererTrait` |
| Computation trait | `common/machine/multiblock/MultiblockComputationMachine.java` via `attachTrait(NetworkedComputationContainer)` |
| Materials | `data/materials/` (26 sets), `registry/material/` |
| Ponder/client | `client/ponder/`, `client/renderer/` (LargeBottleRender removed) |
| Mixins | `mixin/`, `src/main/resources/ctnhcore.mixins.json` |
| EMI + CTPP hiding | `integration/emi/CTNHCoreEmiPlugin.java` (`CTPPDisable()` iterates `CTPPMachines.PLACEABLE_EMITTER`) |

## ARCHITECTURE CONTRACT
Machine/trait/capability/Jade 的所有权边界、字段同步与持久化规则、Jade 数据最小化原则和迁移步骤在 `references/_architecture/AGENTS.md`。改动机器、trait、recipe capability 或 Jade 代码前先读它；本文件只描述本模块的落点。

## DOMAIN GUIDE ROUTING
Read the matching domain guide before editing the corresponding source area.

| Source area | Guide | Read before |
|-------------|-------|-------------|
| `api` | `references/CTNH-Core/api/AGENTS.md` | Multiblock builder, machine features, recipe APIs |
| `client` | `references/CTNH-Core/client/AGENTS.md` | Models, renderers, Core Ponder scenes/tags/plugin |
| `common` | `references/CTNH-Core/common/AGENTS.md` | Blocks, machines, capabilities, items, entities |
| `data` | `references/CTNH-Core/data/AGENTS.md` | Recipe generators, tags, worldgen, materials datagen |
| `event` | `references/CTNH-Core/event/AGENTS.md` | Forge event handlers, task managers |
| `integration` | `references/CTNH-Core/integration/AGENTS.md` | EMI, Create Diesel, Legendary Survival, FTB Essentials, CTPP integration |
| `mixin` | `references/CTNH-Core/mixin/AGENTS.md` | Cross-mod mixins, recipe removal at `RecipeManager.apply()` |
| `registry` | `references/CTNH-Core/registry/AGENTS.md` | Items, blocks, machines, recipe types, materials, sound events |
| `utils` | `references/CTNH-Core/utils/AGENTS.md` | Shared helpers and recipe utilities |

## CONVENTIONS
- Namespace is `io.github.cpearl0.ctnhcore`.
- `src/generated/resources` is large and produced by `:modules:CTNH-Core:runData`.
- GT/GMT recipes are runtime dynamic-pack data (`*GTAddon.addRecipes()` → `GTDynamicPackContents` / CTNH-Lib `CTNHDynamicDataPack`); `runData` produces no JSON for them, and their absence from `src/generated/resources` is expected. See root AGENTS.md CONVENTIONS.
- CI builds this module only; changes in other modules should still be validated through `:modules:CTNH-Core:build` when they affect aggregation.
- Some generated recipe Java lives under `data/recipe/generated`; distinguish Java recipe generators from JSON generated resources.
- Ponder `CTNHCorePonderSceneBuilder` is only a Core adapter around Lib's shared builder; keep reusable builder/text behavior in CTNH-Lib.
- `ctnhcore.mixins.json` covers broad integrations (AECs, Apotheosis, Ars Nouveau, Avaritia, Create, Create Diesel, EIO/JEI, EMI, FTB Chunks, FTB Essentials, GTCEu, JAVD, LDLib, Legendary Survival, Minecraft reload/spawner, Sophisticated, TConstruct, TMRV, Vintage Improvements); inspect target mod versions before changing injection signatures.
- Sound events are registered via `CTNHSoundEvents.SOUND_EVENTS` in `CommonProxy.init()`; the corresponding `sounds.json` and audio assets live under `src/main/resources/assets/ctnhcore/`.
- When referencing items/blocks/fluids, MUST use direct registration objects — static field references (`GTMaterials.Iron`, `CTNHBlocks.MY_BLOCK`, `TagPrefix.ingot`, `AEItems.X`) or registered `ItemLike`/`Fluid` values — never `ResourceLocation` string parsing with `ForgeRegistries.ITEMS/BLOCKS/FLUIDS.getValue(...)` or similar lookups. String ids are allowed only where no registration object exists (upstream-mod-only ids, recipe ids, tag keys, dimension ids). See root AGENTS.md CONVENTIONS.
- Trait migration: machines now attach computation/storage/fluid/capability via `attachTrait()` (`NetworkedComputationContainer`, `NotifiableItemStackHandler`, `MultiblockFluidRendererTrait`, `CoilMachineTrait`); deleted `api/machine/feature/ICoilMachine` — use `getTraitOrThrow(CoilMachineTrait.class).getCoilType()`; `LargeBottleMachine` no longer owns `@DescSynced fluidBlockOffsets` field, instead supplies offsets via `MultiblockFluidRendererTrait` lambda.
- Material rename: `CrudeGoldRefiningMaterials` → `GoldChainMaterials`; `IMPURE_ALUMINIUM_HYDROXIDE_SOLUTION`/`PURE_ALUMINIUM_HYDROXIDE_SOLUTION` → `IMPURE/PURE_SODIUM_ALUMINATE_SOLUTION` (BauxiteProcessingMaterials) with updated formulas (TiO2/NaAl(OH)4/H2O) and lang keys.
- Registry: `GTMachineModify.modifyGTAssembly()` now sets `GCYMMachines.LARGE_ASSEMBLER` supplier to `MultiblockComputationMachine::new` and appends `CTNHRecipeTypes.PRECISION_ASSEMBLY_RECIPES`.

## ANTI-PATTERNS
- Do not manually reformat huge multiblock registry sections protected by Spotless toggles.
- Do not patch `src/generated/resources` as the first choice; change datagen sources instead.
- Do not assume Core-only validation catches module-specific runtime/datagen issues.
- When referencing items/blocks/fluids, MUST use direct registration objects — static field references (`GTMaterials.Iron`, `CTNHBlocks.MY_BLOCK`, `TagPrefix.ingot`, `AEItems.X`) or registered `ItemLike`/`Fluid` values — never `ResourceLocation` string parsing with `ForgeRegistries.ITEMS/BLOCKS/FLUIDS.getValue(...)` or similar lookups. String ids are allowed only where no registration object exists (upstream-mod-only ids, recipe ids, tag keys, dimension ids). See root AGENTS.md CONVENTIONS.
- Do not add broad cross-mod recipes to feature modules unless the feature module owns the whole mechanic; Core is the aggregator for most migrated/script compatibility recipes.
- Do not treat `WPA_old.java` or `MachineModeFancyConfiguratorTest` as current implementation; both are legacy leftovers.
- Do not reintroduce `ICoilMachine` or client `LargeBottleRender`; coil is via `CoilMachineTrait`, fluid render is via `MultiblockFluidRendererTrait`.

## COMMANDS
```text
./gradlew :modules:CTNH-Core:build
./gradlew :modules:CTNH-Core:runData
./gradlew :modules:CTNH-Core:spotlessCheck
./gradlew :modules:CTNH-Core:spotlessApply
```

## SCOPE
Applies to `modules/CTNH-Core` and the CI release artifacts it aggregates. It is a reference guide loaded through the root routing table, not an additional source-tree instruction file.

## READ WHEN
- Adding or changing cross-mod recipes, Core-owned gameplay systems, or GTCEu machine registries.
- Changing Core Ponder scenes/tags or datagen providers that produce `src/generated/resources`.
- A change affects aggregation behavior validated by `:modules:CTNH-Core:build`.

## SOURCE OF TRUTH
- Registration/lifecycle: `CTNHCore.java`, `CTNHCoreGTAddon.java`, `common/CommonProxy.java`.
- Recipe root: `data/recipe/CTNHCoreRecipeAddition.java` and `data/CTNHCoreDatagen.java`.
- Forge metadata and mixins: `src/main/resources/META-INF/mods.toml` and `ctnhcore.mixins.json`.
- Static generated data: providers plus `src/generated/resources`, never the generated files alone.
- Sound events: `registry/sound/CTNHSoundEvents.java` and `src/main/resources/assets/ctnhcore/sounds.json`.

## WORKFLOW
1. Map the changed symbol to its domain and read that domain guide.
2. Check GT addon hook order, event registration, and recipe removal filters.
3. Run the narrowest Gradle task for the affected surface (`runData` for datagen, `build` for aggregation).
4. Re-read the root routing table if the change introduces a new module boundary.
