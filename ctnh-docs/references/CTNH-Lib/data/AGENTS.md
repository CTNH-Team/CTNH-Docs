# CTNH-LIB DATA DOMAIN

## OVERVIEW
Datapack runtime support: dynamic pack + filter + shared removal. 3 Java files.

## WHERE TO LOOK
| Concern | Location |
| Dynamic pack host | CTNHDynamicDataPack.java |
| Static datapack filter | DataFilterPack.java |
| Shared removal registry | recipe/RecipeRemovalHelper.java: FILTERS, remove(), clear(), getFilters(), RemoveFilter |
| Filter fields | RemoveFilter: id/list, idRegex, mod, type, not/or, matches(ResourceLocation) |
| Enforcement point | ../mixin/AGENTS.md: RecipeManagerApplyMixin |

## CONVENTIONS
- Filters applied before RecipeManager parses datapack recipes; dynamic recipes unaffected.
- Top-level fields AND-combined; `not` excludes match, `or` requires one child match.
- `type` derived as namespace + first path segment.
- Module reload must `clear()` before re-registering rules.

## ANTI-PATTERNS
- Reimplementing removal in modules; use RecipeRemovalHelper.
- Filtering dynamic GT recipes here; only datapack map is stripped.
- String ForgeRegistries lookup for filtered outputs; use registry objects to construct filters.

## SCOPE
Datapack ingress only. No recipe creation.

## READ WHEN
Adding/removing datapack recipes across modules.

## SOURCE OF TRUTH
`tech.vixhentx.mcmod.ctnhlib.data` source; mixin applies it.

## WORKFLOW
Register RemoveFilter via helper -> verify RecipeManagerApplyMixin strips map -> in-game check.