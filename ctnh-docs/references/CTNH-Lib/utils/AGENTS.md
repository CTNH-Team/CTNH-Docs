# CTNH-LIB UTILS DOMAIN

## OVERVIEW
共享工具类（8 个 Java 文件）：分块列表、环境判定、NBT 助手、有序 identity map、机器配方模拟工具、通用 registrate 构建器，以及确定性的陨石地形生成器。

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| 已有对象/编解码器注册进 registrate | `utils/AllBuilder2.java`、`utils/CodecBuilder.java` |
| 分块列表 | `utils/ChunkList.java`（`List<T>` 实现，`DEFAULT_CHUNK_SIZE = 1024`，treap 组织分块） |
| 环境判定 | `utils/EnvUtils.java`（`isDataGen`，取自 `FMLLoader` 的 launch handler） |
| NBT 助手 | `utils/ExtendNbtUtils.java`（`writeVec3`/`readVec3`、`writeQuaternionf`/`readQuaternionf`） |
| 有序 identity map | `utils/LockIdentityHashMap.java`（fastutil `AbstractObject2ObjectSortedMap` 派生） |
| 机器配方模拟 | `utils/MachineUtils.java` |
| 陨石地形 | `utils/InfiniteMeteorTerrain.java` |

## CONVENTIONS
- 助手默认静态、无注册表依赖；模块应优先复用 Lib 工具而不是本地复制。
- `AllBuilder2` / `CodecBuilder` 是 `AbstractBuilder` 的薄包装，用于注册“已经构造好的对象”或“已经写好的 codec”；保持泛型、与具体 mod 无关。
- `InfiniteMeteorTerrain` 由世界种子构造（`CELL_SIZE = 64.0`、`DENSITY = 0.30`、材质常量 `AIR/STONE/GRAVEL/METEOR/GLASS`），缓存与结果数组都是实例级运行时状态；`calculate(seed, x, z, int[] type, double typeOffset, double[] offset)` 就地改写材质剖面与高度偏移。
- `MachineUtils` 提供 item / fluid / EU / CWU 四类 `canInput*` / `canOutput*` / `input*` / `output*` 重载（同时有 `IRecipeLogicMachine` 与 `RecipeHandlerGroup` 两种作用域），以及 `applyContents`（按 capability 与 IO 遍历多方块部件）、`getOffset` / `getArea`（按朝向换算相对坐标与 AABB）。
- `MachineUtils` 的 `ItemStack...` 入口先经私有 `nonEmpty()` 过滤 null / 空栈再 `GTRecipeBuilder.ofRaw()`；这是为了避免 “Output item ... is empty” 日志并避免中断合法产出（如数字采矿机 `[item, empty]` 掉落）。
- 当前跨模块消费方：`MachineUtils`（Core / Energy / Mana / CTPP / Bio / Astral / CEI 等 40+ 文件）、`ExtendNbtUtils`（CTPP 旋转机械元件）、`ChunkList` + `LockIdentityHashMap`（CEI EMI 分组）、`EnvUtils`、`AllBuilder2` / `CodecBuilder` / `InfiniteMeteorTerrain` 目前无模块调用。

## ANTI-PATTERNS
- 往 Lib 加模块专属工具；应放所属模块的 `utils/`。
- 在 `MachineUtils` 里绕过 `nonEmpty()` 直接塞 `ItemStack...` 进 `GTRecipeBuilder.ofRaw()`；空栈会触发日志并可能中断合法配方模拟。
- 复制 `ChunkList` / `LockIdentityHashMap` 之类已有结构到模块内。

## SCOPE
适用于 `src/main/java/tech/vixhentx/mcmod/ctnhlib/utils`。

## READ WHEN
- 跨模块复用共享工具逻辑。
- 改 `MachineUtils` 的配方模拟行为（空栈过滤）。

## SOURCE OF TRUTH
- `utils/` 下的工具类源码。

## WORKFLOW
1. 写新助手前先确认 Lib 里没有现成实现。
2. 改 `MachineUtils` 时确认没有空 `ItemStack` 到达 `GTRecipeBuilder.ofRaw()`。
3. 跑 `:modules:CTNH-Lib:build`。
