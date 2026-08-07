# CREATE-ENOUGH-ITEMS UTILS DOMAIN

## OVERVIEW
EMI feature implementations (13 Java files): collapsible groups, duplicate/featured recipe filtering, associated search, fast recipe indexing, drag search fill, and voltage filtering.

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
| Collapsible groups | `utils/emi/collapsible/CEICollapsibleGroups.java` |
| Featured/duplicate filtering | `utils/emi/featured/`, `utils/emi/duplicate/` |
| Associated search | `utils/emi/search/CEIAssociatedSearch.java` |
| Fast recipe indexing | `utils/emi/search/FastRecipeManager.java` |
| Tag relation graph | `utils/emi/search/TagRelationGraph.java` |
| Drag search fill | `utils/emi/search/CEIEmiDragSearchFill.java` |
| Voltage filtering | `utils/emi/voltage/CEIVoltageRecipeFilter.java` |

## CONVENTIONS
- `CEICollapsibleGroups` reads sidebar grouping rules and persists local expanded/collapsed state under `config/cei/collapsible_emi_groups.json`.
- `CEICollapsibleGroups.loadRules()` is now invoked from `ClientProxy` constructor (early) rather than lazily in `rebuild()`, ensuring grouping rules are available before the first EMI UI interaction.
- `CEIFeaturedRecipes`, `CEIDuplicateRecipes`, `CEIAssociatedSearch`, and `CEIVoltageRecipeFilter` back the recipe-page buttons described in the README.
- Rule JSON accepts item IDs, tags, regex forms, negation, grouped OR/AND syntax, and recipe/category/input/output/catalyst selectors for featured filters.
- `ForgeRegistries` usage here is for EMI rule JSON string-ID matching (reading rule files), not recipe item resolution.

## ANTI-PATTERNS
- Do not edit runtime `config/cei/*.json` to change defaults; edit the static rule files in `src/main/resources/assets/cei/emi/`.
- Do not treat voltage filtering as generic EMI filtering; it only handles GTCEu `GTEmiRecipe` paths.

## SCOPE
Applies to `src/main/java/com/ctnh/cei/utils` and its child packages.

## READ WHEN
- Changing EMI sidebar/search/recipe-page feature behavior.

## SOURCE OF TRUTH
- `utils/emi/` classes and the static rule JSON in `src/main/resources/assets/cei/emi/`.

## WORKFLOW
1. Check the matching feature class before editing behavior.
2. Validate rule JSON against the accepted selector syntax.
3. Run `:modules:Create-Enough-Items:build`; validate the EMI surface at runtime.
