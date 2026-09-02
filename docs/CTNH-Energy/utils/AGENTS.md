# CTNH-ENERGY UTILS DOMAIN

## OVERVIEW
Shared helper utilities for Energy (11 Java files), including button/widget helpers and pattern provider targets.

## STRUCTURE
```text
utils/
|-- CEDrawHelper.java, CEUtil.java, MEConfigUtil.java
|-- CEPatternProviderTarget.java, ProviderRecord.java
|-- FakePccCard.java, FakeSizedIntList.java, TempColorSprayBehaviour.java
`-- button/                    # BlitterButton, Blitters, CETextures, ToggleBlitterButton
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Draw helpers | `utils/CEDrawHelper.java` |
| Config utils | `utils/MEConfigUtil.java`, `utils/CEUtil.java` |
| Pattern provider targets | `utils/CEPatternProviderTarget.java`, `utils/ProviderRecord.java` |
| Button widgets | `utils/button/` (BlitterButton, ToggleBlitterButton, Blitters, CETextures) |

## CONVENTIONS
- Keep helpers free of registry dependencies where possible.

## ANTI-PATTERNS
- Do not duplicate helpers that exist in CTNH-Lib `utils/`.

## SCOPE
Applies to `src/main/java/tech/luckyblock/mcmod/ctnhenergy/utils` and its child packages.

## READ WHEN
- Reusing Energy-wide helper logic.

## SOURCE OF TRUTH
- The utility classes in `utils/`.

## WORKFLOW
1. Check CTNH-Lib `utils/` first for an existing shared helper.
2. Run `:modules:CTNH-Energy:build` after changes.
