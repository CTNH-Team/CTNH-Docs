# CTNH-BIO EVENT DOMAIN

## OVERVIEW
Forge event handlers for Bio (3 Java files): GT registry listeners, Jade status provider, Forge capabilities, datagen, material hooks, and transform management.

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Main event handler | `event/EventHandler.java` |
| Forge event handler | `event/ForgeEventHandler.java` |
| Transform manager | `event/TransformManager.java` |

## CONVENTIONS
- Event subscribers are lifecycle entry points; trace them through annotations and registration sites.
- Material hooks and Jade registration flow through this handler.
- `TransformManager` handles entity/machine transform behavior.

## ANTI-PATTERNS
- Do not move event wiring into registry classes.

## SCOPE
Applies to `src/main/java/com/moguang/ctnhbio/event`.

## READ WHEN
- Adding Forge lifecycle or capability event handling in Bio.

## SOURCE OF TRUTH
- `event/EventHandler.java`, `event/ForgeEventHandler.java`, and `common/CommonProxy.java`.

## WORKFLOW
1. Identify the Forge event and its registration site.
2. Run `:modules:CTNH-Bio:build`.
