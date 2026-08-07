# CTNH-LIB REGISTRATE DOMAIN

## OVERVIEW
The shared registrate surface (14 Java files): `CNRegistrate` (extends GTCEu `GTRegistrate`), 10 builder wrappers, lang provider, and networking registration.

## STRUCTURE
```text
registrate/
|-- CNRegistrate.java           # extends GTCEu GTRegistrate; CTNH helpers
|-- CTNHLibNetworking.java      # channel registration
|-- builders/                   # 10 builders
|   |-- CTNHItemBuilder / CTNHBlockBuilder / CTNHEntityBuilder
|   |-- CTNHMachineBuilder / CTNHMultiblockMachineBuilder
|   |-- CTNHRecipeType / CTNHRecipeCategory
|   |-- CTNHMaterial / CTNHTagPrefix
|   `-- ICNBuilder              # builder marker interface
|-- data/                       # ProviderTypes
`-- lang/                       # RegistrateCNLangProvider
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Registrate API | `registrate/CNRegistrate.java` |
| Item/block/entity builders | `registrate/builders/CTNHItemBuilder.java`, `CTNHBlockBuilder.java`, `CTNHEntityBuilder.java` |
| Machine builders | `registrate/builders/CTNHMachineBuilder.java`, `CTNHMultiblockMachineBuilder.java` |
| Recipe builders | `registrate/builders/CTNHRecipeType.java`, `CTNHRecipeCategory.java` |
| Material/tag builders | `registrate/builders/CTNHMaterial.java`, `CTNHTagPrefix.java` |
| Lang provider | `registrate/lang/RegistrateCNLangProvider.java` |
| Data helpers | `registrate/data/ProviderTypes.java` |
| Networking | `registrate/CTNHLibNetworking.java` |

## CONVENTIONS
- `CNRegistrate` extends GTCEu `GTRegistrate` and provides CTNH item/block/entity/recipe helpers.
- All CTNH modules create their registrate through `CNRegistrate` (or a thin wrapper like `CEIRegistrate`).
- Lang/datagen support flows through `RegistrateCNLangProvider` and `com.ctnhlang.*` annotations.
- `ICNBuilder` marks shared builder interfaces; new builders should implement it.

## ANTI-PATTERNS
- Do not add module-specific builders here; they belong in the owning module.
- Do not change builder signatures without checking all consumer modules.

## SCOPE
Applies to `src/main/java/tech/vixhentx/mcmod/ctnhlib/registrate` and its child packages.

## READ WHEN
- Adding a shared builder or registrate helper, or changing lang provider behavior.

## SOURCE OF TRUTH
- `registrate/CNRegistrate.java` and `registrate/builders/` contracts.
- Lang annotation processing: `registrate/lang/RegistrateCNLangProvider.java`.

## WORKFLOW
1. Confirm the builder/helper is shared across modules.
2. Check consumer registrates (Core, Energy, Bio, Mana, Astral, CTPP, CEI).
3. Run `:modules:CTNH-Lib:build`; run `runData` when lang generation changed.
