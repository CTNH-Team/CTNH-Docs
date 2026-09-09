# CTNH-ASTRAL REGISTRY DOMAIN

## OVERVIEW
Registrate surface for Astral (18 Java files): blocks (including worldgen-specific astral/moon/mars blocks), items, machines, rocket content, sounds, and recipe types.

## STRUCTURE
```text
registry/
|-- CARegistrate.java, CABlocks.java, CAItems.java, CACreativeModeTabs.java
|-- CAMachines.java, CAMultiblocks.java
|-- CARocketBlocks.java, CARocketEntityTypes.java
|-- CARecipeConditions.java, CARecipeModifiers.java, CARecipeTypes.java
|-- CTNHBlockInfo.java
|-- sound/                     # CAMusics, CASoundDefinitionsProvider, CASoundEvents
`-- worldgen/                  # AstralBlocks, MarsBlocks, MoonBlocks
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Registrate/root | `registry/CARegistrate.java` |
| Blocks/items | `registry/CABlocks.java`, `registry/CAItems.java` |
| Worldgen blocks | `registry/worldgen/AstralBlocks.java`, `registry/worldgen/MoonBlocks.java`, `registry/worldgen/MarsBlocks.java` |
| Rocket content | `registry/CARocketBlocks.java`, `registry/CARocketEntityTypes.java` |
| Machines/multiblocks | `registry/CAMachines.java`, `registry/CAMultiblocks.java` |
| Recipe types/conditions/modifiers | `registry/CARecipeTypes.java`, `CARecipeConditions.java`, `CARecipeModifiers.java` |
| Sounds | `registry/sound/` (CASoundEvents, CAMusics, CASoundDefinitionsProvider) |

## CONVENTIONS
- Registry classes use the `CA` prefix.
- `CTNHAstralGTAddon.registerTagPrefixes()` initializes `AstralBlocks`, `MoonBlocks`, `CTNHBlockInfo`, and `CATagPrefixes`; `registerElements()` initializes `CAElements`.

## ANTI-PATTERNS
- Do not register the same entry from both registry and CommonProxy paths.

## SCOPE
Applies to `src/main/java/com/ctnh/ctnhastral/registry` and its child packages.

## READ WHEN
- Adding or changing Astral blocks, items, machines, or sounds.

## SOURCE OF TRUTH
- `registry/CARegistrate.java` and `CTNHAstralGTAddon.java` hook order.

## WORKFLOW
1. Identify the registry class group for the entry.
2. Check GT addon hook order and worldgen block dependencies.
3. Run `:modules:CTNH-Astral:build`.
