# CREATE-ENOUGH-ITEMS DATA DOMAIN

## OVERVIEW
Datagen hook for CEI: currently only adds the lang processor.

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Datagen hook | `data/CEIDatagen.java` |

## CONVENTIONS
- `CEIDatagen.init()` currently only adds the lang processor; no generated resource tree was present in the current snapshot.
- Lang/resources live under `src/main/resources/assets/cei/lang/`.

## ANTI-PATTERNS
- Do not hand-edit `src/generated/resources` if one appears later; regenerate via `runData`.

## SCOPE
Applies to `src/main/java/com/ctnh/cei/data`.

## READ WHEN
- Adding CEI datagen output.

## SOURCE OF TRUTH
- `data/CEIDatagen.java` and `common/CommonProxy.init()` wiring.

## WORKFLOW
1. Edit `CEIDatagen`, then run `:modules:Create-Enough-Items:runData`.
2. Inspect generated-resource diffs.
