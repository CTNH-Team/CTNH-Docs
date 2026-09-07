# CTNH-BIO API DOMAIN

## OVERVIEW
Public API surfaces for Bio (61 Java files, the largest Bio domain): living-machine block/entity hierarchy, recipe capabilities, entity/model ingredients, property operators, nutrient serialization, and float multiplier handling.

## STRUCTURE
```text
api/
|-- CBValues.java, IHostAwareEntity.java, ILivingEntityHostBlock.java, ILivingMachine.java
|-- block/                       # LivingMetaMachineBlock, LivingMultiMetaMachineBlock
|-- blockentity/                 # LivingMetaMachineBlockEntity
|-- capability/                  # IEntityContainer.java
|   |-- forge/                   # CBCapabilities
|   `-- recipe/                  # CogniItemRecipeCapability, EntityRecipeCapability, ModelRecipeCapability, NutrientRecipeCapability
|-- entity/                      # LivingMetaMachineEntity (getMachine(), hurt() easter-egg)
|-- gui/                         # CBGuiTextures, CBRecipeTypeUI, LivingMachineUIWidget (left+right configurator panels)
|   `-- widget/                  # EntityWidget
|-- item/                        # LivingMetaMachineItem
|   |-- component/               # IOrganicFluidHandler, OrganicFluidHandlerItemStack(+Simple), OrganicFluidStats, StyleItem
|   `-- tool/                    # CBToolType
|-- machine/                     # BasicLivingMachine, BioCircuitFancyConfigurator
|   |-- multiblock/              # CBPartAbility, WorkableLivingMultiblockMachine
|   `-- trait/                   # NeuralModelContainer, NotifiableEntityContainer, NotifiableNutrientHandler
|-- pattern/                     # GrowingBlockPattern
`-- recipe/
    |-- CBRecipeModifiers.java, CBRecipeType.java
    |-- customlogic/             # BasicLivingLogic, DigestRecipeLogic
    |-- ingredient/
    |   |-- entity/              # ChancedEntityIngredient, EntityIngredient (copyWithMultiplier(float))
    |   |   `-- property/        # IBaseEntityProperty, I*EntityProperty interfaces, SimpleEntityPropertyFactory
    |   |       |-- data/        # EntityProperties, EntityPropertyDetector, EntityPropertyValue
    |   |       `-- utils/       # EntityPropertyBuilder
    |   `-- model/               # ModelIngredient
    |-- lookup/                  # EntityTagMapIngredient, EntityTypeMapIngredient
    `-- matcher/                 # PropertyOperator, PropertyOperators
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Living machine hierarchy | `api/block/`, `api/blockentity/`, `api/entity/`, `api/item/` |
| Living entity host | `api/entity/LivingMetaMachineEntity.java` — `getMachine()` helper, `hurt()` forwards `holder.onHostedEntityHurt()` and on `DamageTypes.PLAYER_ATTACK` randomly tweaks `BasicLivingMachine.getRecipeLogic()` progress (`+1000` 3%, `+20` 27%, `-20` 25%, `reset()` ~4%) |
| Recipe capabilities | `api/capability/recipe/` (Cogni/Entity/Model/Nutrient) |
| Entity/model ingredients | `api/recipe/ingredient/` (incl. `entity/property/` hierarchy and `data/EntityProperties`) |
| Property operators | `api/recipe/matcher/PropertyOperators.java` |
| Lookup ingredients | `api/recipe/lookup/` |
| Machine APIs | `api/machine/`, `api/machine/multiblock/`, `api/machine/trait/` |
| BasicLivingMachine Jade | `api/machine/BasicLivingMachine.java` — overrides `writeMachineJadeData()` / `appendMachineJadeTooltip()` (Health/MaxHealth via `HealthElement`, NutrientAmount/Capacity via `helper.progress()` + `BoxStyle`, StatusEffects list via `getEffectName()`) |
| Machine configurators | `api/machine/BasicLivingMachine.java#attachConfigurators` — `CircuitFancyConfigurator` with `CBGuiTextures.SLOT`, `BioCircuitFancyConfigurator` fallback, `attachAllowSameConfigurators(right)` |
| Capabilities | `api/capability/forge/CBCapabilities.java` |
| GUI | `api/gui/`, `api/gui/widget/` — `LivingMachineUIWidget` sets `BACKGROUND_BIO`, `SLOT`, `TITLE_BAR_BACKGROUND_BIO`, `TAB_LEFT_BIO` sub-textures and `configuratorPanel` + `rightConfiguratorPanel` to `BACKGROUND_SMALL` |

## CONVENTIONS
- `PropertyOperators` and `EntityProperties` are initialized explicitly in `CommonProxy.init()`; do not call them before that.
- `NotifiableNutrientHandler` is attached via `attachTrait(new NotifiableNutrientHandler(this, GTValues.V[tier] * 64))` and listens to `getRecipeLogic()::updateTickSubscription`.
- `attachConfigurators(left,right)` uses `getTraitOptional(ProgrammableCircuitSlotTrait.class)` → `CircuitFancyConfigurator(trait.getStorage()).setSlotBackground(CBGuiTextures.SLOT)` on left, `BioCircuitFancyConfigurator` fallback, power toggle via `CBGuiTextures.BUTTON_POWER`, and `attachAllowSameConfigurators(right)`.
- `LivingMachineUIWidget` now unconditionally configures `titleBar`, `sideTabsWidget` (TAB_LEFT_BIO sub-textures 0/0.5, 1/3f) and both `configuratorPanel` / `rightConfiguratorPanel`.
- Jade: `BasicLivingMachine.writeMachineJadeData` writes `MaxHealth`/`Health` (float), `NutrientAmount`/`NutrientCapacity` (double), `StatusEffects` (ListTag of `Name` json, `Duration`/`Infinite`, `Bad`); `appendMachineJadeTooltip` renders `HealthElement` and nutrient `helper.progress()` with `FormattingUtil.formatNumbers`.
- Nutrient KubeJS keys `NU_IN` / `NU_OUT` are exposed by `CTNHBioGTAddon.registerRecipeKeys()`.
- Entity property interfaces follow `I<Type>EntityProperty` naming (IBooleanEntityProperty, IIntEntityProperty, IStringEntityProperty, ...).
- Recipe capability multiplier methods are `copyWithMultiplier(content, float multiplier)` in `EntityRecipeCapability`, `ModelRecipeCapability`, and `NutrientRecipeCapability`; `EntityIngredient` / `ChancedEntityIngredient` also accept `float` and truncate multiplied integral fields back to `int`.
- NOTE: there is no `api/recipe/content/` subpackage; nutrient serialization lives under `api/capability/recipe/`.

## TRAIT OWNERSHIP
`api/machine/trait/` 的三个 trait 均为 `NotifiableRecipeHandlerTrait<T>` 子类：`NeuralModelContainer`（`ModelIngredient`）、`NotifiableEntityContainer`（`EntityIngredient`）、`NotifiableNutrientHandler`（`Float`）。另有机器内联 `RecipeLogic` 子类 `BasicLivingRecipeLogic`、`CogniAssemblerRecipeLogic`，以及 `ParabioticBridgeHandler extends NotifiableItemStackHandler`。

约束以 `docs/_architecture/AGENTS.md` 为准，本域重点：

- capability 四层分工：Forge capability 对外暴露、recipe capability 描述配方语义与并行/XEI 逻辑、trait 持有 handler 与机器侧状态、机器子类只放机器特有规则。生物 recipe capability 的匹配逻辑属 recipe capability 层，不要下沉进 trait。
- 需要同步或持久化的字段放 trait 并用 managed field 承载；`@DescSynced` 与 `@Persisted` 同用前确认两者都必要；装不下的走 `saveCustomPersistedData` / `loadCustomPersistedData`。
- 一份状态一个所有者：机器字段与 trait 字段禁止并存。

## ANTI-PATTERNS
- Do not bypass `PropertyOperators` / `EntityProperties` when adding entity-model recipe matching.
- Do not collapse biological recipe capabilities into Core; this module owns its living-machine abstractions.
- Do not bypass `CircuitFancyConfigurator` / `BioCircuitFancyConfigurator` slot background when wiring circuit configurators.

## SCOPE
Applies to `src/main/java/com/moguang/ctnhbio/api` and its child packages.

## READ WHEN
- Adding recipe capabilities, entity/model ingredients, or machine API surfaces.
- Changing `BasicLivingMachine` Jade/configurator logic or `LivingMetaMachineEntity` host interaction.

## SOURCE OF TRUTH
- `api/recipe/` contracts and `common/CommonProxy.java` init order.
- `api/machine/BasicLivingMachine.java` and `api/entity/LivingMetaMachineEntity.java` for current Jade/easter-egg behavior.

## WORKFLOW
1. Check `CommonProxy.init()` for PropertyOperators/EntityProperties initialization.
2. Confirm the surface is Bio-specific before adding to `api/`.
3. Run `:modules:CTNH-Bio:build`.
