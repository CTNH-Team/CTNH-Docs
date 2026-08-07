# CTNH-CORE CLIENT DOMAIN

## OVERVIEW
Client-side bootstrap, models, renderers, and Core-owned Create Ponder scenes, tags, and plugin (22 Java files).

## STRUCTURE
```text
client/
|-- ClientProxy.java           # client bootstrap (extends CommonProxy)
|-- ClientUtil.java
|-- model/                     # ModelBase, ModelDefinition, TemplateModel, TurbineRotorModel
|-- ponder/                    # CTNHCorePonderPlugin, CTNHCorePonderSceneBuilder, CTNHCorePonderScenes, CTNHCorePonderTags
|   |-- Electric/              # GregTechMultiblocks, NeutronActivator
|   `-- Kinetic/               # Meadow, MechanicalExporter
|-- renderer/                  # ArcBlockRender, AstralPlanetSpecialEffects, DynamicCasingRender, HyperPlasmaTurbineRender, LargeBottleRender, MartialMoralityEyeRender, TurbineRotorRender
`-- renderer/utils/            # RenderUtils
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Client bootstrap | `client/ClientProxy.java`, `client/ClientUtil.java` |
| Ponder plugin/scenes/tags | `client/ponder/CTNHCorePonderPlugin.java`, `CTNHCorePonderScenes.java`, `CTNHCorePonderTags.java` |
| Core Ponder scenes | `client/ponder/Kinetic/` (Meadow, MechanicalExporter), `client/ponder/Electric/` (GregTechMultiblocks, NeutronActivator) |
| Ponder adapter builder | `client/ponder/CTNHCorePonderSceneBuilder.java` |
| Models | `client/model/` (ModelBase, TemplateModel, TurbineRotorModel) |
| Renderers | `client/renderer/` (ArcBlockRender, DynamicCasingRender, HyperPlasmaTurbineRender, TurbineRotorRender, ...) |

## CONVENTIONS
- Ponder scenes use `scene.title(..., en, cn)` / `scene.showText(..., en, cn)` with text embedded directly in scene files.
- `CTNHCorePonderSceneBuilder` is only a Core adapter around Lib's shared builder; keep reusable builder/text behavior in CTNH-Lib.
- Ponder registration happens from `ClientProxy.onClientSetupEvent()`; client datagen lang extraction happens in `CommonProxy.gatherData()` via `CTNHPonderLang.init(new CTNHCorePonderPlugin())`.

## ANTI-PATTERNS
- Do not move Core Ponder scenes/tags/plugin into CTNH-Lib; only the shared builder belongs there.
- Do not make client-only classes reachable from common construction paths.

## SCOPE
Applies to `src/main/java/io/github/cpearl0/ctnhcore/client` and its child packages.

## READ WHEN
- Adding or changing Core Ponder scenes, tags, or the client render pipeline.
- Changing Core model/layer registrations.

## SOURCE OF TRUTH
- `client/ClientProxy.java` (bootstrap), `client/ponder/CTNHCorePonderPlugin.java` (scene/tag registration).
- Ponder lang extraction: CTNH-Lib `CTNHPonderLang` wired from `common/CommonProxy.gatherData()`.

## WORKFLOW
1. Read the shared Ponder builder guide in `docs/CTNH-Lib/client/AGENTS.md` before writing scenes.
2. Add scene/tag registrations in the plugin; keep reusable text helpers in Lib.
3. Run `:modules:CTNH-Core:runData` after Ponder text changes, then `spotlessCheck`.
