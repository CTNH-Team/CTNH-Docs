# CTNH-MANA INTEGRATION DOMAIN

## OVERVIEW
EMI and Jade integration for Mana magic content (6 Java files).

## STRUCTURE
```text
integration/
|-- emi/                       # CTNHManaEmiPlugin
`-- jade/                      # BaseManaMachineStatusProvider, BloodAltarStatusProvider, ManaHatchStatusProvider, ManaMachineManaStatusProvider, ThirdEyeStatusProvider
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| EMI plugin | `integration/emi/CTNHManaEmiPlugin.java` |
| Jade providers | `integration/jade/` (5 providers) |

## CONVENTIONS
- Keep integrations isolated and optional.
- Magic integration surfaces span recipe builders, mixins, integrations, and client packets; check all four before changing behavior.

## ANTI-PATTERNS
- Do not make integration classes hard dependencies of common code.

## SCOPE
Applies to `src/main/java/com/moguang/ctnhmana/integration` and its child packages.

## READ WHEN
- Changing Mana EMI/Jade integration.

## SOURCE OF TRUTH
- `integration/` classes and their registration sites.

## WORKFLOW
1. Confirm the target mod version before changing hooks.
2. Run `:modules:CTNH-Mana:build`; validate at runtime with the target mod present.
