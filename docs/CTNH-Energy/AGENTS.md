# CTNH-ENERGY MODULE

## OVERVIEW
CTNH-Energy adds AE2/energy integration, pattern buffer machinery, quantum computer systems, AE2 mixins, EMI/Jade integration, and generated resources under mod id `ctnhenergy` (172 Java files).

## STRUCTURE
```text
src/main/java/tech/luckyblock/mcmod/ctnhenergy/
|-- CTNHEnergy.java / CTNHEnergyGTAddon.java / CEConfig.java   # mod entry, GT addon, config
|-- api/                      # 8: CEPredicates, EUItemContext, IAutoMultiplyCPU, IGhostKeyTarget, IMaintainingContext, IPatternProviderLogic, IUpgradeableMenu
|-- client/                   # ClientProxy, EUKeyRenderHandler, Ponder (plugin/scenes/tags + 15 ae2 scenes)
|-- common/                   # CommonProxy, CESettings, AE2/EU logic (me/), machines, quantum computer
|   |-- me/                   # key/ (EUKey, EUKeyType, VoltageKey, VoltageKeyType), cell/ (EUCellInventory, EuCellHandler), parts/p2p/ (EUP2PTunnelPart), service/ (EnergyDistributeService, IEnergyDistributor), strategy/ (EUContainerItemStrategy + context/ CarriedContextEU, PlayerInvContextEU)
|   |-- machine/              # ITagFilter, MEPartMachine, energyhatch/ (3), gui/ (6 widgets), handler/ (3), iohatch/ (3), patternbuffer/ (MEPatternBuffer), utils/ (2)
|   |-- quantumcomputer/      # cpu/ (5), gui/ (4), machine/ (QuantumComputerMultiblockMachine), port/ (2)
|   |-- block/                # QuantumComputerCasingBlock
|   |-- item/                 # DynamoCardItem, EUCellItem, EUCellStats, IEUCell, MaintainingCardItem
|   |-- multi/                # PowerSubstationMachine
|   `-- pattern/              # DynamicProcessingPattern
|-- data/                     # CEDatagen, lang/ (ChineseLangHandler, EnglishLangHandler)
|-- event/                    # ForgeEventHandler, ForgeClientEventHandler
|-- integration/              # emi/ (CEEMIPlugin, EUEmiStack, EUEmiStackSerializer, EUStackConverter), jade/ (AEDeviceEUProvider, AdMEPatternBufferProvider, AdMEPatternBufferProxyProvider, CTNHEnergyJadePlugin), ldlib/ (CELDLibPlugin)
|-- mixin/                    # 49 files: ae2/ (8 subpackages), aecs/, betterP2P/, gtm/, omni/, datagen/
|-- network/                  # packets/QCOpenCPUMenuPacket, syncdata/AEKeyPayLoad
|-- registry/                 # 9: CERegistrate, CEItems, CEBlocks, CEMachines, CEMultiblock, CERecipeTypes, AEMenus, CENetWorking, CECreativeModeTabs
`-- utils/                    # 12: CEDrawHelper, CEUtil, MEConfigUtil, CEPatternProviderTarget, ProviderRecord, FakeSizedIntList, TempColorSprayBehaviour, button/ (BlitterButton, Blitters, CETextures, ToggleBlitterButton)
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Mod entry | `CTNHEnergy.java` |
| GT addon | `CTNHEnergyGTAddon.java` |
| Config/settings | `CEConfig.java`, `common/CESettings.java` |
| AE2/EU logic | `common/me/` (EUKey, VoltageKey, EU cells, EU container strategy, ME machine EU handler, EU P2P tunnel, energy distribution service) |
| Pattern buffer | `common/machine/patternbuffer/MEPatternBuffer.java` |
| AE2 machines/hatches | `common/machine/energyhatch/`, `common/machine/iohatch/`, `common/machine/handler/` |
| Quantum computer | `common/quantumcomputer/` (cpu/, gui/, machine/, port/) |
| Maintaining card | `common/item/MaintainingCardItem.java`, `api/IMaintainingContext.java` |
| Registries | `registry/` |
| EMI/Jade | `integration/` |
| Ponder/client | `client/ponder/` |
| Mixins | `mixin/`, `src/main/resources/ctnhenergy.mixins.json` |

## DOMAIN GUIDE ROUTING
Read the matching domain guide before editing the corresponding source area.

| Source area | Guide | Read before |
|-------------|-------|-------------|
| `api` | `docs/CTNH-Energy/api/AGENTS.md` | Shared API surfaces |
| `client` | `docs/CTNH-Energy/client/AGENTS.md` | Ponder plugin/scenes/tags, render |
| `common` | `docs/CTNH-Energy/common/AGENTS.md` | AE2/EU logic, machines, quantum computer, proxy |
| `data` | `docs/CTNH-Energy/data/AGENTS.md` | CEDatagen, lang |
| `event` | `docs/CTNH-Energy/event/AGENTS.md` | Forge event handlers |
| `integration` | `docs/CTNH-Energy/integration/AGENTS.md` | EMI, Jade, LDLib integration |
| `mixin` | `docs/CTNH-Energy/mixin/AGENTS.md` | AE2/AECS/Better P2P/GTM/Omni patches |
| `network` | `docs/CTNH-Energy/network/AGENTS.md` | Packets and sync data |
| `registry` | `docs/CTNH-Energy/registry/AGENTS.md` | Items, blocks, machines, recipe types |
| `utils` | `docs/CTNH-Energy/utils/AGENTS.md` | Shared helpers |

## CONVENTIONS
- Namespace is `tech.luckyblock.mcmod.ctnhenergy`; registry prefixes generally use `CE`.
- GT/GMT recipes are runtime dynamic-pack data (`CTNHEnergyGTAddon.addRecipes()`); `runData` produces no JSON for them. See root AGENTS.md CONVENTIONS.
- Item/block/fluid references MUST use direct registration objects (`CEItems.X`, `CEBlocks.X`, `AEItems.X`, `AEParts.X`, `GTMaterials.X`) — never `ResourceLocation` string parsing + `ForgeRegistries` lookups. See root AGENTS.md CONVENTIONS.
- AE2 mixins are central to behavior; inspect target class assumptions before changing signatures.
- `src/generated/resources` is produced by `:modules:CTNH-Energy:runData`.
- Ponder `CTNHEnergyPonderSceneBuilder` is a thin adapter around CTNH-Lib's shared builder; `AE2CablePonderHelper` stays in Energy because it depends on AE2 cable bus internals.
- `MaintainingCardItem` implements `IMaintainingContext` to track a stocking amount; lang keys are under `ctnhenergy.maintainingcarditem.*`.

## ANTI-PATTERNS
- Do not change AE2 mixins without checking both mixin JSON and the target AE2 behavior.
- Do not treat quantum computer/menu updates as server-only; UI progress sync is part of the module.
- Do not move `client/ponder/ae2/AE2CablePonderHelper.java` to CTNH-Lib; it is AE2-specific visualization code.
- Do not register EU key/cell behavior only in item code; AE2 key types, storage cell handler, container strategy, upgrades, and P2P attunement are separate CommonProxy hooks.

## COMMANDS
```text
./gradlew :modules:CTNH-Energy:build
./gradlew :modules:CTNH-Energy:runData
./gradlew :modules:CTNH-Energy:spotlessCheck
```

## SCOPE
Applies to `modules/CTNH-Energy` and its submodule repository. It is a reference guide loaded through the root routing table, not an additional source-tree instruction file.

## READ WHEN
- Adding or changing AE2/EU integration, pattern buffer, quantum computer, or Energy Ponder content.
- Changing Energy mixins or datagen providers.

## SOURCE OF TRUTH
- Registration/lifecycle: `CTNHEnergy.java`, `CTNHEnergyGTAddon.java`, `common/CommonProxy.java`.
- Forge metadata and mixins: `src/main/resources/META-INF/mods.toml` and `ctnhenergy.mixins.json`.
- Static generated data: providers plus `src/generated/resources`.

## WORKFLOW
1. Map the changed symbol to its domain and read that domain guide.
2. Check CommonProxy init hooks (AE key types, storage cell handler, container strategy, upgrades, P2P attunement) and GT addon hook order.
3. Run the narrowest Gradle task (`runData` for datagen, `build` for compilation).
4. Re-read the root routing table if the change introduces a new module boundary.