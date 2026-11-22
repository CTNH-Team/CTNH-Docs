# CTNH-ASTRAL CLIENT DOMAIN

## OVERVIEW
Astral 的客户端启动与渲染（6 个 Java 文件）：`ClientProxy`（客户端代理，继承 `CommonProxy`）、`RocketLaunchHud`（火箭发射 HUD）、`CelestialSelectionScreen`（星图选点界面）、`MoonEffects`（五个 Astral 维度的天空效果）、`SiliconCrystalColors`（硅晶方块位置着色）、`ClientEnvironmentTemperature`（服务端温度快照的客户端缓存）。

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| 客户端代理与事件注册 | `client/ClientProxy.java` |
| 维度天空效果注册 | `client/ClientProxy.registerDimensionEffects` → `moon`, `mars`, `venus`, `astral_planet`, `astral_orbit` |
| `galaxy` 着色器 | `client/ClientProxy.registerShaders`, `ClientProxy.getGalaxyShader()`；资源 `assets/ctnhastral/shaders/core/galaxy.{json,fsh,vsh}` |
| 硅晶方块 / 物品着色 | `client/ClientProxy.registerSiliconBlockColors` / `registerSiliconItemColors`, `client/render/SiliconCrystalColors.color(x, y, z, saturation)` |
| 火箭 HUD | `client/RocketLaunchHud.java`；贴图 `assets/ctnhastral/textures/gui/rocket_booster.png` |
| 星图选点界面 | `client/gui/screen/CelestialSelectionScreen.java`；贴图 `assets/ctnhastral/textures/gui/selection_cursor.png` 与 `textures/gui/celestialbodies/*.png` |
| 维度天空渲染 | `client/render/MoonEffects.java` |
| 客户端温度快照 | `client/ClientEnvironmentTemperature.java` |

## CONVENTIONS
- `ClientProxy` 构造时先 `super()` 再执行 `MinecraftForge.EVENT_BUS.addListener(RocketLaunchHud::render)`，随后调用 `init()`（当前为空实现）；客户端钩子一律挂在这里。
- `ClientProxy` 为 `moon` / `mars` / `venus` / `astral_planet` / `astral_orbit` 五个维度效果 id 各注册一个 `new MoonEffects()`；新增 Astral 维度时同步补这一处的 `event.register(...)`。
- `MoonEffects` 标注 `@OnlyIn(Dist.CLIENT)`，继承 `DimensionSpecialEffects`（`SkyType.NORMAL`），用 `ClientProxy.getGalaxyShader()` 绘制星空球（半径 512，48 stacks × 96 slices），并向着色器传入 `GameTime` 与 `CameraYawPitch` uniform；着色器为 `null` 时跳过绘制。不得从 common 构造路径触达。
- `MoonEffects` 的 `getBrightnessDependentFogColor` 返回 `Vec3.ZERO`、`isFoggyAt` 返回 `false`、`getSunriseColor` 返回 `null`——修改天空观感时这三个覆写要一起考虑。
- `ClientProxy` 的着色器回调把 `galaxy` 实例写进 `private static ShaderInstance galaxyShader`（Lombok `@Getter`），自定义着色器只走 `RegisterShadersEvent`，不要另建加载路径。
- 硅晶着色是位置连续函数：`SiliconCrystalColors.color(...)` 只用坐标与饱和度算 hue / strength，不读世界种子、方块实体或动画 tick；`IRIDESCENT_SILICON_CRYSTAL` 饱和度 `.78`、`SILICON_CRUST` `.30`、`SILICON_GRAVEL` `.40`，非 0 tint 层直接返回 `-1`。
- `RocketLaunchHud` 为工具类（私有构造 + 静态 `render`）：通过乘客链查找 `RocketContraptionEntity`，未组装或正在降落时直接返回；未发射时显示跳跃键提示与 `rocket_booster.png` 图标，发射中在屏幕中央显示倒计时秒数，并在屏幕左侧按 `CASpaceConstants.ORBIT_ALTITUDE` 绘制高度进度条。文案用 `@Key/@EN/@CN` 注解的 `Lang` 字段声明，不硬编码字符串。
- `CelestialSelectionScreen` 只负责绘制与请求：按 `CelestialBody.position()` 逐级叠加父天体位置算出星图坐标，悬停显示名称提示，左键可选中天体时发 `C2STeleportToBodyPacket` 并关屏；目标校验、tier 判定与传送全部在服务端 `CelestialTravelHandler`。`isPauseScreen()` 返回 `false`。
- `ClientEnvironmentTemperature` 是唯一的客户端温度来源：`celsius(level, pos)` 在无快照时返回 `Float.NaN`（不以维度底数冒充当前温度），每 20 tick 重新请求一次，缓存超过 2048 条时清理 100 tick 前的读数；`receive(...)` 把服务端开尔文转摄氏度；切换世界或登出（`ClientPlayerNetworkEvent.LoggingOut`）时清空。

## ANTI-PATTERNS
- 让仅客户端的类可从 common 路径触达。
- 在 `MoonEffects` 里硬编码单个维度的天空逻辑；维度效果通过 `ClientProxy.registerDimensionEffects` 绑定。
- 在 HUD 或星图界面直接持有服务端状态或自行发新网络包——数据一律走既有 packet 记录与 `RocketContraptionEntity` 的同步字段。
- 在客户端用维度基准温度兜底展示；无快照时必须返回 `NaN` 并触发重新请求。
- 给硅晶着色引入随机数或 `Math.random()` 之类按帧变化的输入，破坏相邻面的连续光谱。

## SCOPE
适用于 `src/main/java/com/ctnh/ctnhastral/client` 及其子包。

## READ WHEN
- 修改 Astral 维度天空效果、`galaxy` 着色器、火箭 HUD、星图界面或客户端渲染。
- 新增客户端事件监听、渲染层或颜色处理器。

## SOURCE OF TRUTH
- `client/` 下的类，以及 `CTNHAstral` 里 `DistExecutor.unsafeRunForDist` 的代理选择。

## WORKFLOW
1. 先确认客户端代理接线在 `CTNHAstral` 的 `DistExecutor.unsafeRunForDist` 路径上。
2. 新增维度时同时补 `ClientProxy.registerDimensionEffects` 与 `ClientProxy` 的渲染接线。
3. 跑 `:modules:CTNH-Astral:build`；渲染 / Sky / HUD 变更需进 `runClient` 实际观察。
