# CTNH-ENERGY REGISTRY DOMAIN

## OVERVIEW
Registrate surface for Energy (9 Java files): items, blocks, machines, multiblocks, recipe types, and AE menus/network registration.

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Registrate/root | `registry/CERegistrate.java` |
| Items/blocks | `registry/CEItems.java`, `registry/CEBlocks.java` |
| Machines/multiblocks | `registry/CEMachines.java`, `registry/CEMultiblock.java` |
| Recipe types | `registry/CERecipeTypes.java` |
| AE menus | `registry/AEMenus.java` |
| Networking | `registry/CENetWorking.java` |
| Creative tabs | `registry/CECreativeModeTabs.java` |

## CONVENTIONS
- Registry classes use the `CE` prefix.
- `CTNHEnergyGTAddon.initializeAddon()` initializes `CEBlocks` and `CEItems`; broader AE2/EU wiring is in `common/CommonProxy.java`.
- Machines/multiblocks are registered from `common/CommonProxy.registerMachines()`; recipe types from `registerRecipeTypes()`.

## ANTI-PATTERNS
- Do not register the same entry from both registry and CommonProxy paths.

## SCOPE
Applies to `src/main/java/tech/luckyblock/mcmod/ctnhenergy/registry`.

## READ WHEN
- Adding or changing Energy items, blocks, machines, recipe types, or menus.

## SOURCE OF TRUTH
- `registry/CERegistrate.java` and `CTNHEnergyGTAddon.java` / `common/CommonProxy.java` hook order.

## WORKFLOW
1. Identify the registry class group for the entry.
2. Check GT addon hook order and CommonProxy registration.
3. Run `:modules:CTNH-Energy:build`.
