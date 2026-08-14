# CTNH-LIB LANGPROVIDER DOMAIN

## OVERVIEW
The `com.ctnhlang` annotation namespace and the annotation processor consumed by the custom `com.ctnhlang.langprovider` Gradle plugin (13 Java files across both namespaces).

## STRUCTURE
```text
src/main/java/com/ctnhlang/
|-- CN.java
|-- Category.java
|-- Domain.java
|-- EN.java
|-- IgnoreLang.java
|-- Key.java
|-- Lang.java
|-- LangFactory.java
|-- Prefix.java
|-- Suffix.java
`-- langprovider/
    `-- LangKeyBuilder.java

src/main/java/tech/vixhentx/mcmod/ctnhlib/langprovider/
|-- Lang.java
`-- LangProcessor.java
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Bilingual annotations | `com/ctnhlang/CN.java`, `com/ctnhlang/EN.java` |
| Category/domain annotations | `com/ctnhlang/Category.java`, `com/ctnhlang/Domain.java` |
| Other annotation/helper types | `com/ctnhlang/IgnoreLang.java`, `com/ctnhlang/Key.java`, `com/ctnhlang/Lang.java`, `com/ctnhlang/LangFactory.java`, `com/ctnhlang/Prefix.java`, `com/ctnhlang/Suffix.java` |
| Key builder | `com/ctnhlang/langprovider/LangKeyBuilder.java` |
| Processor | `tech/vixhentx/mcmod/ctnhlib/langprovider/Lang.java`, `tech/vixhentx/mcmod/ctnhlib/langprovider/LangProcessor.java` |

## CONVENTIONS
- The main library namespace is `tech.vixhentx.mcmod.ctnhlib`; lang annotations live in the separate `com.ctnhlang` namespace.
- Bilingual (CN/EN) lang registration flows through these annotations and `registrate/lang/RegistrateCNLangProvider.java`.
- `LangKeyBuilder` builds lang keys used by the annotations and processor.

## ANTI-PATTERNS
- Do not rename lang annotations without checking the custom `com.ctnhlang.langprovider` plugin usage.

## SCOPE
Applies to `src/main/java/com/ctnhlang` and `src/main/java/tech/vixhentx/mcmod/ctnhlib/langprovider`.

## READ WHEN
- Changing lang annotation semantics or the annotation processor.

## SOURCE OF TRUTH
- `com/ctnhlang/` annotations, `tech/vixhentx/mcmod/ctnhlib/langprovider/LangProcessor.java`, and the `com.ctnhlang.langprovider` Gradle plugin.

## WORKFLOW
1. Check all modules using `@CN`/`@EN` before changing annotation contracts.
2. Run `:modules:CTNH-Lib:runData` when lang generation is affected.