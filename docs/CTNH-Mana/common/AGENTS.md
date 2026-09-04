# CTNH-MANA COMMON DOMAIN

## OVERVIEW
Shared implementation for Mana (123 Java files, the largest Mana domain): CommonProxy, rituals, items, machines, multiblocks, block entities, events, and trait-backed mana handling.

## STRUCTURE
```text
common/
|-- CommonProxy.java, DigitalWosMachine.java
|-- blockentity/
|   |-- flower/                # 7: AnattaLotusBlockEntity, BlackVeinMarigoldBlockEntity, BloodAntiarisBlockEntity, DemonFlytrapBlockEntity, GenethistleBlockEntity, ParaRosiaBlockEntity, TulpenmanieBlockEntity
|   |-- WitherAconiteTrapBlockEntity.java
|   `-- machine/               # 1: FlowerCakeBlockEntity (GeoBlockEntity shell -> FlowerCakeMachine#getManaTrait)
|-- blocks/                    # 5: CoilType, FrameBlock, ManaIndicatorLight, RuneBlock, WitherAconiteTrapBlock
|-- capability/                # DamageClampCapability
|-- entity/                    # 5: AbstractRampageBee, DeltaSpark, GiantBee, OmegaSpark, RoyalServantBee
|   |-- ai/                    # 8: GiantBee*Goal, RoyalServant*Goal
|   |-- navigation/            # RampageFlyingPathNavigation, RampageNodeEvaluator
|   `-- projectile/            # BeeNukeProjectile, MaliciousThermalilyProjectile, WitherAconiteProjectile
|-- event/zenith/              # 5: ZenithGlitchText, ZenithInvadeEffects, ZenithInvadeEvent, ZenithInvadeManager, ZenithInvadeMessages
|-- gui/                       # 7: AnimationTextureY, ArcButtonWidget, BaseManaMachineGui, ExtendedCentralControlBusCircuitUi, ManaStatusGui, SelectableCircuitSlotWidget, ShroudUi
|-- item/
|   |-- FlowerCakeItem.java, TooltipsBlockItem.java, ZenithDebugToolItem.java
|   |-- bloodmagicjade/        # JadeItem
|   |-- bosssummoner/          # BossSummonerBehavior, IThrowableItem, ThrowItem, ThrowableSummoner
|   |-- caduceus/              # CaduceusItem, MultiToolDefinition
|   |-- dungeon/               # PerfectMineKeyItem
|   |-- equipment/             # KoishiEyeItem, SaberWandItem, TaintedBloodWeepingEye, YurikoRingItem
|   |-- manafuelstick/         # IManaFuelStick
|   |-- manamachineupgrade/    # 9 upgrade items
|   `-- rune/                  # IRuneItem, RuneElementType, SpireUpgradeRuneItem
|-- machine/                   # FlowerCakeBlock, FlowerCakeMachine, GemSublimatorMachine
|-- multiblock/                # 31 classes: ManaReactor, HellForgeMachine, MysticSpire, ZenithMachine, ZenithMatrixMachine, EternalGarden, EternalWosMachine, WishingWill, ManaCondenserMachine, ManaFuelInfuserMachine, TwistedFusionMachine, IndustrialAltarMachine, MeteorCaptureMachine, DemonWillMachine, QuasarEye, NicollDysonBeams, ArcaneHighEnergyCompressionReactorCore, IndustrialSalvagingMachine, IndustrialGemInlayMachine, ...
|-- parts/                     # CMPartsAbility, CentralControlBus, ExtendedCentralControlBus, ManaHatch, RedstoneSignalBroadcastHatch
|   `-- ManaHatches/           # BloodManaHatch, CreativeManaHatch, SparkManaHatch
|-- ritual/                    # MachineRitualSoulNetwork, MachineRitualStoneHost
`-- ritualtypes/               # 6: RitualBeeSummon, RitualBossSummon, RitualCharger, RitualDragonCloud, RitualLifeExtractor, RitualShroudSight
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Common proxy | `common/CommonProxy.java` (no Jade registration; Jade moved to `integration/jade/CTNHManaJadePlugin`) |
| Rituals | `common/ritualtypes/` (6), `common/ritual/` (2) |
| Items | `common/item/` (8 subpackages: caduceus/, equipment/, manamachineupgrade/, rune/, bosssummoner/, ...) |
| Multiblocks | `common/multiblock/` (31) |
| Mystic Spire | `common/multiblock/MysticSpire.java` + `SpireMath.java`/`SpireBigMath.java` + `api/machine/trait/MysticSpireManaTrait.java` |
| Industrial gem inlay machine | `common/multiblock/IndustrialGemInlayMachine.java` |
| Parts | `common/parts/`, `common/parts/ManaHatches/` |
| Extended bus | `common/parts/ExtendedCentralControlBus.java` + `api/machine/trait/ExtendedControlBusCircuitTrait.java` |
| Machines | `common/machine/` (FlowerCakeMachine owns BTManaContainerTrait; FlowerCakeBlock delegates) |
| Block entities | `common/blockentity/flower/` (7), `common/blockentity/machine/FlowerCakeBlockEntity.java` |
| GUI | `common/gui/` (7) |
| Zenith invasion | `common/event/zenith/` (5) |
| Blood Magic recipe builders | `data/recipe/builder/bloodmagic/` (see data domain) |
| Botania recipe builders | `data/recipe/builder/botania/` (see data domain) |

## CONVENTIONS
- Blood Magic/Botania recipe JSON generation is wrapped in `data/recipe/builder/` classes (not under `common/recipe/`; there is no `common/recipe` directory).
- Mana storage is trait-owned: `FlowerCakeMachine`/`ManaMultiBlockMachine` holds `BTManaContainerTrait` (implements `ManaReceiver`); `MysticSpire` holds `MysticSpireManaTrait` (BigInteger true mana). `FlowerCakeBlockEntity` is a `GeoBlockEntity` shell only, exposing `getManaTrait()` from `getMetaMachine()`. Deleted: `ManaMachineBlockEntity`, `MysticSpireBlockEntity`, `IZenithMartixBlockEntity`.
- `InfusionCellCastingCondition` tests `ManaMultiBlockMachine` (not former `ManaMachine`).
- Load-complete hook: `CTNHMana.onFMLoadComplete()` registers the Blood Magic altar component for `CASING_BLOODLOGIC`.
- Multiblock directory is spelled `multiblock` (no legacy `Mutiblock` spelling exists).
- GT/GMT recipes are runtime dynamic-pack data via `CTNHManaGTAddon.addRecipes()`; `runData` produces no JSON for them. Item/block/fluid refs MUST use `CMItems.X`/`CMBlocks.X` etc., never string `ResourceLocation` lookup.

## ANTI-PATTERNS
- Do not change magic integration surfaces without checking recipe builders, mixins, integrations, and client packets together.
- Do not reintroduce mana fields on BlockEntity or duplicate trait state.

## SCOPE
Applies to `src/main/java/com/magicbee/ctnhmana/common` and its child packages.

## READ WHEN
- Implementing rituals, magic items, machines, or multiblocks in Mana.

## SOURCE OF TRUTH
- `common/` classes and `event/EventHandler.java` registration wiring.
- Trait sources `api/machine/trait/BTManaContainerTrait.java` and `MysticSpireManaTrait.java`.

## WORKFLOW
1. Check EventHandler registration order before adding behavior.
2. Verify recipe builder targets for Blood Magic/Botania.
3. Run `:modules:CTNH-Mana:build`.
