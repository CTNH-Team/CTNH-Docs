# CTNH-ENERGY NETWORK DOMAIN

## OVERVIEW
Energy networking (2 Java files): packets and sync data.

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Packets | `network/packets/QCOpenCPUMenuPacket.java` |
| Sync data | `network/syncdata/AEKeyPayLoad.java` |

## CONVENTIONS
- `QCOpenCPUMenuPacket` opens the quantum computer CPU selection menu.
- UI progress sync (quantum computer/menu updates) is part of the module; do not treat it as server-only.

## ANTI-PATTERNS
- Do not register Energy packets through Lib networking; use the module channel.

## SCOPE
Applies to `src/main/java/tech/luckyblock/mcmod/ctnhenergy/network` and its child packages.

## READ WHEN
- Changing Energy packet or sync data behavior.

## SOURCE OF TRUTH
- `network/` classes and `common/CommonProxy.init()` networking registration.

## WORKFLOW
1. Check packet registration in `CommonProxy.init()`.
2. Run `:modules:CTNH-Energy:build`.
