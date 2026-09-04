# CTNH-LIB JADE DOMAIN — REMOVED

## OVERVIEW
Domain removed in f9951f9 (0 Java files). `jade/GTProvidersRegistrar.java`, `jade/JadePriorityManager.java`, and `mixin/GTJadePluginMixin.java` were deleted; `common/CommonProxy.init()` no longer initializes Jade. This file is retained as a tombstone to explain the deletion and prevent reintroduction in Lib.

## STRUCTURE
```text
# no longer present
# former: jade/GTProvidersRegistrar.java (ordered 19 GT providers, 1100-2800)
# former: jade/JadePriorityManager.java (priority-sorted BlockData/BlockComponent registry)
# former: mixin/GTJadePluginMixin.java
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Former registrar | deleted: `jade/GTProvidersRegistrar.java` (see git history f9951f9) |
| Former priority manager | deleted: `jade/JadePriorityManager.java` |
| Former mixin | deleted: `mixin/GTJadePluginMixin.java` |
| Current bootstrap | `common/CommonProxy.java` (`init()` is now empty) |
| Architecture constraints | `docs/_architecture/AGENTS.md` §8 (Jade), §2/§6 (data minimization) |

## CONVENTIONS
- Do not reintroduce Jade provider ordering in CTNH-Lib. If ordering is needed, it is owned directly by GTCEu or the consuming module (Core `registry/jade/CTNHJadePlugin`, Energy/Bio/Mana/CTPP `integration/jade/`).
- Jade NBT minimization still applies per `_architecture` §8: only send information not derivable on client; do not duplicate `@DescSynced` fields (especially `lastRecipe`) via Jade.

## ANTI-PATTERNS
- Do not recreate `GTProvidersRegistrar` or `JadePriorityManager` in Lib.
- Do not add a new `jade/` package to Lib without an architecture decision.

## SCOPE
Applies to the former `src/main/java/tech/vixhentx/mcmod/ctnhlib/jade` (now absent). Keep this tombstone until all consumer docs drop Jade-Lib references.

## READ WHEN
- Investigating why Jade ordering disappeared from Lib or where to add a new Jade provider (answer: outside Lib).

## SOURCE OF TRUTH
- Deletion commit f9951f9; current `common/CommonProxy.java`; `src/main/resources/ctnhlib.mixins.json` (3 mixins, no Jade mixin).

## WORKFLOW
1. Do not restore files in this domain; add Jade providers in the owning feature module.
2. Run `:modules:CTNH-Lib:build` to confirm no Jade references remain.
