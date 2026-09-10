# CTPP MODULE

## OVERVIEW
CTPP（`CT++`）是 Create 与 GregTech 的联动模块，包根 `com.mo_guang.ctpp`，mod id `ctpp`，248 个 Java 文件。承载动能/电动多方块机器、Create 风扇催化处理、自定义配方 builder 与数据生成、GTCEu addon 注册，以及工具箱（Toolbox）与接线柱（Voltage Terminal）系统。入口类：`CTPP`（mod 主类）、`CTPPGTAddon`（GT addon）、`CTPPRegistration` / `CTPPRegistrate`（Registrate）、`CTPPEntityTypes`（实体）；代理为 `CommonProxy` / `ClientProxy`。

## STRUCTURE
源码根 `modules/CTPP/src/main/java/com/mo_guang/ctpp/`（括号内为该域 Java 文件数）。

```text
ctpp/
|-- CTPP.java / CTPPGTAddon.java / CTPPRegistration.java / CTPPRegistrate.java / CTPPEntityTypes.java
|-- api/                      # 17: StressRecipeCapability("su")、CTPPRecipeCapabilities/Conditions、CTPPParallelLogic、
|                              CTPPModifierFunction、CTPPMultiblockBuilder、CTPPPredicates、CTPPPartAbility、
|                              KineticMachineDefinition、IBlockStressValues、IEnergyTransferHandler；
|                              pattern/ (3: CTPPBlockMaps, FactoryStaticBlockPattern, StaticBlockPattern)；
|                              terminal/ (3: TerminalLinkState, TerminalProperties, TerminalWireGeometry)
|-- client/                   # 33: ClientProxy 与 9 个顶层渲染/Visual 类；ponder/ (9)、renderer/ (7)、
|                              terminal/ (2)、toolbox/ (5)
|-- common/                   # 71: CommonProxy；beam/ (4)、block/ (7)、blockentity/ (5)、command/ (2)、
|                              condition/ (2)、data/ (2)、gui/widget/ (1)、item/ (4)、kinetic/fan/ (5)、
|                              machine/ (18)、menu/ (3)、terminal/ (4)、toolbox/ (13)
|-- config/                   # 2: MainConfig, ConfigUtils
|-- data/                     # 52: CTPPDatagen, CuriosTags, ToolboxBlockstates；tags/ (4)、recipe/ (45)
|   |-- recipe/               # 12 顶层 + builder/ (6 顶层 + create/ 11 + diesel/ 4 + vintage/ 10) + fanprocessing/ (2)
|-- dynamicPart/              # 10: 旋转魔杖、移动/旋转 contraption 与渲染器；moving/ (1)、rotation/ (5)
|-- event/                    # 2: ForgeEventHandler, PlaceableEmitterEventHandler
|-- integration/              # 5: jade/ (1)、jei/ (3)、ldlib/ (1)
|-- mixin/                    # 21: create/ (15 = 顶层 5 + diesel/ 4 + fix/ 2 + jei/ 4)、gtm/ (1)、mc/ (1)、顶层 4
|-- network/packet/           # 11: 工具箱、接线柱选线、发射器光束
|-- registry/                 # 12: Registrate 物品/方块/BE/机器/多方块/菜单/网络/配方类型与修饰符、
|                              CreateMaterials、GTMaterialAddon
|-- syncdata/                 # 1: TerminalLinkStateAccessor
`-- util/                     # 6: CommonTooltips, ICustomSlot, IMatrix3dAccessor, IWorkingMachineStep,
                              ItemAxisBuilder, MathUtil
```

已移除项：`CTPPValues`（机械等级改用 `GTValues.VNF`）、`integration/emi`（迁至 CTNH-Core）、`KineticOutputMachineProvider`、转子支架（rotor holder）Mixin、`OreProcessingRecipes`。

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| mod 入口 / GT addon / Registrate | `CTPP.java`, `CTPPGTAddon.java`, `CTPPRegistration.java`, `CTPPRegistrate.java` |
| 公共 API 面 | `api/`（17），含 `api/terminal/TerminalWireGeometry.java` |
| 动态 contraption | `dynamicPart/`（10） |
| 配方实现 | `data/recipe/`（顶层 12，不在 `common/` 下） |
| 风扇催化处理 | 类型 `data/recipe/fanprocessing/`；配方类 `common/kinetic/fan/{acidwashing,breathing,oiling}/` |
| 工具箱系统 | `common/toolbox/`（13）、`common/menu/`、`network/packet/` 工具箱包、`client/toolbox/` UI |
| 可放置发射器 | `common/machine/simple/PlaceableEmitterMachine.java`、`event/PlaceableEmitterEventHandler.java`、`data/recipe/PlaceableEmitterRecipes.java` |
| 反射镜与光束 | `common/block/MirrorBlock.java`、`common/beam/` |
| 接线柱与线缆 | `api/terminal/`、`common/terminal/`、`common/blockentity/VoltageTerminalBlockEntity.java`、`client/renderer/VoltageTerminalRenderer.java`、`syncdata/` |
| 客户端 Ponder / 渲染 | `client/ponder/`（9）、`client/renderer/`（7） |
| Mixin | `mixin/`、`src/main/resources/ctpp.mixins.json` |
| 生成资源（444 个 JSON） | `src/generated/resources/`（`assets/ctpp/` 与 `data/{ctpp,create,curios,forge,gtceu,minecraft}/`） |
| 静态资源 | `src/main/resources/assets/ctpp/` |

## RECIPE TYPES
CTPP 定义两族配方类型：动能/电动机器用 GT 风格 `GTRecipeType`，风扇催化处理用 Create 风格 `ProcessingRecipe`。

### GT Recipe Types（`registry/CTPPRecipeTypes.java`）
经 `CTPPRegistration.REGISTRATE.recipeType(...)` 注册；动能族使用 `StressRecipeCapability`（key `"su"`，Float）而非 EU，配合 `RPMCondition` + `MechanicalTierCondition`。

| Constant | Registry ID | 中文 | Group | I/O items | I/O fluids | Notes |
|---|---|---|---|---|---|---|
| `KINETIC_MIXER_RECIPES` | `kinetic_mixer` | 应力搅拌 | KINETIC | 6/1 | 2/1 | 类型已注册；`MIXER_RECIPES` 的转换挂钩在 `init()` 中被注释掉 |
| `SMASHING_FACTORY_RECIPES` | `smashing_factory_recipes` | 粉碎工厂 | KINETIC | 1/4 | 0/0 | 由 `MACERATOR_RECIPES` 自动生成；剥离概率输出；等级取 `min(getTierByVoltage(eut), 5)`，应力/RPM/速度倍率读 `MainConfig` |
| `KINETIC_GENERATOR_RECIPES` | `kinetic_generator` | 应力发电 | KINETIC | 0/0 | 1/0 | 应力 → EU；输出上限 `tier > 0 ? tier*4*V[tier] : 32` |
| `KINETIC_STEAM_TURBINE_RECIPES` | `kinetic_steam_turbine` | 蒸汽动力 | KINETIC | 0/0 | 1/1 | 蒸汽 → EU |
| `SEAWEED_FARM` | `seaweed_farm` | 海草养殖 | ELECTRIC | 2/4 | 0/1 | 多方块 |
| `WINDMILL_CONTROL` | `windmill_control_center` | 风车控制中心 | ELECTRIC | 0/0 | 1/0 | 多方块 |
| `BOOM_OF_CREATE` | `boom_of_create` | 聚爆应力 | KINETIC | 1/0 | 1/0 | EU 输入 + 爆炸催化 → 应力；`setEUIO(IO.IN)` |
| `BIG_DAM` | `big_dam`（GTCEu 命名空间） | 三峡大坝 | ELECTRIC | 0/0 | 1/0 | 经 `GTCEu.id(...)` 注册 |

### Create 风扇处理配方（`data/recipe/fanprocessing/CTPPRecipeTypeInfo.java`）
实现 Create 的 `IRecipeTypeInfo`，经 `DeferredRegister` 注册在 `ctpp` 命名空间；`CTPPFanProcessingTypes.java` 持有对应的 `FanProcessingType` 注册对象。

| Enum | ID | Max In/Out | Purpose |
|---|---|---|---|
| `BREATHING` | `ctpp:breathing` | 1/12 | 风扇吹拂催化剂 |
| `ACIDWASHING` | `ctpp:acidwashing` | 4/12 | 风扇酸洗催化剂 |
| `OILING` | `ctpp:oiling` | 1/12 | 风扇涂油催化剂（`OilingRecipe.matches()` 当前恒为 `false`） |

### 包装 Create / 附属 mod 的配方 builder（`data/recipe/builder/`）
这些不是新配方类型，产出标准 Create / 附属 mod 的配方 JSON。

**Create 原生（11 个）**——直接写 JSON，`type` 为 `create:<name>`：

| Builder | Recipe type | Notes |
|---|---|---|
| `CompactingRecipeBuilder` | `create:compacting` | 物品/流体 I/O，heated/superheated |
| `CrushingRecipeBuilder` | `create:crushing` | 逐条概率输出 |
| `CuttingRecipeBuilder` | `create:cutting` | 物品 I/O |
| `FillingRecipeBuilder` | `create:filling` | 物品/流体 I/O，支持字符串流体 ID |
| `ItemApplicationRecipeBuilder` | `create:item_application` | 物品 I/O（部署器式） |
| `MechanicalCraftingRecipeBuilder` | `create:mechanical_crafting` | 带 key 的成形图案 |
| `MillingRecipeBuilder` | `create:milling` | 逐条概率输出；`processingTime` 默认 100，必须为正 |
| `MixingRecipeBuilder` | `create:mixing` | 物品/流体 I/O，heated/superheated |
| `PressingRecipeBuilder` | `create:pressing` | 物品 I/O |
| `SequencedAssemblyRecipeBuilder` | `create:sequenced_assembly` | 多步（filling / pressing / deploying / cutting / curving），经 `AllRecipeTypes.SEQUENCED_ASSEMBLY` 取序列化器 |
| `SplashingRecipeBuilder` | `create:splashing` | 物品 I/O |

**Create Diesel Generators（4 个）**——继承 `CTPPProcessingRecipeBuilder`：

| Builder | Target recipe class | Mod |
|---|---|---|
| `BasinFermentingRecipeBuilder` | `BasinFermentingRecipe` | createdieselgenerators |
| `DistillationRecipeBuilder` | `DistillationRecipe` | createdieselgenerators |
| `HammerRecipeBuilder` | `HammerRecipe` | createdieselgenerators |
| `WireCuttingRecipeBuilder` | `WireCuttingRecipe` | createdieselgenerators |

**Vintage Improvements（8 个）**——继承 `AbstractVintageRecipeBuilder`，经 `VintageRecipes` 枚举取类型；`builder/vintage/` 共 10 个文件（8 个 builder + 抽象基类 + `VintageRecipeResult`）：`CentrifugationRecipeBuilder`（`CENTRIFUGATION`）、`CoilingRecipeBuilder`（`COILING`）、`CurvingRecipeBuilder`（`CURVING`）、`HammeringRecipeBuilder`（`HAMMERING`）、`PressurizingRecipeBuilder`（`PRESSURIZING`）、`TurningRecipeBuilder`（`TURNING`）、`VacuumizingRecipeBuilder`（`VACUUMIZING`）、`VibratingRecipeBuilder`（`VIBRATING`）；均支持物品/流体 I/O + RPM + 热量。

### 自定义配方基础设施
- **Capability** `StressRecipeCapability`（key `"su"`，Float）——GT 配方的动能应力 I/O，驱动 `KineticWorkableMultiblockMachine` / `KineticOutputMachine` 的并行计算；注册入口 `CTPPRecipeCapabilities.init()`（由 `CTPPGTAddon.registerRecipeCapabilities()` 调用）。Lang key 为 `ctpp.stressrecipecapability.{capabilityname,stressconsumption,stressproduction,stressinput,stressoutput}`（旧 `recipe.capability.su.name`、`ctpp.top.*` 已移除）。
- **Conditions** `RPMCondition`（`"rpm"`）与 `MechanicalTierCondition`（`"mechanical_tier"`）——动能配方的转速/等级要求；`MechanicalTierCondition` 用 `GTValues.VNF[tier]` 显示。
- **Modifiers** `KINETIC_PARALLEL`（应力倍数 + 精确并行）与 `KINETIC_PERFECT_PARALLEL`（完美并行变体）——两者都只作用于 `KineticWorkableMultiblockMachine`。
- **Recipe builder** `CTPPRecipeBuilder` 扩展 `GTRecipeBuilder`，提供 `.rpm(float)`、`.rpm(float, boolean)`、`.mechanicalTier(int)`、`.inputStress(float)`、`.outputStress(float)`、`.noEUt()`。
- 应力 I/O **没有** KubeJS recipe key 通道：`CTPPGTAddon` 无 `registerRecipeKeys()`，不存在 `SU_IN` / `SU_OUT`。

## ARCHITECTURE CONTRACT
机器/trait/capability/Jade 的所有权边界、字段同步与持久化规则、Jade 数据最小化原则与迁移步骤见 `references/_architecture/AGENTS.md`。改动机器、trait、recipe capability 或 Jade 前先读它；本文件只描述本模块的落点。

## DOMAIN GUIDE ROUTING
| Source area | Guide | Read before |
|-------------|-------|-------------|
| `api/**` | `ctnh-docs/references/CTPP/api/AGENTS.md` | 暴露 recipe capability、多方块构建器、谓词、接线柱线缆几何 |
| `client/**` | `ctnh-docs/references/CTPP/client/AGENTS.md` | 改动 Ponder 场景、渲染器、工具箱 UI |
| `common/**` | `ctnh-docs/references/CTPP/common/AGENTS.md` | 改动代理、机器、动能逻辑、工具箱、风扇处理、反射镜/发射器 |
| `config/**` | `ctnh-docs/references/CTPP/config/AGENTS.md` | 新增或修改模块配置项 |
| `data/**` | `ctnh-docs/references/CTPP/data/AGENTS.md` | 改动配方 provider、tag、模型 |
| `dynamicPart/**` | `ctnh-docs/references/CTPP/dynamicPart/AGENTS.md` | 改动移动/旋转 contraption |
| `event/**` | `ctnh-docs/references/CTPP/event/AGENTS.md` | 新增 Forge 事件处理器 |
| `integration/**` | `ctnh-docs/references/CTPP/integration/AGENTS.md` | 对接 JEI / Jade / LDLib |
| `mixin/**` | `ctnh-docs/references/CTPP/mixin/AGENTS.md` | 给 Create / GT / MC 打补丁 |
| `network/**` | `ctnh-docs/references/CTPP/network/AGENTS.md` | 新增或修改网络包 |
| `registry/**` | `ctnh-docs/references/CTPP/registry/AGENTS.md` | 新增物品、方块、BE、机器、配方类型 |
| `syncdata/**` | `ctnh-docs/references/CTPP/syncdata/AGENTS.md` | 改动接线柱链路同步 |
| `util/**` | `ctnh-docs/references/CTPP/util/AGENTS.md` | 复用共享工具而非另起实现 |

## CONVENTIONS
- 命名空间为 `com.mo_guang.ctpp`；类前缀统一 `CTPP`。
- **GTM 动态包**：GT/GMT 配方经 `CTPPGTAddon.addRecipes()` → `CTPPRecipes.init(provider)` 注册为运行时动态数据包（`GTDynamicPackContents` / CTNH-Lib `CTNHDynamicDataPack`），`runData` 对其**不产出 JSON**；静态 `src/generated/resources` 只含 tags/lang/models/worldgen/非 GT 配方。验证方式为游戏内或 `ConfigHolder.dev.dumpRecipes`。
- **注册对象优先**：引用物品/方块/流体**必须**用静态注册对象（`GTMaterials.Iron`, `CTPPBlocks.MY_BLOCK`, `TagPrefix.ingot`, `AEItems.X`, `CBBlocks.X`, `CEItems.X`, `CMItems.X`, `CABlocks.X`, `CTPPBlocks.X`），**禁止** `ResourceLocation` 字符串解析 + `ForgeRegistries` 查找；字符串 ID 仅限无注册对象的场景（上游 mod 专属 ID、配方 ID、tag key、维度 ID）。
- **应力是独立 capability**：动能 I/O 只走 `StressRecipeCapability`（`"su"`）；并行上限、显示与 Jade 提示都由该 capability 与 `NotifiableStressTrait` 承担。
- **动能机器同速约束**：所有输入仓必须以相同转速运行（`KineticWorkableMultiblockMachine.checkInputSpeedConsistent()`，容差 0.01）；`RPMCondition` 用 `Math.abs(speed)` 判定。
- 配方生成落在顶层 `data/recipe/`（不存在 `common/data/recipe`）。
- `src/generated/resources` 含大量 Create/Forge/Minecraft tag 产物；静态机器部件模型另在 `src/main/resources`，编辑或重生成前先确认路径。
- Create 动能行为由 Mixin 与 `dynamicPart/` 的 contraption 类共同打补丁；改旋转或移动方块行为需同时看两处。

## ANTI-PATTERNS
- 把所有配方 JSON 等同看待：风扇催化产物与静态资源位于不同源码根，GT 配方根本不在 JSON 里。
- 改动能/电动机器等级时只改注册代码，不核对生成的模型与配方。
- 用裸 JSON 键添加应力 I/O，或引用不存在的 KubeJS recipe key（`SU_IN` / `SU_OUT`）。
- 用字符串 ID + `ForgeRegistries` 查找代替已存在的静态注册对象。
- 期望 `runData` 产出 GT 配方 JSON 并据此验证配方。

## COMMANDS
```text
./gradlew :modules:CTPP:build
./gradlew :modules:CTPP:runData
./gradlew :modules:CTPP:spotlessCheck
```

## SCOPE
本模块覆盖 CTPP 的动能/电动机器、Create 联动配方与 builder、数据生成、注册面、客户端渲染与上游 mod 补丁。本文件是经根路由表加载的参考指南，不是额外的源码树指令文件。

## READ WHEN
- 新增或修改动能/电动机器、风扇催化配方或配方 builder。
- 通过 Mixin 或 `dynamicPart/` 改动 Create 动能行为。
- 改动工具箱系统或接线柱/线缆系统。
- 新增注册对象或调整数据生成产物。

## SOURCE OF TRUTH
- 注册与生命周期：`CTPP.java`、`CTPPGTAddon.java`、`common/CommonProxy.java`。
- 配方类型：`registry/CTPPRecipeTypes.java`、`data/recipe/fanprocessing/CTPPRecipeTypeInfo.java`、`data/recipe/builder/`。
- Forge 元数据与 Mixin 配置：`src/main/resources/META-INF/mods.toml`、`src/main/resources/ctpp.mixins.json`。

## WORKFLOW
1. 把改动落到正确域，并读对应域的 `AGENTS.md`（见 DOMAIN GUIDE ROUTING）。
2. 核对 GT addon 挂钩顺序、recipe capability 注册与 datagen 引用。
3. 跑最窄的 Gradle 任务（datagen 用 `runData`，编译用 `build`）。
4. 引入新模块边界时回读本文档的路由表。
