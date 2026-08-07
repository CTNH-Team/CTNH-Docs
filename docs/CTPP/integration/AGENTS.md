# CTPP INTEGRATION DOMAIN

## OVERVIEW
KubeJS and JEI integration for CTPP (3 Java files).

## STRUCTURE
```text
integration/
|-- jei/                       # CTPPJeiPlugin
`-- jei/category/              # FanAcidWashingCategory, FanBreathingCategory
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| KubeJS integration | `integration/kjs/` (kinetic machine builder, stress recipe components) |
| JEI plugin | `integration/jei/CTPPJeiPlugin.java` |
| Fan categories | `integration/jei/category/` (FanAcidWashingCategory, FanBreathingCategory) |

## CONVENTIONS
- KubeJS recipe keys `SU_IN` / `SU_OUT` are registered from `CTPPGTAddon.registerRecipeKeys()`.
- Keep integrations isolated and optional.

## ANTI-PATTERNS
- Do not make integration classes hard dependencies of common code.

## SCOPE
Applies to `src/main/java/com/mo_guang/ctpp/integration` and its child packages.

## READ WHEN
- Changing CTPP KubeJS or JEI integration.

## SOURCE OF TRUTH
- `integration/` classes and `CTPPGTAddon.registerRecipeKeys()`.

## WORKFLOW
1. Confirm the target mod version before changing hooks.
2. Run `:modules:CTPP:build`; validate at runtime with the target mod present.
