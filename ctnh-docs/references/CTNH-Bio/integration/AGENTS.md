# CTNH-BIO INTEGRATION DOMAIN

## OVERVIEW
XEI/Jade/EMI/JEI integration for Bio living machines (8 Java files).

## STRUCTURE
```text
integration/
|-- emi/                       # CTNHBioEmiPlugin
|-- jade/                      # LivingMachineStatusProvider, NutrientElement
|-- jei/                       # CTNHBioJeiPlugin, MobCrushingCategory, RelatedInfoJeiPlugin
`-- xei/
    |-- entry/entity/          # EntityEntryList
    `-- handlers/entity/       # CycleEntityEntryHandler
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| EMI plugin | `integration/emi/CTNHBioEmiPlugin.java` |
| Jade | `integration/jade/` (LivingMachineStatusProvider, NutrientElement) |
| JEI plugins | `integration/jei/` (CTNHBioJeiPlugin, MobCrushingCategory, RelatedInfoJeiPlugin) |
| XEI entity entries | `integration/xei/entry/entity/`, `integration/xei/handlers/entity/` |

## CONVENTIONS
- Living-machine Jade status providers and UI categories are registered here.
- Mob Crushing category pairs with `common/recipe/MobCrushingRecipe.java`.
- Keep integrations isolated and optional.

## ANTI-PATTERNS
- Do not make integration classes hard dependencies of common code.

## SCOPE
Applies to `src/main/java/com/moguang/ctnhbio/integration` and its child packages.

## READ WHEN
- Changing Bio XEI/EMI/JEI/Jade integration.

## SOURCE OF TRUTH
- `integration/` classes and their registration sites.

## WORKFLOW
1. Confirm the target mod version before changing hooks.
2. Run `:modules:CTNH-Bio:build`; validate at runtime with the target mod present.
