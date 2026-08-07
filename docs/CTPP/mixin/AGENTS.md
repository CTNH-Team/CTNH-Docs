# CTPP MIXIN DOMAIN

## OVERVIEW
Create rotation/kinetic fixes, deployer/sequenced assembly fixes, GT bucket and multiblock-state hooks (23 Java files).

## STRUCTURE
```text
mixin/
|-- BlockPatternMixin, GTBucketItemMixin, MultiblockStateMixin, RotationPropagatorMixin, SmartBlockEntityMixin
|-- create/                    # AllCreatePonderScenesMixin, KineticBlockEntityMixin, Matrix3dMixin, ToolboxHandlerClientMixin, WindmillBearingBlockMixin
|   |-- diesel/                # BasinFermentingCategoryMixin, BasinRecipeMixin, CDGJEIMixin, DistillationTankBlockEntityMixin
|   |-- fix/                   # DeployerApplicationRecipeMixin, SequencedAssemblyCategoryMixin
|   `-- jei/                   # RecipeSlotBuilderMixin, SequencedAssemblyCategoryMixin, SequencedAssemblySubCategoryMixin, TMRVSlotWidgetMixin
|-- fix/                       # IRotorHolderMachineMixin, RotorHolderPartMachineMixin
`-- gtm/                       # GTToolTypeMixin
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Create patches | `mixin/create/` (5) |
| Create diesel patches | `mixin/create/diesel/` (4) |
| Create fix patches | `mixin/create/fix/` (2) |
| Create JEI patches | `mixin/create/jei/` (4) |
| Fix patches | `mixin/fix/` (2 rotor holder) |
| GT patches | `mixin/gtm/GTToolTypeMixin.java` |
| Mixin config | `src/main/resources/ctpp.mixins.json` |

## CONVENTIONS
- Create kinetic behavior is patched through mixins and dynamic contraption classes; inspect both when changing rotation or moving-block behavior.
- Keep mixin JSON and package entries synchronized.

## ANTI-PATTERNS
- Do not change injection points without checking upstream target members.

## SCOPE
Applies to `src/main/java/com/mo_guang/ctpp/mixin` and `src/main/resources/ctpp.mixins.json`.

## READ WHEN
- Patching Create rotation/kinetic, deployer/sequenced assembly, or GT bucket/multiblock-state behavior.

## SOURCE OF TRUTH
- `src/main/resources/ctpp.mixins.json` and the mixin classes in `mixin/`.

## WORKFLOW
1. Locate the mixin package and JSON entry.
2. Verify the target member against the loaded Create/GT version.
3. Run `:modules:CTPP:build`; validate at runtime.
