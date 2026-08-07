# CTNH-LIB NETWORK DOMAIN

## OVERVIEW
Shared networking: the block highlight packet used by the client highlight renderer (1 Java file).

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Packets | `network/packets/BlockHighlightPacket.java` |
| Networking init | `registrate/CTNHLibNetworking.java` (see registrate domain) |

## CONVENTIONS
- `BlockHighlightPacket` drives the client highlight system; rendering hooks are in `client/render/highlight/`.
- Channel registration happens in `registrate/CTNHLibNetworking.java` from `common/CommonProxy.java`.

## ANTI-PATTERNS
- Do not add module-specific packets here; register them in the owning module.

## SCOPE
Applies to `src/main/java/tech/vixhentx/mcmod/ctnhlib/network`.

## READ WHEN
- Changing the block highlight packet or shared networking behavior.

## SOURCE OF TRUTH
- `network/packets/BlockHighlightPacket.java` and `registrate/CTNHLibNetworking.java`.

## WORKFLOW
1. Check packet registration in `CTNHLibNetworking`.
2. Run `:modules:CTNH-Lib:build` after changes.
