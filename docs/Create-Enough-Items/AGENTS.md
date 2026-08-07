# CREATE-ENOUGH-ITEMS MODULE

## OVERVIEW
Create-Enough-Items (`cei`) is the CTNH EMI experience module (31 Java files): sidebar collapsible groups, recipe-page filters, associated search, drag-to-search, GTCEu voltage filtering, and static EMI rule resources. Namespace is `com.ctnh.cei` (not `com.moguang.cei`).

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
| Create JEI mixin | `mixin/create/CreateJEIMixin.java` (incl. CategoryBuilderMixin inner class) |
| TMRV mixin | `mixin/tmrv/RecipeManagerMixin.java` |
| EditBox accessor | `mixin/accessor/EditBoxAccessor.java` |
| EMI features | `utils/emi/` (collapsible/, duplicate/, featured/, search/, voltage/) |
| Static rule JSON | `src/main/resources/assets/cei/emi/emi_collapsible_groups.json`, `emi_featured_recipes.json` |
| Lang/resources | `src/main/resources/assets/cei/lang/`, `META-INF/mods.toml`, `cei.mixins.json` |

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
- Mixin targets include EMI, Create JEI, TMRV, and GTCEu EMI classes; inspect target method/field names before changing injection points.
- Rule JSON accepts item IDs, tags, regex forms, negation, grouped OR/AND syntax, and recipe/category/input/output/catalyst selectors for featured filters.

## ANTI-PATTERNS
- Do not move EMI UI behavior into CTNH-Core; CEI owns EMI sidebar/search/recipe-page customization.
- Do not edit runtime `config/cei/*.json` to change defaults; edit the static rule files in `src/main/resources/assets/cei/emi/`.
- Do not treat voltage filtering as generic EMI filtering; it only handles GTCEu `GTEmiRecipe` paths.
- Do not change mixin accessor signatures without checking `cei.mixins.json` and the upstream EMI/GTCEu target members.

## COMMANDS
```text
./gradlew :modules:Create-Enough-Items:build
./gradlew :modules:Create-Enough-Items:runData
./gradlew :modules:Create-Enough-Items:spotlessCheck
```

## SCOPE
Applies to `modules/Create-Enough-Items` and its submodule repository. It is a reference guide loaded through the root routing table, not an additional source-tree instruction file.

## READ WHEN
- Changing EMI sidebar, search, or recipe-page behavior.
- Changing EMI/Create/TMRV mixin targets or static rule JSON.

## SOURCE OF TRUTH
- Registration/lifecycle: `CreateEnoughItems.java`, `common/CommonProxy.java`.
- EMI features: `utils/emi/` classes.
- Static rules: `src/main/resources/assets/cei/emi/` JSON files.

## WORKFLOW
1. Map the changed symbol to its domain and read that domain guide.
2. Check EMI mixin targets and accessor alignment before changing behavior.
3. Run the narrowest Gradle task; validate the EMI surface at runtime.
4. Re-read the root routing table if the change introduces a new module boundary.
