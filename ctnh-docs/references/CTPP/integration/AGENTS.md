# CTPP INTEGRATION DOMAIN

## OVERVIEW
Jade, JEI, and LDLib integration for CTPP (5 Java files). EMI plugin moved to CTNH-Core; KineticOutputMachineProvider removed.

## STRUCTURE
```text
integration/
|-- jade/                      # CTPPJadePlugin (KineticOutputMachineProvider removed, config `jade.plugin_ctpp.kinetic_output_machine_provider` and `ctpp.kineticoutputmachineprovider.kineticoutput` lang removed)
|-- jei/                       # CTPPJeiPlugin
|   `-- category/              # FanAcidWashingCategory, FanBreathingCategory
`-- ldlib/                     # CTPPLDLibPlugin
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| JEI plugin | `integration/jei/CTPPJeiPlugin.java` |
| Fan categories | `integration/jei/category/` (FanAcidWashingCategory, FanBreathingCategory) |
| Jade provider | `integration/jade/CTPPJadePlugin.java` |
| LDLib plugin | `integration/ldlib/CTPPLDLibPlugin.java` |
| EMI (moved) | CTNH-Core `integration/emi/` — do not re-add `integration/emi/CTPPEmiPlugin.java` here |

## CONVENTIONS
- KubeJS recipe keys `SU_IN` / `SU_OUT` are registered from `CTPPGTAddon.registerRecipeKeys()` (not in this domain).
- Keep integrations isolated and optional.

## ANTI-PATTERNS
- Do not make integration classes hard dependencies of common code.
- Do not reintroduce `CTPPEmiPlugin` in CTPP; it lives in Core.
- Do not re-add `KineticOutputMachineProvider`; use `CTPPJadePlugin` only.

## SCOPE
Applies to `src/main/java/com/mo_guang/ctpp/integration` and its child packages.

## READ WHEN
- Changing CTPP JEI/Jade integration.

## SOURCE OF TRUTH
- `integration/` classes and `CTPPGTAddon.registerRecipeKeys()`.

## WORKFLOW
1. Confirm the target mod version before changing hooks.
2. Run `:modules:CTPP:build`; validate at runtime with the target mod present.
