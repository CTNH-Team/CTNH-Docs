# CTNH-LIB JADE DOMAIN

## OVERVIEW
Jade provider ordering infrastructure: ordered GT provider registration shared by all CTNH modules (2 Java files).

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Provider registrar | `jade/GTProvidersRegistrar.java` |
| Priority manager | `jade/JadePriorityManager.java` |

## CONVENTIONS
- `GTProvidersRegistrar` loads ordered GT providers; `JadePriorityManager` lets feature modules register/unregister block data and component providers with explicit priority.
- Feature modules register Jade providers through this shared surface, not directly.
- Core's `registry/jade/CTNHJadePlugin` and Energy's `integration/jade/` providers all go through this manager.

## ANTI-PATTERNS
- Do not bypass `JadePriorityManager` for GT provider ordering; CTNH modules rely on predictable Jade block data/component priority.

## SCOPE
Applies to `src/main/java/tech/vixhentx/mcmod/ctnhlib/jade`.

## READ WHEN
- Changing Jade provider ordering or adding shared provider infrastructure.

## SOURCE OF TRUTH
- `jade/GTProvidersRegistrar.java`, `jade/JadePriorityManager.java`, and Core's `registry/jade/` usage.

## WORKFLOW
1. Check the priority manager contract before changing ordering.
2. Validate with a consumer module's Jade providers at runtime.
3. Run `:modules:CTNH-Lib:build`.
