# CTNH-ENERGY INTEGRATION DOMAIN

## OVERVIEW
EMI plugin plus AE2/ME pattern buffer Jade providers and LDLib integration (9 Java files).

## STRUCTURE
```text
integration/
|-- emi/                       # CEEMIPlugin, EUEmiStack, EUEmiStackSerializer, EUStackConverter
|-- jade/                      # AEDeviceEUProvider, AdMEPatternBufferProvider, AdMEPatternBufferProxyProvider, CTNHEnergyJadePlugin
`-- ldlib/                     # CELDLibPlugin
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| EMI plugin | `integration/emi/CEEMIPlugin.java` + EU stack converter/serializer |
| Jade providers | `integration/jade/` (CTNHEnergyJadePlugin, AEDeviceEUProvider, AdMEPatternBuffer(Proxy)Provider) |
| LDLib integration | `integration/ldlib/CELDLibPlugin.java` |

## CONVENTIONS
- Jade providers expose AE2/ME pattern buffer and EU device info.
- `EUEmiStack`/`EUStackConverter` adapt EU stacks to EMI.
- Keep integrations isolated and optional.

## ANTI-PATTERNS
- Do not make integration classes hard dependencies of common code.

## SCOPE
Applies to `src/main/java/tech/luckyblock/mcmod/ctnhenergy/integration` and its child packages.

## READ WHEN
- Changing Energy EMI/Jade/LDLib integration.

## SOURCE OF TRUTH
- `integration/` classes and their registration sites.

## WORKFLOW
1. Confirm the target mod version before changing hooks.
2. Run `:modules:CTNH-Energy:build`; validate at runtime with the target mod present.
