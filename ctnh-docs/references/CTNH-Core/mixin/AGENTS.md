# CTNH-CORE MIXIN DOMAIN

## OVERVIEW
跨 mod Mixin 补丁（47 个 Java 文件，其中 47 个类带 `@Mixin`）：AECs、Apotheosis、Ars Nouveau、Avaritia、Create、Create Diesel、EIO、EMI、Ecliptic Seasons、FTB Chunks、FTB Essentials、GTCEu、JAVD、Legendary Survival、Minecraft（区块/刷怪/服务器）、TMRV、Vintage Improvements。

## STRUCTURE
```text
mixin/
|-- ChunkMixin / ChunkSerializerMixin / TagLoaderMixin     # Minecraft 核心
|-- mc/                        # MinecraftServerMixin, MobMixin, MonsterMixin, NaturalSpawnerMixin, ServerChunkCacheMixin, ServerChunkCacheAccessor
|-- aecs/                      # EmiPluginMixin
|-- apotheosis/                # EarthsBoonEnchantMixin, SocketHelperMixin
|-- ars_nouveau/               # GlyphRecipeCategoryMixin, TerminalSyncManagerMixin
|-- avaritia/                  # AvaritiaSculkCategoryMixin
|-- create/                    # ChainConveyorRidingHandlerMixin, MechanicalCraftingCategoryMixin, RuntimeDataGeneratorMixin, SpoutCategoryMixin, StockKeeperRequestScreenMixin
|-- creatediesel/              # DistillationCategoryMixin, OilChunksSavedDataMixin, OilScannerItemMixin, PumpjackHoleBlockEntityMixin
|-- dategen/                   # AECSDatagenMixin, CreateOreExcavationDategenMixin, DataGeneratorBanMixin, FTBUltimineDatagenMixin, ImmersiveAircraftDatagenMixin
|-- eclipticseasons/           # BakedQuadRetexturedAndReUVMixin, BakedQuadRetexturedMixin, SnowyBakedModelWrapperOffsetMixin, SnowySeasonBakeModelMixin
|-- eio/                       # MachinesJEIMixin
|-- emi/                       # EmiReloadManagerMixin, GTRecipeEMICategoryMixin, JemiRecipeMixin, JemiStackSerializerMixin
|-- ftbchunks/                 # HeightUtilsMixin
|-- ftbessentials/             # TeleportCommandsMixin
|-- gtceu/                     # GTBlocksMixin, ItemMaterialDataMixin
|   `-- orevein/               # ClientProxyAccessor
|-- javd/                      # PortalBlockMixin
|-- legendarysurvival/         # AltitudeModifierMixin
|-- tmrv/                      # RecipeManagerMixin
`-- vintageimprovements/       # LatheMovingBlockMixin
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Mixin 配置 | `src/main/resources/ctnhcore.mixins.json` |
| Ecliptic Seasons 补丁 | `mixin/eclipticseasons/`（4，全部注册在 `client` 段） |
| Minecraft 核心 mixin | `mixin/mc/` |
| GTCEu mixin | `mixin/gtceu/`, `mixin/gtceu/orevein/` |
| Create mixin | `mixin/create/` |
| Create Diesel mixin | `mixin/creatediesel/`（DistillationCategoryMixin, OilChunksSavedDataMixin, OilScannerItemMixin, PumpjackHoleBlockEntityMixin） |
| AECs / EIO / EMI | `mixin/aecs/`, `mixin/eio/`, `mixin/emi/`（含 JemiRecipeMixin, JemiStackSerializerMixin） |
| Apotheosis / Ars / Avaritia | `mixin/apotheosis/`, `mixin/ars_nouveau/`, `mixin/avaritia/` |
| FTB Chunks / FTB Essentials / JAVD / TMRV | `mixin/ftbchunks/`, `mixin/ftbessentials/`, `mixin/javd/`, `mixin/tmrv/` |
| Datagen mixin | `mixin/dategen/` |
| 区块重载 | `mixin/ChunkMixin.java`, `mixin/ChunkSerializerMixin.java`, `mixin/TagLoaderMixin.java` |
| FTB Essentials accessor | `mixin/mc/ServerChunkCacheAccessor.java`（供 `integration/ftbessentials/AsyncRtpManager` 使用） |
| 配方删除注入 | 由 CTNH-Lib `mixin/RecipeManagerApplyMixin` 承担，不在本模块 |

## CONVENTIONS
- mixin JSON 与包内条目必须同步；两者齐备 Mixin 才会加载。
- `ctnhcore.mixins.json` 的 `mixins` 段（common）与 `client` 段分开登记；客户端类（`creatediesel.DistillationCategoryMixin`、`emi.JemiRecipeMixin`、`emi.JemiStackSerializerMixin`、`eclipticseasons.*`）只在 `client` 段出现。
- 改注入签名前先确认目标 mod 版本。
- `ServerChunkCacheAccessor` 暴露私有的主线程区块 future 方法，供异步 RTP 管理器使用。
- `creatediesel.DistillationCategoryMixin` 与 `emi.JemiRecipeMixin`/`JemiStackSerializerMixin` 是客户端 mixin：前者居中可变高度蒸馏配方，后者修复 EMI 收藏夹中 JEI 自定义渲染器堆栈的往返。
- `mixin/tmrv/RecipeManagerMixin` 修复 TooManyRecipeViewers 的 `addRecipe` 忽略配方检查（重定向 `Set.contains`，`@Redirect` + `@Local`），与配方删除无关。

## ANTI-PATTERNS
- 不核对上游目标成员就改注入点。
- 把兼容性 mixin 当成通用工具使用。
- 在 Core 重新实现已由 CTNH-Lib 提供的配方删除注入。
- 把客户端 mixin 登记进 `mixins` 段（或反之），或让 JSON 与包内类不同步。

## SCOPE
适用于 `src/main/java/io/github/cpearl0/ctnhcore/mixin` 与 `src/main/resources/ctnhcore.mixins.json`。

## READ WHEN
- 打补丁到或排查上述任一 mod 集成。
- 改动 datapack 配方过滤行为（注意实现位于 CTNH-Lib）。

## SOURCE OF TRUTH
- `src/main/resources/ctnhcore.mixins.json` 与 `mixin/` 下的类。
- 上游目标 mod 版本（用于签名校验）。

## WORKFLOW
1. 定位集成对应的 mixin 包与 JSON 条目。
2. 对照已加载的 mod 版本核验目标成员。
3. 跑 `:modules:CTNH-Core:build`；在装有目标 mod 的运行时验证。
