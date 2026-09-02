# CTNH-MANA EVENT DOMAIN

## OVERVIEW
EventHandler for Mana (16 Java files): machines, multiblocks, recipe types, conditions, materials, tag-prefix ignores, networking, client item properties, datagen, and Mana Ponder lang.

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Main event handler | `event/EventHandler.java` |
| Forge events | `event/ForgeEventHandler.java` |
| Key bindings | `event/CMKeyBindings.java` |
| Index events | `event/IndexEventHandler.java` |
| Soul leech events | `event/SoulLeechEventHandler.java` |
| Tainted Blood events | `event/TaintedBloodWeepingEyeEventHandler.java` |
| Third eye events | `event/ThirdEyeEventHandler.java` |
| Ring events | `event/YurikoRingEventHandler.java` |

## CONVENTIONS
- `EventHandler.java` registers machines, multiblocks, recipe types, recipe conditions, materials, tag-prefix ignores, networking, client item properties, datagen, and Mana Ponder lang.
- `EventHandler.clientSetup()` registers item properties for `SABER_WAND` `wand_status` and `CADUCEUS` `tool_type`.
- `EventHandler.gatherData()` uses CTNH-Lib's `CTNHPonderLang.init(new CTNHManaPonderPlugin())` to extract Mana Ponder scene text during client datagen.
- Networking packets are initialized from `event/EventHandler.commonSetup()`.

## ANTI-PATTERNS
- Do not move event wiring into registry classes.

## SCOPE
Applies to `src/main/java/com/magicbee/ctnhmana/event`.

## READ WHEN
- Adding Forge lifecycle, material, or datagen event handling in Mana.

## SOURCE OF TRUTH
- `event/EventHandler.java` and `common/` registration wiring.

## WORKFLOW
1. Identify the Forge event and its registration site.
2. Check both common and client event handler paths.
3. Run `:modules:CTNH-Mana:build`.