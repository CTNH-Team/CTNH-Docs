# CTNH-LIB UTILS DOMAIN

## OVERVIEW
Shared helper utilities (8 Java files): chunk lists, environment detection, NBT helpers, map helpers, machine utilities, generic registrate builders, and a deterministic infinite meteor terrain helper.

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Generic registrate all-object builder | `utils/AllBuilder2.java` |
| Generic registrate codec builder | `utils/CodecBuilder.java` |
| Chunk lists | `utils/ChunkList.java` |
| Environment | `utils/EnvUtils.java` |
| NBT helpers | `utils/ExtendNbtUtils.java` |
| Map helpers | `utils/LockIdentityHashMap.java` |
| Machine utils | `utils/MachineUtils.java` |
| Infinite meteor terrain | `utils/InfiniteMeteorTerrain.java` |

## CONVENTIONS
- Helpers are static utilities unless state requires an instance; keep them free of registry dependencies.
- Modules should prefer Lib utils over duplicating helpers locally.
- `AllBuilder2` and `CodecBuilder` are thin generic `AbstractBuilder` wrappers for registering an already-created entry or a codec entry; keep them generic and mod-agnostic.
- `InfiniteMeteorTerrain` is a seeded, deterministic impact-terrain generator; construct it with the world seed and treat its cache as instance-local runtime state.

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