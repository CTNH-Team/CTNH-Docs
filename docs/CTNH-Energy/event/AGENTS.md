# CTNH-ENERGY EVENT DOMAIN

## OVERVIEW
Forge event handlers for Energy (2 Java files).

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Event handler | `event/ForgeEventHandler.java` |
| Client events | `event/ForgeClientEventHandler.java` |

## CONVENTIONS
- Event subscribers are lifecycle entry points; trace them through annotations and registration sites.

## ANTI-PATTERNS
- Do not move event wiring into registry classes.

## SCOPE
Applies to `src/main/java/tech/luckyblock/mcmod/ctnhenergy/event`.

## READ WHEN
- Adding Forge lifecycle event handling in Energy.

## SOURCE OF TRUTH
- `event/` classes and `common/CommonProxy.java`.

## WORKFLOW
1. Identify the Forge event and its registration site.
2. Run `:modules:CTNH-Energy:build`.
