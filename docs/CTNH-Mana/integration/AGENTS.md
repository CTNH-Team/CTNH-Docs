# CTNH-MANA INTEGRATION DOMAIN

## OVERVIEW
EMI and Jade integration for Mana magic content (3 Java files).

## STRUCTURE
```text
integration/
|-- emi/                       # CTNHManaEmiPlugin
`-- jade/                      # 2: CTNHManaJadePlugin, ThirdEyeStatusProvider
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| EMI plugin | `integration/emi/CTNHManaEmiPlugin.java` |
| Jade plugin | `integration/jade/CTNHManaJadePlugin.java` (registers providers; replaces former `CommonProxy` JadePriorityManager registrations) |
| Jade providers | `integration/jade/ThirdEyeStatusProvider.java` |

## CONVENTIONS
- Keep integrations isolated and optional.
- Jade registration is centralized in `CTNHManaJadePlugin`; `CommonProxy.init()` no longer registers `ManaHatchStatusProvider`/`ManaMachineManaStatusProvider`/`BaseManaMachineStatusProvider`/`BloodAltarStatusProvider`/`EternalWosStatusProvider`/`GemSublimatorStatusProvider` — those providers were removed. Check plugin before re-adding.
- Magic integration surfaces span recipe builders, mixins, integrations, and client packets; check all four before changing behavior.
- GT/GMT recipes are runtime dynamic-pack data; integration must not assume static JSON. Item/block/fluid refs MUST use registration objects (`CMItems.X` etc.), not string lookups.

## ANTI-PATTERNS
- Do not make integration classes hard dependencies of common code.
- Do not reintroduce deleted Jade providers without restoring their `BlockEntity`/`Block` targets (now trait-backed).

## SCOPE
Applies to `src/main/java/com/magicbee/ctnhmana/integration` and its child packages.

## READ WHEN
- Changing Mana EMI/Jade integration.

## SOURCE OF TRUTH
- `integration/` classes and their registration sites (`CTNHManaJadePlugin`, EMI plugin).

## WORKFLOW
1. Confirm the target mod version before changing hooks.
2. Run `:modules:CTNH-Mana:build`; validate at runtime with the target mod present.
