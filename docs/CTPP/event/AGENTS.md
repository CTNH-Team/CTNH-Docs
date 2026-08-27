# CTPP EVENT DOMAIN

## OVERVIEW
Forge event handlers for CTPP (1 Java file).

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Event handler | `event/ForgeEventHandler.java` |

## CONVENTIONS
- Event subscribers are lifecycle entry points; trace them through annotations and registration sites.

## ANTI-PATTERNS
- Do not move event wiring into registry classes.

## SCOPE
Applies to `src/main/java/com/mo_guang/ctpp/event`.

## READ WHEN
- Adding Forge lifecycle event handling in CTPP.

## SOURCE OF TRUTH
- `event/` classes and `common/CommonProxy.java`.

## WORKFLOW
1. Identify the Forge event and its registration site.
2. Run `:modules:CTPP:build`.