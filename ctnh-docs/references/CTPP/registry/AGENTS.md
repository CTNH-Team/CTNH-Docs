# CTPP REGISTRY DOMAIN

## OVERVIEW
Registrate surface for CTPP (12 Java files): items, blocks, entities, machines, multiblocks, menus, and recipe types.

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Registrate/root | `registry/CTPPRegistration.java`, `registry/CTPPRegistrate.java` |
| Items/blocks/entities | `registry/CTPPItems.java`, `registry/CTPPBlocks.java`, `CTPPEntityTypes.java` (top-level) |
| Machines/multiblocks | `registry/CTPPMachines.java`, `registry/CTPPMultiblockMachines.java` |
| Materials | `registry/CreateMaterials.java`, `registry/GTMaterialAddon.java` |
| Recipe types/modifiers | `registry/CTPPRecipeTypes.java`, `registry/CTPPRecipeModifiers.java` |
| Menus/network | `registry/CTPPMenus.java`, `registry/CTPPNetwork.java` |
| Creative tabs | `registry/CTPPCreativeModeTabs.java` |
| Block entities | `registry/CTPPBlockEntities.java` |

## CONVENTIONS
- Registry classes use the `CTPP` prefix.
- `CTPP.java` initializes client/common proxy through `DistExecutor` and calls `CTPPEntityTypes.init()`.
- `CTPPRecipeTypes` defines the 8 GT recipe types (see module guide) plus `init()` for MACERATOR→粉碎工厂 conversion.

## ANTI-PATTERNS
- Do not register the same entry from both registry and CommonProxy paths.

## SCOPE
Applies to `src/main/java/com/mo_guang/ctpp/registry`.

## READ WHEN
- Adding or changing CTPP items, blocks, machines, recipe types, or materials.

## SOURCE OF TRUTH
- `registry/CTPPRegistrate.java` and `CTPPGTAddon.java` hook order.

## WORKFLOW
1. Identify the registry class group for the entry.
2. Check GT addon hook order and datagen references.
3. Run `:modules:CTPP:runData` when data is affected.