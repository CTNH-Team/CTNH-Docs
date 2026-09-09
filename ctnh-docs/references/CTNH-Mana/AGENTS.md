# CTNH-Mana MODULE

## OVERVIEW
Botania / BloodMagic / Apotheosis x GT integration module. ~333 Java files under `com.magicbee.ctnhmana`. Entry: `CTNHMana`, `CTNHManaGTAddon`, `CMConfig`, `common/CommonProxy`, `client/ClientProxy`.

## STRUCTURE
```
com.magicbee.ctnhmana/
  CTNHMana.java // mod entry
  CTNHManaGTAddon.java // GT addon: addRecipes/removeRecipes
  CMConfig.java
  api/ // effect(16), machine/gem+trait, mixin/IBloodAltarLogic, networks, pattern, recipe/condition(4)+customlogic(6)
  client/ // ClientProxy, ZenithInvadeClient, ZenithMatrixEffect, gui/radial, model(8), ponder, render(17)+particle, utils
  common/ // CommonProxy, DigitalWosMachine, blockentity+flower(7), blocks(5), capability, entity+ai+navigation+projectile, event/zenith(5), gui(7), item/*, machine(3), multiblock(31), parts, ritual/ritualtypes
  data/ // CMDatagen, ManaData, lang(3), materials, recipe(35+builder11+utils1), tags(2)
  event/ (16)
  integration/ // emi(1), jade(2)
  mixin/ // ae2(2), ars(4), bloodmagic(4), botania(6), emi(1), minecraft(1)
  networking/packets(7) // CMNetworking
  registry/ (19+items1+multiblock5+sounds2)
  utils/ (3)
```
Mixins config: `src/main/resources/*.mixins.json` (verify actual filename in resources).

## WHERE TO LOOK
| Concern | Location |
|---|---|
| Mod init / proxies | `CTNHMana.java`, `common/CommonProxy.java`, `client/ClientProxy.java`, `CMConfig.java` |
| GT recipes add/remove | `CTNHManaGTAddon.java` -> `data/recipe/*`, delegates removal to `data/recipe/ManaRecipeRemoval` + CTNH-Lib `RecipeRemovalHelper` |
| Registries | `registry/CMBlocks`, `CMItems`, `CMBlockEntities`, `CMEntities`, `CMMachines`, `CMMultiblockMachines`, `CMRecipeTypes`, `CMMobEffects`, `CMMaterials`, `GTMaterialAddon` |
| Multiblocks / machines | `common/multiblock/*` (31: `MysticSpire`, `ZenithMachine`, `EternalGarden`, `HellForgeMachine`...), `common/machine/*`, `common/parts/*`, `api/machine/trait/*` |
| Datagen / recipes / tags / lang | `data/CMDatagen.java`, `data/ManaData.java`, `data/recipe/*`, `data/tags/*`, `data/lang/*` -> see `data/AGENTS.md` |
| Client render/ponder | `client/render/*`, `client/model/*`, `client/ponder/*` |
| Network / integration | `networking/packets/CMNetworking.java`, `integration/emi+jade/*` |
| Mixins | `mixin/*` + `api/mixin/IBloodAltarLogic.java` |

## DOMAIN GUIDE ROUTING
| Source area | Guide | Read before |
|---|---|---|
| `data/` recipes/removal/builders/tags/lang | `data/AGENTS.md` | editing any `data/recipe/*`, `ManaRecipeRemoval` |
| `common/multiblock`, `common/machine`, `api/machine` | module doc only (no sub-guide) | adding machine/trait/logic |
| `registry/*` | module doc only | adding block/item/machine/effect |
| `mixin/*`, `integration/*`, `networking/*`, `event/*`, `client/*` | module doc only | cross-mod compat / packets / render |

## CONVENTIONS
- GTM dynamic pack: GT/GMT recipes via `*GTAddon.addRecipes()` register as runtime dynamic datapack (`GTDynamicPackContents` / CTNH-Lib `CTNHDynamicDataPack`), `runData` produces NO JSON for them; static `src/generated/resources` only tags/lang/models/worldgen/non-GT recipes; verify in-game or `ConfigHolder.dev.dumpRecipes`.
- Reference items/blocks/fluids via static registry objects (`GTMaterials.*`, `CMBlocks.*`, `CMItems.*`, `TagPrefix.*`, `AEItems.*`, `CBBlocks.*`, `CEItems.*`, `CMItems.*`, `CABlocks.*`, `CTPPBlocks.*`), forbid `ResourceLocation` string parse + `ForgeRegistries` lookup; string IDs only when no registry object exists (upstream mod-specific ID, recipe ID, tag key, dimension ID).
- Recipe removal via CTNH-Lib: `ManaRecipeRemoval.init()` + `RecipeRemovalHelper.remove(new RemoveFilter().id/type/idRegex(...))` called from `CTNHManaGTAddon.removeRecipes(Consumer<ResourceLocation> ignoredConsumer)`; no local `Consumer.accept` loop, no `DataFilterPack`.

## ANTI-PATTERNS
- No `DataFilterPack.removeRecipe*` in Mana; no resurrected `data/recipe/RecipeRemoval` with `Consumer<ResourceLocation>` loop.
- No `ResourceLocation.parse + ForgeRegistries` lookup where registry object exists.
- No expecting GT recipe JSON under `src/generated/resources`; no static JSON for `addRecipes()` output.
- No new top-level domain package without module-doc routing update.

## COMMANDS
- `./gradlew :modules:CTNH-Mana:build`
- `./gradlew :modules:CTNH-Mana:runData` // static only; GT recipes not emitted
- Verify removal in-game or `ConfigHolder.dev.dumpRecipes`.

## SCOPE
Mana-multiblock/magic-system + compat recipes only. Core GT/registrate infra -> CTNH-Core/CTNH-Lib.

## READ WHEN
Touching `CTNHManaGTAddon`, `data/recipe/*`, registry, multiblock, mixin, packets.

## SOURCE OF TRUTH
`modules/CTNH-Mana/src/main/java` tree + `CTNHManaGTAddon.java` diff; `src/main/resources/*.mixins.json`.

## WORKFLOW
Discovery -> Scoring -> Generate -> Review; module-doc for entry/registry/structure, `data/AGENTS.md` for recipe/removal changes; telegraphic, no fabrication.
