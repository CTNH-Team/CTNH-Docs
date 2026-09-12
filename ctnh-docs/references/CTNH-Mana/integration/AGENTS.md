# CTNH-MANA INTEGRATION DOMAIN

## OVERVIEW
EMI 与 Jade 集成（3 个 Java 文件），负责把 Mana 的配方工作站与第三方信息面板接入外部查看器。

## STRUCTURE
```text
integration/
├── emi/                       # CTNHManaEmiPlugin
└── jade/                      # 2: CTNHManaJadePlugin, ThirdEyeStatusProvider
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| EMI 插件 | `integration/emi/CTNHManaEmiPlugin.java`（`@EmiEntrypoint`，`register` 里为 `CMRecipeTypes.TwistCollapse` 挂 `AHCC`、为 `CMRecipeTypes.METEOR_RITUAL_GUIDE` 挂 `RITUAL_MECHANICAL_ARRAY` 作为工作站） |
| Jade 插件 | `integration/jade/CTNHManaJadePlugin.java`（`@WailaPlugin`，`register` 用 `registerBlockDataProvider(new ThirdEyeStatusProvider(), BlockEntity.class)`，`registerClient` 用 `registerBlockComponent(..., Block.class)`） |
| Jade provider | `integration/jade/ThirdEyeStatusProvider.java`（`IBlockComponentProvider` + `IServerDataProvider<BlockAccessor>`；携带第三只眼时显示魔力进度，覆盖 `BindableSpecialFlowerBlockEntity` / `FunctionalFlowerBase` / `ManaReceiver` 等目标） |

## CONVENTIONS
- 集成类保持隔离与可选：不成为 `common/` 的硬依赖。
- Jade 注册集中在 `CTNHManaJadePlugin`；`CommonProxy` 不注册任何 Jade provider，新增 provider 只在插件里注册，且必须同时给出服务端 data 与客户端 component 两侧目标类型。
- 魔法集成面横跨配方 builder、mixin、集成与客户端包四处，改动前四处同查。
- GT/GMT 配方是运行时动态包数据，集成层不得假定存在静态 JSON。
- 物品/方块/流体引用使用静态注册对象（`CMItems.X` 等），不用字符串查找。
- EMI 侧接入 GT 配方类别时统一用 `GTRecipeEMICategory.CATEGORIES.apply(...)` + `EmiStack.of(machineDefinition.asStack())` 的写法。

## ANTI-PATTERNS
- 让集成类成为 `common/` 的硬依赖，或在 `common/` 中直接引用 EMI / Jade API。
- 在 `CTNHManaJadePlugin` 之外注册 Jade provider（例如塞回 `CommonProxy`）。
- 假设 `src/generated/resources` 下存在 GT 配方 JSON 来做集成展示。

## SCOPE
适用于 `src/main/java/com/magicbee/ctnhmana/integration` 及其子包。

## READ WHEN
- 改动 Mana 的 EMI 工作站映射或 Jade 信息展示。
- 新增第三方查看器的集成入口。

## SOURCE OF TRUTH
- `integration/emi/CTNHManaEmiPlugin.java`、`integration/jade/CTNHManaJadePlugin.java` 及其 provider。
- 注册对象与配方类型来源：`registry/CMMultiblockMachines`、`registry/CMRecipeTypes`。

## WORKFLOW
1. 确认目标 mod 版本与注解入口（`@EmiEntrypoint` / `@WailaPlugin`）未被上游改动。
2. 新增 Jade provider 时同时实现服务端数据与客户端组件两侧，并在插件内注册。
3. 跑 `:modules:CTNH-Mana:build`，在装有目标 mod 的运行时验证。