# CTNH-CORE MODULE

## OVERVIEW
CTNH-Core is the aggregate/core mod and CI release target (Java files, the largest module). It hosts shared CTNH gameplay systems, GTCEu integration, large machine registries, generated data, Core-owned Ponder scenes, and cross-mod content.

## STRUCTURE
```text
src/main/java/io/github/cpearl0/ctnhcore/
|-- CTNHCore.java             # Forge mod initialization
|-- CTNHCoreGTAddon.java      # GTCEu addon hooks; addRecipes() dispatches data/recipe/**
|-- CTNHConfig.java           # module config
|-- api/                      # public APIs: multiblock builder, patterns, machine features
|   |-- CTNHMultiblockBuilder.java
|   |-- Pattern/              # AsynBlockPattern, CTNHBlockMaps, CTNHBoilerFireboxType, CTNHPredicates (AsynBlockPattern now null/empty guards for AE extract)
|   |-- data/material/        # icon sets/types, property keys, catalyst property
|   |-- gui/                  # CTNHGuiTextures
|   |-- jade/                 # multithread recipe/output/thread providers
|   |-- machine/feature/      # ICoilMachine, IDigitalMiner, IDynamicCasing
|   |-- machine/multiblock/   # UnlimitedItemStackTransfer
|   `-- recipe/               # DigitalMinerLogic
|-- client/                   # ClientProxy, models, renderers, Core Ponder
|   |-- ClientProxy.java / ClientUtil.java
|   |-- model/                # ModelBase, ModelDefinition, TemplateModel, TurbineRotorModel
|   |-- ponder/               # plugin/scenes/tags + Electric/ and Kinetic/ scene groups
|   |-- renderer/             # ArcBlockRender, DynamicCasingRender, HyperPlasmaTurbineRender, ...
|   `-- util/                 # SnowOverlayQuadOffset
|-- common/                   # CommonProxy, blocks, machines, capabilities, items, entities
|   |-- block/                # CoilType, PhotovoltaicBlock, TurbineRotorBlock, blockdata/
|   |-- capability/           # EIOCapacitorProvider
|   |-- entity/monster/       # AstralSlime, SightSeerSpitter
|   |-- gui/                  # WPAAcceleratorGui, terminal/widget widgets
|   |-- item/                 # ArkOfHomoItem, AstronomyCircuitItem, MEAdvancedTerminalItem, ...
|   |-- machine/cover/        # CreativeEnergyCover
|   |-- machine/multiblock/   # 5 top-level + electric/ + generator/ + kinetic/ + part/ + quantum/
|   |   |-- electric/         # WideParticleAccelerator, NeutronActivatorMachine, PlanetMiner, ...
|   |   |   |-- multithread/  # CNCAlloySmelter
|   |   |   `-- rareearth/    # ProcessControlMachine, ProcessControlProfile, ...
|   |   |-- generator/        # Arc_Reactor, HyperPlasmaTurbineMachine, MegaTurbineMachine, ...
|   |   |-- kinetic/          # 5: IndustrialPrimitiveBlastFurnaceMachine, KineticCentrifugeMachine, ...
|   |   |-- part/             # CTNHPartAbility, CatalystHatchPartMachine, Creative*PartMachine, ...
|   |   `-- quantum/          # quantum_core
|   |-- machine/simple/       # DigitalMiner, EfficiencyGeneratorMachine, ...
|   |-- machine/trait/        # ScalableReservoirComputingLogic, providable_net/ (ProvidableNetHandler)
|   |-- recipe/               # KeepIngredientShapedRecipe, condition classes, CTNHRecipeBuilder
|   `-- world/                # CTNHChunkLoading
|-- data/                     # datagen: recipes, tags, materials, worldgen
|   |-- CTNHCoreDatagen.java  # datagen entry
|   |-- CreateRecipeTypes.java # mechanicalTier now Math.min(tier,5) (was *2)
|   |-- item/                 # CrystalItems
|   |-- machines/             # GTNNMachines
|   |-- materials/            # 26 sets: BoronChainMaterials NEW (borax_acid_solution, boron_trioxide), GoldChainMaterials RENAMED from CrudeGoldRefiningMaterials, Boric Acid now dust+components H3BO3 + DISABLE_DECOMPOSITION, NaquadahMaterials, PlatinumLineMaterials, ...
|   |-- recipe/               # 35 top-level (WaferRecipes NEW) + age/ chain/ create/ wood/ migrated/ modmodify/ multiblock/ ...
|   |   |-- CTNHCoreRecipeAddition.java # now dispatches BoronChain.init() + WaferRecipes.init()
|   |   |-- RecipeRemoval.java      # adds gtceu:electrolyzer/decomposition_electrolyzing_borax, wildcard engrave_ram_*/lpic_*/ssoc_*
|   |   |-- WaferRecipes.java       # NEW: precision circuit wafer masking (rubber-masked wafers)
|   |   |-- chain/BoronChain.java   # NEW: boron chain
|   |-- tags/                 # biome/entity/block/fluid/item tag providers, TagClearHelper
|   `-- worldgen/             # CTNHBiomeModifiers
|-- event/                    # ForgeEventHandler, BuildTaskManager, DimensionFlightHandler
|-- integration/              # EMI, Create Diesel, Legendary Survival, FTB Essentials, CTPP
|   `-- emi/CTNHCoreEmiPlugin.java # now CTPPDisable() hides CTPPMachines.PLACEABLE_EMITTER
|-- mixin/                    # cross-mod mixins across many target mods; mc/ RecipeManagerApplyMixin
|-- registry/                 # 50 root+child classes; adventure/ jade/ machines/ material/ ores/ sound/
|   `-- CTNHItems.java        # NEW: BSC_CHIP, BSC_WAFER, BSC_WAFER_RUBBER_MASKED, LPIC_WAFER_RUBBER_MASKED, RAM_WAFER_RUBBER_MASKED, RUBBER_MASKED_SILICON_WAFER, SSOC_WAFER_RUBBER_MASKED (renamed from *_masked)
`-- utils/                    # CTNHCommonTooltips, CoilTierHelper, LayeredBiMap, ...
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Mod entry | `CTNHCore.java` |
| GT addon | `CTNHCoreGTAddon.java` |
| Config | `CTNHConfig.java` |
| Registries | `registry/` (50 root+child classes) |
| Recipe generation root | `data/recipe/CTNHCoreRecipeAddition.java` (dispatched from `addRecipes()`) |
| Boron chain | `data/materials/BoronChainMaterials.java`, `data/recipe/chain/BoronChain.java` |
| Wafer/precision circuits | `data/recipe/WaferRecipes.java`, `registry/CTNHItems.java` (BSC_*, *_RUBBER_MASKED) |
| Gold chain rename | `data/materials/GoldChainMaterials.java` (was `CrudeGoldRefiningMaterials.java`) |
| Create kinetic conversion | `data/CreateRecipeTypes.java` (mechanicalTier Math.min(tier,5)) |
| Recipe removals | `data/recipe/RecipeRemoval.java` + `mixin/mc/RecipeManagerApplyMixin.java` |
| Multiblocks (electric) | `common/machine/multiblock/electric/` (including `multithread/` and `rareearth/`) |
| Multiblocks (generator) | `common/machine/multiblock/generator/` (12 machines) |
| Multiblocks (parts) | `common/machine/multiblock/part/` (12 machines) |
| Machine traits/net | `common/machine/trait/providable_net/` |
| Materials | `data/materials/` (26 sets), `registry/material/` |
| Ponder/client | `client/ponder/`, `client/renderer/` |
| Mixins | `mixin/`, `src/main/resources/ctnhcore.mixins.json` |
| EMI + CTPP hiding | `integration/emi/CTNHCoreEmiPlugin.java` (`CTPPDisable()` iterates `CTPPMachines.PLACEABLE_EMITTER`) |
| Sound events | `registry/sound/CTNHSoundEvents.java` |
| AE pattern fix | `api/Pattern/AsynBlockPattern.java` (null/empty guard on foundItemStack) |

## ARCHITECTURE CONTRACT
Machine/trait/capability/Jade 的所有权边界、字段同步与持久化规则、Jade 数据最小化原则和迁移步骤在 `docs/_architecture/AGENTS.md`。改动机器、trait、recipe capability 或 Jade 代码前先读它；本文件只描述本模块的落点。

## DOMAIN GUIDE ROUTING
Read the matching domain guide before editing the corresponding source area.

| Source area | Guide | Read before |
|-------------|-------|-------------|
| `api` | `docs/CTNH-Core/api/AGENTS.md` | Multiblock builder, machine features, recipe APIs |
| `client` | `docs/CTNH-Core/client/AGENTS.md` | Models, renderers, Core Ponder scenes/tags/plugin |
| `common` | `docs/CTNH-Core/common/AGENTS.md` | Blocks, machines, capabilities, items, entities |
| `data` | `docs/CTNH-Core/data/AGENTS.md` | Recipe generators, tags, worldgen, materials datagen |
| `event` | `docs/CTNH-Core/event/AGENTS.md` | Forge event handlers, task managers |
| `integration` | `docs/CTNH-Core/integration/AGENTS.md` | EMI, Create Diesel, Legendary Survival, FTB Essentials, CTPP integration |
| `mixin` | `docs/CTNH-Core/mixin/AGENTS.md` | Cross-mod mixins, recipe removal at `RecipeManager.apply()` |
| `registry` | `docs/CTNH-Core/registry/AGENTS.md` | Items, blocks, machines, recipe types, materials, sound events |
| `utils` | `docs/CTNH-Core/utils/AGENTS.md` | Shared helpers and recipe utilities |

## CONVENTIONS
- Namespace is `io.github.cpearl0.ctnhcore`.
- `src/generated/resources` is large and produced by `:modules:CTNH-Core:runData`.
- GT/GMT recipes are runtime dynamic-pack data (`*GTAddon.addRecipes()` → `GTDynamicPackContents` / CTNH-Lib `CTNHDynamicDataPack`); `runData` produces no JSON for them, and their absence from `src/generated/resources` is expected. See root AGENTS.md CONVENTIONS.
- CI builds this module only; changes in other modules should still be validated through `:modules:CTNH-Core:build` when they affect aggregation.
- Some generated recipe Java lives under `data/recipe/generated`; distinguish Java recipe generators from JSON generated resources.
- Ponder `CTNHCorePonderSceneBuilder` is only a Core adapter around Lib's shared builder; keep reusable builder/text behavior in CTNH-Lib.
- `ctnhcore.mixins.json` covers broad integrations (AECs, Apotheosis, Ars Nouveau, Avaritia, Create, Create Diesel, EIO/JEI, EMI, FTB Chunks, FTB Essentials, GTCEu, JAVD, LDLib, Legendary Survival, Minecraft reload/spawner, Sophisticated, TConstruct, TMRV, Vintage Improvements); inspect target mod versions before changing injection signatures.
- Spelling quirk: mixin package is `dategen` (not `datagen`).
- Sound events are registered via `CTNHSoundEvents.SOUND_EVENTS` in `CommonProxy.init()`; the corresponding `sounds.json` and audio assets live under `src/main/resources/assets/ctnhcore/`.
- When referencing items/blocks/fluids, MUST use direct registration objects — static field references (`GTMaterials.Iron`, `CTNHBlocks.MY_BLOCK`, `TagPrefix.ingot`, `AEItems.X`) or registered `ItemLike`/`Fluid` values — never `ResourceLocation` string parsing with `ForgeRegistries.ITEMS/BLOCKS/FLUIDS.getValue(...)` or similar lookups. String ids are allowed only where no registration object exists (upstream-mod-only ids, recipe ids, tag keys, dimension ids). See root AGENTS.md CONVENTIONS.
- Material rename: `CrudeGoldRefiningMaterials` → `GoldChainMaterials` (same file, class rename); imports updated in `AlumiumChain.java`, `SunRecipes.java`.
- New boron materials: `BORAX_ACID_SOLUTION` (liquid, formula 2NaCl+4H3BO3+5H2O) and `BORON_TRIOXIDE` (dust, B2O3, DISABLE_DECOMPOSITION) in `BoronChainMaterials`; `BORIC_ACID` changed to dust+liquid with components H3BO3 and DISABLE_DECOMPOSITION.
- Create kinetic tier fix: `CreateRecipeTypes` mechanicalTier now `Math.min(GTUtil.getTierByVoltage(EUt),5)` for pressor/mixer/centrifuge/sifter/lathe (removed `*2`).
- Recipe removal now uses wildcards `engrave_ram_*`, `engrave_lpic_*`, `engrave_ssoc_*` and removes `gtceu:electrolyzer/decomposition_electrolyzing_borax`.
- Wafer items renamed `*_masked` → `*_rubber_masked` plus new `RUBBER_MASKED_SILICON_WAFER` and `SSOC_WAFER_RUBBER_MASKED`; models under `assets/ctnhcore/models/item/*rubber_masked*.json` and lang keys updated.

## ANTI-PATTERNS
- Do not manually reformat huge multiblock registry sections protected by Spotless toggles.
- Do not patch `src/generated/resources` as the first choice; change datagen sources instead.
- Do not assume Core-only validation catches module-specific runtime/datagen issues.
- When referencing items/blocks/fluids, MUST use direct registration objects — static field references (`GTMaterials.Iron`, `CTNHBlocks.MY_BLOCK`, `TagPrefix.ingot`, `AEItems.X`) or registered `ItemLike`/`Fluid` values — never `ResourceLocation` string parsing with `ForgeRegistries.ITEMS/BLOCKS/FLUIDS.getValue(...)` or similar lookups. String ids are allowed only where no registration object exists (upstream-mod-only ids, recipe ids, tag keys, dimension ids). See root AGENTS.md CONVENTIONS.
- Do not add broad cross-mod recipes to feature modules unless the feature module owns the whole mechanic; Core is the aggregator for most migrated/script compatibility recipes.
- Do not treat `WPA_old.java` or `MachineModeFancyConfiguratorTest` as current implementation; both are legacy leftovers.

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
