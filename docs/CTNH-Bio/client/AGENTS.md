# CTNH-BIO CLIENT DOMAIN

## OVERVIEW
Client-side rendering and models for Bio living machines (14 Java files).

## STRUCTURE
```text
client/
|-- ClientProxy.java
|-- Text/                      # ModelOutputLine
|-- model/                     # BioReactorModel, BioelectricForgeModel, CBModels, DecomposerModel, DigesterModel, GreatFleshModel, VatModel
`-- renderer/                  # BasicLivingMachineEntityRenderer, ColorableEntityRenderer, ColorableMachineBlockEntityRenderer, ColorableMachineItemRenderer, LivingMetaMachineBERProvider
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Client proxy | `client/ClientProxy.java` |
| Renderers | `client/renderer/` (BasicLivingMachineEntityRenderer, Colorable* renderers, LivingMetaMachineBERProvider) |
| Models | `client/model/` (CBModels, VatModel, DigesterModel, GreatFleshModel, BioReactorModel, ...) |
| Client text | `client/Text/ModelOutputLine.java` |

## CONVENTIONS
- Colorable entity/machine/item renderers pair with the colorable living-machine content.
- Keep client-only classes out of common construction paths.

## ANTI-PATTERNS
- Do not put rendering logic in machine implementation classes.

## SCOPE
Applies to `src/main/java/com/moguang/ctnhbio/client` and its child packages.

## READ WHEN
- Changing living-machine renderers or models.

## SOURCE OF TRUTH
- `client/renderer/` classes and the entity/machine render registrations.

## WORKFLOW
1. Check the entity/machine registration before changing renderers.
2. Run `:modules:CTNH-Bio:build` and validate the runtime surface if available.
