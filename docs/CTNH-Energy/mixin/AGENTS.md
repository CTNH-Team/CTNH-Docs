# CTNH-ENERGY MIXIN DOMAIN

## OVERVIEW
AE2, AE2CS/AECS, Better P2P, GTM, Omni Cells, and ME Requester integration mixins (59 Java files, the largest Energy domain). These are central to Energy behavior.

## STRUCTURE
```text
mixin/
|-- ae2/                       # CableBusContainerMixin, SettingsMixin
|   |-- cpu/                   # CraftingCPUMenuMixin, CraftingCpuLogicMixin, CraftingServiceMixin, ExecutingCraftingJobCircuitMixin
|   |-- emi/                   # 9 mixins: AbstractRecipeHandlerMixin, CraftingHelperMixin, EmiAeBaseScreenStackProviderMixin, EmiEncodePatternHandlerMixin, EmiItemStackConverterMixin, EmiScreenBaseMixin, EmiStackHelperCircuitMixin, EmiUseCraftingRecipeHandlerMixin, FillCraftingGridFromRecipePacketMixin
|   |-- energy/                # 7: ChestBlockEntityMixin, DriveBlockEntityMixin, EnergyOverlayGridMixin, InterfaceEnergyDistributorLogic, MEInventoryHandlerMixin, PatternProviderEnergyDistributorLogic, StorageBusPartMixin
|   |-- menu/                  # AEBaseMenuMixin
|   |-- misc/                  # 7: BodyProviderAdapterMixin, ColorApplicatorItemMixin, IOBusPartMixin, PartPlacementMixin, PowerUnitsMixin, UpgradeInventoriesMixin, WirelessAccessPointBlockEntityMixin
|   |-- patternencodingpanel/  # ProcessingEncodingPanelMixin, StyleManagerMixin
|   `-- patternprovider/       # 7: PatternContainerGroupMixin, PatternProviderLogicHostMixin, PatternProviderLogicMixin, PatternProviderMenuMixin, PatternProviderScreenMixin, PatternProviderTargetCacheMixin, SettingToggleButtonMixin
|-- ae2ct/                     # CraftingTreeScreenMixin, CraftingTreeWidgetAccessor
|-- aecs/                      # CrystalSeedItemMixin, ResonatingPatternProviderLogicMixin
|-- betterP2P/                 # CommonProxyMixin
|-- datagen/                   # AECSDatagenMixin
|-- gtm/                       # BlockPatternMixin
|-- omni/                      # AEUniversalCellInventoryMixin, OCItemsMixin, OmniCraftingBlockEntityMixin
`-- pcc/                       # (removed in current source)
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| AE2 patches | `mixin/ae2/` + 9 subpackages (circuit/cpu/emi/energy/menu/misc/part/patternencodingpanel/patternprovider) |
| AE2CS/AECS patches | `mixin/aecs/` |
| Better P2P | `mixin/betterP2P/` |
| GTM patches | `mixin/gtm/` |
| Omni Cells | `mixin/omni/` |
| Datagen mixins | `mixin/datagen/` |
| Mixin config | `src/main/resources/ctnhenergy.mixins.json` |

## CONVENTIONS
- AE2 mixins are central to behavior; inspect target class assumptions before changing signatures.
- Keep mixin JSON and package entries synchronized.

## ANTI-PATTERNS
- Do not change AE2 mixins without checking both mixin JSON and the target AE2 behavior.

## SCOPE
Applies to `src/main/java/tech/luckyblock/mcmod/ctnhenergy/mixin` and `src/main/resources/ctnhenergy.mixins.json`.

## READ WHEN
- Patching AE2, AECS, Better P2P, GTM, Omni Cells, or ME Requester behavior.

## SOURCE OF TRUTH
- `src/main/resources/ctnhenergy.mixins.json` and the mixin classes in `mixin/`.

## WORKFLOW
1. Locate the integration's mixin package and JSON entry.
2. Verify the target member against the loaded mod version.
3. Run `:modules:CTNH-Energy:build`; validate at runtime.