# CTNH-MANA API DOMAIN

## OVERVIEW
`api/` 是 CTNH-Mana 的跨域契约层（35 个 Java 文件）：魔法多方块图案谓词与方块映射、16 个生物效果、4 个配方条件、6 个自定义配方逻辑、Botania 效果包扩展，以及三类机器 trait。

## STRUCTURE
```text
api/
├── effect/                    # 16: ArmorBreakEffect, BladeUnleashedEffect, IndexTargetEffect, KarmaEffect, KarmaFortunaEffect, MagicalAntagonismEffect, PainShieldEffect, PhysicalAntagonismEffect, RageEffect, RealityDissociationEffect, RootedEffect, ShroudGazeEffect, SoulLeechEffect, TaintedBloodEffect, WishingFlyEffect, WitherCloudEffect
├── machine/gem/               # GemSublimatorRules
├── machine/trait/             # 3: BTManaContainerTrait, ExtendedControlBusCircuitTrait, MysticSpireManaTrait
├── mixin/                     # IBloodAltarLogic
├── networks/                  # BotaniaEffectPacketExtend, BotaniaExtendEffectType
├── pattern/                   # CMBlockMaps, CMPredicates
├── recipe/condition/          # 4: BloodAltarCondition, HellForgeCondition, InfusionCellCastingCondition, ZenithCondition
└── recipe/customlogic/        # 6: DigitalWellOfSufferLogic, EternalGardenLogic, IndustrialGemCuttingLogic, IndustrialGemSublimatorGenericLogic, IndustrialGemSublimatorLogic, IndustrialSalvagingLogic
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| 图案与谓词 | `api/pattern/CMBlockMaps.java`（`BloodMagicRuneBlock: Map<Integer, Supplier<? extends Block>>`、`initBlocks()`）, `api/pattern/CMPredicates.java`（`BMRuneBlocks`，20 个血魔法符文方块） |
| 生物效果 | `api/effect/`（16，均 `extends MobEffect`），注册在 `registry/CMMobEffects` |
| 魔力容器 trait | `api/machine/trait/BTManaContainerTrait.java` |
| 尖塔魔力 trait | `api/machine/trait/MysticSpireManaTrait.java` |
| 扩展总成电路 trait | `api/machine/trait/ExtendedControlBusCircuitTrait.java` |
| 宝石规则 | `api/machine/gem/GemSublimatorRules.java`（`final`，含 `rarityByPath(String)`） |
| 配方条件 | `api/recipe/condition/`（4），注册在 `registry/CMRecipeConditions` |
| 自定义配方逻辑 | `api/recipe/customlogic/`（6，均 `implements GTRecipeType.ICustomRecipeLogic`） |
| 网络契约 | `api/networks/BotaniaEffectPacketExtend.java`, `api/networks/BotaniaExtendEffectType.java`（枚举，字段 `argCount`：`SPARK_MANA_FLOW(3)`, `SPARK_MANA_FLOW_REVERSE(3)`, `TERRA_PLATE(1)`, `SPARK_NET_INDICATOR(2)`） |
| Mixin 契约 | `api/mixin/IBloodAltarLogic.java`（`CM$resetCapacity(int)`, `CM$setCapacityMultiplier(float)`, `CM$BroadcastPos(BlockPos)`, `CM$ConsumeLPIfEnough(int)`） |

## CONVENTIONS
- `BTManaContainerTrait extends MachineTrait implements ManaReceiver`：持久化 `@Persisted maxBTMana`（仅 `@Getter`）与 `@Persisted BTMana`（`@Getter @Setter`）；`setMaxBTMana(int)` 以 `Math.max(0, ...)` 夹紧并同步压低 `BTMana`；默认容量 `10_000`。它是 BTMana 的唯一归属者，取代旧版 `ManaMachineBlockEntity` 上的字段。
- `MysticSpireManaTrait extends MachineTrait implements ManaReceiver`：`@Persisted` 存 `int maxBTMana/BTMana` 与 `String trueMana/trueManaCapacity`；BigInteger 经 `SpireBigMath.parsePersisted` / `toPersistString` / `nonNegative` 转换；暴露 `getTrueManaBig` / `getTrueManaCapBig` / `getTrueManaRoomBig` / `setTrueManaCapacityBig` / `setMaxMana` / `syncManaCache` / `mysticOutboundTickCap(int)` / `mysticInboundTickBudget(int)` / `mysticDrainMana(int)` / `sendMana(long)` / `receiveMana(int)`。
- `ExtendedControlBusCircuitTrait`（`final`）：`@Persisted CustomItemStackHandler storage`，构造 `(MetaMachine, int laneCount)`，`setFilter(IntCircuitBehaviour::isIntegratedCircuit)`，内容变更回调 `onChanged`。
- `api/recipe/customlogic/` 的 6 个类实现 `GTRecipeType.ICustomRecipeLogic`，负责自定义配方匹配，**不是** `RecipeLogic` 子类。
- API 类不得把仅客户端类引入通用构造路径。
- GT/GMT 配方是运行时动态包数据（`CTNHManaGTAddon.addRecipes()` → CTNHDynamicDataPack），`runData` 对其不产出 JSON。
- 物品/方块/流体引用必须用静态注册对象（`CMItems.X`, `CMBlocks.X`），不得字符串解析 + `ForgeRegistries` 查找。

## RECIPE LOGIC BOUNDARY
本模块唯一的 `RecipeLogic` 子类是 `common/multiblock/ZenithMatrixMachine` 内的静态嵌套类 `ZenithMatrixRecipeLogic`。`api/recipe/customlogic/` 的 6 个类实现 `GTRecipeType.ICustomRecipeLogic`，只做配方匹配。约束以 `references/_architecture/AGENTS.md` §6 为准：

- `RecipeLogic` 负责当前 recipe、工作状态、配方上下文，以及经 `ContentListMap.forEachEntry` 按 capability 顺序分发输出 tooltip。
- 输出内容的解释属 `RecipeCapability` 自己的职责；**不要在 `RecipeLogic` 里加 capability 类型判断**。
- 遍历 recipe 内容统一走 `forEachEntry`，不要遍历 `asMap().entrySet()` 再手排。
- `lastRecipe` 已由 `@DescSynced` 同步，Jade 中禁止重复序列化。

## ANTI-PATTERNS
- 在 API 类里写游戏逻辑；实现应落在 `common/` 或 `registry/`。
- 把魔力持久化到 BlockEntity；trait 才是唯一真实来源。
- 给 `maxBTMana` 加 Lombok `@Setter`（需显式夹紧 setter）。
- 把 `api/recipe/customlogic/` 的类当作 `RecipeLogic` 使用或据此扩展工作循环逻辑。

## SCOPE
适用于 `src/main/java/com/magicbee/ctnhmana/api` 及其子包。

## READ WHEN
- 向其他代码暴露魔法多方块图案或配方契约。
- 新增或修改魔力存储 trait、尖塔魔力 trait、扩展总成电路 trait。
- 新增生物效果或配方条件。

## SOURCE OF TRUTH
- `api/pattern/` 契约与 `registry/` 接线。
- `api/machine/trait/*` 的宿主：`common/parts/ManaHatch`、`common/machine/FlowerCakeMachine`、`common/multiblock/MysticSpire`、`common/parts/ExtendedCentralControlBus`。

## WORKFLOW
1. 确认该接口确实被跨域共享，再放进 `api/`。
2. trait 改动同步检查宿主机器的 `attachTrait` / `attachPersistentTrait` 调用点与 Jade 显示。
3. 跑 `:modules:CTNH-Mana:build`。