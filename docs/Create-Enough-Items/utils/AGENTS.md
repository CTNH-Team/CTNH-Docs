# CREATE-ENOUGH-ITEMS UTILS DOMAIN

## OVERVIEW
EMI feature implementations (13 Java files): collapsible sidebar groups, duplicate/featured recipe filtering, associated search, fast recipe indexing, drag search fill, and GTCEu voltage filtering for the recipe page.

## STRUCTURE
```text
utils/emi/
|-- TooltipBakeQueue.java
|-- collapsible/               # CEICollapsibleGroups
|-- duplicate/                 # CEIDuplicateRecipeScreen, CEIDuplicateRecipes
|-- featured/                  # CEIFeaturedRecipeScreen, CEIFeaturedRecipes
|-- search/                    # 5: CEIAssociatedSearch, CEIAssociatedSearchRecipeScreen, CEIEmiDragSearchFill, FastRecipeManager, TagRelationGraph
`-- voltage/                   # CEIVoltageRecipeFilter, CEIVoltageRecipeScreen
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Collapsible groups (rules, state, group lookup for tooltip) | `utils/emi/collapsible/CEICollapsibleGroups.java` |
| Featured/duplicate filtering | `utils/emi/featured/`, `utils/emi/duplicate/` |
| Duplicate-recipe ID blocklist (Create + Vintage Improvements) | `utils/emi/duplicate/CEIDuplicateRecipes.java` |
| Associated search | `utils/emi/search/CEIAssociatedSearch.java` |
| Fast recipe indexing | `utils/emi/search/FastRecipeManager.java` |
| Tag relation graph | `utils/emi/search/TagRelationGraph.java` |
| Drag search fill | `utils/emi/search/CEIEmiDragSearchFill.java` |
| Voltage filtering | `utils/emi/voltage/CEIVoltageRecipeFilter.java` |

## CONVENTIONS
- `CEICollapsibleGroups` reads sidebar grouping rules and persists local expanded/collapsed state under `config/cei/collapsible_emi_groups.json`.
- `CEICollapsibleGroups.loadRules()` is now invoked from `ClientProxy` constructor (early) rather than lazily in `rebuild()`, ensuring grouping rules are available before the first EMI UI interaction.
- `EmiScreenManagerInputMixin` calls `CEICollapsibleGroups.getGroup(ingredient)` to append `cei.emi.collapsible.group.count` and `cei.emi.collapsible.group.toggle` lines to the hovered ingredient tooltip.
- `CEIFeaturedRecipes`, `CEIDuplicateRecipes`, `CEIAssociatedSearch`, and `CEIVoltageRecipeFilter` back the recipe-page filters described in the README.
- `CEIDuplicateRecipes` filters via a hardcoded blocklist: `create:automatic_packing`, `create:block_cutting`, `create:fan_smoking`, `create:fan_blasting`, and `vintageimprovements:unpacking` (the Vintage Improvements vibrating-table auto-generated `unpacking` recipe that duplicates a Create compacting recipe). The Vintage entry is built by a `vintageImprovementsId()` helper; IDs are built with `ResourceLocation.tryBuild`, not `ForgeRegistries`.
- Rule JSON accepts item IDs, tags, regex forms, negation, grouped OR/AND syntax, and recipe/category/input/output/catalyst selectors for featured filters.
- `ForgeRegistries` usage here is for EMI rule JSON string-ID matching (reading rule files), not recipe item resolution.

## ANTI-PATTERNS
- Do not edit runtime `config/cei/*.json` to change defaults; edit the static rule files in `src/main/resources/assets/cei/emi/`.
- Do not treat voltage filtering as generic EMI filtering; it only handles GTCEu `GTEmiRecipe` paths.
- Do not resolve the `CEIDuplicateRecipes` ID blocklist through `ForgeRegistries`; keep the hardcoded `ResourceLocation` list.

## SCOPE
Applies to `src/main/java/com/ctnh/cei/utils` and its child packages.

## READ WHEN
- Changing EMI sidebar/search/recipe-page feature behavior.
- Changing collapsible-group tooltip content or grouping rule lookup.
- Changing the duplicate-recipe ID blocklist (Create/Vintage Improvements or other upstream recipe IDs).

## SOURCE OF TRUTH
- `utils/emi/` classes and the static rule JSON in `src/main/resources/assets/cei/emi/`.
- For duplicate filtering, `utils/emi/duplicate/CEIDuplicateRecipes.java` is the source of the recipe-ID blocklist.

## WORKFLOW
1. Check the matching feature class before editing behavior.
2. For duplicate filtering, verify new upstream recipe IDs against the actual generated recipe IDs before adding to the `CEIDuplicateRecipes` blocklist.
3. Validate rule JSON against the accepted selector syntax.
4. Run `:modules:Create-Enough-Items:build`; validate the EMI surface at runtime.
