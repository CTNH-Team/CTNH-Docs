# CTNH-ENERGY EVENT DOMAIN

## OVERVIEW
CTNH-Energy 的 Forge 事件处理器（2 个 Java 文件）。

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| 公共事件 | `event/ForgeEventHandler`（`BlockEvent.EntityPlaceEvent`：放置样板提供者时自动配置相邻 `SimpleTieredMachine` 的 `AutoOutputTrait`——开启物品/流体自动输出、设置输出面、允许从输出面输入） |
| 客户端事件 | `event/ForgeClientEventHandler`（`ItemTooltipEvent`：为 AE2 Omni 合成单元追加并行数提示，COMPLEX 家族追加样板自动翻倍提示；按住 Shift 时经 `PatternAuthorData.addEncodedTimeLine` 追加编码时间与署名行） |

## CONVENTIONS
- 两个处理器都用 `@Mod.EventBusSubscriber(modid = CTNHEnergy.MODID, bus = Bus.FORGE)` 注册；客户端处理器额外限定 `value = Dist.CLIENT`。
- 事件回调只做转发与轻量判断，实际逻辑复用 `utils/CEUtil`、`common/pattern/PatternAuthorData`。
- 放置事件在服务端主线程延后执行（`level.getServer().execute(...)`）后再读取方块实体。
- 工具提示文案用 `@Category("tooltip")` + `@CN` / `@EN` 声明，键落到 `ctnhenergy.tooltip.*`。

## ANTI-PATTERNS
- 把事件注册搬到 `registry/` 或代理类中。
- 在事件里直接读写上游字段而不走 `api/` 与 `common/` 的既有入口。

## SCOPE
`modules/CTNH-Energy/src/main/java/tech/luckyblock/mcmod/ctnhenergy/event/`。

## READ WHEN
- 新增 Energy 的 Forge 生命周期 / 玩家交互事件监听
- 修改工具提示注入或放置时的自动配置行为

## SOURCE OF TRUTH
`event/` 下的处理器与 `common/CommonProxy` 的事件总线接线。

## WORKFLOW
1. 确认事件挂在 `FORGE` 还是 mod 事件总线，并选定 `Dist` 限定。
2. 逻辑下沉到 `common/` 或 `utils/`，事件类只保留判断与转发。
3. `:modules:CTNH-Energy:build` 编译；行为在游戏内验证。
