# CREATE-ENOUGH-ITEMS REGISTRY DOMAIN

## OVERVIEW
CEI registrate: a thin `CNRegistrate` wrapper using mod id `cei`.

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Registrate | `registry/CEIRegistrate.java` |

## CONVENTIONS
- `CEIRegistrate.create()` wraps CTNH-Lib's `CNRegistrate` with mod id `cei`.
- `CreateEnoughItems.REGISTRATE` is created from `CEIRegistrate.create()` and registered in `CommonProxy.init()`.
- No `*GTAddon.java` exists in this module; GTCEu integration is currently through EMI/GTCEu mixins and recipe inspection helpers.

## ANTI-PATTERNS
- Do not register GTCEu content here without adding the corresponding listeners in `CommonProxy`.

## SCOPE
Applies to `src/main/java/com/ctnh/cei/registry`.

## READ WHEN
- Changing CEI registrate setup.

## SOURCE OF TRUTH
- `registry/CEIRegistrate.java` and `common/CommonProxy.init()`.

## WORKFLOW
1. Check `CommonProxy.init()` registrate wiring.
2. Run `:modules:Create-Enough-Items:build`.
