# CREATE-ENOUGH-ITEMS MODULE

## OVERVIEW
Create-Enough-Items (`cei`) is the CTNH EMI experience module (31 Java files): sidebar collapsible groups (with member-count/toggle tooltips), recipe-page filters (with focused-page preservation on refresh), associated search, drag-to-search, GTCEu voltage filtering (with one-click reset), cheat-mode fluid-container filling, disabled center search bar, and static EMI rule resources. Namespace is `com.ctnh.cei` (not `com.moguang.cei`).

## STRUCTURE
```text
src/main/java/com/ctnh/cei/
|-- CreateEnoughItems.java    # mod entry (@Mod)
|-- client/                   # ClientProxy
|-- common/                   # CommonProxy
|-- data/                     # CEIDatagen (lang processor)
|-- event/                    # ForgeClientEventHandler
|-- mixin/                    # 12: accessor/ (EditBoxAccessor), create/ (CreateJEIMixin), emi/ (8), emi/accessor/ (GTEmiRecipeAccessor), tmrv/ (RecipeManagerMixin)
|-- registry/                 # CEIRegistrate
`-- utils/                    # 13: emi/ (TooltipBakeQueue), emi/collapsible/, emi/duplicate/, emi/featured/, emi/search/ (5), emi/voltage/
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Mod entry | `CreateEnoughItems.java` |
| Proxies | `client/ClientProxy.java`, `common/CommonProxy.java` |
| Registrate | `registry/CEIRegistrate.java` |
| Datagen hook | `data/CEIDatagen.java` |
| EMI mixins | `mixin/emi/` (8), `mixin/emi/accessor/GTEmiRecipeAccessor.java` |
| EMI screen-manager behavior | `mixin/emi/EmiScreenManagerMixin.java` (fluid-stack give → GT `FLUID_CELL`, cursor-container fill, `centerSearchBar` forced off) |
| Collapsible-group G button + group tooltip | `mixin/emi/EmiScreenManagerInputMixin.java` (draws G button left of search box, appends group count/toggle tooltip lines) |
| Voltage-filter reset button | `mixin/emi/EmiScreenManagerInputMixin.java` + `mixin/emi/RecipeScreenMixin.java` (draws/handles reset button; `cei$resetVoltageFilter`) |
| Recipe-page filter refresh | `mixin/emi/RecipeScreenMixin.java` (applies CEI filters, restores focused category/page instead of resetting to tab 0) |
| Create JEI mixin | `mixin/create/CreateJEIMixin.java` (incl. CategoryBuilderMixin inner class) |
| TMRV mixin | `mixin/tmrv/RecipeManagerMixin.java` |
| EditBox accessor | `mixin/accessor/EditBoxAccessor.java` |
| EMI features | `utils/emi/` (collapsible/, duplicate/, featured/, search/, voltage/ (filter + reset)) |
| Static rule JSON | `src/main/resources/assets/cei/emi/emi_collapsible_groups.json`, `emi_featured_recipes.json` |
| Lang/resources | `src/main/resources/assets/cei/lang/`, `META-INF/mods.toml`, `cei.mixins.json` |

## ARCHITECTURE CONTRACT
Machine/trait/capability/Jade 的所有权边界、字段同步与持久化规则、Jade 数据最小化原则和迁移步骤在 `docs/_architecture/AGENTS.md`。改动机器、trait、recipe capability 或 Jade 代码前先读它；本文件只描述本模块的落点。

## DOMAIN GUIDE ROUTING
Read the matching domain guide before editing the corresponding source area.

| Source area | Guide | Read before |
|-------------|-------|-------------|
| `client` | `docs/Create-Enough-Items/client/AGENTS.md` | ClientProxy |
| `common` | `docs/Create-Enough-Items/common/AGENTS.md` | CommonProxy |
| `data` | `docs/Create-Enough-Items/data/AGENTS.md` | CEIDatagen |
| `event` | `docs/Create-Enough-Items/event/AGENTS.md` | ForgeClientEventHandler |
| `mixin` | `docs/Create-Enough-Items/mixin/AGENTS.md` | EMI/Create/TMRV mixins and accessors |
| `registry` | `docs/Create-Enough-Items/registry/AGENTS.md` | CEIRegistrate |
| `utils` | `docs/Create-Enough-Items/utils/AGENTS.md` | EMI feature implementations |

## CONVENTIONS
- Namespace is `com.ctnh.cei`; class prefixes use `CEI`.
- This module depends on `:modules:CTNH-Lib` via `dependencies.gradle`; it does not depend on CTNH-Core.
- User toggle state is runtime config under `config/cei/`; built-in defaults are static JSON under `src/main/resources/assets/cei/emi/`.
- `EmiScreenManagerMixin` converts EMI fluid-stack give into a GT `FLUID_CELL`, fills the held container on `mouseReleased`, and forces `EmiConfig.centerSearchBar` off; these are code-intrinsic EMI patches, not config options.
- `EmiScreenManagerInputMixin` draws the collapsible-group G button to the **left** of the EMI search box, appends group member-count and Alt+Left-click toggle lines to the hovered ingredient tooltip, and draws the voltage-filter reset button below the min/max tier buttons.
- `RecipeScreenMixin.cei$refreshFilteredRecipes()` preserves the focused recipe category/page when filters change; it no longer resets `tabPage`/`tab`/`page` to 0.
- Rule JSON accepts item IDs, tags, regex forms, negation, grouped OR/AND syntax, and recipe/category/input/output/catalyst selectors for featured filters.

## ANTI-PATTERNS
- Do not move EMI UI behavior into CTNH-Core; CEI owns EMI sidebar/search/recipe-page customization.
- Do not handle EMI cheat-mode container filling outside `mixin/emi/EmiScreenManagerMixin.java`; it is screen-manager behavior owned by CEI.
- Do not edit runtime `config/cei/*.json` to change defaults; edit the static rule files in `src/main/resources/assets/cei/emi/`.
- Do not treat voltage filtering as generic EMI filtering; it only handles GTCEu `GTEmiRecipe` paths.
- Do not change mixin accessor signatures without checking `cei.mixins.json` and the upstream EMI/GTCEu target members.
- Do not reintroduce the old `RecipeScreenMixin` filter-refresh reset to tab 0/page 0; CEI preserves the focused recipe page.

## COMMANDS
```text
./gradlew :modules:Create-Enough-Items:build
./gradlew :modules:Create-Enough-Items:runData
./gradlew :modules:Create-Enough-Items:spotlessCheck
```

## SCOPE
Applies to `modules/Create-Enough-Items` and its submodule repository. It is a reference guide loaded through the root routing table, not an additional source-tree instruction file.

## READ WHEN
- Changing EMI sidebar, search, recipe-page, or screen-manager give/fill behavior.
- Changing EMI/Create/TMRV mixin targets or static rule JSON.
- Changing the collapsible-group G button or group tooltip rendering.
- Changing the voltage-filter reset button or recipe-page filter refresh behavior.

## SOURCE OF TRUTH
- Registration/lifecycle: `CreateEnoughItems.java`, `common/CommonProxy.java`.
- EMI features: `utils/emi/` classes.
- EMI screen-manager behavior: `mixin/emi/EmiScreenManagerMixin.java`, `mixin/emi/EmiScreenManagerInputMixin.java`.
- Recipe-page filter refresh: `mixin/emi/RecipeScreenMixin.java`.
- Static rules: `src/main/resources/assets/cei/emi/` JSON files.

## WORKFLOW
1. Map the changed symbol to its domain and read that domain guide.
2. Check EMI mixin targets and accessor alignment before changing behavior.
3. Run the narrowest Gradle task; validate the EMI surface at runtime.
4. Re-read the root routing table if the change introduces a new module boundary.