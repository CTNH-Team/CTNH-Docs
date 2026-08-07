# CREATE-ENOUGH-ITEMS CLIENT DOMAIN

## OVERVIEW
Client-side bootstrap for CEI.

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Client proxy | `client/ClientProxy.java` |
| Collapsible rule bootstrap | `client/ClientProxy.java` (constructor -> `CEICollapsibleGroups.loadRules()`) |

## CONVENTIONS
- ClientProxy handles client-side init; common registration stays in `common/CommonProxy.java`.
- The `ClientProxy` constructor eagerly calls `CEICollapsibleGroups.loadRules()` so EMI collapsible group rules are compiled before any sidebar rebuild; `CEICollapsibleGroups.rebuild()` no longer loads rules lazily.

## ANTI-PATTERNS
- Do not make client-only classes reachable from common paths.

## SCOPE
Applies to `src/main/java/com/ctnh/cei/client`.

## READ WHEN
- Changing CEI client bootstrap.

## SOURCE OF TRUTH
- `client/ClientProxy.java` and `CreateEnoughItems.java` wiring.

## WORKFLOW
1. Check proxy wiring in `CreateEnoughItems.java`.
2. Verify collapsible rule load ordering against `CEICollapsibleGroups.loadRules()`.
3. Run `:modules:Create-Enough-Items:build`.