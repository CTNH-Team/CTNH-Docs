# CTNH-BIO MIXIN DOMAIN

## OVERVIEW
Compatibility mixins (19 Java files) for Biomancy, Hostile Neural Networks, EMI/ALI, Create, and GTCEu recipe/machine internals.

## STRUCTURE
```text
mixin/
|-- GTMixin.java               # root
|-- ali/                       # EmiGamePlayLootMixin, EmiScrollWidgetMixin
|-- biomancy/                  # BiomancyJeiPluginMixin, InjectorItemMixin, InjectorScreenMixin, VialHolderBlockEntityMixin
|-- create/                    # CrushingWheelControllerBlockEntityMixin
|-- emi/                       # EmiApiMixin, RecipeScreenMixin
|-- gtm/                       # GTRecipeTypeMixin, IThermalFluidHandlerItemStackMixin, MultiblockDisplayText$BuilderMixin, ThermalFluidStatsMixin
`-- hostilenetworks/           # CacheModelMixin, DataModelItemMixin, HostileEventsMixin, HostileJeiPluginMixin, SimChamberTileEntityMixin
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Biomancy patches | `mixin/biomancy/` |
| HNN patches | `mixin/hostilenetworks/` |
| EMI/ALI | `mixin/emi/`, `mixin/ali/` |
| Create patches | `mixin/create/` |
| GTCEu patches | `mixin/gtm/` |
| Mixin config | `src/main/resources/ctnhbio.mixins.json` |

## CONVENTIONS
- Keep mixin JSON and package entries synchronized.
- Treat these as compatibility patches, not generic helpers.
- Despoil-loot catalyst display (EMI workstation) moved to Core; `mixin/ali/EmiCompatibilityMixin` was removed from both source and `ctnhbio.mixins.json`.

## ANTI-PATTERNS
- Do not change injection points without checking upstream target members.
- Do not re-add `mixin/ali/EmiCompatibilityMixin`; despoil-loot catalyst display is owned by Core.

## SCOPE
Applies to `src/main/java/com/moguang/ctnhbio/mixin` and `src/main/resources/ctnhbio.mixins.json`.

## READ WHEN
- Patching Biomancy, HNN, EMI/ALI, Create, or GTCEu behavior.

## SOURCE OF TRUTH
- `src/main/resources/ctnhbio.mixins.json` and the mixin classes in `mixin/`.

## WORKFLOW
1. Locate the integration's mixin package and JSON entry.
2. Verify the target member against the loaded mod version.
3. Run `:modules:CTNH-Bio:build`; validate at runtime.
