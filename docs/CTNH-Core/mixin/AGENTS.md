# CTNH-CORE MIXIN DOMAIN

## OVERVIEW
Broad cross-mod mixins (34 Java files): AECs, Apotheosis, Ars Nouveau, Avaritia, Create, EIO/JEI, EMI, FTB Chunks, GTCEu, JAVD, LDLib, Legendary Survival, Minecraft reload/spawner, Sophisticated, TConstruct, TMRV, and Vintage Improvements. Also hosts the datapack recipe removal hook.

## STRUCTURE
```text
mixin/
|-- ChunkMixin / ChunkSerializerMixin / TagLoaderMixin     # Minecraft core
|-- mc/                        # MinecraftServerMixin, MobMixin, MonsterMixin, NaturalSpawnerMixin, RecipeManagerApplyMixin, ServerChunkCacheMixin
|-- aecs/                      # EmiPluginMixin
|-- apotheosis/                # EarthsBoonEnchantMixin, SocketHelperMixin
|-- ars_nouveau/               # GlyphRecipeCategoryMixin
|-- avaritia/                  # AvaritiaSculkCategoryMixin
|-- create/                    # ChainConveyorRidingHandlerMixin, MechanicalCraftingCategoryMixin, SpoutCategoryMixin, StockKeeperRequestScreenMixin
|-- dategen/                   # NOTE: spelled dategen, not datagen — AECSDatagenMixin, CreateOreExcavationDategenMixin, DataGeneratorBanMixin, FTBUltimineDatagenMixin, ImmersiveAircraftDatagenMixin
|-- eio/                       # MachinesJEIMixin
|-- emi/                       # EmiReloadManagerMixin, GTRecipeEMICategoryMixin
|-- ftbchunks/                 # HeightUtilsMixin
|-- gtceu/                     # GTBlocksMixin, ItemMaterialDataMixin
|   `-- orevein/               # ClientProxyAccessor (only non-Mixin-named accessor)
|-- javd/                      # PortalBlockMixin
|-- legendarysurvival/         # AltitudeModifierMixin
|-- tmrv/                      # RecipeManagerMixin
`-- vintageimprovements/       # LatheMovingBlockMixin
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Mixin config | `src/main/resources/ctnhcore.mixins.json` |
| Minecraft core mixins | `mixin/mc/` (incl. `RecipeManagerApplyMixin.java` at `RecipeManager.apply()` HEAD) |
| GTCEu mixins | `mixin/gtceu/`, `mixin/gtceu/orevein/` |
| Create mixins | `mixin/create/` |
| AECs / EIO / EMI | `mixin/aecs/`, `mixin/eio/`, `mixin/emi/` |
| Apotheosis / Ars / Avaritia | `mixin/apotheosis/`, `mixin/ars_nouveau/`, `mixin/avaritia/` |
| FTB Chunks / JAVD / TMRV | `mixin/ftbchunks/`, `mixin/javd/`, `mixin/tmrv/` |
| Datagen mixins | `mixin/dategen/` (spelling preserved) |
| Chunk reload | `mixin/ChunkMixin.java`, `mixin/ChunkSerializerMixin.java`, `mixin/TagLoaderMixin.java` |

## CONVENTIONS
- Keep mixin JSON and package entries synchronized; both are required for a mixin to load.
- `RecipeManagerApplyMixin.java` removes matching incoming datapack entries at `RecipeManager.apply()` HEAD; dynamic recipes are intentionally not filtered.
- Inspect target mod versions before changing injection signatures.
- The datagen mixin package is spelled `dategen`; do not "fix" it to `datagen` without updating the mixin JSON refmap.

## ANTI-PATTERNS
- Do not change injection points without checking the upstream target members.
- Do not treat compatibility mixins as generic helpers.

## SCOPE
Applies to `src/main/java/io/github/cpearl0/ctnhcore/mixin` and `src/main/resources/ctnhcore.mixins.json`.

## READ WHEN
- Patching or tracing any of the listed mod integrations.
- Changing datapack recipe filtering behavior.

## SOURCE OF TRUTH
- `src/main/resources/ctnhcore.mixins.json` and the mixin classes in `mixin/`.
- Upstream target mod versions for signature validation.

## WORKFLOW
1. Locate the integration's mixin package and JSON entry.
2. Verify the target member against the loaded mod version.
3. Run `:modules:CTNH-Core:build`; validate at runtime with the target mod present.
