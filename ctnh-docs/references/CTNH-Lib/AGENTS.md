# CTNH-LIB MODULE

## OVERVIEW
Shared library for all CTNH modules. 59 Java files. Entry `CTNHLib.java`, proxies `common/CommonProxy.java` + `client/ClientProxy.java`.

## STRUCTURE
```
com/ctnhlang/ (11 java)
  CN.java, EN.java, Lang.java, LangFactory.java, Key.java, Prefix.java, Suffix.java, Domain.java, Category.java, IgnoreLang.java
  langprovider/LangKeyBuilder.java
tech/vixhentx/mcmod/ctnhlib/ (48 java)
  CTNHLib.java
  api/CTNHValues.java, CrossParallelRecipeLogic.java, ICrossParallelRecipeLogicMachine.java
  client/ClientProxy.java, ponder/CTNHPonderLang.java+CTNHPonderSceneBuilder.java+CTNHPonderTagHelper.java, render/ColorData.java+highlight/HighlightHandler.java+HighlightRender.java
  command/CTNHCommands.java+CTNHCommandChatHelper.java+CTNHCommandInspector.java
  common/CommonProxy.java+MultiblockHelper.java
  data/CTNHDynamicDataPack.java+DataFilterPack.java+recipe/RecipeRemovalHelper.java
  langprovider/Lang.java+LangProcessor.java
  mixin/GTRecipesMixin.java+MachineBuilderMixin.java+RecipeManagerApplyMixin.java+TMRVMixin.java
  network/packets/BlockHighlightPacket.java
  registrate/CNRegistrate.java+CTNHLibNetworking.java+builders/*(10)+data/ProviderTypes.java+lang/RegistrateCNLangProvider.java
  utils/AllBuilder2.java+ChunkList.java+CodecBuilder.java+EnvUtils.java+ExtendNbtUtils.java+InfiniteMeteorTerrain.java+LockIdentityHashMap.java+MachineUtils.java
src/main/resources/ctnhlib.mixins.json
```

## WHERE TO LOOK
| Concern | Location |
| Mod entry, proxy wiring | CTNHLib.java, common/CommonProxy.java, client/ClientProxy.java |
| Cross-parallel logic | api/CrossParallelRecipeLogic.java, api/ICrossParallelRecipeLogicMachine.java, api/CTNHValues.java |
| Dynamic pack, recipe filtering | data/CTNHDynamicDataPack.java, data/DataFilterPack.java, data/recipe/RecipeRemovalHelper.java |
| RecipeManager pre-filter | mixin/RecipeManagerApplyMixin.java |
| GTM/Machine tweaks | mixin/GTRecipesMixin.java, mixin/MachineBuilderMixin.java, mixin/TMRVMixin.java |
| Registrate builders | registrate/builders/CTNHMachineBuilder.java, CTNHMultiblockMachineBuilder.java, CTNHBlockBuilder.java, CTNHItemBuilder.java, CTNHEntityBuilder.java, CTNHRecipeType.java, CTNHRecipeCategory.java, CTNHMaterial.java, CTNHTagPrefix.java, ICNBuilder.java |
| Lang pipeline | com/ctnhlang/*, langprovider/Lang.java+LangProcessor.java, registrate/lang/RegistrateCNLangProvider.java |
| Network/highlight | registrate/CTNHLibNetworking.java, network/packets/BlockHighlightPacket.java, client/render/highlight/* |
| Commands/debug | command/CTNHCommands.java, command/CTNHCommandInspector.java |
| Mixins list | src/main/resources/ctnhlib.mixins.json |

## DOMAIN GUIDE ROUTING
| Source area | Guide | Read before |
| data/*, data/recipe/* | data/AGENTS.md | touching removal filters or dynamic pack |
| mixin/* | mixin/AGENTS.md | touching RecipeManager/mixin json |
| registrate/builders/* | registrate/AGENTS.md if exists else this file | adding machine/block/item |
| com/ctnhlang/*, langprovider/* | langprovider routing in this file | adding lang keys |
| api/*, utils/*, client/*, command/*, common/*, network/* | this file only | no sub-guide |

## CONVENTIONS
- GTM dynamic pack: GT/GMT recipes via `*GTAddon.addRecipes()` are runtime dynamic datapack (`GTDynamicPackContents` / CTNH-Lib `CTNHDynamicDataPack`), `runData` emits no JSON for them; static `src/generated/resources` only tags/lang/models/worldgen/non-GT recipes; verify in-game or `ConfigHolder.dev.dumpRecipes`.
- Registry objects first: ref items/blocks/fluids via static registry objects (`GTMaterials.Iron`, `CTNHBlocks.MY_BLOCK`, `TagPrefix.ingot`, `AEItems.X`, `CBBlocks.X`, `CEItems.X`, `CMItems.X`, `CABlocks.X`, `CTPPBlocks.X`), forbid `ResourceLocation` string + `ForgeRegistries` lookup; string IDs only when no registry object (upstream mod IDs, recipe IDs, tag keys, dimension IDs).
- Removal registry centralized: `data/recipe/RecipeRemovalHelper` owns `FILTERS`; `remove()`, `clear()`, `getFilters()` only entry points.
- Builders via `CNRegistrate`, lang via `ctnhlang` + `LangProcessor`.

## ANTI-PATTERNS
- ForgeRegistries lookup by string when registry object exists.
- runData JSON for GT dynamic recipes.
- Duplicating RecipeRemoval logic in modules; use lib helper.
- Adding domain AGENTS.md for unchanged domains.

## COMMANDS
- Build lib: `./gradlew :modules:CTNH-Lib:build`
- runData (static only): `./gradlew :modules:CTNH-Lib:runData`
- Check mixins json after adding mixin class.

## SCOPE
CTNH-Lib shared code only. No gameplay content, no module-specific recipes.

## READ WHEN
Touching cross-module utils, dynamic pack, removal, mixins, registrate builders.

## SOURCE OF TRUTH
`modules/CTNH-Lib/src/main/java` + `src/main/resources/ctnhlib.mixins.json`. Code over docs.

## WORKFLOW
Discovery -> Scoring -> Generate data/mixin on change -> Review for redundancy/fabrication.