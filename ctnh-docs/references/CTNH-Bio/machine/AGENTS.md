# CTNH-BIO MACHINE DOMAIN

## OVERVIEW
Living-machine implementations (7 Java files): Brain in a Vat, Hostile Observer, Great Flesh, Cogni assembler, and multiblock parts.

## STRUCTURE
```text
machine/
|-- braininavat/              # Brain, BrainInAVatMachine
|-- bioobservation/           # HostileObserverMachine
|-- greatflesh/               # GreatFleshMachine
`-- multiblock/               # CogniAssemblerMachine
    `-- part/                 # NeuralModelAccessorMachine, ParabioticBridgePartMachine
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Brain in a Vat | `machine/braininavat/` (Brain, BrainInAVatMachine) |
| Bio observation | `machine/bioobservation/HostileObserverMachine.java` |
| Great flesh | `machine/greatflesh/GreatFleshMachine.java` |
| Cogni assembler | `machine/multiblock/CogniAssemblerMachine.java` |
| Multiblock parts | `machine/multiblock/part/` (NeuralModelAccessorMachine, ParabioticBridgePartMachine) |

## CONVENTIONS
- Machine implementations reference `api/machine/` contracts (BasicLivingMachine, WorkableLivingMultiblockMachine); registrate entries live in `registry/CBMachines.java` / `registry/CBMultiblocks.java`.
- Multiblock parts implement `CBPartAbility` from `api/machine/multiblock/`.
- These are Bio-specific living machines; Core must not absorb them.

## ANTI-PATTERNS
- Do not move machine logic into recipe or registry classes.

## SCOPE
Applies to `src/main/java/com/moguang/ctnhbio/machine` and its child packages.

## READ WHEN
- Implementing or changing Bio living machines.

## SOURCE OF TRUTH
- `machine/` implementations and `api/machine/` contracts.

## WORKFLOW
1. Check the machine's registry entry and API contract.
2. Run `:modules:CTNH-Bio:build`; validate the runtime surface if available.
