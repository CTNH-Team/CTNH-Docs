# CTPP CLIENT DOMAIN

## OVERVIEW
Client-side rendering, toolbox UI, and CTPP Ponder plugin/scenes/tags, including Carbon Brushes (26 Java files).

## STRUCTURE
```text
client/
|-- ClientProxy.java, CTPPPartialModels.java
|-- CarbonBrushesRenderer.java, CarbonBrushesVisual.java, GeneratorCoilRenderer.java, GeneratorCoilVisual.java
|-- KineticMachineBlockEntityRenderer.java, MagnetTooltipHandler.java, SplitShaftVisual.java
|-- ponder/                    # CTPPPonderPlugin, CTPPPonderSceneBuilder, CTPPPonderScenes, CTPPPonderTags
|   |-- electric/              # CarbonBrushes
|   `-- kinetic/               # BigDam, KineticHatch, SmashingFactory, WindmillControlCenter
|-- renderer/                  # CTPPToolboxCurioRenderer, CTPPToolboxRenderer, GTWireCutterRenderer
`-- toolbox/                   # CTPPToolboxClientState, CTPPToolboxKeyHandler, CTPPToolboxOverlay, CTPPToolboxRadialScreen, CTPPToolboxScreen
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Client proxy | `client/ClientProxy.java` |
| Ponder plugin/scenes/tags | `client/ponder/` (incl. Carbon Brushes electric scene) |
| Renderers | `client/renderer/` (toolbox, wire cutter), top-level visuals (CarbonBrushes, GeneratorCoil, KineticMachine) |
| Toolbox UI | `client/toolbox/` (5 classes) |
| Partial models | `client/CTPPPartialModels.java` |

## CONVENTIONS
- Keep client-only classes out of common construction paths.

## ANTI-PATTERNS
- Do not put rendering logic in machine implementation classes.

## SCOPE
Applies to `src/main/java/com/mo_guang/ctpp/client` and its child packages.

## READ WHEN
- Changing CTPP Ponder scenes, tags, renderers, or toolbox UI.

## SOURCE OF TRUTH
- `client/ponder/` classes and their registration sites.

## WORKFLOW
1. Check Ponder registration wiring in `common/CommonProxy.java`.
2. Run `:modules:CTPP:build`; validate the runtime surface if available.
