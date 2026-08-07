# CTNH-LIB MODULE

## OVERVIEW
CTNH-Lib is the shared support module for CTNH code (57 Java files). It contains common proxies, registrate builder wrappers, dynamic datapack helpers, language annotations, shared Ponder support, right-side configurator UI, Jade priority infrastructure, and client highlight networking.

## STRUCTURE
```text
src/main/java/tech/vixhentx/mcmod/ctnhlib/
|-- CTNHLib.java             # library mod initialization
|-- api/                     # CTNHValues, CrossParallelRecipeLogic, ICrossParallelRecipeLogicMachine
|-- client/                  # ClientProxy, right configurator UI, highlight render, Ponder framework
|   |-- ponder/              # CTNHPonderLang, CTNHPonderSceneBuilder, CTNHPonderTagHelper
|   |-- render/              # ColorData
|   `-- render/highlight/    # HighlightHandler, HighlightRender
|-- command/                 # CTNHCommandChatHelper, CTNHCommandInspector, CTNHCommands
|-- common/                  # CommonProxy, MultiblockHelper
|-- data/                    # CTNHDynamicDataPack, DataFilterPack
|-- jade/                    # GTProvidersRegistrar, JadePriorityManager
|-- langprovider/            # Lang, LangProcessor (annotations processor; see com.ctnhlang)
|-- mixin/                   # GTJadePluginMixin, GTRecipesMixin, MachineBuilderMixin, TMRVMixin
|-- network/packets/         # BlockHighlightPacket
|-- registrate/              # CNRegistrate, CTNHLibNetworking
|   |-- builders/            # 10 builders (CTNHItemBuilder, CTNHMachineBuilder, CTNHRecipeType, ...)
|   |-- data/                # ProviderTypes
|   `-- lang/                # RegistrateCNLangProvider
|-- utils/                   # ChunkList, EnvUtils, ExtendNbtUtils, LockIdentityHashMap, MachineUtils
`-- src/main/java/com/ctnhlang/  # separate annotation namespace
    `-- langprovider/        # LangKeyBuilder
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Mod entry | `CTNHLib.java` |
| Registrate helpers | `registrate/` |
| Builder APIs | `registrate/builders/` (10 builders) |
| Dynamic data | `data/` (`CTNHDynamicDataPack`, `DataFilterPack`) |
| Shared GUI | `client/` (RightConfiguratorPanel, RCUIWidget) |
| Highlight rendering | `client/render/highlight/` (`HighlightHandler`, `HighlightRender`), `network/packets/BlockHighlightPacket.java` |
| Jade priority | `jade/` |
| Ponder framework | `client/ponder/` (`CTNHPonderLang`, `CTNHPonderSceneBuilder`, `CTNHPonderTagHelper`) |
| Lang annotations | `com/ctnhlang/` (separate namespace, `LangKeyBuilder`) |
| Mixins | `mixin/`, `src/main/resources/ctnhlib.mixins.json` |

## DOMAIN GUIDE ROUTING
Read the matching domain guide before editing the corresponding source area.

| Source area | Guide | Read before |
|-------------|-------|-------------|
| `api` | `docs/CTNH-Lib/api/AGENTS.md` | Shared values, cross-parallel recipe logic |
| `client` | `docs/CTNH-Lib/client/AGENTS.md` | Right configurator UI, highlight render, Ponder framework |
| `command` | `docs/CTNH-Lib/command/AGENTS.md` | Chat helper, inspector commands |
| `common` | `docs/CTNH-Lib/common/AGENTS.md` | CommonProxy, MultiblockHelper |
| `data` | `docs/CTNH-Lib/data/AGENTS.md` | Dynamic datapack and filter packs |
| `jade` | `docs/CTNH-Lib/jade/AGENTS.md` | GT provider ordering |
| `langprovider` | `docs/CTNH-Lib/langprovider/AGENTS.md` | @CN/@EN annotations and processor |
| `mixin` | `docs/CTNH-Lib/mixin/AGENTS.md` | GT Jade ordering, builder adjustments, TMRV, datagen shutdown |
| `network` | `docs/CTNH-Lib/network/AGENTS.md` | BlockHighlightPacket |
| `registrate` | `docs/CTNH-Lib/registrate/AGENTS.md` | CNRegistrate and builder wrappers |
| `utils` | `docs/CTNH-Lib/utils/AGENTS.md` | Shared helpers |

## CONVENTIONS
- Main library namespace is `tech.vixhentx.mcmod.ctnhlib`; lang annotation namespace is `com.ctnhlang`.
- `CTNHDynamicDataPack` is the runtime pack that carries GT/GMT recipes (via `GTDynamicPackContents`) into the recipe manager; that is why `runData` never emits JSON for GT/GMT recipes. See root AGENTS.md CONVENTIONS.
- Item/block/fluid references MUST use direct registration objects (`GTMaterials.X`, `TagPrefix.ingot`) — never `ResourceLocation` string parsing + `ForgeRegistries` lookups. In Lib, `ResourceLocation` appears only for recipe/tag/advancement ID path generation, not item resolution. See root AGENTS.md CONVENTIONS.
- Resource count is intentionally tiny compared with gameplay modules.
- Changes here can affect all CTNH modules through shared builders, annotations, Jade provider ordering, right configurator UI, highlight packets, and shared Ponder support.

## ANTI-PATTERNS
- Do not add gameplay-specific logic to CTNH-Lib unless it is genuinely shared.
- Do not move module-specific Ponder scene/tag/plugin code or Energy's AE2 cable helper into CTNH-Lib.
- Do not rename lang annotations without checking the custom `com.ctnhlang.langprovider` plugin usage.
- Do not bypass `JadePriorityManager` for GT provider ordering; CTNH modules rely on predictable Jade block data/component priority.

## COMMANDS
```text
./gradlew :modules:CTNH-Lib:build
./gradlew :modules:CTNH-Lib:runData
./gradlew :modules:CTNH-Lib:spotlessCheck
```

## SCOPE
Applies to `modules/CTNH-Lib` and every CTNH module that consumes its shared APIs. It is a reference guide loaded through the root routing table, not an additional source-tree instruction file.

## READ WHEN
- Adding a shared registration helper, builder, or annotation consumed by multiple modules.
- Changing Jade provider ordering, the right configurator UI, highlight packets, or the shared Ponder builder.
- Any change that could ripple into other CTNH modules through shared infrastructure.

## SOURCE OF TRUTH
- Registration/lifecycle: `CTNHLib.java`, `common/CommonProxy.java`, `registrate/CNRegistrate.java`.
- Forge metadata and mixins: `src/main/resources/META-INF/mods.toml` and `ctnhlib.mixins.json`.
- Lang annotation processing: the `com.ctnhlang.langprovider` Gradle plugin and `registrate/lang/RegistrateCNLangProvider.java`.

## WORKFLOW
1. Confirm the behavior is genuinely shared before adding it to Lib.
2. Check all consumer modules (Core, Energy, Bio, Mana, Astral, CTPP, CEI) for affected call sites.
3. Run `:modules:CTNH-Lib:build` and the narrowest consumer task; run `runData` when lang or Ponder extraction changed.
4. Re-read the root routing table if a new shared surface is introduced.
