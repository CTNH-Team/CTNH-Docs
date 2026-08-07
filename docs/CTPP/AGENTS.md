# CTPP MODULE

## OVERVIEW
CTPP (`CT++`) is the Create/GregTech compatibility module (219 Java files). It defines kinetic/electric machines, Create fan catalyst recipes, custom recipe builders, generated data, GTCEu addon registration, and a toolbox system under mod id `ctpp`.

## STRUCTURE
```text
src/main/java/com/mo_guang/ctpp/
|-- CTPP.java / CTPPGTAddon.java / CTPPRegistration.java / CTPPRegistrate.java / CTPPEntityTypes.java
|-- api/                      # 13: StressRecipeCapability, CTPPMultiblockBuilder, CTPPParallelLogic, KineticMachineDefinition, CTPPRecipeCapabilities/Conditions, predicates, block maps
|-- client/                   # 26: ClientProxy, Ponder (plugin/scenes/tags + electric/kinetic/), renderers (CarbonBrushes, GeneratorCoil), toolbox UI
|-- common/                   # 58: CommonProxy, blocks, block entities, machines (kinetic), toolbox (13), fan processing, commands
|   |-- kinetic/fan/          # acidwashing/ (AcidWashingProcessingType), breathing/ (BreathingFanProcessingType), oiling/ (OilingRecipe)
|   |-- machine/              # IKineticMachine, KineticWorkableTieredMachine, SimpleKineticWorkable(Multiblock)Machine, kinetic traits
|   |   |-- multiblock/       # BigDamMachine, KineticGeneratorMachine, KineticWorkableMultiblockMachine, WindMillControlMachine (windmillController/)
|   |   `-- simple/           # CarbonBrushesGeneratorMachine, ElectricGearBoxMachine
|   `-- toolbox/              # 13: CTPPToolboxBinding(s), CTPPToolboxInventory, CTPPToolboxService, CTPPToolboxSnapshot, CTPPToolboxSavedData, CTPPToolboxStackData, ...
|-- config/                   # 2: ConfigUtils, MainConfig
|-- data/                     # 53: CTPPDatagen, CuriosTags, ToolboxBlockstates, tags/ (4), recipe/ (top-level + builders)
|   `-- recipe/
|       |-- 12 top-level: CTPPRecipes, BigDamRecipes, BoomOfCreateRecipes, DieselGeneratorRecipes, KineticGeneratorRecipes, KineticSteamTurbineRecipes, SmashingFactoryRecipes, SeaweedFarmRecipes, WindmillControlRecipes, OreProcessingRecipes, ItemRecipes, ToolRecipes
|       |-- builder/          # AcidWashingRecipeGen, BreathingRecipeGen, CTPPProcessingRecipeBuilder, CTPPRecipeBuilder, CTPPRecipeHelper, CTPPRecipeProvider
|       |   |-- create/       # 11: Compacting, Crushing, Cutting, Filling, ItemApplication, MechanicalCrafting, Milling, Mixing, Pressing, SequencedAssembly, Splashing
|       |   |-- ctpp/         # MetalSmeltingRecipeBuilder
|       |   |-- diesel/       # BasinFermenting, Distillation, Hammer, WireCutting
|       |   `-- vintage/      # AbstractVintageRecipeBuilder, Centrifugation, Coiling, Curving, Hammering, Pressurizing, Turning, Vacuumizing, Vibrating, VintageRecipeResult
|       `-- fanprocessing/    # NOTE: no underscore — CTPPFanProcessingTypes, CTPPRecipeTypeInfo
|-- dynamicPart/              # 10: QuaternionRotationState, RotationWandItem, SimpleBearingContraption, SimpleContraptionEntityRenderer, SimpleMovingContraption, FixedAxisRotatingContraptionEntity, IContraptionMultiblock, RubiksCubeContraptionEntity, SimpleRotatingContraption(+Entity)
|-- event/                    # ForgeEventHandler
|-- integration/              # 3: jei/ (CTPPJeiPlugin), jei/category/ (FanAcidWashingCategory, FanBreathingCategory)
|-- mixin/                    # 23: create/ (5 + diesel/ + fix/ + jei/), fix/ (2), gtm/ (1), root (5)
|-- network/                  # 6 toolbox packets
|-- registry/                 # 12: CTPPRegistrate-based items/blocks/entities/machines/multiblocks/menus/recipe types + CreateMaterials, GTMaterialAddon
`-- util/                     # 7: CTPPValues, CommonTooltips, ICustomSlot, IMatrix3dAccess, IWorkingMachineStep, ItemAxisBuilder, MathUtil
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Mod entry | `CTPP.java` |
| GT addon | `CTPPGTAddon.java` |
| Registrate | `CTPPRegistrate.java`, `CTPPRegistration.java` |
| API | `api/` (13) |
| Dynamic contraptions | `dynamicPart/` (10) |
| KubeJS integration | `integration/kjs/` |
| Recipes/datagen | `data/recipe/` (top-level, NOT under common/) |
| Fan processing | `data/recipe/fanprocessing/` (no underscore) |
| Toolbox system | `common/toolbox/` (13 classes), `network/` (6 packets), `client/` toolbox UI |
| Ponder/client | `client/ponder/` |
| Mixins | `mixin/`, `src/main/resources/ctpp.mixins.json` |
| Generated resources | `src/generated/resources/data/ctpp/recipes/` |
| Static resources | `src/main/resources/assets/ctpp/` |

## RECIPE TYPES
CTPP defines two recipe-type families: GT-style `GTRecipeType` for kinetic/electric machines, and Create-style `ProcessingRecipe` for fan catalyst processing.

### GT Recipe Types (`registry/CTPPRecipeTypes.java`)
Registered via `CTPPRegistration.REGISTRATE.recipeType(...)`. Kinetic types use `StressRecipeCapability` (key `"su"`, Float) instead of EU, with `RPMCondition` + `MechanicalTierCondition`.

| Constant | Registry ID | 中文 | Group | I/O items | I/O fluids | Notes |
|---|---|---|---|---|---|---|
| `KINETIC_MIXER_RECIPES` | `kinetic_mixer` | 应力搅拌 | KINETIC | 6/1 | 2/1 | Commented out |
| `SMASHING_FACTORY_RECIPES` | `smashing_factory_recipes` | 粉碎工厂 | KINETIC | 1/4 | 0/0 | Auto-gen from `MACERATOR_RECIPES`; strips chanced outputs; reads tier/voltage limits from config |
| `KINETIC_GENERATOR_RECIPES` | `kinetic_generator` | 应力发电 | KINETIC | 0/0 | 1/0 | Stress → EU |
| `KINETIC_STEAM_TURBINE_RECIPES` | `kinetic_steam_turbine` | 蒸汽动力 | KINETIC | 0/0 | 1/1 | Steam → EU |
| `SEAWEED_FARM` | `seaweed_farm` | 海草养殖 | ELECTRIC | 2/4 | 0/1 | Multiblock |
| `WINDMILL_CONTROL` | `windmill_control_center` | 风车控制中心 | ELECTRIC | 0/0 | 1/0 | Multiblock |
| `BOOM_OF_CREATE` | `boom_of_create` | 聚爆应力 | KINETIC | 1/0 | 1/0 | EU IN, explosive catalyst → stress |
| `BIG_DAM` | `big_dam` (GTCEu namespace) | 三峡大坝 | ELECTRIC | 0/0 | 1/0 | Registered under `GTCEu.id(...)` |

### Create Fan Processing Recipes (`data/recipe/fanprocessing/CTPPRecipeTypeInfo.java`)
Uses `IRecipeTypeInfo` / `ProcessingRecipe` from Create. Registered as `DeferredRegister` entries under `ctpp` namespace. `CTPPFanProcessingTypes.java` holds the enum of types.

| Enum | ID | Max In/Out | Purpose |
|---|---|---|---|
| `BREATHING` | `ctpp:breathing` | 1/12 | Fan blowing catalyst |
| `ACIDWASHING` | `ctpp:acidwashing` | 4/12 | Fan washing - acid catalyst |
| `OILING` | `ctpp:oiling` | 1/12 | Fan processing - oil catalyst |

### Wrapped Create / Addon Recipe Builders (`data/recipe/builder/`)
CTPP wraps Create and addon recipe types with datagen-friendly builders. These are NOT new recipe types; they produce standard Create/addon recipe JSON.

**Create vanilla (11 builders)** — direct JSON builders with `"type": "create:<name>"`:

| Builder | Recipe type | Notes |
|---|---|---|
| `CompactingRecipeBuilder` | `create:compacting` | item/fluid I/O, heated/superheated |
| `CrushingRecipeBuilder` | `create:crushing` | item I/O with chanced outputs per entry |
| `CuttingRecipeBuilder` | `create:cutting` | item I/O |
| `FillingRecipeBuilder` | `create:filling` | item/fluid I/O |
| `ItemApplicationRecipeBuilder` | `create:item_application` | item I/O (deployer-style) |
| `MechanicalCraftingRecipeBuilder` | `create:mechanical_crafting` | shaped pattern with key |
| `MillingRecipeBuilder` | `create:milling` | item I/O with chanced outputs per entry |
| `MixingRecipeBuilder` | `create:mixing` | item/fluid I/O, heated/superheated |
| `PressingRecipeBuilder` | `create:pressing` | item I/O |
| `SequencedAssemblyRecipeBuilder` | `create:sequenced_assembly` | multi-step (filling, pressing, deploying, cutting, curving) |
| `SplashingRecipeBuilder` | `create:splashing` | item I/O |

**Create Diesel Generators (4 builders)** — use `ProcessingRecipeBuilder<>`:

| Builder | Target recipe class | Mod |
|---|---|---|
| `BasinFermentingRecipeBuilder` | `BasinFermentingRecipe` | createdieselgenerators |
| `DistillationRecipeBuilder` | `DistillationRecipe` | createdieselgenerators |
| `HammerRecipeBuilder` | `HammerRecipe` | createdieselgenerators |
| `WireCuttingRecipeBuilder` | `WireCuttingRecipe` | createdieselgenerators |

**Vintage Improvements (8 builders)** — extend `AbstractVintageRecipeBuilder`, use `VintageRecipes` enum:

| Builder | VintageRecipes enum | Notes |
|---|---|---|
| `CentrifugationRecipeBuilder` | `CENTRIFUGATION` | item/fluid I/O, RPM, heat |
| `CoilingRecipeBuilder` | `COILING` | item/fluid I/O, RPM, heat |
| `CurvingRecipeBuilder` | `CURVING` | item/fluid I/O, RPM, heat |
| `HammeringRecipeBuilder` | `HAMMERING` | item/fluid I/O, RPM, heat |
| `PressurizingRecipeBuilder` | `PRESSURIZING` | item/fluid I/O, RPM, heat |
| `TurningRecipeBuilder` | `TURNING` | item/fluid I/O, RPM, heat |
| `VacuumizingRecipeBuilder` | `VACUUMIZING` | item/fluid I/O, RPM, heat |
| `VibratingRecipeBuilder` | `VIBRATING` | item/fluid I/O, RPM, heat |

**CTPP (1 builder)**:

| Builder | Recipe type | Notes |
|---|---|---|
| `MetalSmeltingRecipeBuilder` | ctpp metal smelting | `data/recipe/builder/ctpp/` |

### Custom recipe infrastructure
- **Capability** `StressRecipeCapability` (`"su"` key, Float) — kinetic stress I/O for GT recipes; drives parallel calculation in `KineticWorkableMultiblockMachine` / `KineticOutputMachine`.
- **KubeJS keys** `CTPPGTAddon.SU_IN` / `SU_OUT` — script-facing stress recipe components registered by `registerRecipeKeys()`.
- **Conditions** `RPMCondition` (`"rpm"`) and `MechanicalTierCondition` (`"mechanical_tier"`) — RPM/tier requirements on kinetic recipes.
- **Modifiers** `KINETIC_PARALLEL` (stress-multiplier + accurate parallel) and `KINETIC_PERFECT_PARALLEL` (perfect parallel variant) — both target `KineticWorkableMultiblockMachine`.
- **Recipe builder** `CTPPRecipeBuilder` extends `GTRecipeBuilder` with `.rpm(float)`, `.tier(int)`, `.inputStress(float)`, `.outputStress(float)`, `.noEUt()`.

## DOMAIN GUIDE ROUTING
Read the matching domain guide before editing the corresponding source area.

| Source area | Guide | Read before |
|-------------|-------|-------------|
| `api` | `docs/CTPP/api/AGENTS.md` | Recipe capabilities, multiblock builder, predicates |
| `client` | `docs/CTPP/client/AGENTS.md` | Ponder plugin/scenes/tags, renderers, toolbox UI |
| `common` | `docs/CTPP/common/AGENTS.md` | Proxy, machines, kinetic logic, toolbox, fan processing |
| `config` | `docs/CTPP/config/AGENTS.md` | Module config |
| `data` | `docs/CTPP/data/AGENTS.md` | Recipe providers, tags, models |
| `dynamicPart` | `docs/CTPP/dynamicPart/AGENTS.md` | Moving/rotating contraptions |
| `event` | `docs/CTPP/event/AGENTS.md` | Forge event handlers |
| `integration` | `docs/CTPP/integration/AGENTS.md` | KubeJS and JEI integration |
| `mixin` | `docs/CTPP/mixin/AGENTS.md` | Create/GT patches |
| `network` | `docs/CTPP/network/AGENTS.md` | Toolbox packets |
| `registry` | `docs/CTPP/registry/AGENTS.md` | Items, blocks, machines, recipe types |
| `util` | `docs/CTPP/util/AGENTS.md` | Shared helpers |

## CONVENTIONS
- Namespace is `com.mo_guang.ctpp`; class prefixes use `CTPP`.
- GT/GMT recipes are runtime dynamic-pack data (`CTPPGTAddon.addRecipes()`); `runData` produces no JSON for them. See root AGENTS.md CONVENTIONS.
- Item/block/fluid references MUST use direct registration objects (`CTPPBlocks.X`, `CTPPItems.X`, `GTMaterials.X`, `TagPrefix.ingot`) — never `ResourceLocation` string parsing + `ForgeRegistries` lookups. See root AGENTS.md CONVENTIONS.
- `src/generated/resources` contains many Create/Forge/Minecraft tag outputs from datagen.
- Static machine part models also exist under `src/main/resources`; check path before regenerating or editing.
- Create kinetic behavior is patched through mixins and dynamic contraption classes; inspect both when changing rotation or moving-block behavior.
- Recipe generation lives at the top-level `data/recipe/` (there is no `common/data/recipe`); fan-processing package is spelled `fanprocessing` (no underscore).

## ANTI-PATTERNS
- Do not treat all recipe JSON as equivalent: fan catalyst/generated outputs and static assets live in different source roots.
- Do not change kinetic/electric machine tiers without checking both registry code and generated models/recipes.
- Do not add stress I/O by raw JSON keys alone; use `StressRecipeCapability`, KubeJS recipe keys, and `CTPPRecipeBuilder` together.

## COMMANDS
```text
./gradlew :modules:CTPP:build
./gradlew :modules:CTPP:runData
./gradlew :modules:CTPP:spotlessCheck
```

## SCOPE
Applies to `modules/CTPP` and its submodule repository. It is a reference guide loaded through the root routing table, not an additional source-tree instruction file.

## READ WHEN
- Adding or changing kinetic/electric machines, fan catalyst recipes, or recipe builders.
- Changing Create kinetic behavior through mixins or dynamic contraption classes.
- Changing the toolbox system.

## SOURCE OF TRUTH
- Registration/lifecycle: `CTPP.java`, `CTPPGTAddon.java`, `common/CommonProxy.java`.
- Recipe types: `registry/CTPPRecipeTypes.java`, `data/recipe/fanprocessing/CTPPRecipeTypeInfo.java`, builders under `data/recipe/builder/`.
- Forge metadata and mixins: `src/main/resources/META-INF/mods.toml` and `ctpp.mixins.json`.

## WORKFLOW
1. Map the changed symbol to its domain and read that domain guide.
2. Check GT addon hook order, recipe capability registration, and datagen references.
3. Run the narrowest Gradle task (`runData` for datagen, `build` for compilation).
4. Re-read the root routing table if the change introduces a new module boundary.
