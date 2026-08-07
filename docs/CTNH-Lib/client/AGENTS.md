# CTNH-LIB CLIENT DOMAIN

## OVERVIEW
Client-side shared infrastructure: ClientProxy, right configurator UI, block highlight rendering, and the shared Ponder framework (7 Java files).

## STRUCTURE
```text
client/
|-- ClientProxy.java
|-- ponder/                    # CTNHPonderLang, CTNHPonderSceneBuilder, CTNHPonderTagHelper
|-- render/                    # ColorData
`-- render/highlight/          # HighlightHandler, HighlightRender
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Client bootstrap | `client/ClientProxy.java` |
| Right configurator UI | `client/gui/RightConfiguratorPanel.java`, `IRCFancyUIProvider.java`, `RCUIWidget.java` |
| Highlight rendering | `client/render/highlight/HighlightHandler.java`, `HighlightRender.java` |
| Ponder framework | `client/ponder/CTNHPonderSceneBuilder.java`, `CTNHPonderLang.java`, `CTNHPonderTagHelper.java` |
| Color data | `client/render/ColorData.java` |

## CONVENTIONS
- `RightConfiguratorPanel`, `IRCFancyUIProvider`, and `RCUIWidget` let Core/Energy part machines attach right-side widgets through a shared surface.
- `CTNHPonderSceneBuilder` provides shared baseplate/camera helpers, `title/showText` bilingual text registration via module-supplied `LangRegistrar`, and shared Ponder scene lang extraction for datagen.
- `CTNHPonderLang` is reusable datagen lang extraction; modules pass their mod id, registrate lang callback, and their own `PonderPlugin` to `init(...)`.
- `CTNHPonderTagHelper` provides shared Ponder tag registration helpers.
- `ClientProxy.java` hooks render-level events into `HighlightHandler`/`HighlightRender`; packets use `network/packets/BlockHighlightPacket.java`.

## ANTI-PATTERNS
- Do not move module-specific Ponder scenes/tags/plugins or Energy's AE2 cable helper into Lib.
- Do not add module-specific GUI logic to the shared right configurator panel.

## SCOPE
Applies to `src/main/java/tech/vixhentx/mcmod/ctnhlib/client` and its child packages.

## READ WHEN
- Changing the right configurator UI, highlight rendering, or shared Ponder builder/lang/tag extraction.

## SOURCE OF TRUTH
- `client/ClientProxy.java` (bootstrap), `client/gui/RightConfiguratorPanel.java`, `client/ponder/CTNHPonderSceneBuilder.java`.

## WORKFLOW
1. Confirm the change is shared across modules before editing Lib client code.
2. Check Core/Energy Ponder adapters for affected call sites.
3. Run `:modules:CTNH-Lib:build` and the narrowest consumer task.
