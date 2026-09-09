# CTPP SYNCDATA DOMAIN

## OVERVIEW
Sync-data accessor for CTPP (1 Java file): terminal link state synchronization.

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Terminal link accessor | `syncdata/TerminalLinkStateAccessor.java` |
| Terminal link state | `api/terminal/TerminalLinkState.java`, `api/terminal/TerminalProperties.java` |
| Consumers | `common/blockentity/VoltageTerminalBlockEntity.java`, `client/terminal/` |

## CONVENTIONS
- Accessor is used for field-managed sync storage (`FieldManagedStorage`) of `VoltageTerminalBlockEntity` links.

## ANTI-PATTERNS
- Do not bypass accessor for direct NBT sync.

## SCOPE
Applies to `src/main/java/com/mo_guang/ctpp/syncdata`.

## READ WHEN
- Changing terminal wire sync or link state persistence.

## SOURCE OF TRUTH
- `syncdata/TerminalLinkStateAccessor.java` and `common/blockentity/VoltageTerminalBlockEntity.java`.

## WORKFLOW
1. Check sync storage wiring in `VoltageTerminalBlockEntity`.
2. Run `:modules:CTPP:build`.
