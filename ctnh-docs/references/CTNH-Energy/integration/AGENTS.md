# CTNH-ENERGY INTEGRATION DOMAIN

## OVERVIEW
外置 mod 对接（9 个 Java 文件）：EMI 插件与 EU 堆叠适配、Jade 的 AE 设备 EU 信息提供器、LDLib 同步载荷注册。

## STRUCTURE
```text
integration/
├─ emi/     # CEEMIPlugin, EUEmiStack, EUEmiStackSerializer, EUStackConverter
├─ jade/    # CTNHEnergyJadePlugin, AEDeviceEUProvider
│           # AdMEPatternBufferProvider / AdMEPatternBufferProxyProvider 全文件注释、未注册
└─ ldlib/   # CELDLibPlugin
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| EMI 插件 | `integration/emi/CEEMIPlugin`（`@EmiEntrypoint`；`initialize` 注册 `EUEmiStackSerializer`，`register` 注册 `EUStackConverter`、把 `EUEmiStack.of(1)` 加为 EMI 堆叠、按 NBT `voltage` 区分动力卡并移除基础动力卡堆叠） |
| EU 堆叠与序列化 | `integration/emi/EUEmiStack`, `EUEmiStackSerializer`, `EUStackConverter` |
| Jade 插件 | `integration/jade/CTNHEnergyJadePlugin`（`@WailaPlugin`；服务端注册 `AEDeviceEUProvider` 的 block data，客户端注册同名 block component） |
| Jade EU 信息 | `integration/jade/AEDeviceEUProvider`（读 `ce_network_tier` / `ce_dynamo_tier` 服务端数据，输出 `ctnhenergy.jade.ae_eu.network_voltage` 与 `...dynamo_voltage`） |
| LDLib 集成 | `integration/ldlib/CELDLibPlugin`（`@LDLibPlugin`，`onLoad` 里 `registerSimple(AEKeyPayLoad.class, AEKeyPayLoad::new, AEKey.class, 100)`） |

## CONVENTIONS
- 插件入口用对应 mod 的注解（`@EmiEntrypoint` / `@WailaPlugin` / `@LDLibPlugin`），不在注册表类里手工挂接。
- Jade 只暴露 AE 设备的网络电压等级与动力卡输出电压；样板总成的 Jade 提供器当前整文件注释、且在 `common/CommonProxy.init()` 中的注册调用同样被注释，属未启用状态。
- `EUEmiStack` / `EUStackConverter` 只做 EU 与 EMI 堆叠的互相转换，不承载玩法逻辑。
- 集成类只被对应插件路径引用，不做成 `common/` 的硬依赖。

## ANTI-PATTERNS
- 让 `common/` 或 `registry/` 直接依赖集成类（应为单向：集成 → 模块内部）。
- 在未确认上游 mod 版本与 API 的前提下改注入点或序列化格式。
- 直接删除 Jade 样板总成提供器的注释代码块而不确认是否要重新启用。

## SCOPE
`modules/CTNH-Energy/src/main/java/tech/luckyblock/mcmod/ctnhenergy/integration/` 及其子包。

## READ WHEN
- 新增或修改 EMI / Jade / LDLib 对接
- 调整 EU 堆叠在 EMI 中的显示或序列化

## SOURCE OF TRUTH
`integration/` 下的插件类与其注解注册点；Jade 显示键以 `data/lang/*LangHandler` 为准。

## WORKFLOW
1. 先确认目标 mod 的版本与 API 形态，再改钩子。
2. `:modules:CTNH-Energy:build` 编译；在装有目标 mod 的实例中运行验证。