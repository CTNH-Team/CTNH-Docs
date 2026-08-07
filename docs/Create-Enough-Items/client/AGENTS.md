# CREATE-ENOUGH-ITEMS CLIENT DOMAIN

## OVERVIEW
Client-side bootstrap for CEI.

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Client proxy | `client/ClientProxy.java` |
| Collapsible groups rule loading | `utils/emi/collapsible/CEICollapsibleGroups.java` (called from ClientProxy constructor) |

## CONVENTIONS
- ClientProxy handles client-side init; common registration stays in `common/CommonProxy.java`.
- `ClientProxy` constructor calls `CEICollapsibleGroups.loadRules()` to load sidebar grouping rules early, before EMI UI is built.
- Keep client-only classes out of common paths.

## ANTI-PATTERNS
- Do not make client-only classes reachable from common paths.

## SCOPE
Applies to `src/main/java/com/ctnh/cei/client`.

## READ WHEN
- Changing CEI client bootstrap or early rule loading.

## SOURCE OF TRUTH
- `client/ClientProxy.java` and `CreateEnoughItems.java` wiring.

## WORKFLOW
1. Check proxy wiring in `CreateEnoughItems.java`.
2. Verify `CEICollapsibleGroups.loadRules()` is called before any EMI UI access.
3. Run `:modules:Create-Enough-Items:build`.
