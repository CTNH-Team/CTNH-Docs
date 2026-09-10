# CTNH-ASTRAL CLIENT DOMAIN

## OVERVIEW
Astral 的客户端启动与渲染（3 个 Java 文件）：`ClientProxy`（客户端代理，继承 `CommonProxy`）、`RocketLaunchHud`（火箭发射 HUD）、`render/MoonEffects`（月球维度天空效果）。

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| 客户端代理与事件注册 | `client/ClientProxy.java` |
| 维度天空效果注册 | `client/ClientProxy.registerDimensionEffects` → `ctnhastral:moon` |
| `galaxy` 着色器 | `client/ClientProxy.registerShaders`, `ClientProxy.getGalaxyShader()`；资源 `assets/ctnhastral/shaders/core/galaxy.json` |
| 火箭 HUD | `client/RocketLaunchHud.java` |
| 月球天空渲染 | `client/render/MoonEffects.java` |

## CONVENTIONS
- `ClientProxy` 构造时先 `super()` 再执行 `MinecraftForge.EVENT_BUS.addListener(RocketLaunchHud::render)`，随后调用 `init()`；客户端钩子一律挂在这里。
- `MoonEffects` 标注 `@OnlyIn(Dist.CLIENT)`，继承 `DimensionSpecialEffects`，用 `ClientProxy.getGalaxyShader()` 绘制星空球（半径 512，48 × 96 分段）并叠绘 Ad Astra 的 `textures/environment/earth.png`；不得从 common 构造路径触达。
- `MoonEffects` 的 `getBrightnessDependentFogColor` 返回 `Vec3.ZERO`、`isFoggyAt` 返回 `false`、`getSunriseColor` 返回 `null`——修改天空观感时这三个覆写要一起考虑。
- `RocketLaunchHud` 为工具类（私有构造 + 静态 `render`）：通过乘客链查找 `RocketContraptionEntity`，未组装或正在降落时直接返回；未发射时显示跳跃键提示，发射中显示倒计时数字与高度进度条（进度基于 `AdAstraConfig.atmosphereLeave`）。文案用 `@Key/@EN/@CN` 注解的 `Lang` 字段声明，不硬编码字符串。
- HUD 贴图直接引用 Ad Astra 的 `textures/gui/sprites/overlay/rocket_bar.png` 与 `rocket.png`，不复制到本模块资源目录。

## ANTI-PATTERNS
- 让仅客户端的类可从 common 路径触达。
- 在 `MoonEffects` 里硬编码月球之外维度的天空逻辑；维度效果通过 `ClientProxy` 注册表绑定。
- 在 HUD 中直接持有服务端状态或自行发网络包——数据一律走 `RocketContraptionEntity` 的同步字段。

## SCOPE
适用于 `src/main/java/com/ctnh/ctnhastral/client` 及其子包。

## READ WHEN
- 修改 Astral 维度天空效果、`galaxy` 着色器、火箭 HUD 或客户端渲染。
- 新增客户端事件监听或渲染层注册。

## SOURCE OF TRUTH
- `client/` 下的类，以及 `CTNHAstral` 里 `DistExecutor` 的代理选择。

## WORKFLOW
1. 先确认客户端代理接线在 `CTNHAstral` 的 `DistExecutor.unsafeRunForDist` 路径上。
2. 跑 `:modules:CTNH-Astral:build`；渲染/Sky 变更需进 `runClient` 实际观察。
