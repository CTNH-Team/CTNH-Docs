# CREATE-ENOUGH-ITEMS MIXIN DOMAIN

## OVERVIEW
EMI mixins (recipe screen buttons, sidebar behavior, search refresh hooks, tag expansion, recipe manager replacement), Create JEI mixin, TMRV mixin, and accessors (12 Java files).

## STRUCTURE
```text
mixin/
|-- accessor/                  # EditBoxAccessor
|-- create/                    # CreateJEIMixin (incl. CategoryBuilderMixin inner class)
|-- emi/                       # 8: EmiApiTagExpandMixin, EmiRecipesMixin, EmiScreenManagerInputMixin, EmiScreenManagerMixin, EmiScreenManagerScreenSpaceMixin, EmiSearchMixin, EmiTagsMixin, RecipeScreenMixin
|-- emi/accessor/              # GTEmiRecipeAccessor
`-- tmrv/                      # RecipeManagerMixin
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| EMI mixins | `mixin/emi/` (8) |
| GTEmiRecipe accessor | `mixin/emi/accessor/GTEmiRecipeAccessor.java` |
| Create JEI mixin | `mixin/create/CreateJEIMixin.java` |
| TMRV mixin | `mixin/tmrv/RecipeManagerMixin.java` |
| EditBox accessor | `mixin/accessor/EditBoxAccessor.java` |
| Mixin config | `src/main/resources/cei.mixins.json` (6 mixins + 7 client) |

## CONVENTIONS
- Mixin targets include EMI, Create JEI, TMRV, and GTCEu EMI classes; inspect target method/field names before changing injection points.
- Keep accessor names aligned with mixin targets.
- Keep mixin JSON and package entries synchronized.

## ANTI-PATTERNS
- Do not change mixin accessor signatures without checking `cei.mixins.json` and the upstream EMI/GTCEu target members.

## SCOPE
Applies to `src/main/java/com/ctnh/cei/mixin` and `src/main/resources/cei.mixins.json`.

## READ WHEN
- Patching EMI recipe screen, sidebar, search, tag expansion, recipe manager, Create JEI, or TMRV behavior.

## SOURCE OF TRUTH
- `src/main/resources/cei.mixins.json` and the mixin/accessor classes in `mixin/`.

## WORKFLOW
1. Locate the mixin package and JSON entry.
2. Verify the target member against the loaded EMI/GTCEu version.
3. Run `:modules:Create-Enough-Items:build`; validate the EMI surface at runtime.
