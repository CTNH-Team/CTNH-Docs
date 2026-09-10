# CTNH-MANA EVENT DOMAIN

## OVERVIEW
`event/` 是 CTNH-Mana 的事件层（16 个 Java 文件）：1 个 MOD 总线空标记类、1 个客户端按键绑定类、13 个 Forge 总线事件处理器（效果副作用、伤害管线、Boss 精英怪），以及 1 个 mythic Boss 池。

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| MOD 总线标记 | `event/EventHandler.java`（`@Mod.EventBusSubscriber(modid = ctnhmana, bus = MOD)`，类体为空，不含任何注册逻辑） |
| 组合 Forge 事件 | `event/ForgeEventHandler.java`（capability 挂载、物品 tooltip、生物死亡、客户端按键） |
| 按键绑定 | `event/CMKeyBindings.java`（CLIENT + MOD 总线；`OPEN_CADUCEUS` 默认 N、`FORTUNA` 默认 C，分类 `key.category.ctnhmana.general`） |
| 伤害钳制 | `event/DamageClampHandler.java` + `common/capability/DamageClampCapability` |
| 破甲 | `event/ArmorBreakEventHandler.java`（施加破甲时削一层抗性提升） |
| 索引 / 业力 | `event/IndexEventHandler.java` |
| 奥法拮抗 / 物理拮抗 | `event/MagicalAntagonismEventHandler.java`, `event/PhysicalAntagonismEventHandler.java` |
| 苦难护盾 | `event/PainShieldEventHandler.java` |
| 现实解离 | `event/RealityDissociationEventHandler.java` |
| 灵魂汲取 | `event/SoulLeechEventHandler.java` |
| 污血泣泪 | `event/TaintedBloodWeepingEyeEventHandler.java` |
| 第三只眼 | `event/ThirdEyeEventHandler.java` |
| 百合子戒指 | `event/YurikoRingEventHandler.java` |
| 矿工精英怪 | `event/MinerEliteHandler.java` + `event/MythicBossPool.java` |

## CONVENTIONS
- `event/EventHandler` 只是 MOD 总线的空标记类；注册编排在 `common/CommonProxy`，不要在 `EventHandler` 里加注册或 `gatherData` 逻辑。
- 各类分工：`DamageClampHandler` 在 `LivingHurtEvent` 上以 `HIGHEST` 记录护甲前伤害、`LOWEST` 把累计非护甲减伤按 sigmoid 收缩到 `CMConfig.INSTANCE.damageClamp` 上限，仅对玩家生效，且跳过已取消事件。
- 拮抗类效果在服务端判定，经 `CMMobEffects.*` 取效果实例；魔法/物理伤害白名单以伤害类型 id 的 path 匹配，爆炸与弹射物走 `DamageTypeTags`。
- `CMKeyBindings` 是唯一在 `event/` 内注册客户端按键的地方；实际按键行为在 `ForgeEventHandler.keyEvent`（`OnlyIn(Dist.CLIENT)`），且仅当主手为 `CaduceusItem` 时开轮盘或发包。
- `PainShieldEventHandler` 的意志消耗只检索 Curios 饰品栏中的 `IDemonWillGem`；等级下降需先 `removeEffect` 再按降低后的 amplifier 重新添加。
- `MinerEliteHandler.trySpawnMinerElite(ServerLevel, DungeonRoomPlacement)` 由 `mixin/bloodmagic/DungeonSynthesizerMixin` 在矿工房间放置成功后调用；精英怪用 NBT 标记 `ctnhmana_miner_elite` 判定死亡落箱（战利品表 `ctnhmana:chests/miner_elite`）。
- `MythicBossPool` 是代码内构造的 mythic 品质 Boss 池（主世界 6 / 下界 6 / 末地 2），供 `MinerEliteHandler` 按权重抽取。
- 所有文案经 CTNH-Lib lang provider（`classify` 到 `data/lang/*` 的 `Lang` 数组），不硬编码中文。

## ANTI-PATTERNS
- 把注册、datagen 或生命周期逻辑放回 `event/EventHandler`（该类为空标记）。
- 在 `event/` 内直接注册网络包（应在 `common/CommonProxy.onCommonSetup()`）。
- 在客户端与服务端双侧同时执行效果判定（效果处理器统一在服务端判定，客户端分支只做表现）。
- 在 `MinerEliteHandler` 之外复制精英怪生成或落箱逻辑，而不复用 `TAG_MINER_ELITE` 标记。

## SCOPE
适用于 `src/main/java/com/magicbee/ctnhmana/event`。

## READ WHEN
- 新增或修改生物效果的事件副作用。
- 改动伤害管线（减伤钳制、拮抗免疫、伤害倍率）。
- 改动索引 / 业力 / 虚境相关的事件判定。
- 新增或改动矿工房间精英怪与 Boss 池。

## SOURCE OF TRUTH
- `event/` 各类的 `@Mod.EventBusSubscriber` 声明与订阅方法。
- 事件编排与注册：`common/CommonProxy.java`。

## WORKFLOW
1. 先判断事件属于 MOD 总线还是 FORGE 总线，选对应订阅方式。
2. 效果类改动同步检查 `api/effect/*` 与 `registry/CMMobEffects` 的注册项。
3. 跑 `:modules:CTNH-Mana:build`；伤害或生成改动在游戏内验证。
