# CTNH-BIO MODULE

## OVERVIEW
CTNH-Bio adds Biomancy/living-machine systems, entity/recipe capabilities, biological machines, and generated recipes/resources under mod id `ctnhbio` (175 Java files).

## STRUCTURE
```text
src/main/java/com/moguang/ctnhbio/
|-- CTNHBio.java / CTNHBioGTAddon.java / CBConfig.java   # mod entry, GT addon, config
|-- api/                      # 61 files: recipe capabilities, living-machine APIs, ingredients
|   |-- block/ blockentity/ entity/    # LivingMetaMachine block/entity hierarchy
|   |-- capability/recipe/    # CogniItem/Entity/Model/Nutrient recipe capabilities
|   |-- item/component/       # OrganicFluidHandler stack, StyleItem
|   |-- machine/              # BasicLivingMachine, traits (NeuralModelContainer, Notifiable*)
|   |-- pattern/              # GrowingBlockPattern
|   `-- recipe/               # customlogic/ ingredient/ lookup/ matcher/ (no content/ subpackage)
|-- client/                   # renderers (BasicLivingMachineEntityRenderer, Colorable*), models (VatModel, DigesterModel, ...)
|-- common/                   # CommonProxy, MobCrushingRecipe, PrimordialSerum, AssemblyStepItem
|-- data/                     # CBDatagen, 28 files: recipes (living/multi), lang, loot, materials, tags
|-- event/                    # EventHandler, ForgeEventHandler, TransformManager
|-- integration/              # EMI, Jade (LivingMachineStatusProvider), JEI (3), XEI (entity entries/handlers)
|-- machine/                  # living-machine implementations: braininavat/ bioobservation/ greatflesh/ multiblock/
|-- mixin/                    # 20 files: Biomancy, HNN, EMI/ALI, Create, GTCEu patches
|-- registry/                 # 17 files: CBBlocks, CBItems, CBMachines, CBMultiblocks, CBRecipeTypes, ...
`-- utils/                    # CBMachineNames, DecomposingRecipeHandler, DespoilLootHelper, ...
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Mod entry | `CTNHBio.java` |
| GT addon | `CTNHBioGTAddon.java` |
| Config | `CBConfig.java` |
| API/capabilities | `api/` (61 files) |
| Living systems | `machine/braininavat/` (Brain, BrainInAVatMachine), `machine/bioobservation/` (HostileObserverMachine), `machine/greatflesh/` (GreatFleshMachine), `machine/multiblock/` (CogniAssemblerMachine + part/) |
| Recipe ingredients | `api/recipe/ingredient/` (entity/model ingredient + property/ hierarchy), `api/recipe/matcher/` (PropertyOperators), `api/recipe/lookup/` |
| Mob crushing | `common/recipe/MobCrushingRecipe.java`, `common/recipe/MobCrushingRecipeManager.java`, `integration/jei/MobCrushingCategory.java` |
| Datagen | `data/` |
| XEI/Jade/client | `integration/`, `client/` |
| Mixins | `mixin/`, `src/main/resources/ctnhbio.mixins.json` |

## DOMAIN GUIDE ROUTING
Read the matching domain guide before editing the corresponding source area.

| Source area | Guide | Read before |
|-------------|-------|-------------|
| `api` | `docs/CTNH-Bio/api/AGENTS.md` | Recipe capabilities, entity/model ingredients, machine APIs |
| `client` | `docs/CTNH-Bio/client/AGENTS.md` | Renderers, models, GUI textures |
| `common` | `docs/CTNH-Bio/common/AGENTS.md` | CommonProxy, conditions, items, recipes, serums |
| `data` | `docs/CTNH-Bio/data/AGENTS.md` | Recipe generators, lang, loot, materials, tags |
| `event` | `docs/CTNH-Bio/event/AGENTS.md` | EventHandler, ForgeEventHandler, TransformManager |
| `integration` | `docs/CTNH-Bio/integration/AGENTS.md` | XEI/Jade/EMI/JEI integration |
| `machine` | `docs/CTNH-Bio/machine/AGENTS.md` | Living-machine implementations |
| `mixin` | `docs/CTNH-Bio/mixin/AGENTS.md` | Biomancy/HNN/EMI/Create/GTCEu patches |
| `registry` | `docs/CTNH-Bio/registry/AGENTS.md` | Items, blocks, entities, machines, recipes |
| `utils` | `docs/CTNH-Bio/utils/AGENTS.md` | Shared helpers |

## CONVENTIONS
- Namespace is `com.moguang.ctnhbio`; registry prefixes generally use `CB`.
- GT/GMT recipes are runtime dynamic-pack data (`CTNHBioGTAddon.addRecipes()`); `runData` produces no JSON for them. See root AGENTS.md CONVENTIONS.
- Item/block/fluid references MUST use direct registration objects (`CBBlocks.X`, `CBItems.X`, `GTMaterials.X`, `TagPrefix.ingot`) — never `ResourceLocation` string parsing + `ForgeRegistries` lookups. See root AGENTS.md CONVENTIONS.
- `src/main/resources/data/ctnhbio/recipes/decomposing` has many hand-authored/static recipe JSON files.
- `src/generated/resources` is produced by `:modules:CTNH-Bio:runData`.
- Mixins span Biomancy, Hostile Neural Networks, EMI/ALI, Create, and GTCEu recipe/machine internals; treat them as compatibility patches, not generic helpers.

## ANTI-PATTERNS
- Do not collapse biological recipe capabilities into Core; this module owns its living-machine abstractions.
- Do not assume all recipe JSON is generated; check whether it is under `src/main/resources` or `src/generated/resources`.
- Do not bypass `PropertyOperators` / `EntityProperties` when adding entity-model recipe matching; those registries are initialized explicitly in `CommonProxy.init()`.

## COMMANDS
```text
./gradlew :modules:CTNH-Bio:build
./gradlew :modules:CTNH-Bio:runData
./gradlew :modules:CTNH-Bio:spotlessCheck
```

## SCOPE
Applies to `modules/CTNH-Bio` and its submodule repository. It is a reference guide loaded through the root routing table, not an additional source-tree instruction file.

## READ WHEN
- Adding or changing living-machine content, biological recipe capabilities, or Bio-specific recipes.
- Changing Bio datagen providers or mixin patches.

## SOURCE OF TRUTH
- Registration/lifecycle: `CTNHBio.java`, `CTNHBioGTAddon.java`, `common/CommonProxy.java`.
- Forge metadata and mixins: `src/main/resources/META-INF/mods.toml` and `ctnhbio.mixins.json`.
- Static generated data: providers plus `src/generated/resources`, plus hand-authored JSON under `src/main/resources/data/ctnhbio/recipes/decomposing`.

## WORKFLOW
1. Map the changed symbol to its domain and read that domain guide.
2. Check GT addon hook order, CommonProxy init, and PropertyOperators/EntityProperties registries.
3. Run the narrowest Gradle task (`runData` for datagen, `build` for compilation).
4. Re-read the root routing table if the change introduces a new module boundary.
