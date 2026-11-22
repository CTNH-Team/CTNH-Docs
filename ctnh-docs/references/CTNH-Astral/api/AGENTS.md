# CTNH-ASTRAL API DOMAIN

## OVERVIEW
Astral 的公共 API 面（1 个 Java 文件）：战利品表构建器。当前只有 `api/loot/LootBuilder` 一个类，被 `registry/CTNHBlockInfo`、`registry/worldgen/AstralBlocks`、`registry/worldgen/MoonBlocks` 的 `loot(...)` 回调使用。

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| 精准采集掉落表构建 | `api/loot/LootBuilder.java`（`createSingleItemTableWithSilkTouch(block, itemLike)`） |
| 内部派发与爆炸条件 | `api/loot/LootBuilder.java`（`createSilkTouchDispatchTable`, `createSelfDropDispatchTable`, `applyExplosionCondition`, `HAS_SILK_TOUCH`） |
| 调用方 | `registry/CTNHBlockInfo.java`, `registry/worldgen/AstralBlocks.java`, `registry/worldgen/MoonBlocks.java` |

## CONVENTIONS
- API 类不得把仅客户端类泄漏到 common 构造路径。
- `createSingleItemTableWithSilkTouch(Block, ItemLike)` 是唯一公开入口：`HAS_SILK_TOUCH` 命中时掉自身，否则掉传入的 `itemLike`，并叠加 `ExplosionCondition.survivesExplosion()`；其余方法为 `protected static`，改动即影响全部三个调用方的掉落行为。
- `HAS_SILK_TOUCH` 是 `MatchTool.toolMatches(...)` 构造的 `protected static final` 条件，精度附魔等级下界为 1。
- 注册侧调用一律在 Registrate 的 `loot(...)` 回调里完成，不要另建 LootTable 数据生成器。
- 珍稀方块（如 `ASTRAL_STONE` → `ASTRAL_COBBLESTONE`、`MOON_STONE` → `MOON_COBBLESTONE`、`ASTRAL_GRASS_BLOCK` → `ASTRAL_DIRT`）走本构建器；普通方块在回调里用 `RegistrateBlockLootTables::dropSelf`。

## ANTI-PATTERNS
- 在 API 类里加入玩法逻辑（环境判定、配方处理、状态同步）。
- 直接改 `HAS_SILK_TOUCH` 的判定语义而不检查全部三个调用方。
- 新增需要精准采集派发的方块时手写 `LootPool`，绕过本构建器。

## SCOPE
适用于 `src/main/java/com/ctnh/ctnhastral/api` 及其子包。

## READ WHEN
- 暴露新的 Astral API 面。
- 新增需要精准采集派发的方块掉落表。

## SOURCE OF TRUTH
- `api/` 下的类及其调用方。

## WORKFLOW
1. 先确认该面确实被跨包共享，再放进 `api/`。
2. 跑 `:modules:CTNH-Astral:build`；掉落表变更需在游戏内破坏方块验证。
