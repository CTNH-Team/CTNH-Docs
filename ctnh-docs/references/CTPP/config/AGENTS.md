# CTPP CONFIG DOMAIN

## OVERVIEW
CTPP 的模块配置（2 个 Java 文件），基于 `dev.toma.configuration` 的 `@Config` 体系，配置 id 为 `ctpp`。

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| 配置定义 | `config/MainConfig.java`（`@Config(id = CTPP.MODID)`，`INSTANCE` 持有 `gtmConfig` 与 `ctnhConfig` 两组） |
| 配置读取助手 | `config/ConfigUtils.java`（`gtmEnabled(machineName)` / `ctnhEnabled(machineName)`，按 `enable + machineName` 反射取字段） |
| 配置项 lang | `MainConfig` 中的 `@Key` + `@CN` / `@EN` `Lang` 字段（如 `config.ctpp.option.enableGTMKineticOutputBox`） |
| 初始化 | `common/CommonProxy` 构造函数中调用 `MainConfig.init()` |

## CONVENTIONS
- 配置项统一走 `MainConfig`；读取用 `ConfigUtils.gtmEnabled(...)` / `ctnhEnabled(...)`，不要自行反射或直读字段。
- `SMASHING_FACTORY_RECIPES` 的应力需求、RPM 需求、速度倍率与最大处理等级都从 `MainConfig.INSTANCE.ctnhConfig` 读取（见 `CTPPRecipeTypes.init()`）。
- 配置初始化早于注册流程（`CommonProxy` 构造中 `init()` → `CTPPNetwork.init()` → `MainConfig.init()`）。

## ANTI-PATTERNS
- 在配置初始化之前读取配置值。
- 绕过 `ConfigUtils` 直接按字段名反射访问配置组。
- 新增配置项不加 `@Key` / `@CN` / `@EN`，导致配置界面无文案。

## SCOPE
适用于 `src/main/java/com/mo_guang/ctpp/config`。

## READ WHEN
- 新增或修改 CTPP 的配置项。
- 改动应力搅拌/粉碎工厂等由配置驱动的机器或配方参数。

## SOURCE OF TRUTH
- `config/MainConfig.java` 的字段定义。
- `common/CommonProxy.java` 中的初始化顺序。

## WORKFLOW
1. 在 `MainConfig` 中加字段并补齐 `@Key` / `@CN` / `@EN`。
2. 读取侧统一走 `ConfigUtils`。
3. 跑 `:modules:CTPP:build`；配置界面在游戏内确认。
