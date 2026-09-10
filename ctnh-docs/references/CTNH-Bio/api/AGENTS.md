# CTNH-BIO API DOMAIN

## OVERVIEW
Bio 的公开 API 面（61 个 Java 文件，本模块最大域）：活体机器 block / blockentity / entity / item 层级、recipe capability、实体与模型原料、属性算子、营养序列化与浮点乘法处理。

## STRUCTURE
```
api/
├─ CBValues.java, IHostAwareEntity.java, ILivingEntityHostBlock.java, ILivingMachine.java
├─ block/                       # LivingMetaMachineBlock, LivingMultiMetaMachineBlock
├─ blockentity/                 # LivingMetaMachineBlockEntity
├─ capability/                  # IEntityContainer
│  ├─ forge/                    # CBCapabilities（ENTITY_CONTAINER）
│  └─ recipe/                   # CogniItemRecipeCapability, EntityRecipeCapability,
│                               #   ModelRecipeCapability, NutrientRecipeCapability
├─ entity/                      # LivingMetaMachineEntity
├─ gui/                         # CBGuiTextures, CBRecipeTypeUI, LivingMachineUIWidget
│  └─ widget/                   # EntityWidget
├─ item/                        # LivingMetaMachineItem
│  ├─ component/                # IOrganicFluidHandler, OrganicFluidHandlerItemStack(+Simple),
│  │                            #   OrganicFluidStats, StyleItem
│  └─ tool/                     # CBToolType
├─ machine/                     # BasicLivingMachine, BioCircuitFancyConfigurator
│  ├─ multiblock/               # CBPartAbility, WorkableLivingMultiblockMachine
│  └─ trait/                    # NeuralModelContainer, NotifiableEntityContainer, NotifiableNutrientHandler
├─ pattern/                     # GrowingBlockPattern
└─ recipe/
   ├─ CBRecipeModifiers.java, CBRecipeType.java
   ├─ customlogic/              # BasicLivingLogic, DigestRecipeLogic
   ├─ ingredient/
   │  ├─ entity/                # ChancedEntityIngredient, EntityIngredient
   │  │  ├─ property/           # IBaseEntityProperty, IAutoGetValueEntityProperty,
   │  │  │                      #   I*EntityProperty, SimpleEntityPropertyFactory
   │  │  │  └─ data/            # EntityProperties, EntityPropertyDetector, EntityPropertyValue
   │  │  └─ utils/              # EntityPropertyBuilder
   │  └─ model/                 # ModelIngredient
   ├─ lookup/                   # EntityTagMapIngredient, EntityTypeMapIngredient
   └─ matcher/                  # PropertyOperator, PropertyOperators
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| 活体机器层级 | `api/block/`, `api/blockentity/`, `api/entity/`, `api/item/` |
| 宿主实体交互 | `api/entity/LivingMetaMachineEntity.java` — `getMachine()`；`hurt()` 转发 `holder.onHostedEntityHurt()`，并在 `DamageTypes.PLAYER_ATTACK` 时随机改动 `BasicLivingMachine.getRecipeLogic()` 进度（`+1000` 3%、`+20` 27%、`-20` 25%、`reset()` 4%，仅当 `getLastRecipe() != null`） |
| recipe capability | `api/capability/recipe/`（Cogni / Entity / Model / Nutrient） |
| 实体 / 模型原料 | `api/recipe/ingredient/`（含 `entity/property/` 层级与 `property/data/EntityProperties`） |
| 属性算子 | `api/recipe/matcher/PropertyOperators.java` |
| 查找型原料 | `api/recipe/lookup/` |
| 机器 API | `api/machine/`, `api/machine/multiblock/`, `api/machine/trait/` |
| 机器 Jade 数据 | `api/machine/BasicLivingMachine.java` — 覆写 `writeMachineJadeData()` / `appendMachineJadeTooltip()` |
| 机器配置器 | `api/machine/BasicLivingMachine.java#attachConfigurators` |
| Forge capability | `api/capability/forge/CBCapabilities.java` |
| GUI | `api/gui/`, `api/gui/widget/` — `LivingMachineUIWidget` 设置 `BACKGROUND_BIO`, `SLOT`, `TITLE_BAR_BACKGROUND_BIO`, `TAB_LEFT_BIO` 与 `configuratorPanel` / `rightConfiguratorPanel` 的 `BACKGROUND_SMALL` |
| 生长图案 | `api/pattern/GrowingBlockPattern.java` |

## CONVENTIONS
- `PropertyOperators` 与 `EntityProperties` 在 `CommonProxy.init()` 中显式初始化；在此之前不得调用。
- `NotifiableNutrientHandler` 在构造期挂载：`BasicLivingMachine` 用 `attachTrait(new NotifiableNutrientHandler(this, GTValues.V[tier] * 64))`，`WorkableLivingMultiblockMachine` 用 `attachTrait(new NotifiableNutrientHandler(this, capacity))` 并以 `addChangedListener(getRecipeLogic()::updateTickSubscription)` 订阅；不要在机器字段里另存营养值。
- `attachConfigurators(left, right)`：`getTraitOptional(ProgrammableCircuitSlotTrait.class)` → `new CircuitFancyConfigurator(trait.getStorage()).setSlotBackground(CBGuiTextures.SLOT)`；电源开关用 `CBGuiTextures.BUTTON_POWER` 的上下半子纹理；有 Cover 的朝向逐个附到 left；末尾 `attachAllowSameConfigurators(right)`（GT `IAllowSameUIProvider` 默认方法）。`BioCircuitFancyConfigurator` 是 `CircuitFancyConfigurator` 子类，当前模块内无调用点。
- `LivingMachineUIWidget` 构造期无条件配置 `titleBar`（`TITLE_BAR_BACKGROUND_BIO`）、`playerInventory` 槽位背景（`SLOT`）、`sideTabsWidget`（`TAB_LEFT_BIO` 子纹理：普通 `(0, 1/3f, 0.5f, 1/3f)`，悬停/按下 `(0.5f, 1/3f, 0.5f, 1/3f)`）以及 `configuratorPanel` / `rightConfiguratorPanel`（`BACKGROUND_SMALL`）。
- Jade：`BasicLivingMachine.writeMachineJadeData` 写 `MaxHealth`/`Health`（float）、`NutrientAmount`/`NutrientCapacity`（double）、`StatusEffects`（ListTag，元素为 `Name` JSON、`Duration` 或 `Infinite`、`Bad`）；`appendMachineJadeTooltip` 用 `HealthElement` 渲染生命、用营养 `helper.progress()`（`ctnhbio.jade.nutrient_stored` + `FormattingUtil.formatNumbers`）渲染营养条、用 `jade.potion` 行汇总状态效果。只写客户端推导不出的数据。
- 实体属性接口按 `I<Type>EntityProperty` 命名（`IBooleanEntityProperty`, `IIntEntityProperty`, `IStringEntityProperty` 等），工厂为 `SimpleEntityPropertyFactory`。
- capability 的乘法方法签名是 `copyWithMultiplier(content, float multiplier)`（`EntityRecipeCapability`, `ModelRecipeCapability`, `NutrientRecipeCapability`）；`EntityIngredient` / `ChancedEntityIngredient` 同样接受 `float`，乘法结果按 `(int)` 截断；`CogniItemRecipeCapability extends ItemRecipeCapability`。
- 没有 `api/recipe/content/` 子包；营养序列化位于 `api/capability/recipe/`。
- `api/capability/forge/CBCapabilities` 声明 `ENTITY_CONTAINER` capability 与 `register(RegisterCapabilitiesEvent)`；模块内无调用点。

## TRAIT OWNERSHIP
`api/machine/trait/` 的三个 trait 均为 `NotifiableRecipeHandlerTrait<T>` 子类：`NeuralModelContainer`（`ModelIngredient`）、`NotifiableEntityContainer`（`EntityIngredient`）、`NotifiableNutrientHandler`（`Float`）。另有机器内联 `RecipeLogic` 子类 `BasicLivingRecipeLogic`（`api/machine/BasicLivingMachine`）、`CogniAssemblerRecipeLogic`（`machine/multiblock/CogniAssemblerMachine`），以及 `ParabioticBridgeHandler extends NotifiableItemStackHandler`（`machine/multiblock/part/ParabioticBridgePartMachine`）。

约束以 `ctnh-docs/references/_architecture/AGENTS.md` 为准，本域重点：

- capability 四层分工：Forge capability 对外暴露、recipe capability 描述配方语义与并行/XEI 逻辑、trait 持有 handler 与机器侧状态、机器子类只放机器特有规则。生物 recipe capability 的匹配逻辑属 recipe capability 层，不要下沉进 trait。
- 需要同步或持久化的字段放 trait 并用 managed field 承载；`@DescSynced` 与 `@Persisted` 同用前确认两者都必要；装不下的走 `saveCustomPersistedData` / `loadCustomPersistedData`。
- 一份状态一个所有者：机器字段与 trait 字段禁止并存。

## ANTI-PATTERNS
- 新增实体/模型配方匹配时绕过 `PropertyOperators` / `EntityProperties`。
- 把生物 recipe capability 合并进 Core；活体机器抽象归本模块所有。
- 接线电路配置器时绕过 `CircuitFancyConfigurator` 的槽位背景设置。
- 让 `api/` 反向依赖 `machine/` / `registry/` 的实现类；客户端专属类只能出现在渲染路径上（现状：`api/item/LivingMetaMachineItem.java` 引用 `client/model/CBModels`，这是唯一例外，不要照此扩散）。

## SCOPE
`src/main/java/com/moguang/ctnhbio/api` 及其全部子包。

## READ WHEN
- 新增 recipe capability、实体/模型原料或机器 API 面。
- 修改 `BasicLivingMachine` 的 Jade / 配置器逻辑，或 `LivingMetaMachineEntity` 的宿主交互。

## SOURCE OF TRUTH
- `api/recipe/` 契约与 `common/CommonProxy.java` 的初始化顺序。
- `api/machine/BasicLivingMachine.java`、`api/entity/LivingMetaMachineEntity.java` 的当前 Jade / 宿主行为。

## WORKFLOW
1. 先确认要加的 API 面确实是 Bio 专属、且会被跨域或跨模块引用。
2. 检查 `CommonProxy.init()` 中 `PropertyOperators` / `EntityProperties` 的初始化时机。
3. 跑 `:modules:CTNH-Bio:build`。
