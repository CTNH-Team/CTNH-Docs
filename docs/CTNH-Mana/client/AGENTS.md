# CTNH-MANA CLIENT DOMAIN

## OVERVIEW
Caduceus radial menu plus Mana-owned Ponder plugin, tags, scenes, adapter builder, models, rendering, and Zenith invasion client mirror (33 Java files).

## STRUCTURE
```text
client/
|-- ClientProxy.java, ZenithInvadeClient.java, ZenithMatrixEffect.java
|-- gui/radial/                # CaduceusRadialMenu, RadialMenu, RadialMenuScreen, RadialMenuSlot
|-- model/                     # CMModels, MagicCubeModel, ModelBase, ModelDefinition, StarCakeBlockModel, StarCakeItemModel
|-- ponder/                    # CTNHManaPonderPlugin, CTNHManaPonderSceneBuilder, CTNHManaPonderScenes, CTNHManaPonderTags
|   `-- mana/                  # MagicRituals, MysticSpire, PonderParticleUtil
|-- render/                    # 11: DeltaSparkRenderer, DemonWillRender, EternalGardenRender, ManaCondenserRender, ManaReactorRender, OmegaSparkRenderer, ShroudGazingRender, StarCakeItemRender, StarCakeMachineBERProvider, StarCakeRender, ZenithMatrixRender
|   `-- particle/              # IconParticle
`-- utils/                     # RenderUtils
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Caduceus radial menu | `client/gui/radial/` (4 classes) |
| Ponder plugin | `client/ponder/CTNHManaPonderPlugin.java` |
| Ponder scenes/tags | `client/ponder/CTNHManaPonderScenes.java`, `CTNHManaPonderTags.java` |
| Mystic Spire scenes | `client/ponder/mana/` (MagicRituals, MysticSpire, PonderParticleUtil) |
| Ponder adapter builder | `client/ponder/CTNHManaPonderSceneBuilder.java` |
| Models | `client/model/` (CMModels, MagicCubeModel, StarCake models) |
| Renderers | `client/render/` (11 renderers) |
| Zenith invasion client | `client/ZenithInvadeClient.java` |

## CONVENTIONS
- Ponder scenes use `scene.title(..., en, cn)` / `scene.showText(..., en, cn)` with text embedded directly in scene files.
- `CTNHManaPonderSceneBuilder` is a thin adapter around CTNH-Lib's shared builder.
- Ponder lang extraction happens via `event/EventHandler.gatherData()` using CTNH-Lib's `CTNHPonderLang.init(new CTNHManaPonderPlugin())`.

## ANTI-PATTERNS
- Do not move Mana Ponder scenes/tags/plugins to Core or Lib.
- Do not change Caduceus/Saber client behavior without checking both networking packets and item property model predicates.

## SCOPE
Applies to `src/main/java/com/moguang/ctnhmana/client` and its child packages.

## READ WHEN
- Adding or changing Mana Ponder scenes, the Caduceus radial menu, or rendering.
- Working on Zenith invasion client effects.

## SOURCE OF TRUTH
- `client/ponder/CTNHManaPonderPlugin.java` and `event/EventHandler.gatherData()` wiring.

## WORKFLOW
1. Read the shared Ponder builder guide in `docs/CTNH-Lib/client/AGENTS.md` before writing scenes.
2. Add scene/tag registrations in the plugin.
3. Run `:modules:CTNH-Mana:runData` after Ponder text changes.