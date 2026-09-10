# CTNH-MANA REGISTRY DOMAIN

## OVERVIEW
Mana 的 registrate 注册面（27 个 Java 文件：19 个根类 + 8 个子包类）：物品、方块、方块实体、实体、机器、多方块定义、材料、元素、tag prefix、配方类型与条件、效果、音效、粒子与 GUI 贴图。

## STRUCTURE
```text
registry/
├── 19 root classes: CMRegistrate, CMBlockEntities, CMBlocks, CMCreativeModeTabs, CMElements, CMEntities,
│                    CMGuiTextures, CMItems, CMMachines, CMMaterials, CMMobEffects, CMModelLayers,
│                    CMMultiblockMachines, CMParticleTypes, CMRecipeConditions, CMRecipeTypes,
│                    CMTagPrefixes, CMTags, GTMaterialAddon
├── items/                    # CMFuelItems
├── multiblock/               # 5 分组: BloodMagic, Botania, ManaMachine, Misc, ZenithMachine
└── sounds/                   # CMSoundDefinitionsProvider, CMSoundEvent
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Registrate 根 | `registry/CMRegistrate.java`（`CTNHMana.REGISTRATE = CMRegistrate.create()`，由 `CommonProxy.init()` 调 `registerRegistrate()`） |
| 物品 | `registry/CMItems.java`, `registry/items/CMFuelItems.java` |
| 方块 / BE / 实体 | `registry/CMBlocks.java`, `registry/CMBlockEntities.java`, `registry/CMEntities.java` |
| 机器与多方块 | `registry/CMMachines.java`, `registry/CMMultiblockMachines.java`，分组定义在 `registry/multiblock/`（BloodMagic 1277 行、Botania 2035 行、ManaMachine 539 行、Misc 3025 行、ZenithMachine 425 行） |
| 材料 / 元素 / tag prefix | `registry/CMMaterials.java`, `registry/CMElements.java`, `registry/CMTagPrefixes.java`, `registry/GTMaterialAddon.java` |
| 配方类型 / 条件 | `registry/CMRecipeTypes.java`（28 个 `GTRecipeType`）, `registry/CMRecipeConditions.java` |
| 效果 / 音效 / 粒子 / 贴图 / 模型层 | `registry/CMMobEffects.java`, `registry/sounds/{CMSoundEvent, CMSoundDefinitionsProvider}`, `registry/CMParticleTypes.java`, `registry/CMGuiTextures.java`, `registry/CMModelLayers.java` |
| 创造栏 / tag | `registry/CMCreativeModeTabs.java`, `registry/CMTags.java` |

## CONVENTIONS
- 注册类统一 `CM` 前缀（材料添加器为 `GTMaterialAddon`）。
- 注册入口按归属分发，不要跨类重复注册：
  - `CTNHManaGTAddon.initializeAddon()` → `CMItems.init()`, `CMBlocks.init()`, `CMBlockEntities.init()`；`registerTagPrefixes()` → `CMTagPrefixes.init()`；`registerElements()` → `CMElements.init()`。
  - `CommonProxy.init()` → `CMParticleTypes`, `CMMobEffects`, `CMSoundEvent` 的 DeferredRegister 注册，`CMEntities.init()`, `CMCreativeModeTabs.init()`, `CTNHMana.REGISTRATE.registerRegistrate()`, `CMDatagen.init()`, `CMConfig.init()`。
  - `CommonProxy` 的 GTCEu 泛型监听 → `CMMachines.init()` + `CMMultiblockMachines.init()`（`MachineDefinition`）、`CMRecipeTypes.init()`（`GTRecipeType`）、`CMRecipeConditions.init()`（`RecipeConditionType`）。
  - 材质：`registerMaterial` 建 `ctnhmana` 材质注册表，`registerMaterials`/`addMaterialFlag` → `CMMaterials.init()` / `GTMaterialAddon.init()`。
- 配方移除经 `CTNHManaGTAddon.removeRecipes(...)` → `data/recipe/ManaRecipeRemoval`，不在注册类里写删除逻辑。
- 多方块图案、中文名、tooltip 与配方类型接线写在 `registry/multiblock/<分组>`，实现留在 `common/multiblock/`。
- 新增 tag 常量放 `registry/CMTags`，tag 数据生成在 `data/tags/`。

## ANTI-PATTERNS
- 同一注册项同时从 `registry/` 与 `CommonProxy` / `CTNHManaGTAddon` 两条路径注册。
- 在 `registry/` 里写机器行为或配方逻辑（应在 `common/` 与 `data/`）。
- 绕过 `CMRegistrate` 自行 new 注册表，或跳过 CTNH-Lib 的 registrate 基类。
- 在 `registry/multiblock/` 之外定义多方块图案与名称。

## SCOPE
适用于 `src/main/java/com/magicbee/ctnhmana/registry` 及其子包。

## READ WHEN
- 新增或修改 Mana 物品、方块、BE、实体、机器、多方块、材料、元素、tag prefix、配方类型/条件、效果、音效或粒子。
- 调整注册入口的调用顺序。

## SOURCE OF TRUTH
- `registry/CMRegistrate.java` 与各 `CM*` 注册类的定义。
- 调用顺序以 `CTNHManaGTAddon.java`、`common/CommonProxy.java` 为准。

## WORKFLOW
1. 确定条目属于哪个注册类分组。
2. 按归属在 GT addon 钩子或 `CommonProxy` 生命周期中接线，不重复注册。
3. 涉及数据时跑 `:modules:CTNH-Mana:runData`，否则跑 `:modules:CTNH-Mana:build`。