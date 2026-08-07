# CTNH-MANA MODULE

## OVERVIEW
CTNH-Mana adds magic-themed CTNH content, Botania/Blood Magic style integrations, mana multiblocks, rituals, custom items, client radial UI, and generated resources under mod id `ctnhmana` (271 Java files, the second-largest module).

## STRUCTURE
```text
src/main/java/com/moguang/ctnhmana/
|-- CTNHMana.java / CTNHManaGTAddon.java / CMConfig.java   # mod entry, GT addon, config
|-- api/                      # 18: effect/ (8), mixin/ (IBloodAltarLogic), networks/ (2), pattern/ (2), recipe/condition/ (4), recipe/customlogic/ (1)
|-- client/                   # 33: ZenithInvadeClient, radial menu, Ponder, models, renderers (11), particles
|-- common/                   # 104: CommonProxy, DigitalWosMachine, blocks, blockentities, entities, events, items, machines, multiblocks (29), parts, rituals
|   |-- item/                 # bloodmagicjade/ bosssummoner/ caduceus/ equipment/ manafuelstick/ manamachineupgrade/ (8) rune/ (3) + ZenithDebugToolItem
|   |-- multiblock/           # 29: ManaReactor, HellForgeMachine, MysticSpire, ZenithMachine, EternalGarden, WishingWill, IndustrialSalvagingMachine, ...
|   |-- parts/                # CMPartsAbility, CentralControlBus, ExtendedCentralControlBus, ManaHatch, RedstoneSignalBroadcastHatch + ManaHatches/ (3)
|   |-- ritualtypes/          # 5: RitualBossSummon, RitualCharger, RitualDragonCloud, RitualLifeExtractor, RitualShroudSight
|   `-- ritual/               # MachineRitualSoulNetwork, MachineRitualStoneHost
|-- data/                     # 50: CMDatagen, ManaData, recipes (31 + builders), lang (3), materials, tags
|-- event/                    # 8: EventHandler, ForgeEventHandler, CMKeyBindings, IndexEventHandler, SoulLeechEventHandler, TaintedBloodWeepingEyeEventHandler, ThirdEyeEventHandler, YurikoRingEventHandler
|-- integration/              # 6: emi/ (1), jade/ (5)
|-- mixin/                    # 15: ae2/ (2), ars/ (4), bloodmagic/ (2), botania/ (6), emi/ (1)
|-- networking/               # 6: CMNetworking, CaduceusPacket, IndexFortunaPacket, IndexTargetBlockPacket, IndexTargetParticlePacket, ZenithInvadePacket
|-- registry/                 # 27: CMRegistrate + items/ (1) + multiblock/ (5) + sounds/ (2)
`-- utils/                    # 3: CTNHManaUtils, EnvUtils, ModUtils
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Mod entry | `CTNHMana.java` |
| GT addon | `CTNHManaGTAddon.java` |
| Config | `CMConfig.java` |
| Pattern helpers | `api/pattern/` (CMBlockMaps, CMPredicates) |
| Multiblocks | `common/multiblock/` (29 machines) |
| Rituals | `common/ritualtypes/` (5), `common/ritual/` (2) |
| Magic items | `common/item/` (8 subpackages: caduceus/, equipment/, manamachineupgrade/, rune/, ...) |
| Registries | `registry/` (27) |
| Recipe builders | `data/recipe/builder/bloodmagic/`, `data/recipe/builder/botania/`, `data/recipe/builder/apotheosis/` |
| Networking | `networking/packets/` (6) |
| Client UI/Ponder | `client/` (radial menu, ponder/mana/ scenes) |
| Mixins/integrations | `mixin/`, `integration/emi/`, `integration/jade/` |
| Zenith invasion | `common/event/zenith/`, `client/ZenithInvadeClient.java` |

## DOMAIN GUIDE ROUTING
Read the matching domain guide before editing the corresponding source area.

| Source area | Guide | Read before |
|-------------|-------|-------------|
| `api` | `docs/CTNH-Mana/api/AGENTS.md` | Pattern helpers, effects, recipe/network APIs |
| `client` | `docs/CTNH-Mana/client/AGENTS.md` | Caduceus radial menu, Ponder plugin/scenes/tags, ZenithInvadeClient |
| `common` | `docs/CTNH-Mana/common/AGENTS.md` | Proxy, rituals, items, machines, multiblocks, recipe builders |
| `data` | `docs/CTNH-Mana/data/AGENTS.md` | Recipe generators, lang, materials, tags |
| `event` | `docs/CTNH-Mana/event/AGENTS.md` | EventHandler wiring |
| `integration` | `docs/CTNH-Mana/integration/AGENTS.md` | EMI, Jade integration |
| `mixin` | `docs/CTNH-Mana/mixin/AGENTS.md` | Ars/Blood Magic/Botania/EMI patches |
| `networking` | `docs/CTNH-Mana/networking/AGENTS.md` | Packets |
| `registry` | `docs/CTNH-Mana/registry/AGENTS.md` | Items, machines, multiblocks, recipe types |
| `utils` | `docs/CTNH-Mana/utils/AGENTS.md` | Shared helpers |

## CONVENTIONS
- Namespace is `com.moguang.ctnhmana`; registry prefixes generally use `CM`.
- GT/GMT recipes are runtime dynamic-pack data (`CTNHManaGTAddon.addRecipes()`); `runData` produces no JSON for them. See root AGENTS.md CONVENTIONS.
- Item/block/fluid references MUST use direct registration objects (`CMItems.X`, `CMBlocks.X`, `CMMaterials.X`, `GTMaterials.X`, `TagPrefix.ingot`) — never `ResourceLocation` string parsing + `ForgeRegistries` lookups. See root AGENTS.md CONVENTIONS.
- Generated resources are large; use `:modules:CTNH-Mana:runData` after datagen or Ponder text changes.
- Ponder `CTNHManaPonderSceneBuilder` is a thin adapter around CTNH-Lib's shared builder; keep Mana-specific scenes/tags/plugins in CTNH-Mana, not Core or Lib.
- Blood Magic/Botania/Ars/EMI compatibility is spread across recipe builders, mixins, integrations, and client packets; check all four before changing a magic integration surface.

## ANTI-PATTERNS
- Do not assume magic integrations are isolated from GTCEu; machine/recipe registration still flows through GT addon patterns.
- Do not change Caduceus/Saber client behavior without checking both networking packets and item property model predicates.

## COMMANDS
```text
./gradlew :modules:CTNH-Mana:build
./gradlew :modules:CTNH-Mana:runData
./gradlew :modules:CTNH-Mana:spotlessCheck
```

## SCOPE
Applies to `modules/CTNH-Mana` and its submodule repository. It is a reference guide loaded through the root routing table, not an additional source-tree instruction file.

## READ WHEN
- Adding or changing magic content, rituals, mana multiblocks, or Botania/Blood Magic integration.
- Changing Mana datagen providers or Ponder scenes.

## SOURCE OF TRUTH
- Registration/lifecycle: `CTNHMana.java`, `CTNHManaGTAddon.java`, `event/EventHandler.java`.
- Forge metadata and mixins: `src/main/resources/META-INF/mods.toml` and `ctnhmana.mixins.json`.
- Static generated data: providers plus `src/generated/resources`.

## WORKFLOW
1. Map the changed symbol to its domain and read that domain guide.
2. Check GT addon hook order, EventHandler wiring, and networking packets.
3. Run the narrowest Gradle task (`runData` for datagen, `build` for compilation).
4. Re-read the root routing table if the change introduces a new module boundary.