# CREATE-ENOUGH-ITEMS MIXIN DOMAIN

## OVERVIEW
EMI mixins (recipe screen buttons, sidebar behavior, search refresh hooks, tag expansion, recipe manager replacement, fluid-stack give handling, cursor-container filling, center-search-bar disable, collapsible-group tooltip, G-button placement left of the search box, voltage-filter reset button, recipe-page filter refresh preserving focused category/page), Create JEI mixin, TMRV mixin, and accessors (12 Java files).

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
| EMI mixins | `mixin/emi/` (8) — `EmiScreenManagerMixin` handles fluid-stack give → GT `FLUID_CELL`, cursor-container fill, and `centerSearchBar` forced off; `EmiScreenManagerInputMixin` draws the G button left of the search box and appends group count/toggle tooltip lines |
| Voltage-filter reset button | `mixin/emi/EmiScreenManagerInputMixin.java` + `mixin/emi/RecipeScreenMixin.java` (draws/handles reset button; `cei$resetVoltageFilter`) |
| Recipe-page filter refresh | `mixin/emi/RecipeScreenMixin.java` (applies CEI filters, restores focused category/page via `cei$restoreFocusedPage`) |
| GTEmiRecipe accessor | `mixin/emi/accessor/GTEmiRecipeAccessor.java` |
| Create JEI mixin | `mixin/create/CreateJEIMixin.java` |
| TMRV mixin | `mixin/tmrv/RecipeManagerMixin.java` |
| EditBox accessor | `mixin/accessor/EditBoxAccessor.java` |
| Mixin config | `src/main/resources/cei.mixins.json` (6 mixins + 7 client) |

## CONVENTIONS
- Mixin targets include EMI, Create JEI, TMRV, and GTCEu EMI classes; inspect target method/field names before changing injection points.
- `EmiScreenManagerMixin` is `remap = false` and targets `EmiScreenManager`; it uses `Redirect` for fluid-stack give, `Inject` at `deleteCursor` inside `mouseReleased` to fill the held container, and `ModifyExpressionValue` on `EmiConfig.centerSearchBar` to disable the centered search box.
- `EmiScreenManagerMixin` syncs filled containers with `CreateItemC2SPacket`, except in creative instabuild.
- `EmiScreenManagerMixin` resolves the handled screen through `EmiApi.getHandledScreen()`; it no longer `@Shadow`s `Minecraft client`.
- `EmiScreenManagerInputMixin` positions the collapsible-group toggle button at `search.getX() - TOGGLE_BUTTON_SIZE - TOGGLE_BUTTON_GAP` (left of the search box) and `@Redirect`s `EmiIngredient.getTooltip()` in `renderCurrentTooltip` to append `cei.emi.collapsible.group.count` and `cei.emi.collapsible.group.toggle` lines for group members.
- `EmiScreenManagerInputMixin` also draws the voltage-filter reset button (56×16) below the min/max tier buttons and handles left-click to call `CEIVoltageRecipeScreen.cei$resetVoltageFilter()`; the min/max button Y is `height - 38` to leave room for the reset row.
- `RecipeScreenMixin` shadows `tabPageSize` (not `tabPage`) and `setPage`; `cei$refreshFilteredRecipes()` captures the focused category and page before applying filters, then restores them via `cei$restoreFocusedPage()` instead of resetting to tab 0/page 0.
- Keep accessor names aligned with mixin targets.
- Keep mixin JSON and package entries synchronized.

## ANTI-PATTERNS
- Do not change mixin accessor signatures without checking `cei.mixins.json` and the upstream EMI/GTCEu target members.
- Do not bypass the creative-instabuild skip before sending `CreateItemC2SPacket` in the `mouseReleased` fill path.
- Do not reintroduce a `@Shadow Minecraft client` in `EmiScreenManagerMixin`; use `EmiApi.getHandledScreen()`.
- Do not move the collapsible-group G button back to the right side of the search box; current behavior is left-aligned next to the search field.
- Do not reintroduce the old `RecipeScreenMixin` filter-refresh reset to `tabPage = 0; tab = 0; page = 0`; preserve the focused category/page.
- Do not place the voltage reset button above or overlapping the min/max tier buttons; it is drawn below them at `cei$getVoltageMinButtonY() + 18`.

## SCOPE
Applies to `src/main/java/com/ctnh/cei/mixin` and `src/main/resources/cei.mixins.json`.

## READ WHEN
- Patching EMI recipe screen, sidebar, search, tag expansion, recipe manager, screen-manager give/fill, Create JEI, or TMRV behavior.
- Changing collapsible-group tooltip rendering or G button placement.
- Changing the voltage-filter reset button or recipe-page filter refresh behavior.

## SOURCE OF TRUTH
- `src/main/resources/cei.mixins.json` and the mixin/accessor classes in `mixin/`, especially `mixin/emi/EmiScreenManagerMixin.java`, `mixin/emi/EmiScreenManagerInputMixin.java`, and `mixin/emi/RecipeScreenMixin.java`.

## WORKFLOW
1. Locate the mixin package and JSON entry.
2. Verify the target member against the loaded EMI/GTCEu version.
3. Run `:modules:Create-Enough-Items:build`; validate the EMI surface at runtime.