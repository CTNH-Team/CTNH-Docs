# CTPP API DOMAIN

## OVERVIEW
CTPP 的公共 API 面（17 个 Java 文件）：应力 recipe capability、GT 配方类型条件注册、多方块构建器与图案谓词、动能并行计算、动能机器定义，以及接线柱线缆几何。

## STRUCTURE
```text
api/
|-- CTPPModifierFunction.java, CTPPMultiblockBuilder.java, CTPPParallelLogic.java
|-- CTPPPartAbility.java, CTPPPredicates.java
|-- CTPPRecipeCapabilities.java, CTPPRecipeConditions.java
|-- IBlockStressValues.java, IEnergyTransferHandler.java, KineticMachineDefinition.java, StressRecipeCapability.java
|-- pattern/                   # CTPPBlockMaps, FactoryStaticBlockPattern, StaticBlockPattern
`-- terminal/                  # TerminalLinkState, TerminalProperties, TerminalWireGeometry
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| 应力 capability | `api/StressRecipeCapability.java`（key `"su"`，Float；`CAP` 单例） |
| capability 注册 | `api/CTPPRecipeCapabilities.java`（`SU` 是 `StressRecipeCapability.CAP` 的别名，`init()` 注册进 `GTRegistries.RECIPE_CAPABILITIES`） |
| 配方条件注册 | `api/CTPPRecipeConditions.java`（`RPM` → `"rpm"`、`MECHANICAL_TIER` → `"mechanical_tier"`；实现类在 `common/condition/`） |
| 多方块构建器 | `api/CTPPMultiblockBuilder.java` |
| 动能并行 | `api/CTPPParallelLogic.java`（`getKineticParallelAmount`） |
| 配方修饰函数 | `api/CTPPModifierFunction.java`（`inputStressMultiplier`, `accurateParallel`） |
| 动能机器定义 | `api/KineticMachineDefinition.java`, `api/IBlockStressValues.java`, `api/IEnergyTransferHandler.java` |
| part 能力与高亮色 | `api/CTPPPartAbility.java`（`INPUT_KINETIC` / `OUTPUT_KINETIC` / `MECHANICAL_UPGRADE`，由 `CTPPGTAddon.registerMultiblockPreviewHighlighters()` 注册预览高亮） |
| 图案谓词 / 方块映射 | `api/CTPPPredicates.java`, `api/pattern/{CTPPBlockMaps, FactoryStaticBlockPattern, StaticBlockPattern}` |
| 线缆几何 | `api/terminal/TerminalWireGeometry.java`（`points()` / `bounds()` / `radius()` / `segmentCount()`） |
| 线缆同步状态 | `api/terminal/TerminalLinkState.java`（`@DescSynced` + `@Persisted` 托管字段）、`api/terminal/TerminalProperties.java` |

## CONVENTIONS
- `StressRecipeCapability`（key `"su"`，Float）是动能应力 I/O 与并行上限的唯一入口：`getMaxParallelByInput` 汇总 `NotifiableStressTrait` 的输入应力后除以配方应力；`limitMaxParallelByOutput` 按输出应力收口。
- 并行计算统一走 `CTPPParallelLogic.getKineticParallelAmount(group, recipe, limit, perfect)`：非 perfect 模式对输入并行取平方根，再经 `limitByOutputMerging` 收口。不要在机器子类里重算。
- `CTPPRecipeBuilder`（在 `data/recipe/builder/`）扩展 `GTRecipeBuilder`，提供 `.rpm(float)`、`.rpm(float, boolean)`、`.mechanicalTier(int)`、`.inputStress(float)`、`.outputStress(float)`、`.noEUt()`。
- `TerminalWireGeometry` 是悬链线下垂（`sag = min(2.5, length * 0.08)`）与线径（`0.035 * sqrt(multiplier)`）的唯一来源；渲染器与碰撞检测都必须调用它。
- 应力 I/O 没有 KubeJS recipe key 通道：`CTPPGTAddon` 无 `registerRecipeKeys()`，不存在 `SU_IN` / `SU_OUT`。

## ANTI-PATTERNS
- 用裸 JSON 键拼应力 I/O；必须经 `StressRecipeCapability` + `CTPPRecipeBuilder`。
- 把线缆几何数学复制到 `client/renderer/VoltageTerminalRenderer` 或 `common/terminal/TerminalWireHazardManager`；一律调用 `TerminalWireGeometry.points()` / `bounds()`。
- 把只服务单一域的实现塞进 `api/`。

## SCOPE
适用于 `src/main/java/com/mo_guang/ctpp/api` 及其子包。

## READ WHEN
- 暴露动能/电动机器 API 或 recipe capability 契约。
- 改动接线柱线缆渲染或碰撞判定。
- 改动 GT 配方条件或动能并行计算入口。

## SOURCE OF TRUTH
- `api/` 契约与 `api/CTPPRecipeCapabilities.java` 的注册接线。
- `api/terminal/TerminalWireGeometry.java` 的线缆数学。

## WORKFLOW
1. 确认该面确实被跨域共享，再放进 `api/`。
2. 核对 `registry/` 中 capability / 条件 / 修饰符的注册接线。
3. 跑 `:modules:CTPP:build`。
