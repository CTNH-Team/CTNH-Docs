# CTNH-ENERGY CLIENT DOMAIN

## OVERVIEW
Energy-owned AE2 Ponder plugin, scene/tag registrations, adapter builder, scene implementations, and rendering (21 Java files).

## STRUCTURE
```text
client/
|-- ClientProxy.java
|-- render/                    # EUKeyRenderHandler
`-- ponder/
    |-- CTNHEnergyPonderPlugin.java, CTNHEnergyPonderSceneBuilder.java, CTNHEnergyPonderScenes.java, CTNHEnergyPonderTags.java
    `-- ae2/                   # 15 scenes: AE2CablePonderHelper, AnnihilationPlane, BuddingQuartz, Cable, Controller, CraftingProcessUnit, CraftingSystem, FormationPlane, IOPort, ImportExportBus, Interface, MolecularAssembler, PatternProvider, QuantumNetworkBridge, StorageBus
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Ponder plugin | `client/ponder/CTNHEnergyPonderPlugin.java` |
| Ponder scenes/tags | `client/ponder/CTNHEnergyPonderScenes.java`, `CTNHEnergyPonderTags.java` |
| AE2 Ponder scenes | `client/ponder/ae2/` (15 scenes) |
| Ponder adapter builder | `client/ponder/CTNHEnergyPonderSceneBuilder.java` |
| AE2 cable helper | `client/ponder/ae2/AE2CablePonderHelper.java` |
| EU key rendering | `client/render/EUKeyRenderHandler.java` |

## CONVENTIONS
- Ponder scenes use `scene.title(..., en, cn)` / `scene.showText(..., en, cn)` with text embedded directly in scene files.
- `CTNHEnergyPonderSceneBuilder` is a thin adapter around CTNH-Lib's shared builder.
- Datagen wires `common/CommonProxy.gatherData()` on the mod event bus and calls CTNH-Lib's `CTNHPonderLang.init(new CTNHEnergyPonderPlugin())` to extract Ponder language entries.

## ANTI-PATTERNS
- Do not move `client/ponder/ae2/AE2CablePonderHelper.java` to CTNH-Lib; it is AE2-specific visualization code.
- Do not move Energy Ponder scenes/tags/plugin into CTNH-Lib.

## SCOPE
Applies to `src/main/java/tech/luckyblock/mcmod/ctnhenergy/client` and its child packages.

## READ WHEN
- Adding or changing Energy Ponder scenes, tags, or rendering.

## SOURCE OF TRUTH
- `client/ponder/CTNHEnergyPonderPlugin.java` and `common/CommonProxy.gatherData()` wiring.

## WORKFLOW
1. Read the shared Ponder builder guide in `docs/CTNH-Lib/client/AGENTS.md` before writing scenes.
2. Add scene/tag registrations in the plugin.
3. Run `:modules:CTNH-Energy:runData` after Ponder text changes.
