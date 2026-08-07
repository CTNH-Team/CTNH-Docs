# CTNH-LIB UTILS DOMAIN

## OVERVIEW
Shared helper utilities (5 Java files): chunk lists, environment detection, NBT helpers, map helpers, and machine utilities.

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Chunk lists | `utils/ChunkList.java` |
| Environment | `utils/EnvUtils.java` |
| NBT helpers | `utils/ExtendNbtUtils.java` |
| Map helpers | `utils/LockIdentityHashMap.java` |
| Machine utils | `utils/MachineUtils.java` |

## CONVENTIONS
- Helpers are static utilities unless state requires an instance; keep them free of registry dependencies.
- Modules should prefer Lib utils over duplicating helpers locally.

## ANTI-PATTERNS
- Do not add module-specific helpers here; put them in the owning module's `utils/`.

## SCOPE
Applies to `src/main/java/tech/vixhentx/mcmod/ctnhlib/utils`.

## READ WHEN
- Reusing shared helper logic across modules.

## SOURCE OF TRUTH
- The utility classes in `utils/`.

## WORKFLOW
1. Check whether the helper already exists in Lib before writing a new one.
2. Run `:modules:CTNH-Lib:build` after changes.
