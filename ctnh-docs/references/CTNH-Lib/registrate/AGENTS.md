# CTNH-LIB REGISTRATE DOMAIN

## OVERVIEW
共享 registrate 表面（14 个 Java 文件）：`CNRegistrate`（继承 GTCEu `GTRegistrate`）、10 个构建器包装、zh_cn lang provider、provider 类型与网络注册。

## STRUCTURE
```text
registrate/
├── CNRegistrate.java           # extends GTRegistrate；CTNH 物品/方块/实体/机器/材料/配方类型助手
├── CTNHLibNetworking.java      # 通道注册
├── builders/                   # 10 个文件
│   ├── CTNHItemBuilder / CTNHBlockBuilder / CTNHEntityBuilder
│   ├── CTNHMachineBuilder / CTNHMultiblockMachineBuilder
│   ├── CTNHRecipeType / CTNHRecipeCategory
│   ├── CTNHMaterial / CTNHTagPrefix
│   └── ICNBuilder              # 构建器标记接口
├── data/                       # ProviderTypes（CNLANG）
└── lang/                       # RegistrateCNLangProvider
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Registrate API | `registrate/CNRegistrate.java` |
| 物品 / 方块 / 实体构建器 | `registrate/builders/{CTNHItemBuilder, CTNHBlockBuilder, CTNHEntityBuilder}.java` |
| 机器构建器 | `registrate/builders/{CTNHMachineBuilder, CTNHMultiblockMachineBuilder}.java` |
| 配方类型 / 类别 | `registrate/builders/{CTNHRecipeType, CTNHRecipeCategory}.java` |
| 材料 / 标签前缀 | `registrate/builders/{CTNHMaterial, CTNHTagPrefix}.java` |
| 中文 lang 写入 | `CNRegistrate#genLang`、`#genLang(..., Object...)`、`#addRawLang`、`#addRawCNLang`、`#addCNLang`、`#addLangProcessor`、`#addLang` |
| Provider 类型 | `registrate/data/ProviderTypes.java`（`CNLANG = ProviderType.register("ctnhlib_cnlang", ...)`） |
| Lang provider | `registrate/lang/RegistrateCNLangProvider.java` |
| 网络注册 | `registrate/CTNHLibNetworking.java` |

## CONVENTIONS
- `CNRegistrate extends GTRegistrate`，提供 `item/block/entity/machine/multiblock/material/recipeType/recipeCategory/oreTagPrefix/tagPrefix` 等 CTNH 助手；机器与多方块构建器实现 `ICNBuilder`（`getCNLangValue()`），由 `mixin/MachineBuilderMixin` 在 `register()` 时把中文名写进 `CNLANG`。
- 所有 CTNH 模块的 registrate 都继承 `CNRegistrate`（Core `CTNHRegistrate`、Energy `CERegistrate`、Bio `CBRegistrate`、Mana `CMRegistrate`、Astral `CARegistrate`、CTPP `CTPPRegistrate`、CEI `CEIRegistrate`）。
- 双语条目两条路径：`com.ctnhlang` 注解经 `LangProcessor`（`CNRegistrate#addLangProcessor`），或直接 `genLang/addRawLang`；`keys` 集合与 `addDataGenerator(CNLANG, ...)` 负责把 `genLang` 条目送进 provider。
- `ProviderTypes.CNLANG` 的注册 id 必须是 `ctnhlib_cnlang`（不能是裸 `cnlang`）：`ProviderType.register` 内部是 `RegistrateDataProvider.TYPES.put(name, type)`，第三方 mod `ae2pw` 内置了本类的拷贝也用 `cnlang`，撞名后 zh_cn 子 provider 会挂到它的链上，Lib 的 `@CN` 条目一条都读不到，`LanguageProvider.run()` 直接返回——`zh_cn.json` 不写盘且不报错。`ctnhlib_` 前缀用于独占命名。
- `ICNBuilder` 标记共享构建器接口；新构建器应实现它。
- `RegistrateCNLangProvider` 输出 `zh_cn`，`getSide()` 为 `LogicalSide.CLIENT`，`addTranslations()` 里调 `owner.genData(CNLANG, this)`。

## ANTI-PATTERNS
- 往 Lib 加模块专属构建器；应放所属模块。
- 不检查全部消费模块就改构建器签名。
- 把 `ProviderTypes.CNLANG` 改回 `cnlang`；会重新引入 ae2pw 的 `runData` 撞名（zh_cn 为空）。

## SCOPE
适用于 `src/main/java/tech/vixhentx/mcmod/ctnhlib/registrate` 及其子包。

## READ WHEN
- 加共享构建器或 registrate 助手，或改 lang provider 行为。

## SOURCE OF TRUTH
- `registrate/CNRegistrate.java` 与 `registrate/builders/` 的契约。
- Lang 注解处理：`registrate/lang/RegistrateCNLangProvider.java` 与 `registrate/data/ProviderTypes.java`。

## WORKFLOW
1. 先确认构建器/助手确实被多个模块共享。
2. 检查消费方 registrate（Core、Energy、Bio、Mana、Astral、CTPP、CEI）。
3. 跑 `:modules:CTNH-Lib:build`；lang 生成有改动时在消费模块跑 `runData`，确认 `src/generated/resources/assets/<modid>/lang/zh_cn.json` 非空。
