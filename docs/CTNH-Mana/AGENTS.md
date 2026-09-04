# CTNH-MANA MODULE

## OVERVIEW
CTNH-Mana adds magic-themed CTNH content, Botania/Blood Magic style integrations, mana multiblocks, rituals, custom items, client radial UI, and generated resources under mod id `ctnhmana` (338 Java files, the second-largest module).

## STRUCTURE
```text
src/main/java/com/magicbee/ctnhmana/
|-- CTNHMana.java / CTNHManaGTAddon.java / CMConfig.java   # mod entry, GT addon, config
|-- api/                      # 32: effect/ (16), machine/gem/ (1), mixin/ (IBloodAltarLogic), networks/ (2), pattern/ (2), recipe/condition/ (4), recipe/customlogic/ (6)
|-- client/                   # 41: ZenithInvadeClient, radial menu (4), Ponder (7), models (8), renderers (17), particles
|-- common/                   # 128: CommonProxy, DigitalWosMachine, blocks (5), blockentities (13), capability, entities (5), events, items (28), machines (3), multiblocks (30), parts (8), rituals
|   |-- item/                 # bloodmagicjade/ bosssummoner/ (4) caduceus/ dungeon/ equipment/ (4) manafuelstick/ manamachineupgrade/ (9) rune/ (3) + ZenithDebugToolItem
|   |-- multiblock/           # 30: ManaReactor, HellForgeMachine, MysticSpire, ZenithMachine, EternalGarden, WishingWill, IndustrialSalvagingMachine, IndustrialGemInlayMachine, ...
|   |-- parts/                # CMPartsAbility, CentralControlBus, ExtendedCentralControlBus, ManaHatch, RedstoneSignalBroadcastHatch + ManaHatches/ (3)
|   |-- ritualtypes/          # 6: RitualBeeSummon, RitualBossSummon, RitualCharger, RitualDragonCloud, RitualLifeExtractor, RitualShroudSight
|   `-- ritual/               # MachineRitualSoulNetwork, MachineRitualStoneHost
|-- data/                     # 55: CMDatagen, ManaData, recipes (35 + builders), lang (3), materials, tags
|-- event/                    # 16: EventHandler, ForgeEventHandler, CMKeyBindings, ArmorBreakEventHandler, DamageClampHandler, IndexEventHandler, MagicalAntagonismEventHandler, MinerEliteHandler, MythicBossPool, PainShieldEventHandler, PhysicalAntagonismEventHandler, RealityDissociationEventHandler, SoulLeechEventHandler, TaintedBloodWeepingEyeEventHandler, ThirdEyeEventHandler, YurikoRingEventHandler
|-- integration/              # 8: emi/ (1), jade/ (7)
|-- mixin/                    # 18: ae2/ (2), ars/ (4), bloodmagic/ (4), botania/ (6), emi/ (1), minecraft/ (1)
|-- networking/packets/       # 7: CMNetworking, AntagonismPacket, CaduceusPacket, IndexFortunaPacket, IndexTargetBlockPacket, IndexTargetParticlePacket, ZenithInvadePacket
|-- registry/                 # 27: 19 root classes (CMRegistrate, ...) + items/ (1) + multiblock/ (5) + sounds/ (2)
`-- utils/                    # 3: CTNHManaUtils, EnvUtils, ModUtils
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Mod entry | `CTNHMana.java` |
| GT addon | `CTNHManaGTAddon.java` |
| Config | `CMConfig.java` |
| Pattern helpers | `api/pattern/` (CMBlockMaps, CMPredicates) |
| Multiblocks | `common/multiblock/` (30 machines) |
| Rituals | `common/ritualtypes/` (6), `common/ritual/` (2) |
| Magic items | `common/item/` (8 subpackages: caduceus/, equipment/, manamachineupgrade/, rune/, ...) |
| Registries | `registry/` (27) |
| Recipe builders | `data/recipe/builder/bloodmagic/`, `data/recipe/builder/botania/`, `data/recipe/builder/apotheosis/` |
| Networking | `networking/packets/` (7) |
| Client UI/Ponder | `client/` (radial menu, ponder/mana/ scenes) |
| Mixins/integrations | `mixin/` (18), `integration/emi/` (1), `integration/jade/` (7) |
| Zenith invasion | `common/event/zenith/`, `client/ZenithInvadeClient.java` |

## ARCHITECTURE CONTRACT
Machine/trait/capability/Jade 的所有权边界、字段同步与持久化规则、Jade 数据最小化原则和迁移步骤在 `docs/_architecture/AGENTS.md`。改动机器、trait、recipe capability 或 Jade 代码前先读它；本文件只描述本模块的落点。

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
| `mixin` | `docs/CTNH-Mana/mixin/AGENTS.md` | Ars/Blood Magic/Botania/AE2/EMI/Minecraft patches |
| `networking` | `docs/CTNH-Mana/networking/AGENTS.md` | Packets |
| `registry` | `docs/CTNH-Mana/registry/AGENTS.md` | Items, machines, multiblocks, recipe types |
| `utils` | `docs/CTNH-Mana/utils/AGENTS.md` | Shared helpers |

## CONVENTIONS
- Namespace is `com.magicbee.ctnhmana`; registry prefixes generally use `CM`.
- GT/GMT recipes are runtime dynamic-pack data (`CTNHManaGTAddon.addRecipes()`); `runData` produces no JSON for them. See root AGENTS.md CONVENTIONS.
- Item/block/fluid references MUST use direct registration objects (`CMItems.X`, `CMBlocks.X`, `CMMaterials.X`, `GTMaterials.X`, `TagPrefix.ingot`) — never `ResourceLocation` string parsing + `ForgeRegistries` lookups. See root AGENTS.md CONVENTIONS.
- Generated resources are large; use `:modules:CTNH-Mana:runData` after datagen or Ponder text changes.
- Ponder `CTNHManaPonderSceneBuilder` is a thin adapter around CTNH-Lib's shared builder; keep Mana-specific scenes/tags/plugins in CTNH-Mana, not Core or Lib.
- Blood Magic/Botania/Ars/Apotheosis/EMI compatibility is spread across recipe builders, mixins, integrations, and client packets; check all four before changing a magic integration surface. Apotheosis support lives in `data/recipe/builder/apotheosis/`, not in `mixin/`.

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