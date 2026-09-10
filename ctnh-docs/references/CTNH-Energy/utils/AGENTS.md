# CTNH-ENERGY UTILS DOMAIN

## OVERVIEW
CTNH-Energy 的共享工具（11 个 Java 文件）：EU/能量网络查询、菜单配置读写、样板提供者目标适配、绘制辅助与按钮控件。

## STRUCTURE
```text
utils/
├─ CEUtil.java, CEDrawHelper.java, MEConfigUtil.java
├─ CEPatternProviderTarget.java, ProviderRecord.java
├─ FakeSizedIntList.java, TempColorSprayBehaviour.java
└─ button/   # BlitterButton, ToggleBlitterButton, Blitters, CETextures
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| 能量 / 网络查询 | `utils/CEUtil`（`getUpgradeable(BlockEntity, Direction)`, `isInSameGrid`, `getSides`, `getGridTier(IGrid/IGridNode)`, `clampToLong(BigInteger)`, `ingredientFromGenericStacks`, `isCrafting(...)`） |
| 机器配置读写 | `utils/MEConfigUtil`（`writeGhostCircuit/readGhostCircuit`, `writeDistinctBuses/readDistinctBuses`, `writeConfigHandler/readConfigHandler`, `writeAutoPull/readAutoPull`, `writeMinStackSize/readMinStackSize`, `writeMaxStackSize/readMaxStackSize`） |
| 样板提供者目标 | `utils/CEPatternProviderTarget`（继承 AE2 `PatternProviderTarget`，声明 `onlyHasPatternInput(IPatternDetails, boolean)` 与 `getStorage()`；文件内旧的静态包装实现为注释状态） |
| 提供者记录 | `utils/ProviderRecord`（record，字段 `ICraftingProvider provider, Boolean block`） |
| 固定长度伪列表 | `utils/FakeSizedIntList`（继承 fastutil `AbstractIntList`，`ofSize(int)`，元素固定 -1） |
| 临时染色行为 | `utils/TempColorSprayBehaviour`（继承 AE2 `ColorSprayBehaviour`，重写 `useItemDurability`） |
| 绘制辅助 | `utils/CEDrawHelper`（`drawStringRightBorder`，被 `common/machine/gui/AEConfigSlotWidget` 静态导入） |
| 按钮控件 | `utils/button/{BlitterButton, ToggleBlitterButton, Blitters, CETextures}` |

## CONVENTIONS
- `utils/` 不依赖 `registry/`；允许依赖 `common/` 的存储与服务类（`CEUtil` 依赖 `common/me/*`，`MEConfigUtil` 依赖 `common/machine/utils/GenericStackHandler`）。
- 配置读写统一走 `MEConfigUtil` 的 write/read 配对方法，不要各自手写 NBT 键名。
- 逻辑副作用优先交给调用方：工具类只做解析、转换与查询。
- `button/` 与 `CEDrawHelper` 属客户端绘制路径，改动后需在游戏内目视验证。

## ANTI-PATTERNS
- 复制 CTNH-Lib `ctnhlib/utils/` 已有的通用工具，或重复实现模板化的 NBT 读写。
- 在各机器类里重复手写电路/总线/拉取量的 NBT 键，而不复用 `MEConfigUtil`。
- 在 `utils/` 中直接注册对象或声明注册表条目。

## SCOPE
`modules/CTNH-Energy/src/main/java/tech/luckyblock/mcmod/ctnhenergy/utils/` 及其子包。

## READ WHEN
- 需要复用 Energy 已有的能量网络查询、配置读写、样板目标或按钮控件
- 新增全局共享的辅助逻辑

## SOURCE OF TRUTH
`utils/` 下的工具类，以及其在 `common/` 与 `mixin/` 中的调用点。

## WORKFLOW
1. 先在 CTNH-Lib `utils/` 与 `utils/` 中查找是否已有实现。
2. 新增工具类保持无注册依赖，命名与既有前缀一致。
3. `:modules:CTNH-Energy:build` 编译；涉及绘制的改动在游戏内验证。