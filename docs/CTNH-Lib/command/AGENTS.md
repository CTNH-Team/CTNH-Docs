# CTNH-LIB COMMAND DOMAIN

## OVERVIEW
Shared chat helper and inspector commands available across CTNH runtime (3 Java files).

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Chat helper | `command/CTNHCommandChatHelper.java` |
| Inspector | `command/CTNHCommandInspector.java` |
| Command registration | `command/CTNHCommands.java` |

## CONVENTIONS
- Commands are registered through the shared command entry; keep player-facing output consistent.
- `CTNHCommandInspector` uses `ForgeRegistries` only to render registry keys (e.g., `ForgeRegistries.FLUIDS.getKey(...)`), not to resolve recipe items by string.

## ANTI-PATTERNS
- Do not add module-specific commands here; register them in the owning module.

## SCOPE
Applies to `src/main/java/tech/vixhentx/mcmod/ctnhlib/command`.

## READ WHEN
- Changing shared chat helpers or inspector behavior.

## SOURCE OF TRUTH
- `command/CTNHCommands.java` and its registration site.

## WORKFLOW
1. Check whether the command belongs in Lib or a feature module.
2. Run `:modules:CTNH-Lib:build` after changes.
