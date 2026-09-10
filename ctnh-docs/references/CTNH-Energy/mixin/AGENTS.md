# CTNH-ENERGY MIXIN DOMAIN

## OVERVIEW
`mixin/`（59 个 Java 文件）以 Mixin 方式扩展上游 AE2 及其附属（AE2CT / AE2PW / AE2CS / BetterP2P / datagen）、GTM 与 Omni，为 EU 存储、样板署名、电路样板、样板提供者与量子计算机提供必须的侵入式补丁。

## STRUCTURE
```
mixin/
├─ ae2/                    (48)
│  ├─ CableBusContainerMixin, SettingsMixin
│  ├─ circuit/             PatternDetailsHelperMixin, ProcessingPatternMixin
│  ├─ cpu/                 CraftConfirmMenuMixin, CraftingCPUMenuMixin, CraftingCpuLogicMixin,
│  │                       CraftingServiceMixin, ExecutingCraftingJobCircuitMixin
│  ├─ emi/                 9 个（AbstractRecipeHandlerMixin, CraftingHelperMixin, EmiAeBaseScreenStackProviderMixin,
│  │                       EmiEncodePatternHandlerMixin, EmiItemStackConverterMixin, EmiScreenBaseMixin,
│  │                       EmiStackHelperCircuitMixin, EmiUseCraftingRecipeHandlerMixin,
│  │                       FillCraftingGridFromRecipePacketMixin）
│  ├─ energy/              ChestBlockEntityMixin, DriveBlockEntityMixin, EnergyOverlayGridMixin,
│  │                       InterfaceEnergyDistributorLogic, MEInventoryHandlerMixin,
│  │                       PatternProviderEnergyDistributorLogic, StorageBusPartMixin
│  ├─ menu/                AEBaseMenuMixin
│  ├─ misc/                7 个（BodyProviderAdapterMixin, ColorApplicatorItemMixin, IOBusPartMixin,
│  │                       PartPlacementMixin, PowerUnitsMixin, UpgradeInventoriesMixin,
│  │                       WirelessAccessPointBlockEntityMixin）
│  ├─ part/                ExportBusPartMixin, ImportBusPartMixin, StackTransferContextImplMixin,
│  │                       StorageExportStrategyMixin, StorageImportStrategyMixin
│  ├─ patternencodingpanel/ PatternEncodingTermMenuMixin, ProcessingEncodingPanelMixin, StyleManagerMixin
│  └─ patternprovider/     7 个（PatternContainerGroupMixin, PatternProviderLogicHostMixin,
│                          PatternProviderLogicMixin, PatternProviderMenuMixin, PatternProviderScreenMixin,
│                          PatternProviderTargetCacheMixin, SettingToggleButtonMixin）
├─ ae2ct/                  CraftingTreeScreenMixin, CraftingTreeWidgetAccessor
├─ ae2pw/                  PatternWorkStationMenuMixin
├─ aecs/                   CrystalSeedItemMixin, ResonatingPatternProviderLogicMixin
├─ betterP2P/              CommonProxyMixin（同文件内另有包级 ClientProxyMixin）
├─ datagen/                AECSDatagenMixin
├─ gtm/                    BlockPatternMixin
└─ omni/                   AEUniversalCellInventoryMixin, OCItemsMixin, OmniCraftingBlockEntityMixin
```

注册清单：单文件 `src/main/resources/ctnhenergy.mixins.json`，`mixins` 段 54 项（含内部类 `ae2.emi.AbstractRecipeHandlerMixin$PartiallyCraftableMixin`），`client` 段 6 项。

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| 样板署名注入时机 | `mixin/ae2/patternencodingpanel/PatternEncodingTermMenuMixin`（`encode` 的 HEAD / TAIL 两处注入） |
| 编码槽编码前状态跟踪 | 同上（`@Unique ctnhenergy$wasEmptyBeforeEncode`） |
| 编码统计 | 同上（仅有空白样板时调 `CEStats.awardEncodedPattern`）；另见 `mixin/ae2/cpu/CraftConfirmMenuMixin` 的 `ctnhenergy$awardMECraftRequest` |
| 样板编码面板 / 处理样板面板 | `mixin/ae2/patternencodingpanel/ProcessingEncodingPanelMixin`, `StyleManagerMixin` |
| 电路样板 | `mixin/ae2/circuit/PatternDetailsHelperMixin`, `ProcessingPatternMixin` |
| CPU / 合成逻辑 | `mixin/ae2/cpu/*`（含 `CraftingServiceMixin` 纳管 `QuantumComputerCluster` 虚拟 CPU） |
| CPU 自动翻倍 | `mixin/ae2/cpu/CraftingCpuLogicMixin`（实现 `IAutoMultiplyCPU`）, `mixin/omni/OmniCraftingBlockEntityMixin` |
| ME 设备能耗与 EU 分配 | `mixin/ae2/energy/*` |
| 样板提供者逻辑 / 界面 | `mixin/ae2/patternprovider/*` |
| 导入导出总线下发策略 | `mixin/ae2/part/StorageImportStrategyMixin`, `StorageExportStrategyMixin` |
| EMI 集成 | `mixin/ae2/emi/*` |
| 合成树 / 工作台 | `mixin/ae2ct/*`, `mixin/ae2pw/*` |
| AE2CS / datagen | `mixin/aecs/*`, `mixin/datagen/AECSDatagenMixin`（取消 AE2CS 自带 datagen） |
| GTM 样板匹配 | `mixin/gtm/BlockPatternMixin`（把 `QuantumComputerCasingBlock` 位置收进 `qcCasings` match context） |
| Omni 存储单元 | `mixin/omni/*` |
| BetterP2P EU 隧道 | `mixin/betterP2P/CommonProxyMixin`（注册 `EUP2PTunnelPart`） |

## CONVENTIONS
- 模块自有注入成员沿用 `ctnhenergy$` 或 `CE$` 前缀；纯新增的私有字段/方法加 `@Unique`，目标成员用 `@Shadow` 访问。
- 样板署名必须覆盖两条路径：槽位为空时消耗空白样板的全新编码，以及槽位已有样板被覆盖的“修改样板”。两条路径都调 `PatternAuthorData.addAuthorLore(stack, player.getScoreboardName())`。
- 只有消耗空白样板的全新编码才计入统计（`CEStats.awardEncodedPattern`），由 `ctnhenergy$wasEmptyBeforeEncode` 判定。
- 注入前先做空栈与 `PatternDetailsHelper.isEncodedPattern(stack)` 校验，非编码样板直接返回；客户端侧直接 return。
- 新增补丁类必须同步登记到 `src/main/resources/ctnhenergy.mixins.json` 的 `mixins` 或 `client` 段（客户端专属补丁放 `client` 段）。

## ANTI-PATTERNS
- 仅在“消耗空白样板”分支写署名，导致修改已有样板时署名停留在原作者或丢失。
- 直接向 Lore 追加署名行而不清理旧行，产生多条署名。
- 用 `ctnhenergy$` / `CE$` 之外的前缀命名自有注入成员，或未标 `@Shadow` 直接读写上游字段。
- 在 `mixin/` 中用 `ResourceLocation` 字符串反查注册对象，而非 `CEItems.*` / `CEBlocks.*` / `AEItems.*` 等静态对象。
- 新增 mixin 类但不更新 `ctnhenergy.mixins.json`，或把客户端专属补丁错放进 `mixins` 段。

## SCOPE
`modules/CTNH-Energy/src/main/java/tech/luckyblock/mcmod/ctnhenergy/mixin/` 下全部子包与 `src/main/resources/ctnhenergy.mixins.json`。

## READ WHEN
- 修改 AE2 样板编码 / 署名 / 处理样板面板行为
- 修改 AE2 CPU、合成逻辑、能耗或 EU 分配补丁
- 修改 AE2 附属（AE2CT / AE2PW / AE2CS / BetterP2P）或 Omni、GTM 补丁
- 新增任何 `@Mixin` 目标

## SOURCE OF TRUTH
`modules/CTNH-Energy/src/main/java/tech/luckyblock/mcmod/ctnhenergy/mixin/` 与 `src/main/resources/ctnhenergy.mixins.json`；上游行为以对应上游 mod 版本源码为准。署名与统计的权威实现仍在 `common/pattern/PatternAuthorData` 与 `common/stats/CEStats`，mixin 只负责调用时机。

## WORKFLOW
1. 确认能否用 `api/` 或事件替代；必须侵入时才写 Mixin。
2. 按上游包路径落到对应子包（`ae2/`, `ae2ct/`, `aecs/`, `omni/` …），并在 `ctnhenergy.mixins.json` 登记。
3. 业务逻辑委托给 `common/`（如署名 → `PatternAuthorData`），不在 mixin 内复制实现。
4. `:modules:CTNH-Energy:build` 编译；行为在游戏内验证。