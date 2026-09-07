# CTNH-CORE API DOMAIN

## OVERVIEW
Public API surfaces for Core (18 Java files): the multiblock builder, machine feature hooks, GUI/Jade/recipe integration points, and material data helpers. Code outside Core uses these surfaces to build machines and recipes without reaching into implementation classes.

## STRUCTURE
```text
api/
|-- CTNHMultiblockBuilder.java
|-- Pattern/                   # AsynBlockPattern, CTNHBlockMaps, CTNHBoilerFireboxType, CTNHPredicates (AsynBlockPattern extract/search now guards null/empty foundItemStack)
|-- data/material/             # CTNHMaterialIconSet, CTNHMaterialIconType, CTNHPropertyKeys, CatalystProperty
|-- gui/                       # CTNHGuiTextures
|-- jade/                      # MultithreadRecipeLogicProvider, MultithreadRecipeOutputProvider, ThreadStatusProvider
|-- machine/feature/           # ICoilMachine, IDigitalMiner, IDynamicCasing
|-- machine/multiblock/        # UnlimitedItemStackTransfer
`-- recipe/                    # DigitalMinerLogic
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Multiblock builder | `api/CTNHMultiblockBuilder.java`, `api/machine/multiblock/` |
| Machine features | `api/machine/feature/` (`ICoilMachine`, `IDigitalMiner`, `IDynamicCasing`) |
| Pattern helpers | `api/Pattern/` (`AsynBlockPattern`, `CTNHBlockMaps`, `CTNHPredicates`) |
| AE pattern NPE fix | `api/Pattern/AsynBlockPattern.java` (`extractInventory` and `searchAEStorage` now `foundItemStack != null && !isEmpty()` before `AEItemKey.of`) |
| Material data | `api/data/material/` (icon sets/types, property keys, catalyst property) |
| GUI textures | `api/gui/CTNHGuiTextures.java` |
| Jade providers | `api/jade/` (multithread recipe/output/thread status) |
| Recipe APIs | `api/recipe/` (`DigitalMinerLogic`) |

## CONVENTIONS
- API classes must not leak client-only classes into common construction paths.
- Prefer interface surfaces (`ICoilMachine`, `IDigitalMiner`, `IDynamicCasing`) over concrete implementations when exposing machines to other modules.
- Jade provider interfaces in `api/jade/` back the registry-level `CTNHJadePlugin`.

## JADE PROVIDERS
`api/jade/` 的 `MultithreadRecipeLogicProvider`、`MultithreadRecipeOutputProvider`、`ThreadStatusProvider` 是 GTCEu `RecipeLogicProvider` / `RecipeOutputProvider` 的多线程变体，经 CTNH-Lib `JadePriorityManager` 注册（现状优先级表见 `docs/CTNH-Lib/jade/AGENTS.md`）。

- 统一单入口机器 provider 是迁移目标（`docs/_architecture/AGENTS.md` §8/§9）；这三个 provider 属该迁移的下游，改动前先读架构契约。
- Jade 服务端数据只写客户端推导不出的信息：`lastRecipe` 已由 `@DescSynced` 同步，禁止在 Jade 中重复序列化；能耗、并行、线程状态能推导则不写 NBT。

## ANTI-PATTERNS
- Do not add gameplay logic to API classes; keep implementation in `common/` or `registry/`.
- Do not reference module-specific classes from shared API surfaces.

## SCOPE
Applies to `src/main/java/io/github/cpearl0/ctnhcore/api` and its child packages.

## READ WHEN
- Exposing a new machine, feature, or recipe surface to other CTNH modules.
- Changing the multiblock builder or machine feature hooks.

## SOURCE OF TRUTH
- `api/CTNHMultiblockBuilder.java` and `api/machine/feature/` contracts.
- Registry wiring in `registry/` and `common/CommonProxy.java`.

## WORKFLOW
1. Confirm the surface is genuinely shared before adding it to `api/`.
2. Check consumers in Core and feature modules for affected call sites.
3. Run `:modules:CTNH-Core:build` and the narrowest consumer task.
