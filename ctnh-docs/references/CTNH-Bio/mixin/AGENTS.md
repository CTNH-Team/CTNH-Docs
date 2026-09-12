# CTNH-BIO MIXIN DOMAIN

## OVERVIEW
针对上游 mod 的兼容补丁（18 个 Java 文件）：Biomancy、Hostile Neural Networks、EMI/ALI、Create、GTCEu 的配方与机器内部实现。

## STRUCTURE
```
mixin/
├─ ali/                       # EmiGamePlayLootMixin, EmiScrollWidgetMixin
├─ biomancy/                  # BiomancyJeiPluginMixin, InjectorItemMixin, InjectorScreenMixin, VialHolderBlockEntityMixin
├─ create/                    # CrushingWheelControllerBlockEntityMixin
├─ emi/                       # EmiApiMixin, RecipeScreenMixin
├─ gtm/                       # GTRecipeTypeMixin, IThermalFluidHandlerItemStackMixin,
│                             #   MultiblockDisplayText$BuilderMixin, ThermalFluidStatsMixin
└─ hostilenetworks/           # CacheModelMixin, DataModelItemMixin, HostileEventsMixin,
                              #   HostileJeiPluginMixin, SimChamberTileEntityMixin
```

`src/main/resources/ctnhbio.mixins.json` 当前登记：

- `mixins`：`ali.EmiGamePlayLootMixin`, `ali.EmiScrollWidgetMixin`, `biomancy.BiomancyJeiPluginMixin`, `biomancy.InjectorItemMixin`, `biomancy.VialHolderBlockEntityMixin`, `create.CrushingWheelControllerBlockEntityMixin`, `emi.EmiApiMixin`, `gtm.GTRecipeTypeMixin`, `gtm.IThermalFluidHandlerItemStackMixin`, `hostilenetworks.CacheModelMixin`, `hostilenetworks.HostileEventsMixin`, `hostilenetworks.HostileJeiPluginMixin`, `hostilenetworks.SimChamberTileEntityMixin`, `hostilenetworks.DataModelItemMixin`
- `client`：`biomancy.InjectorScreenMixin`, `emi.RecipeScreenMixin`, `gtm.ThermalFluidStatsMixin`

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Biomancy 补丁 | `mixin/biomancy/`（注入器物品/界面、小瓶方块实体、JEI 插件） |
| HNN 补丁 | `mixin/hostilenetworks/`（模型缓存、数据模型物品、敌对事件、JEI 插件、模拟仓方块实体） |
| EMI / ALI 补丁 | `mixin/emi/`, `mixin/ali/` |
| Create 补丁 | `mixin/create/CrushingWheelControllerBlockEntityMixin.java` |
| GTCEu 补丁 | `mixin/gtm/` |
| Mixin 配置 | `src/main/resources/ctnhbio.mixins.json` |

## CONVENTIONS
- 新增 Mixin 必须同步 `ctnhbio.mixins.json`：`client` 专用补丁放 `client` 数组（`InjectorScreenMixin`, `RecipeScreenMixin`, `ThermalFluidStatsMixin`），其余放 `mixins`。
- 按目标 mod 分目录（`biomancy/`, `hostilenetworks/`, `emi/`, `ali/`, `create/`, `gtm/`），不要堆在单一目录。
- GTCEu 目标成员一律 `remap = false`（见 `MultiblockDisplayText$BuilderMixin`）。
- `mixin/gtm/MultiblockDisplayText$BuilderMixin.java` 目前整体为注释掉的注入代码，但仍在 `mixins` 数组中登记；改动模型输出行的显示逻辑时以该文件的注释代码为参考起点，并确认目标成员签名。
- 这些是兼容补丁而非通用工具：注入点必须对照目标 mod 的当前版本成员。

## ANTI-PATTERNS
- 加补丁不改 `ctnhbio.mixins.json`，或把客户端专用注入放进 `mixins` 数组（会导致服务端加载失败）。
- despoil 战利品催化剂展示由 `CTNH-Core` 的 `CTNHExtraEmiPlugin` 处理（`ctnhbio:despoil_loot` 类别）；本模块不实现 `mixin/ali/EmiCompatibilityMixin`。
- 不复核上游成员签名就改注入点。
- 用 Mixin 实现本该由 `api/` / `registry/` 提供的功能。

## SCOPE
`src/main/java/com/moguang/ctnhbio/mixin` 与 `src/main/resources/ctnhbio.mixins.json`。

## READ WHEN
- 给 Biomancy / HNN / EMI / ALI / Create / GTCEu 打补丁或改现有补丁。

## SOURCE OF TRUTH
- `src/main/resources/ctnhbio.mixins.json` 与 `mixin/` 下的补丁类；上游目标成员以对应 mod 的当前版本为准。

## WORKFLOW
1. 定位集成目标的 mixin 包与 JSON 条目。
2. 对照已加载的 mod 版本核实目标成员。
3. 跑 `:modules:CTNH-Bio:build`，并在运行时验证注入是否生效。
