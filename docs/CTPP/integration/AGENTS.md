# CTPP INTEGRATION DOMAIN

## OVERVIEW
Jade, JEI, and LDLib integration for CTPP (6 Java files).

## STRUCTURE
```text
integration/
|-- jei/                       # CTPPJeiPlugin
|-- jei/category/              # FanAcidWashingCategory, FanBreathingCategory
|-- jade/                      # KineticOutputMachineProvider
`-- ldlib/                     # CTPPLDLibPlugin
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| JEI plugin | `integration/jei/CTPPJeiPlugin.java` |
| Fan categories | `integration/jei/category/` (FanAcidWashingCategory, FanBreathingCategory) |
| Jade provider | `integration/jade/KineticOutputMachineProvider.java` |
| LDLib plugin | `integration/ldlib/CTPPLDLibPlugin.java` |

## CONVENTIONS
- KubeJS recipe keys `SU_IN` / `SU_OUT` are registered from `CTPPGTAddon.registerRecipeKeys()` (not in this domain).
- Keep integrations isolated and optional.

## ANTI-PATTERNS
- Do not make integration classes hard dependencies of common code.

## SCOPE
Applies to `src/main/java/com/mo_guang/ctpp/integration` and its child packages.

## READ WHEN
- Changing CTPP JEI integration.

## SOURCE OF TRUTH
- `integration/` classes and `CTPPGTAddon.registerRecipeKeys()`.

## WORKFLOW
1. Confirm the target mod version before changing hooks.
2. Run `:modules:CTPP:build`; validate at runtime with the target mod present.