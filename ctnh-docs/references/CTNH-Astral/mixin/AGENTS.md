# CTNH-ASTRAL MIXIN DOMAIN

## OVERVIEW
Ad Astra oxygen/temperature and Minecraft chunk-generator/packet hooks (4 Java files).

## STRUCTURE
```text
mixin/
|-- adastra/                   # OxygenApilmplMixin, TemperatureApilmplMixin
`-- minecraft/                 # NoiseBasedChunkGeneratorMixin, ServerGamePacketListenerImplMixin
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Ad Astra oxygen | `mixin/adastra/OxygenApilmplMixin.java` |
| Ad Astra temperature | `mixin/adastra/TemperatureApilmplMixin.java` |
| Chunk generation | `mixin/minecraft/NoiseBasedChunkGeneratorMixin.java` |
| Packet handling | `mixin/minecraft/ServerGamePacketListenerImplMixin.java` |
| Mixin config | `src/main/resources/ctnhastral.mixins.json` |

## CONVENTIONS
- Keep mixin JSON and package entries synchronized.
- Ad Astra hooks target oxygen/temperature behavior; they pair with the `common/oxygen/` system.
- Verify upstream API targets before changing.

## ANTI-PATTERNS
- Do not change Ad Astra oxygen/temperature behavior without checking both mixin JSON entries and the upstream API targets.

## SCOPE
Applies to `src/main/java/com/ctnh/ctnhastral/mixin` and `src/main/resources/ctnhastral.mixins.json`.

## READ WHEN
- Patching Ad Astra or Minecraft chunk-generation behavior.

## SOURCE OF TRUTH
- `src/main/resources/ctnhastral.mixins.json` and the mixin classes in `mixin/`.

## WORKFLOW
1. Verify the target member against the loaded Ad Astra/MC version.
2. Run `:modules:CTNH-Astral:build`; validate at runtime.
