# CTNH-CORE EVENT DOMAIN

## OVERVIEW
Forge event handlers and background task managers for Core runtime behavior (5 Java files).

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Main event handler | `event/ForgeEventHandler.java` |
| Client events | `event/ForgeClientEventHandler.java` |
| Dimension flight | `event/DimensionFlightHandler.java` |
| Build tasks | `event/BuildTaskManager.java` |
| Network events | `event/ProvidableNetEventHandler.java` |

## CONVENTIONS
- Event subscribers and registry callbacks are lifecycle entry points; trace them through annotations, not ordinary Java callers.
- Capability attach hooks (EIO capacitor capabilities, namespace/remap helpers) are wired through `common/capability/` from here.
- `ProvidableNetEventHandler` works with `common/machine/trait/providable_net/` machines.
- `ForgeEventHandler` also hosts the soul torch easter egg (`onSoulTorchEasterEgg`), which spawns a firework and plays the `easter_egg_clown` sound event.

## ANTI-PATTERNS
- Do not move event logic into registry classes; keep lifecycle wiring in `event/`.
- Do not make client-only event subscribers reachable from common paths.

## SCOPE
Applies to `src/main/java/io/github/cpearl0/ctnhcore/event`.

## READ WHEN
- Adding Forge lifecycle, capability, or network event handling in Core.
- Tracing runtime hooks that have few ordinary Java callers.

## SOURCE OF TRUTH
- `event/ForgeEventHandler.java`, `event/ForgeClientEventHandler.java`, and the mod event bus wiring in `common/CommonProxy.java`.

## WORKFLOW
1. Identify the Forge event and its registration site.
2. Check both common and client event handler classes.
3. Run `:modules:CTNH-Core:build` and validate the runtime surface if available.