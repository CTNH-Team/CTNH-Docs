# CTNH-MANA MIXIN DOMAIN

## OVERVIEW
对 Ars Nouveau、Blood Magic、Botania、AE2、EMI 与 Minecraft 本体的兼容补丁（18 个 Java 文件，其中 1 个已整体注释），配置写在 `src/main/resources/ctnhmana.mixins.json`。

## STRUCTURE
```text
mixin/
├── ae2/                       # WirelessTerminalItemMixin, WirelessTerminalMenuHostMixin
├── ars/                       # MixinEmiLecternRecipeHandler, PotionJarMixin, PotionTankMixin, StoredItemStackMixin(已整体注释，未注册)
├── bloodmagic/                # 4: BloodAltarMixin, DemonWillHolderMixin, DungeonSynthesizerMixin, TileAltarAccessor
├── botania/                   # 6: BotaniaEntitiesMixin, FunctionalFlowerBaseAccessor, ManaPoolBlockEntityMixin, MixinForgePacketHandler, PetruniaMixin, WitherAconiteMixin
├── emi/                       # TagEmiIngredientMixin
└── minecraft/                 # EntityAccessor
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Mixin 配置 | `src/main/resources/ctnhmana.mixins.json`（`package: com.magicbee.ctnhmana.mixin`、`compatibilityLevel: JAVA_17`、`refmap: mixins.ctnhmana.refmap.json`、`mixins` 17 条目、`client` 为空） |
| AE2 补丁 | `mixin/ae2/`（2） |
| Ars Nouveau 补丁 | `mixin/ars/`（3 生效 + `StoredItemStackMixin` 注释态） |
| Blood Magic 补丁 | `mixin/bloodmagic/`（4，含 `TileAltarAccessor`，经 `api/mixin/IBloodAltarLogic` 暴露契约；`DungeonSynthesizerMixin` 调 `MinerEliteHandler.trySpawnMinerElite`） |
| Botania 补丁 | `mixin/botania/`（6） |
| EMI 补丁 | `mixin/emi/TagEmiIngredientMixin.java` |
| Minecraft 补丁 | `mixin/minecraft/EntityAccessor.java` |

## CONVENTIONS
- mixin JSON 的条目与 `mixin/` 下的类保持同步：新增类必须加入 `mixins` 列表，否则不会被加载。
- `mixin/ars/StoredItemStackMixin.java` 的类体已整体注释，因此不在 JSON 中；恢复它需连同 JSON 条目一起改。
- refmap 名 `mixins.ctnhmana.refmap.json` 与 mod id 一致，勿改名。
- 兼容补丁按目标 mod 分包（`mixin/<mod>/`），不要堆进 `mixin/minecraft/`。
- 魔法兼容面横跨 mixin、配方 builder、集成与客户端包四处，改动一个集成面时四处同查。
- Accessor 类（`TileAltarAccessor`, `FunctionalFlowerBaseAccessor`, `EntityAccessor`）只暴露访问器，不放业务逻辑。

## ANTI-PATTERNS
- 改动注入点前不核对上游目标成员（成员名/描述符随上游版本变化）。
- 新增 mixin 类但漏加 `ctnhmana.mixins.json` 条目，或反之删除类后遗留条目。
- 把 `StoredItemStackMixin` 当作生效补丁引用（其源码处于注释状态）。
- 修改 refmap 名称或在 `mixin/` 下新建未经 JSON 注册的包。

## SCOPE
适用于 `src/main/java/com/magicbee/ctnhmana/mixin` 与 `src/main/resources/ctnhmana.mixins.json`。

## READ WHEN
- 给 Ars Nouveau、Blood Magic、Botania、AE2、EMI 或 Minecraft 实体打补丁。
- 新增、删除或重命名 mixin 类。
- 改动访问器暴露的成员。

## SOURCE OF TRUTH
- `src/main/resources/ctnhmana.mixins.json` 与 `mixin/` 下的类定义。
- 上游目标成员以 vendored 上游参考副本为准；只有任务明确指向 GTCEu 内部时才改动 vendored 代码。

## WORKFLOW
1. 定位目标 mod 的 mixin 包与 JSON 条目。
2. 对照当前加载的上游 mod 版本核对目标成员名与描述符。
3. 跑 `:modules:CTNH-Mana:build`，在游戏内验证注入是否生效（启动日志中的 mixin 应用记录）。