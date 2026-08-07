# CTNH-MANA NETWORKING DOMAIN

## OVERVIEW
Mana networking (5 Java files): Caduceus and Index Fortuna/target packets.

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Networking init | `networking/packets/CMNetworking.java` |
| Caduceus packet | `networking/packets/CaduceusPacket.java` |
| Index packets | `networking/packets/IndexFortunaPacket.java`, `IndexTargetBlockPacket.java`, `IndexTargetParticlePacket.java` |

## CONVENTIONS
- Packets are initialized from `event/EventHandler.commonSetup()`.

## ANTI-PATTERNS
- Do not change Caduceus/Saber client behavior without checking both networking packets and item property model predicates.

## SCOPE
Applies to `src/main/java/com/moguang/ctnhmana/networking` and its child packages.

## READ WHEN
- Changing Mana packet behavior.

## SOURCE OF TRUTH
- `networking/packets/` classes and `event/EventHandler.commonSetup()`.

## WORKFLOW
1. Check packet registration in `EventHandler.commonSetup()`.
2. Run `:modules:CTNH-Mana:build`.
