# CTPP NETWORK DOMAIN

## OVERVIEW
CTPP networking packets (8 Java files), all toolbox-related.

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Action packet | `network/packet/CTPPToolboxActionPacket.java` |
| Bindings packets | `network/packet/CTPPToolboxBindingsPacket.java`, `CTPPToolboxMenuFiltersPacket.java` |
| Open packet | `network/packet/CTPPToolboxOpenNearestPacket.java` |
| Snapshot packets | `network/packet/CTPPToolboxSnapshotPacket.java`, `CTPPToolboxSnapshotRequestPacket.java` |
| Terminal wire packets | `network/packet/CTPPTerminalCancelWireSelectionPacket.java`, `CTPPTerminalWireSelectionPacket.java` |

## CONVENTIONS
- All packets serve the toolbox system (`common/toolbox/`, `client/toolbox/`) and terminal wire selection.
- Packets are registered through the module channel (`registry/CTPPNetwork.java`).

## ANTI-PATTERNS
- Do not register CTPP packets through Lib networking.

## SCOPE
Applies to `src/main/java/com/mo_guang/ctpp/network` and its child packages.

## READ WHEN
- Changing CTPP packet behavior.

## SOURCE OF TRUTH
- `network/` classes and their registration site (`registry/CTPPNetwork.java`).

## WORKFLOW
1. Check packet registration wiring.
2. Run `:modules:CTPP:build`.