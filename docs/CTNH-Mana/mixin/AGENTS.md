# CTNH-MANA MIXIN DOMAIN

## OVERVIEW
Ars Nouveau, Blood Magic, Botania, and EMI compatibility mixins (10 Java files).

## STRUCTURE
```text
mixin/
|-- ars/                       # MixinEmiLecternRecipeHandler, StoredItemStackMixin
|-- bloodmagic/                # BloodAltarMixin, TileAltarAccessor
|-- botania/                   # BotaniaEntitiesMixin, FunctionalFlowerBaseAccessor, ManaPoolBlockEntityMixin, MixinForgePacketHandler, PetruniaMixin
`-- emi/                       # TagEmiIngredientMixin
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Ars Nouveau patches | `mixin/ars/` |
| Blood Magic patches | `mixin/bloodmagic/` (incl. TileAltarAccessor) |
| Botania patches | `mixin/botania/` (5) |
| EMI patches | `mixin/emi/TagEmiIngredientMixin.java` |
| Mixin config | `src/main/resources/ctnhmana.mixins.json` |

## CONVENTIONS
- Keep mixin JSON and package entries synchronized.
- Magic compatibility is spread across mixins, recipe builders, integrations, and client packets; check all four before changing a magic integration surface.

## ANTI-PATTERNS
- Do not change injection points without checking upstream target members.

## SCOPE
Applies to `src/main/java/com/moguang/ctnhmana/mixin` and `src/main/resources/ctnhmana.mixins.json`.

## READ WHEN
- Patching Ars Nouveau, Blood Magic, Botania, or EMI behavior.

## SOURCE OF TRUTH
- `src/main/resources/ctnhmana.mixins.json` and the mixin classes in `mixin/`.

## WORKFLOW
1. Locate the integration's mixin package and JSON entry.
2. Verify the target member against the loaded mod version.
3. Run `:modules:CTNH-Mana:build`; validate at runtime.
