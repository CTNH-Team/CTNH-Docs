# CTNH-ASTRAL API DOMAIN

## OVERVIEW
Public API surface for Astral (1 Java file): loot builder.

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Loot builder | `api/loot/LootBuilder.java` |

## CONVENTIONS
- API classes must not leak client-only classes into common construction paths.

## ANTI-PATTERNS
- Do not add gameplay logic to API classes.

## SCOPE
Applies to `src/main/java/com/ctnh/ctnhastral/api` and its child packages.

## READ WHEN
- Exposing an Astral API surface.

## SOURCE OF TRUTH
- `api/` classes and their consumers.

## WORKFLOW
1. Confirm the surface is genuinely shared before adding it to `api/`.
2. Run `:modules:CTNH-Astral:build`.
