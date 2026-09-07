# CTNH-ASTRAL COMMON DOMAIN

## OVERVIEW
Shared bootstrap and implementation for Astral (20 Java files): CommonProxy, blocks, enchantments, entities, machines, and the oxygen/atmosphere environment system. Rocket dimension transfer is controller-independent since the rocket assembly refactor.

## STRUCTURE
```text
common/
|-- CommonProxy.java, CAFluidInteractions.java
|-- block/                     # AstralFlowerBlock, AstralGrass, AstralGrassBlock, AstralSaplingBlock, AstralTallGrassBlock, MarsSaplingBlock, SiliconBuddingBlock
|-- enchantment/               # VacuumSealEnchantment
|-- entity/                    # RocketContraptionEntity
|-- event/                     # RocketDimensionTravelHandler
|-- machine/
|   |-- multiblock/            # RocketAssemblyPlatformMachine
|   `-- simple/                # OxygenEnricherMachine
|-- oxygen/                    # AtmosphereType, OxygenAreaSource, OxygenEnvironment, OxygenEnvironmentService, OxygenMachineRules
`-- recipe/                    # OxygenCondition
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Common proxy | `common/CommonProxy.java` |
| Oxygen/atmosphere | `common/oxygen/` (OxygenEnvironmentService, OxygenEnvironment, OxygenAreaSource, OxygenMachineRules, AtmosphereType) |
| Rocket entities | `common/entity/RocketContraptionEntity.java`, `common/event/RocketDimensionTravelHandler.java` |
| Rocket transfer state/persistence | `common/entity/RocketContraptionEntity.java` (NBT state), `common/event/RocketDimensionTravelHandler.java` (RocketState capture/apply) |
| Machines | `common/machine/multiblock/RocketAssemblyPlatformMachine.java`, `common/machine/simple/OxygenEnricherMachine.java` |
| Blocks | `common/block/` (astral grass/sapling/flower, Mars sapling, silicon budding) |
| Recipes/conditions | `common/recipe/OxygenCondition.java` |

## CONVENTIONS
- `CommonProxy.registerMaterials()` also calls `CAMaterials.tagPrefixIgnore()`.
- `CommonProxy.commonSetup()` registers `CAOverworldRegion`, `CANetherRegion`, and overworld/nether surface rules (TerraBlender).
- `CommonProxy.gatherData()` bootstraps biome, configured/placed feature, dimension type, level stem, noise settings, structure, structure set, and density function registries.
- The oxygen system pairs with the OxygenEnricherMachine and the Ad Astra oxygen mixins.
- `RocketDimensionTravelHandler` captures rocket state as a `RocketState` record (thrust, fuel capacity, remaining fuel, assembled, launching, launch ticks, countdown ticks) before travel and applies it to the detached rocket after travel; `RocketAssemblyPlatformMachine` is not involved in this transfer path.
- `RocketContraptionEntity.create()` is controller-free (`(Level, Contraption, Vec3)`); detached rockets use `createDetached(level, contraption, persistenceAnchor, pivot)` and `getController()` returns `null`.
- `RocketContraptionEntity` persists rocket fields via `writeAdditional`/`readAdditional` (RocketAssembled, RocketLaunching, RocketLaunchTicks, RocketCountdownTicks, RocketLanding, RocketLandingPad, RocketThrust, RocketFuelCapacity, RocketRemainingFuel) and removes the legacy `CTNHAstralRocket` persistent-data key on read.
- `RocketAssemblyPlatformMachine` persists rocket state via LDLib `@Persisted` managed fields (`TAG_THRUST`, `TAG_FUEL_CAPACITY`, `TAG_REMAINING_FUEL`, `TAG_LAUNCHING`, `TAG_LAUNCH_TICKS` on `rocketThrust`, `rocketFuelCapacity`, `rocketRemainingFuel`, `launching`, `launchTicks`); value changes drive dirty/save automatically, no manual `markDirty()` needed. Legacy saves without `TAG_REMAINING_FUEL` default to full tank (`rocketRemainingFuel = rocketFuelCapacity`).
- `setPersistenceAnchor()` keeps `controllerPos` as an inert anchor for `SimpleRotatingContraptionEntity` compatibility without tying the rocket to a controller multiblock.

## TRAIT OWNERSHIP
`OxygenEnricherMachine` 内联 `OxygenEnricherRecipeLogic extends RecipeLogic`。约束以 `docs/_architecture/AGENTS.md` 为准，本域重点：

- 氧气/大气环境状态（`common/oxygen/`）的所有权归 service 与机器，不要在 trait 与机器间重复持有。
- 需要客户端读取的环境状态用 `@DescSynced` 承载，不要为 Jade/HUD 另开一条 NBT 通道。
- `RecipeLogic` 不做 capability 类型判断；配方内容解释归 recipe capability。

## ANTI-PATTERNS
- Do not bypass CommonProxy registration order.
- Do not reintroduce `RocketAssemblyPlatformMachine` controller calls in `RocketDimensionTravelHandler` for dimension transfer; use `RocketState` capture/apply.
- Do not store rocket transfer state under the legacy `CTNHAstralRocket` persistent-data key; entity NBT fields are authoritative.
- Do not call `markDirty()` for `RocketAssemblyPlatformMachine` `@Persisted` rocket fields; LDLib managed fields handle persistence automatically.

## SCOPE
Applies to `src/main/java/com/ctnh/ctnhastral/common`.

## READ WHEN
- Changing Astral bootstrap, structures, sounds, enchantments, rockets, or oxygen system registration.
- Changing rocket dimension-transfer state persistence or detached-contraption behavior.

## SOURCE OF TRUTH
- `common/CommonProxy.java` and `CTNHAstral.java`.
- Rocket transfer behavior: `common/event/RocketDimensionTravelHandler.java`, `common/entity/RocketContraptionEntity.java`.

## WORKFLOW
1. Check `CommonProxy` registration order before adding hooks.
2. For rocket transfer changes, trace `RocketDimensionTravelHandler` capture/apply and entity NBT read/write together.
3. Run `:modules:CTNH-Astral:build`.
