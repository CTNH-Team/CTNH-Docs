# CTNH-BIO EVENT DOMAIN

## OVERVIEW
Bio 的事件层（3 个 Java 文件）：数据生成钩子、Forge 事件订阅（服务端 tick 与物品 tooltip）以及血肉转换实体的临时登记表。

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| 数据生成钩子 | `event/EventHandler.java` — 类级 `@Mod.EventBusSubscriber(modid = CTNHBio.MODID, bus = MOD)`，`gatherData(GatherDataEvent)` 注册 `VanillaRecipeProvider`（`VanillaRecipes` 仍为注释态） |
| Forge 事件订阅 | `event/ForgeEventHandler.java` — `@Mod.EventBusSubscriber(modid = CTNHBio.MODID, bus = FORGE)` |
| 血肉转换登记 | `event/TransformManager.java` — `FLESH_BLOB_LIST` 与 `addEntity(LivingEntity)` |

## CONVENTIONS
- `ForgeEventHandler.onServerTick(TickEvent.ServerTickEvent)` 只在 `Phase.END` 生效：遍历 `TransformManager.FLESH_BLOB_LIST`，实体所在位置与其下方均可替换时移除实体并在该位置放置 `CBMultiblocks.GREAT_FLESH` 方块；向列表添加实体只用 `TransformManager.addEntity()`，不要直接改列表。
- `ForgeEventHandler.onItemTooltip(ItemTooltipEvent)` 为 HNN 的 `DEEP_LEARNER` / `SIM_CHAMBER` 追加说明行，文案用 CTNH-Lib 的 `@CN` / `@EN` 注解式 `Lang` 字段（类上带 `@Category("item_tooltip")`）；新增 tooltip 文案沿用这套注解，不要硬编码字符串。
- `EventHandler.gatherData` 是 Bio 的数据生成入口之一；provider 的挂载清单以 `data/CBDatagen.java` 为准，两处不要重复注册同一个 provider。

## ANTI-PATTERNS
- 把事件接线写进 `registry/` 或 `common/` 的注册类。
- 绕过 `TransformManager` 直接操作 `FLESH_BLOB_LIST`，或在非服务端侧改动方块。
- 在事件处理器里硬编码可翻译文本，绕过 `@CN` / `@EN` lang 机制。

## SCOPE
本域覆盖 `src/main/java/com/moguang/ctnhbio/event` 下的全部类。

## READ WHEN
- 新增 Bio 的 Forge 生命周期 / capability 事件处理。
- 修改血肉转换行为或物品 tooltip 附加说明。

## SOURCE OF TRUTH
- `event/EventHandler.java`, `event/ForgeEventHandler.java`, `event/TransformManager.java`，以及 `common/CommonProxy.java` 的注册上下文。

## WORKFLOW
1. 先确认目标 Forge 事件与订阅点（注解式 `@Mod.EventBusSubscriber` 还是 `CommonProxy` 的 `addGenericListener`）。
2. 跑 `:modules:CTNH-Bio:build`；涉及 tick / tooltip 的改动在游戏内验证。
