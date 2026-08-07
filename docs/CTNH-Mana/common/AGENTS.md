# CTNH-MANA COMMON DOMAIN

## OVERVIEW
Shared implementation for Mana (104 Java files, the largest Mana domain): CommonProxy, rituals, items, machines, multiblocks, block entities, events, and recipe builders for Blood Magic/Botania.

## STRUCTURE
```text
common/
|-- CommonProxy.java, DigitalWosMachine.java
|-- blockentity/
|   |-- flower/                # 7: AnattaLotusBlockEntity, BlackVeinMarigoldBlockEntity, BloodAntiarisBlockEntity, DemonFlytrapBlockEntity, GenethistleBlockEntity, ParaRosiaBlockEntity, TulpenmanieBlockEntity
|   `-- machine/               # 5: FlowerCakeBlockEntity, ManaMachineBlockEntity, IZenithMartixBlockEntity, MysticSpireBlockEntity, ZenithEyeBlockEntity
|-- blocks/                    # CoilType, FrameBlock, ManaIndicatorLight, RuneBlock
|-- entity/                    # DeltaSpark, OmegaSpark
|-- event/zenith/              # 5: ZenithGlitchText, ZenithInvadeEffects, ZenithInvadeEvent, ZenithInvadeManager, ZenithInvadeMessages
|-- gui/                       # 7: AnimationTextureY, ArcButtonWidget, BaseManaMachineGui, ExtendedCentralControlBusCircuitUi, ManaStatusGui, SelectableCircuitSlotWidget, ShroudUi
|-- item/
|   |-- FlowerCakeItem.java, TooltipsBlockItem.java, ZenithDebugToolItem.java
|   |-- bloodmagicjade/        # JadeItem
|   |-- bosssummoner/          # BossSummonerBehavior, IThrowableItem, ThrowItem, ThrowableSummoner
|   |-- caduceus/              # CaduceusItem, MultiToolDefinition
|   |-- equipment/             # KoishiEyeItem, SaberWandItem, TaintedBloodWeepingEye, YurikoRingItem
|   |-- manafuelstick/         # IManaFuelStick
|   |-- manamachineupgrade/    # 8 upgrade items
|   `-- rune/                  # IRuneItem, RuneElementType, SpireUpgradeRuneItem
|-- machine/                   # FlowerCakeBlock, FlowerCakeMachine
|-- multiblock/                # 29 machines: ManaReactor, HellForgeMachine, MysticSpire, ZenithMachine, ZenithMatrixMachine, EternalGarden, EternalWosMachine, WishingWill, ManaCondenserMachine, ManaFuelInfuserMachine, TwistedFusionMachine, IndustrialAltarMachine, MeteorCaptureMachine, DemonWillMachine, QuasarEye, NicollDysonBeams, ArcaneHighEnergyCompressionReactorCore, IndustrialSalvagingMachine, ...
|-- parts/                     # CMPartsAbility, CentralControlBus, ExtendedCentralControlBus, ManaHatch, RedstoneSignalBroadcastHatch
|   `-- ManaHatches/           # BloodManaHatch, CreativeManaHatch, SparkManaHatch
|-- ritual/                    # MachineRitualSoulNetwork, MachineRitualStoneHost
`-- ritualtypes/               # 5: RitualBossSummon, RitualCharger, RitualDragonCloud, RitualLifeExtractor, RitualShroudSight
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Common proxy | `common/CommonProxy.java` |
| Rituals | `common/ritualtypes/` (5), `common/ritual/` (2) |
| Items | `common/item/` (8 subpackages: caduceus/, equipment/, manamachineupgrade/, rune/, bosssummoner/, ...) |
| Multiblocks | `common/multiblock/` (29) |
| Parts | `common/parts/`, `common/parts/ManaHatches/` |
| Machines | `common/machine/` (FlowerCake) |
| Block entities | `common/blockentity/flower/` (7), `common/blockentity/machine/` (5) |
| GUI | `common/gui/` (7) |
| Zenith invasion | `common/event/zenith/` (5) |
| Blood Magic recipe builders | `data/recipe/builder/bloodmagic/` (see data domain) |
| Botania recipe builders | `data/recipe/builder/botania/` (see data domain) |

## CONVENTIONS
- Blood Magic/Botania recipe JSON generation is wrapped in `data/recipe/builder/` classes (not under `common/recipe/`; there is no `common/recipe` directory).
- Load-complete hook: `CTNHMana.onFMLoadComplete()` registers the Blood Magic altar component for `CASING_BLOODLOGIC`.
- Multiblock directory is spelled `multiblock` (no legacy `Mutiblock` spelling exists).

## ANTI-PATTERNS
- Do not change magic integration surfaces without checking recipe builders, mixins, integrations, and client packets together.

## SCOPE
Applies to `src/main/java/com/moguang/ctnhmana/common` and its child packages.

## READ WHEN
- Implementing rituals, magic items, machines, or multiblocks in Mana.

## SOURCE OF TRUTH
- `common/` classes and `event/EventHandler.java` registration wiring.

## WORKFLOW
1. Check EventHandler registration order before adding behavior.
2. Verify recipe builder targets for Blood Magic/Botania.
3. Run `:modules:CTNH-Mana:build`.