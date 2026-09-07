# CTNH-LIB COMMAND DOMAIN

## OVERVIEW
Shared chat helper and inspector commands plus dev ore-vein viewer (3 Java files).

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Chat helper | `command/CTNHCommandChatHelper.java` |
| Inspector | `command/CTNHCommandInspector.java` (`/ctnh hand`, `/ctnh showtag`) |
| Command registration | `command/CTNHCommands.java` (`/ctnh` root, permission 0 for hand/showtag, permission 2 for showores) |
| Dev vein viewer | `command/CTNHCommands.java#executeShowOres` (`/ctnh showores <radius 1-4>`) |
| Lang keys | `src/main/resources/assets/ctnhlib/lang/{en_us,zh_cn}.json` (`command.ctnhlib.showores.done`) |

## CONVENTIONS
- Commands are registered through the shared command entry; keep player-facing output consistent via `CTNHCommandChatHelper`.
- `CTNHCommandInspector` uses `ForgeRegistries` only to render registry keys (e.g., `ForgeRegistries.FLUIDS.getKey(...)`), not to resolve recipe items by string. This is the sole allowed `ForgeRegistries` lookup in Lib.
- `/ctnh showores <radius>` is a dev-only command (requires permission level 2, player-only): iterates chunk columns around player (`radius` 1-4), skips unloaded chunks and `hasOnlyAir` sections, keeps blocks matching `forge:ores` tag, replaces all other non-air blocks with `Blocks.AIR` via `level.setBlock(..., Block.UPDATE_CLIENTS)`, reports cleared/kept/skipped/elapsedMs via `command.ctnhlib.showores.done`.
- `@SuppressWarnings("removal")` on `CTNHCommands` suppresses deprecated Brigadier/Forge API warnings.

## ANTI-PATTERNS
- Do not add module-specific commands here; register them in the owning module.
- Do not widen `showores` radius beyond 4 or run it on production worlds; it destructively clears blocks.

## SCOPE
Applies to `src/main/java/tech/vixhentx/mcmod/ctnhlib/command`.

## READ WHEN
- Changing shared chat helpers, inspector behavior, or the `showores` dev tool.

## SOURCE OF TRUTH
- `command/CTNHCommands.java` and its registration site (`common/CommonProxy` event bus).

## WORKFLOW
1. Check whether the command belongs in Lib or a feature module.
2. After changing `showores`, verify tag `forge:ores` filtering and `Block.UPDATE_CLIENTS` propagation in a test world.
3. Run `:modules:CTNH-Lib:build` after changes.
