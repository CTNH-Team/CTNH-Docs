# CTNH-LIB LANGPROVIDER DOMAIN

## OVERVIEW
`com.ctnhlang` 注解散名空间，以及 `tech.vixhentx.mcmod.ctnhlib.langprovider` 下的注释处理器和双语 lang 管线（两个包根合计 13 个 Java 文件）。

## STRUCTURE
```text
src/main/java/com/ctnhlang/
├── CN.java, EN.java                     # 字段级双语注解
├── Category.java, Domain.java           # 类型级分组
├── Prefix.java, Suffix.java             # 类型级前后缀
├── Key.java, IgnoreLang.java            # 显式 key / 跳过
├── Lang.java, LangFactory.java          # 运行时 Lang 接口与工厂注解
└── langprovider/
    └── LangKeyBuilder.java              # key 生成

src/main/java/tech/vixhentx/mcmod/ctnhlib/langprovider/
├── Lang.java                            # `@LangFactory` 实现，`genLang` / `genLangArray`
└── LangProcessor.java                   # ASM 扫描注解并写入 registrate
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| 字段级双语注解 | `com/ctnhlang/CN.java`、`com/ctnhlang/EN.java` |
| 类型级分组注解 | `com/ctnhlang/Category.java`、`com/ctnhlang/Domain.java`、`com/ctnhlang/Prefix.java`、`com/ctnhlang/Suffix.java` |
| 显式 key / 跳过 | `com/ctnhlang/Key.java`、`com/ctnhlang/IgnoreLang.java` |
| key 生成 | `com/ctnhlang/langprovider/LangKeyBuilder.java` |
| 注释处理器 | `tech/vixhentx/mcmod/ctnhlib/langprovider/LangProcessor.java` |
| 运行时 Lang 实现 | `tech/vixhentx/mcmod/ctnhlib/langprovider/Lang.java` |
| 写入入口 | `registrate/CNRegistrate.java#addLangProcessor`、`#addRawLang`、`#genLang` |

## CONVENTIONS
- 主库命名空间是 `tech.vixhentx.mcmod.ctnhlib`；lang 注解单独放在 `com.ctnhlang`。
- `LangProcessor` 通过 `ModFileScanData` 收集字段级 `@EN`/`@CN`/`@IgnoreLang`，用 ASM `ClassNode` 读取字段；数组字段走 `LangKeyBuilder.buildIndexedKeys`（`key.0`、`key.1`…），单值字段走 `buildKey`；带 `@IgnoreLang` 的字段跳过；`@EN`/`@CN` 数组长度不一致只告警不报错；异常经 `CTNHLib.LOGGER` 记录后继续。
- 生成的条目经 `CNRegistrate.addRawLang(key, en, cn)` 进入 `CNLANG` provider，由 `registrate/lang/RegistrateCNLangProvider` 输出 `zh_cn.json`。消费方在各自 `*Datagen` 里调 `REGISTRATE.addLangProcessor()`（Core / Energy / Bio / Mana / Astral / CTPP / CEI）。
- `tech/vixhentx/mcmod/ctnhlib/langprovider/Lang` 标 `@LangFactory`，默认工厂方法名 `genLang`、数组工厂 `genLangArray`；`Lang.translate(...)` 返回 `Component.translatable(key, args)`。
- 自定义 Gradle 插件 `com.ctnhlang.langprovider` 在根 `build.gradle` 经 `ctnhLang { modId = mod_id }` 配置；插件本体的源码不在本仓库内，改注解契约前先确认消费方编译。

## ANTI-PATTERNS
- 未经检查 Gradle 插件与消费方用法就重命名 `com.ctnhlang` 注解。
- 在字段上用 `@IgnoreLang` 之外的字符串 key 硬编码代替 `LangKeyBuilder` 规则。
- 在 Lib 内注册模块专属 lang 条目（应放所属模块的 datagen / 注解字段）。

## SCOPE
适用于 `src/main/java/com/ctnhlang` 与 `src/main/java/tech/vixhentx/mcmod/ctnhlib/langprovider`。

## READ WHEN
- 改 lang 注解散名语义、key 生成规则或注释处理器。

## SOURCE OF TRUTH
- `com/ctnhlang/` 注解、`tech/vixhentx/mcmod/ctnhlib/langprovider/LangProcessor.java`，以及根 `build.gradle` 的 `com.ctnhlang.langprovider` 插件（`ctnhLang { modId }`）。

## WORKFLOW
1. 改注解契约前先检查所有使用 `@CN`/`@EN` 的模块。
2. 在消费模块跑 `runData` 并确认 `src/generated/resources/assets/<modid>/lang/zh_cn.json` 非空。
