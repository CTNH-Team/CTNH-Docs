# CREATE-ENOUGH-ITEMS EVENT DOMAIN

## OVERVIEW
Event handlers for CEI.

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Client event handler | `event/ForgeClientEventHandler.java` |

## CONVENTIONS
- Event subscribers are lifecycle entry points; trace them through annotations and registration sites.

## ANTI-PATTERNS
- Do not move event wiring into registry classes.

## SCOPE
Applies to `src/main/java/com/ctnh/cei/event`.

## READ WHEN
- Adding Forge lifecycle event handling in CEI.

## SOURCE OF TRUTH
- `event/` classes and `common/CommonProxy.java`.

## WORKFLOW
1. Identify the Forge event and its registration site.
2. Run `:modules:Create-Enough-Items:build`.
