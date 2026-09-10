# CTNH-LIB MIXIN DOMAIN

## OVERVIEW
Bytecode patches for GTM and RecipeManager. 4 Java files. Config `src/main/resources/ctnhlib.mixins.json`.

## WHERE TO LOOK
| Concern | Location |
| Datapack recipe strip | RecipeManagerApplyMixin.java: @Mixin(RecipeManager, priority 1100), @Inject(apply* HEAD), removeIf + RemoveFilter.matches |
| GT recipe handling | GTRecipesMixin.java |
| Machine builder tweak | MachineBuilderMixin.java |
| TMRV tweak | TMRVMixin.java |
| Registration | ctnhlib.mixins.json: mixins=[GTRecipesMixin, MachineBuilderMixin, RecipeManagerApplyMixin, TMRVMixin] |

## CONVENTIONS
- New mixin class must be added to `ctnhlib.mixins.json` mixins array; client mixins to client array.
- Keep priority explicit when ordering matters (RecipeManagerApplyMixin=1100).
- Mixin reads lib state only (RecipeRemovalHelper.getFilters()); no direct module refs.
- Early-return when filter list empty.

## ANTI-PATTERNS
- Adding mixin .java without json entry.
- Parsing recipes in mixin; only strip map keys, leave parsing to RecipeManager.
- Touching dynamic GT recipes here.

## SCOPE
Mixins owned by lib only. No gameplay logic.

## READ WHEN
Adding/changing any ctnhlib mixin or mixins json.

## SOURCE OF TRUTH
`tech.vixhentx.mcmod.ctnhlib.mixin` + `ctnhlib.mixins.json`.

## WORKFLOW
Add class -> register in json -> verify HEAD inject + filter delegation.