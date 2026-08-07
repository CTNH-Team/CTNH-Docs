# CTNH-ASTRAL MODULE

## OVERVIEW
CTNH-Astral adds astral content, GTCEu materials, enchantments, proxies, custom worldgen/dimension code, and an oxygen/atmosphere environment system under mod id `ctnhastral` (86 Java files).

## STRUCTURE
```text
src/main/java/com/ctnh/ctnhastral/
|-- CTNHAstral.java / CTNHAstralGTAddon.java    # mod entry, GT addon
|-- api/                      # loot/LootBuilder
|-- client/                   # ClientProxy, RocketLaunchHud, render/MoonEffects
|-- common/                   # CommonProxy, blocks, enchantments, entities, machines, oxygen system, recipes
|   |-- block/                # AstralFlowerBlock, AstralGrass(Block), AstralSaplingBlock, AstralTallGrassBlock, MarsSaplingBlock, SiliconBuddingBlock
|   |-- entity/               # RocketContraptionEntity
|   |-- event/                # RocketDimensionTravelHandler
|   |-- machine/multiblock/   # RocketAssemblyPlatformMachine
|   |-- machine/simple/       # OxygenEnricherMachine
|   |-- oxygen/               # AtmosphereType, OxygenAreaSource, OxygenEnvironment, OxygenEnvironmentService, OxygenMachineRules
|   `-- recipe/               # OxygenCondition
|-- data/                     # CAElements, CAEnchantments, CAMaterials, CARecipes, CATagPrefixes, GTMateralAdjust, lang/, worldgen/
|   `-- worldgen/             # worldgen root: CABiomes, CADensityFunctions, CADimensionTypes, CADimensions, CANetherRegion, CANoiseSetting, CAOverworldRegion, CASurfaceRuleData + biome/ feature/ structure/
|-- mixin/                    # adastra/ (Oxygen/Temperature), minecraft/ (chunk generator, packet listener)
|-- registry/                 # CABlocks, CAItems, CAMachines, CAMultiblocks, CARocketBlocks, CARocketEntityTypes, CTNHBlockInfo, CARegistrate, recipe types/conditions/modifiers, creative tabs + sound/ + worldgen/
`-- utils/                    # ModUtils
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Mod entry | `CTNHAstral.java` |
| GT addon | `CTNHAstralGTAddon.java` |
| Proxies | `client/`, `common/CommonProxy.java` |
| Oxygen/atmosphere | `common/oxygen/` (OxygenEnvironmentService, OxygenEnvironment, OxygenMachineRules, ...) |
| Rocket content | `common/entity/RocketContraptionEntity.java`, `common/event/RocketDimensionTravelHandler.java`, `client/RocketLaunchHud.java`, `registry/CARocketBlocks.java`, `registry/CARocketEntityTypes.java`, `common/machine/multiblock/RocketAssemblyPlatformMachine.java` |
| Core data | `data/CAElements.java`, `CAMaterials.java` (incl. Seawater), `CATagPrefixes.java`, `CARecipes.java` |
| Worldgen | `data/worldgen/` (root dimension classes + biome/ feature/ structure/) |
| Structures/features | `data/worldgen/structure/` (12 classes), `data/worldgen/feature/` (5) |
| Mixins | `mixin/`, `src/main/resources/ctnhastral.mixins.json` |
| Resources | `src/main/resources/assets/ctnhastral/`, `assets/gtceu/` (legacy), `src/generated/resources/` (lang, blockstates, noise settings) |

## DOMAIN GUIDE ROUTING
Read the matching domain guide before editing the corresponding source area.

| Source area | Guide | Read before |
|-------------|-------|-------------|
| `api` | `docs/CTNH-Astral/api/AGENTS.md` | Loot builder |
| `client` | `docs/CTNH-Astral/client/AGENTS.md` | ClientProxy, RocketLaunchHud, MoonEffects |
| `common` | `docs/CTNH-Astral/common/AGENTS.md` | CommonProxy, oxygen system, rockets, machines |
| `data` | `docs/CTNH-Astral/data/AGENTS.md` | Materials, elements, worldgen, lang |
| `mixin` | `docs/CTNH-Astral/mixin/AGENTS.md` | Ad Astra and chunk-generator hooks |
| `registry` | `docs/CTNH-Astral/registry/AGENTS.md` | Blocks (incl. rocket/moon/mars), sounds |
| `utils` | `docs/CTNH-Astral/utils/AGENTS.md` | ModUtils |

## CONVENTIONS
- Namespace is `com.ctnh.ctnhastral`; class prefixes generally use `CA`.
- GT/GMT recipes are runtime dynamic-pack data (`CTNHAstralGTAddon.addRecipes()`); `runData` produces no JSON for them. See root AGENTS.md CONVENTIONS.
- Item/block/fluid references MUST use direct registration objects (`CABlocks.X`, `CAMaterials.X`, `GTMaterials.X`, `TagPrefix.ingot`) — never `ResourceLocation` string parsing + `ForgeRegistries` lookups. See root AGENTS.md CONVENTIONS.
- This module has `src/generated/resources` (lang, blockstates, noise settings, e.g. `seawater.json`, `moon.json`); many material model JSON files are static resources under `src/main/resources`.
- Worldgen classes are concentrated under `data/worldgen`; dimension classes live directly in the `worldgen` root (no `dimension/` subpackage).
- Datagen output is mostly dynamic registry/sound provider driven; don't infer missing JSON means missing worldgen.
- Moon dimension default fluid is `CAMaterials.Seawater` (replacing `GTMaterials.SaltWater`); seawater textures live under `assets/ctnhastral/textures/block/fluids/fluid.seawater*.png`.

## ANTI-PATTERNS
- Do not assume assets under `assets/gtceu` are Astral-owned; fluid textures for Astral materials (e.g. seawater) are under `assets/ctnhastral/textures/block/fluids/` in `src/main/resources`.
- Do not edit one worldgen registry without checking related biome/source/dimension/noise classes.
- Do not change Ad Astra oxygen/temperature behavior without checking both mixin JSON entries and the upstream API targets.

## COMMANDS
```text
./gradlew :modules:CTNH-Astral:build
./gradlew :modules:CTNH-Astral:runData
./gradlew :modules:CTNH-Astral:spotlessCheck
```

## SCOPE
Applies to `modules/CTNH-Astral` and its submodule repository. It is a reference guide loaded through the root routing table, not an additional source-tree instruction file.

## READ WHEN
- Adding or changing astral content, materials, worldgen, dimension, rocket, or oxygen code.
- Changing Ad Astra or chunk-generator mixin hooks.

## SOURCE OF TRUTH
- Registration/lifecycle: `CTNHAstral.java`, `CTNHAstralGTAddon.java`, `common/CommonProxy.java`.
- Forge metadata and mixins: `src/main/resources/META-INF/mods.toml` and `ctnhastral.mixins.json`.
- Worldgen: bootstraps in `CommonProxy.gatherData()` and classes under `data/worldgen/`.

## WORKFLOW
1. Map the changed symbol to its domain and read that domain guide.
2. Check GT addon hook order and worldgen bootstraps as a group.
3. Run the narrowest Gradle task (`runData` for datagen, `build` for compilation).
4. Re-read the root routing table if the change introduces a new module boundary.
