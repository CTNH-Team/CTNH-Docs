# storyboard NBT 规范与自动生成

Ponder 的结构来自 `assets/<modid>/ponder/<path>.nbt`：一个 **gzip 压缩的二进制 NBT**
（根 TAG_Compound），等价于「结构模板」。本文件给出格式、几何规则和生成流程。

## 1. 文件与格式事实（本仓库实测）

| 项 | 值 |
|----|----|
| 位置 | `src/main/resources/assets/<modid>/ponder/<path>.nbt` |
| 压缩 | gzip（全部 39 个现有文件头均为 `1f 8b`） |
| `DataVersion` | 3465（当前全部 storyboard 一致） |
| 根标签 | `TAG_Compound`，键：`size` / `entities` / `blocks` / `palette` / `DataVersion` |

载荷（忽略键顺序）：

```text
size       : int[3]                  x / y / z 尺寸
DataVersion: int
palette    : list<compound>          Name + 可选 Properties（值都是 string）
blocks     : list<compound>          pos: int[3]、state: int(palette 下标)、可选 nbt: compound
entities   : list<compound>          nbt: 实体完整 NBT、blockPos: int[3]
```

- `state` 是 **palette 的下标**，不是字符串。同名方块不同状态（properties 不同）必须各占一条 palette。
- `Properties` 的值统一是字符串（`"facing":"north"`、`"power":"0"`）。
- 方块实体数据放在 block 条目的 `nbt` 里，例如机械动力的容器：
  `{"nbt":{"id":"gtceu:bronze_drum","Fluid":{...},"ForgeCaps":{}},"pos":[3,1,0],"state":20}`。
- **坐标以 0 为起点、不得越界**；`size` 是上界（合法范围 `0 <= c < size`）。
- **y=0 是地板层，结构从 y>=1 开始。**

## 2. 地板规则（CTNH 约定）

| 时代 | 地板方块 | 注册 id |
|------|----------|---------|
| 机械时代 | 安山机壳 | `create:andesite_casing` |
| 电力时代 | 列车机壳 | `create:railway_casing` |

实测佐证：`coke_oven`（机械）、`meadow`（动力）、`bigdam`（机械）、`kinetic_hatch`（机械）
= 安山机壳；`neutron_activator`、`carbonbrushes`、`windmill_control_center`（电力）
= 列车机壳。少数机械动力交互场景用 `create:brass_casing`（如 `smashing_factory`），
属于既有先例，新场景按时代选上面两种。

尺寸：**地板 = 结构水平外接矩形每边各外扩 1 格**，即每个水平轴 +2。

```text
结构 3x3  -> 地板 5x5   (blaze 1x1x3 -> 3x3；smashing_factory 5x5 -> 7x7；kinetic_hatch 5x1 -> 7x7)
```

以土高炉 `primitive_blast_furnace`（GT pattern 3x3x4）为例：结构 3x3 → 地板 5x5，
成品 `size = [5, 5, 5]`，结构占 `x1..3 / y1..4 / z1..3`，四周各留 1 格地板。

地板必须铺满整个 `size` 的水平面（无空洞），否则 Ponder 基座会缺块。

## 3. 机器摆放

### 单方块机器
只放对应的那一个方块，仍然要铺地板、仍然标注 `"controller": true`（脚本用它做校验锚点）。

### 多方块机器
1. 打开机器定义（`MultiblockMachineDefinition`）的 `pattern(...)`，按 `aisle(...)` 顺序还原结构。
2. 记号映射（GT `FactoryBlockPattern.start()` = `LEFT / UP / FRONT`）：
   - 每行字符串的**第 n 个字符** → 左侧轴，字符 **0 → x=0**
   - 每个 aisle 里的**第 m 行** → `UP`，行 0 → `y=1`（y=0 留给地板）
   - **第 a 个 aisle** → `FRONT`，aisle 0 → 正面那一层；z 从 0 递增
3. 符号取方块：`where('X', blocks(CASING_PRIMITIVE_BRICKS.get()))` → `gtceu:firebricks`；
   `Predicates.air()` 的符号（`#`、`&`）**不放方块**；
   `Predicates.controller(blocks(definition.getBlock()))` 的符号 → 主方块，标 `"controller": true`。
4. 还原完用 `--print` 核对 footprint，再按第 2 节套地板。

```text
例：primitive_blast_furnace
  .aisle("XXX", "XXX", "XXX", "XXX")   <- aisle 0
  .aisle("XXX", "X&X", "X#X", "X#X")   <- aisle 1
  .aisle("XXX", "XYX", "XXX", "XXX")   <- aisle 2，Y 是控制器
=> 结构 3(宽) x 4(高) x 3(深)，X=gtceu:firebricks，Y=gtceu:primitive_blast_furnace
=> 地板 5x5，size=[5,5,5]，主方块落在中心
```

## 4. 主方块朝向（面向玩家）

默认镜头下，**正面朝北（`facing=north`）的方块正对玩家**。已用 Ponder 自己的相机数学验算：
默认 `xRotation=-35`、`yRotation=55+90`，相机落在场景的 `(-x, +y, -z)` 象限，
可见面为 **NORTH / WEST / UP**，其中 NORTH 正对视线。

因此主方块与所有朝向类方块统一写：

```json
{ "pos": [2, 2, 1], "block": "gtceu:primitive_blast_furnace", "controller": true }
```

脚本会自动补 `facing=north` + `upwards_facing=north`。现有 CTNH 场景 100% 一致：
`coke_oven`、`meadow`、`neutron_activator` 都是 `{facing=north, upwards_facing=north}`；
`ctpp:carbon_brushes`、`ctpp:lv_kinetic_input_box`、`gtceu:ulv_output_hatch` 全是 `facing=north`。

若要把主方块转到别的朝向，就在蓝图里显式写 `"props": {"facing": "south"}`——
脚本会保留你的值并打印警告（因为它偏离了 CTNH 惯例）。

### 4.1 例外：`RotationState.NONE` 的机器没有朝向属性

GT 的 `MetaMachineBlock.createBlockStateDefinition` **只在 `RotationState != NONE` 时**才注册
`facing` / `upwards_facing`。注册时声明 `.rotationState(RotationState.NONE)` 的机器
（典型：各种**桶 Drum**、各类**储罐**）blockstate 里只有一条 `"variants": {"": {…}}`，
**不存在** `facing`。

给它们硬塞 `facing` 不会崩——原版 `NbtUtils.readBlockState` 对"方块没有该属性"是
**静默跳过**的（只对"属性存在但取值非法"打 warn）——但那是脏数据，会掩盖真实状态。
蓝图里对该方块（或对整个蓝图）写 `"controller_props": false` 即可：

```json
{ "pos": [0, 3, 0], "block": "gtceu:bronze_drum", "controller": true, "controller_props": false }
```

`--print` 会显示 `"props": {}`，确认没有被补朝向。判断方法：打开该机器的注册代码看
`.rotationState(...)`，或直接查生成的 blockstate json 有没有 `facing` 变体。

## 5. 自动生成流程

```bash
# 1) 写蓝图（JSON），LLM 只写这个可读文件
#    CTNH-Docs/ctnh-ponder/assets/storyboard-blueprint.template.json 是 3x3x4 土高炉的完整样例

# 2) 先干跑：只打印尺寸 / 地板 / 控制器，不落盘
python CTNH-Docs/ctnh-ponder/scripts/build_storyboard_nbt.py my_blueprint.json --print

# 3) 确认无误后产出 .nbt（输出路径取自蓝图 output，或用 -o 指定）
python CTNH-Docs/ctnh-ponder/scripts/build_storyboard_nbt.py my_blueprint.json

# 4) 校验已存在的文件（尺寸、越界、地板空洞、palette 未用项）
python CTNH-Docs/ctnh-ponder/scripts/build_storyboard_nbt.py --check <path>.nbt
```

脚本零依赖（Python 3 标准库 `json` / `struct` / `gzip`），输出确定：palette 与 blocks 排序、
gzip mtime 归零，同一份蓝图重复生成字节一致。

### 蓝图字段

| 字段 | 必填 | 说明 |
|------|------|------|
| `output` | 建议 | 目标 `.nbt` 路径，相对仓库根 |
| `age` | 是（或给 `floor`） | `mechanical` / `electric`，决定地板方块 |
| `floor` | 否 | 直接指定地板方块 id，覆盖 `age` |
| `floor_padding` | 否 | 每边外扩格数，默认 1 |
| `data_version` | 否 | 默认 3465 |
| `structure` | 是 | `{pos:[x,y,z], block:"id", props:{}, nbt:{}, controller:true}` 列表 |
| `controller_props` | 否 | 默认 `true`；`false` 时不给主方块补 `facing`/`upwards_facing`（见 4.1） |
| `entities` | 否 | 原样透传的实体列表 |

`props` 的值会转成字符串；需要非 int 的 NBT 类型时用带类型标记的对象，
例如 `{"__b":1}`（byte）、`{"__s":1}`（short）、`{"__l":1}`（long）、`{"__f":1.5}`（float）。

### 脚本会拦下的错误

- 没有 `controller: true` 的方块
- 结构块落在 `y=0`（与地板冲突）
- 坐标重复、越界、地板有空洞
- 同一方块同时用于地板与结构
- palette 里有从未被引用的条目
- `age` 取值非法且未显式给 `floor`

## 6. GT 管道：连接状态必须写进 NBT

GT 的管道（`gtceu:bronze_normal_fluid_pipe` 等 `FluidPipeBlock`）**不从邻居现算连接**，
而是把连接存成方块实体自己的位掩码字段：

```java
// PipeBlockEntity
@DescSynced @Persisted @RequireRerender
protected int connections = Node.ALL_CLOSED;   // 0b000000
```

渲染取的是它：`IPipeNode#getModelData` → `PIPE_CONNECTION_MASK` → `BakedPipeModel`。
Ponder 的 level **不跑 `serverTick`**，也没有"放下方块时自动连接"的逻辑，
所以只摆一个管道方块而不写 `connections`，场景里就是一根**光秃秃的中心柱**（看起来"没连上"）。

位 = `1 << Direction.ordinal()`，ordinal 顺序是
`DOWN=0, UP=1, NORTH=2, SOUTH=3, WEST=4, EAST=5`：

| 需要的连接 | 计算 | 值 |
|-----------|------|----|
| 上 + 下（竖直贯通，最常见） | `(1<<0)` + `(1<<1)` | `3` |
| 上 + 下 + 北 + 南 | `3 \| (1<<2) \| (1<<3)` | `15` |
| 只朝下 | `1<<0` | `1` |
| 全通 | `Node.ALL_OPENED` | `63` |

蓝图里写在方块的 `nbt` 中（键名就是字段名 `connections`，LDLib 的 `@Persisted` 默认用字段名）：

```json
{ "pos": [0, 2, 0], "block": "gtceu:bronze_normal_fluid_pipe",
  "nbt": { "id": "gtceu:bronze_normal_fluid_pipe", "connections": 3 } }
```

**验证方法**：`--check` 只校验几何，不会告诉你连接不对；要在游戏里 `/ponder <sceneId>`
看管道是否呈现"已连接"的粗管形状。管道方块**只有 `WATERLOGGED` 一个 blockstate 属性**，
连接形状是模型层的，所以不要试图用 `props` 表达连接。

## 7. 注意

- **不要手改 `src/generated/resources`**；只写 `src/main/resources/.../ponder/*.nbt`。
- 生成完仍要走 datagen 与游戏内确认：`runData` 只验证 lang，NBT 的观感、镜头、时序必须在
  游戏里用 `/ponder <sceneId>` 看；结构不显示时先看日志 `Ponder schematic missing`。
- `.nbt` 是二进制，不要用文本工具编辑；改结构就改蓝图重新生成。
