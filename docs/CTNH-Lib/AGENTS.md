# CTNH-LIB MODULE

## OVERVIEW
CTNH-Lib is the shared support module for CTNH code (57 Java files: 11 in `com.ctnhlang`, 46 in `tech.vixhentx.mcmod.ctnhlib`). It contains common proxies, registrate builder wrappers, dynamic datapack helpers, language annotations, shared Ponder support, and client highlight networking. Jade priority infrastructure removed in f9951f9.

## STRUCTURE
```text
src/main/java/tech/vixhentx/mcmod/ctnhlib/
|-- CTNHLib.java             # library mod initialization
|-- api/                     # CTNHValues, CrossParallelRecipeLogic, ICrossParallelRecipeLogicMachine (3)
|-- client/                  # ClientProxy, highlight render, Ponder framework
|   |-- ponder/              # CTNHPonderLang, CTNHPonderSceneBuilder, CTNHPonderTagHelper (3)
|   |-- render/              # ColorData (1)
|   `-- render/highlight/    # HighlightHandler, HighlightRender (2)
|-- command/                 # CTNHCommandChatHelper, CTNHCommandInspector, CTNHCommands (3)
|-- common/                  # CommonProxy, MultiblockHelper (2)
|-- data/                    # CTNHDynamicDataPack, DataFilterPack (2)
|-- langprovider/            # Lang, LangProcessor (2)
|-- mixin/                   # GTRecipesMixin, MachineBuilderMixin, TMRVMixin (3)
|-- network/packets/         # BlockHighlightPacket (1)
|-- registrate/              # CNRegistrate, CTNHLibNetworking (14 total)
|   |-- builders/            # 10 builders (CTNHItemBuilder, CTNHMachineBuilder, CTNHRecipeType, ...)
|   |-- data/                # ProviderTypes (ctnhlib_cnlang)
|   `-- lang/                # RegistrateCNLangProvider
`-- utils/                   # AllBuilder2, ChunkList, CodecBuilder, EnvUtils, ExtendNbtUtils, InfiniteMeteorTerrain, LockIdentityHashMap, MachineUtils (8)

src/main/java/com/ctnhlang/   # separate annotation namespace (11)
|-- CN.java, EN.java, Category.java, Domain.java, IgnoreLang.java, Key.java, Lang.java, LangFactory.java, Prefix.java, Suffix.java (10)
`-- langprovider/            # LangKeyBuilder (1)
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Mod entry | `CTNHLib.java` |
| Registrate helpers | `registrate/` |
| Builder APIs | `registrate/builders/` (10 builders) |
| Dynamic data | `data/` (`CTNHDynamicDataPack`, `DataFilterPack`) |
| Client bootstrap | `client/ClientProxy.java` |
| Highlight rendering | `client/render/highlight/` (`HighlightHandler`, `HighlightRender`), `network/packets/BlockHighlightPacket.java` |
| Ponder framework | `client/ponder/` (`CTNHPonderLang`, `CTNHPonderSceneBuilder`, `CTNHPonderTagHelper`) |
| Lang annotations | `com/ctnhlang/` (separate namespace: `CN`, `EN`, `Category`, `Domain`, `IgnoreLang`, `Key`, `Lang`, `LangFactory`, `Prefix`, `Suffix`; `langprovider/LangKeyBuilder.java`) |
| Mixins | `mixin/` (`GTRecipesMixin`, `MachineBuilderMixin`, `TMRVMixin`), `src/main/resources/ctnhlib.mixins.json` (3 mixins) |
| Shared helpers | `utils/` (AllBuilder2, ChunkList, CodecBuilder, EnvUtils, ExtendNbtUtils, InfiniteMeteorTerrain, LockIdentityHashMap, MachineUtils) |
| Commands | `command/CTNHCommands.java` (`/ctnh hand` + dev `/ctnh showores`) |

## ARCHITECTURE CONTRACT
Machine/trait/capability/Jade 的所有权边界、字段同步与持久化规则、Jade 数据最小化原则和迁移步骤在 `docs/_architecture/AGENTS.md`。改动机器、trait、recipe capability 或 Jade 代码前先读它；本文件只描述本模块的落点。

## DOMAIN GUIDE ROUTING
Read the matching domain guide before editing the corresponding source area.

| Source area | Guide | Read before |
|-------------|-------|-------------|
| `api` | `docs/CTNH-Lib/api/AGENTS.md` | Shared values, cross-parallel recipe logic |
| `client` | `docs/CTNH-Lib/client/AGENTS.md` | Highlight render, Ponder framework |
| `command` | `docs/CTNH-Lib/command/AGENTS.md` | Chat helper, inspector, showores dev command |
| `common` | `docs/CTNH-Lib/common/AGENTS.md` | CommonProxy, MultiblockHelper |
| `data` | `docs/CTNH-Lib/data/AGENTS.md` | Dynamic datapack and filter packs |
| `langprovider` | `docs/CTNH-Lib/langprovider/AGENTS.md` | @CN/@EN annotations and processor |
| `mixin` | `docs/CTNH-Lib/mixin/AGENTS.md` | Builder adjustments, TMRV, datagen shutdown |
| `network` | `docs/CTNH-Lib/network/AGENTS.md` | BlockHighlightPacket |
| `registrate` | `docs/CTNH-Lib/registrate/AGENTS.md` | CNRegistrate and builder wrappers |
| `utils` | `docs/CTNH-Lib/utils/AGENTS.md` | Shared helpers |

## CONVENTIONS
- Main library namespace is `tech.vixhentx.mcmod.ctnhlib`; lang annotation namespace is `com.ctnhlang`.
- `CTNHDynamicDataPack` is the runtime pack that carries GT/GMT recipes (via `GTDynamicPackContents`) into the recipe manager; that is why `runData` never emits JSON for GT/GMT recipes. Static `src/generated/resources` only contains tags/lang/models/worldgen/non-GT recipes; verify GT recipes in-game or via `ConfigHolder.dev.dumpRecipes`. See root AGENTS.md CONVENTIONS.
- Item/block/fluid references MUST use direct registration objects (`GTMaterials.X`, `TagPrefix.ingot`, `CTNHBlocks.X`, `AEItems.X`, etc.) — never `ResourceLocation` string parsing + `ForgeRegistries` lookups. `ResourceLocation` strings are only for recipe/tag/advancement/dimension IDs where no registry object exists. See root AGENTS.md CONVENTIONS. In Lib, `ResourceLocation` appears only for recipe/tag/advancement ID path generation and `CTNHCommands` tag inspection rendering (`ForgeRegistries.FLUIDS.getKey` for display), not item resolution.
- GTCEu 的 trait 基础设施（`api/machine/trait/`：`MachineTrait`、`RecipeLogic`、`WorkLogic`、`ICapabilityTrait`、`Notifiable*`、`*ComputationPortTrait` 等 17 个类）属 **vendored 上游**，不在 CTNH-Lib 内；Lib 只提供 `api/CrossParallelRecipeLogic`（跨并行共享 `RecipeLogic`）。改 trait 基类只在任务明确针对 GTCEu 内部时进行。
- `registrate/data/ProviderTypes.CNLANG` 注册 id 为 `ctnhlib_cnlang`（非 `cnlang`），避免与第三方 mod `ae2pw` 内置拷贝撞车导致 `zh_cn.json` 空写盘。详见 registrate 域文档。
- 拼写怪癖：Core mixin 包是 `dategen`（非 datagen）；CTPP fan 包是 `fanprocessing`（无下划线）；Mana 是 `multiblock`（无 `Mutiblock` 遗留）。
- Resource count is intentionally tiny compared with gameplay modules.
- Changes here can affect all CTNH modules through shared builders, annotations, highlight packets, and shared Ponder support.

## ANTI-PATTERNS
- Do not add gameplay-specific logic to CTNH-Lib unless it is genuinely shared.
- Do not move module-specific Ponder scene/tag/plugin code or Energy's AE2 cable helper into CTNH-Lib.
- Do not rename lang annotations without checking the custom `com.ctnhlang.langprovider` plugin usage.
- Do not reintroduce `jade/` provider ordering in Lib; Jade ordering was removed in f9951f9 and is owned by consumer modules/GTCEu directly.

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
- Changing highlight packets or the shared Ponder builder.
- Any change that could ripple into other CTNH modules through shared infrastructure.

## SOURCE OF TRUTH
- Registration/lifecycle: `CTNHLib.java`, `common/CommonProxy.java`, `registrate/CNRegistrate.java`.
- Forge metadata and mixins: `src/main/resources/META-INF/mods.toml` and `ctnhlib.mixins.json` (3 mixins).
- Lang annotation processing: the `com.ctnhlang.langprovider` Gradle plugin and `registrate/lang/RegistrateCNLangProvider.java` via `registrate/data/ProviderTypes.CNLANG` (`ctnhlib_cnlang`).

## WORKFLOW
1. Confirm the behavior is genuinely shared before adding it to Lib.
2. Check all consumer modules (Core, Energy, Bio, Mana, Astral, CTPP, CEI) for affected call sites.
3. Run `:modules:CTNH-Lib:build` and the narrowest consumer task; run `runData` when lang or Ponder extraction changed.
4. Re-read the root routing table if a new shared surface is introduced.
