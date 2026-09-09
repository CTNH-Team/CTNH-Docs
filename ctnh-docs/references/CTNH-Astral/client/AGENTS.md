# CTNH-ASTRAL CLIENT DOMAIN

## OVERVIEW
Client-side bootstrap and rendering for Astral (3 Java files): ClientProxy, rocket launch HUD, and custom dimension sky effects.

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Client proxy | `client/ClientProxy.java` |
| Rocket HUD | `client/RocketLaunchHud.java` |
| Sky effects | `client/render/MoonEffects.java` |

## CONVENTIONS
- `MoonEffects` registers custom dimension sky effects and is client-only; do not reach it from common construction paths.
- `RocketLaunchHud` pairs with the rocket contraption entity.

## ANTI-PATTERNS
- Do not make client-only classes reachable from common paths.

## SCOPE
Applies to `src/main/java/com/ctnh/ctnhastral/client` and its child packages.

## READ WHEN
- Changing Astral dimension sky effects, rocket HUD, or client rendering.

## SOURCE OF TRUTH
- `client/` classes and mod entry wiring.

## WORKFLOW
1. Check client proxy wiring in `CTNHAstral.java`.
2. Run `:modules:CTNH-Astral:build`; validate the runtime surface if available.
