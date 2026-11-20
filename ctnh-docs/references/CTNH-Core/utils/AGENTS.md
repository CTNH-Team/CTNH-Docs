# CTNH-CORE UTILS DOMAIN

## OVERVIEW
Core 的共享辅助工具（9 个 Java 文件）：tooltip、机器工具、配方辅助、光伏倍率、数学与结构工具。

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Tooltip | `utils/CTNHCommonTooltips.java` |
| 机器工具 | `utils/CTNHMachineUtils.java`, `utils/CoilTierHelper.java` |
| 配方辅助 | `utils/CTNHRecipeHelper.java` |
| 数据结构 | `utils/LayeredBiMap.java`, `utils/OrientedItem.java` |
| 光伏维度倍率 | `utils/CTNHCelestialPower.java` |
| 数学/结构 | `utils/MathUtils.java`, `utils/StructureUtils.java` |

## CONVENTIONS
- 辅助方法默认静态；需要状态时才用实例，并尽量不依赖注册表。
- 机器注册工厂集中在 `CTNHMachineUtils`：`registerTieredMachines(name, factory, builder, tiers...)`、`registerSimpleMachines(...)`、`registerSimpleComputationMachines(...)`、`registerEfficiencyGeneratorMachines(...)`、`registerTieredMultis(...)`、`registerLargeCombustionEngine(name, tier, ..., cnName)`。
- 分级机器中文名走 `registerTieredMachines(name, cnname, factory, builder, tiers...)` 重载，内部 `.cnLangValue(VNF[tier] + cnname)`；需要逐级独立中文名的机器用带 `cnname` 的形式，不要另起一套 `@Key` + `Lang` 字段。
- `registerLargeCombustionEngine` 的 `cnName` 是必填形参，直接 `.cnLangValue(cnName)`。
- 光伏倍率统一从 `CTNHCelestialPower` 取：`solarFactor(Level)` 用 CTNH-Astral `CACelestialBodies.EARTH.solarPower() / body.solarPower()` 的平方（光照越弱倍率越高；维度不在天体表或光照非正时返回 0），`photovoltaicRate(Level)` 给整数倍率（主世界/暮色森林/精灵乡 1、以太 2、其余按 `solarFactor` 四舍五入且下限 1，`solarFactor` 为 0 时给 0），`solarMultiplier(Level)` 给倍数（主世界/暮色森林/精灵乡 0.5、以太 1.0、卫星维度乘 `ORBIT_BONUS` = 4、其余取 `solarFactor`，`solarFactor` 为 0 时给 1.0），`isOrbit(Level)` 判天体是否卫星。`PhotovoltaicPowerStationMachine`、`PhotoVoltaicDroneStation`、`SpacePhotovoltaicBaseStation` 都从这里取倍率。

## ANTI-PATTERNS
- 重复实现 CTNH-Lib `utils/` 已有的辅助。
- 在这里加玩法逻辑；utils 只放共享机制。
- 绕过 `CTNHMachineUtils` 的工厂另写一份分级机器注册与翻译声明。

## SCOPE
适用于 `src/main/java/io/github/cpearl0/ctnhcore/utils`。

## READ WHEN
- 需要复用 Core 范围的 tooltip、机器或配方逻辑。

## SOURCE OF TRUTH
- `utils/` 下的工具类；共享 CTNH 辅助见 `references/CTNH-Lib/utils/AGENTS.md`。

## WORKFLOW
1. 先在 CTNH-Lib `utils/` 里找现成共享辅助。
2. 只有在 Lib 共享不合适时才在此加 Core 专属辅助。
3. 改动后跑 `:modules:CTNH-Core:build`。
