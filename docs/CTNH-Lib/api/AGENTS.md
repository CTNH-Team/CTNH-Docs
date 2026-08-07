# CTNH-LIB API DOMAIN

## OVERVIEW
Shared API values and cross-parallel recipe logic consumed by multiple CTNH modules (3 Java files).

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Shared constants | `api/CTNHValues.java` |
| Cross-parallel recipe logic | `api/CrossParallelRecipeLogic.java`, `api/ICrossParallelRecipeLogicMachine.java` |

## CONVENTIONS
- API surfaces here are consumed by feature modules; keep them stable and dependency-free.
- `CrossParallelRecipeLogic` implements shared parallel recipe behavior used by machine trait implementations (e.g., Core's `SimpleComputationContainer`).

## ANTI-PATTERNS
- Do not add module-specific constants to `CTNHValues`; put them in the owning module.

## SCOPE
Applies to `src/main/java/tech/vixhentx/mcmod/ctnhlib/api`.

## READ WHEN
- Adding shared values or cross-parallel recipe behavior used by multiple modules.

## SOURCE OF TRUTH
- `api/CrossParallelRecipeLogic.java` and its machine interface contract.

## WORKFLOW
1. Confirm the value/logic is used by more than one module.
2. Check consumers in Core/Energy/Bio before changing signatures.
3. Run `:modules:CTNH-Lib:build`.
