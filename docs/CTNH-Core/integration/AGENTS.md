# CTNH-CORE INTEGRATION DOMAIN

## OVERVIEW
Optional third-party integrations owned by Core (4 Java files): EMI and Legendary Survival.

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| EMI plugins | `integration/emi/CTNHCoreEmiPlugin.java`, `integration/emi/CTNHExtraEmiPlugin.java` |
| Legendary Survival | `integration/legendary/ArmorModifier.java`, `integration/legendary/UnderfloorHeatingSystemTempModifier.java` |

## CONVENTIONS
- Keep integrations isolated and optional; they must not become hard dependencies of common code.
- Broad cross-mod recipe compatibility generally belongs in Core (aggregator), while feature modules keep their own mechanic integrations.
- Legendary Survival modifiers integrate with the Underfloor Heating System machine.

## ANTI-PATTERNS
- Do not move optional integrations into base modules.
- Do not require integration classes at class-load time from non-integration code.

## SCOPE
Applies to `src/main/java/io/github/cpearl0/ctnhcore/integration`.

## READ WHEN
- Changing EMI or Legendary Survival compatibility in Core.

## SOURCE OF TRUTH
- `integration/emi/` and `integration/legendary/` classes; wiring in `common/CommonProxy.java`.

## WORKFLOW
1. Confirm the integration target mod version before changing hooks.
2. Check mixin JSON entries when integration relies on mixins.
3. Run `:modules:CTNH-Core:build` and validate at runtime with the target mod present.
