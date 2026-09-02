# CTNH-MANA NETWORKING DOMAIN

## OVERVIEW
Mana networking (7 Java files): Caduceus, Index Fortuna/target, and Zenith invasion packets.

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Networking init | `networking/packets/CMNetworking.java` |
| Antagonism packet | `networking/packets/AntagonismPacket.java` |
| Caduceus packet | `networking/packets/CaduceusPacket.java` |
| Index packets | `networking/packets/IndexFortunaPacket.java`, `IndexTargetBlockPacket.java`, `IndexTargetParticlePacket.java` |
| Zenith invasion packet | `networking/packets/ZenithInvadePacket.java` |

## CONVENTIONS
- Packets are initialized from `event/EventHandler.commonSetup()`.

## ANTI-PATTERNS
- Do not change Caduceus/Saber client behavior without checking both networking packets and item property model predicates.

## SCOPE
Applies to `src/main/java/com/magicbee/ctnhmana/networking` and its child packages.

## READ WHEN
- Changing Mana packet behavior.

## SOURCE OF TRUTH
- `networking/packets/` classes and `event/EventHandler.commonSetup()`.

## WORKFLOW
1. Check packet registration in `EventHandler.commonSetup()`.
2. Run `:modules:CTNH-Mana:build`.