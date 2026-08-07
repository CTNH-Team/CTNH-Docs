# CTNH-LIB LANGPROVIDER DOMAIN

## OVERVIEW
The `com.ctnhlang` annotation namespace (`@CN`, `@EN`, category/domain annotations) and the annotation processor consumed by the custom `com.ctnhlang.langprovider` Gradle plugin.

## STRUCTURE
```text
src/main/java/tech/vixhentx/mcmod/ctnhlib/langprovider/   # Lang, LangProcessor
src/main/java/com/ctnhlang/langprovider/                  # LangKeyBuilder (separate namespace)
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Annotations | `src/main/java/com/ctnhlang/` (`@CN`, `@EN`, category/domain annotations) |
| Key builder | `src/main/java/com/ctnhlang/langprovider/LangKeyBuilder.java` |
| Processor | `langprovider/Lang.java`, `langprovider/LangProcessor.java` |

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
- `com/ctnhlang/` annotations, `langprovider/LangProcessor.java`, and the `com.ctnhlang.langprovider` Gradle plugin.

## WORKFLOW
1. Check all modules using `@CN`/`@EN` before changing annotation contracts.
2. Run `:modules:CTNH-Lib:runData` when lang generation is affected.
