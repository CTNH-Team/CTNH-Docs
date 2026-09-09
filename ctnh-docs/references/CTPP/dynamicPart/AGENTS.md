# CTPP DYNAMICPART DOMAIN

## OVERVIEW
Dynamic contraption support (10 Java files): rotation wand, moving/rotating contraption entities, renderers, and rotation state helpers.

## STRUCTURE
```text
dynamicPart/
|-- QuaternionRotationState.java, RotationWandItem.java
|-- SimpleBearingContraption.java, SimpleContraptionEntityRenderer.java
|-- moving/                    # SimpleMovingContraption
`-- rotation/                  # FixedAxisRotatingContraptionEntity, IContraptionMultiblock, RubiksCubeContraptionEntity, SimpleRotatingContraption, SimpleRotatingContraptionEntity
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Moving contraptions | `dynamicPart/moving/SimpleMovingContraption.java` |
| Rotation logic | `dynamicPart/rotation/` (5 classes) |
| Rotation wand | `dynamicPart/RotationWandItem.java` |
| Rotation state | `dynamicPart/QuaternionRotationState.java` |

## CONVENTIONS
- Create kinetic behavior is patched through mixins and dynamic contraption classes; inspect both when changing rotation or moving-block behavior.
- `SimpleRotatingContraptionEntity.tick()` sets running state before attempting reattach to controller.

## ANTI-PATTERNS
- Do not change rotation behavior without checking the matching Create mixins.

## SCOPE
Applies to `src/main/java/com/mo_guang/ctpp/dynamicPart` and its child packages.

## READ WHEN
- Changing rotation wand, moving/rotating contraption, or rotation state behavior.

## SOURCE OF TRUTH
- `dynamicPart/` classes and `mixin/create/` patches.

## WORKFLOW
1. Check both dynamic contraption classes and Create mixins before editing.
2. Run `:modules:CTPP:build`; validate the runtime surface if available.