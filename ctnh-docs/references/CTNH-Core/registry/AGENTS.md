# CTNH-CORE REGISTRY DOMAIN

## OVERVIEW
Core 的 Registrate 注册面（50 个根 + 子包类）：物品、方块、方块实体、创造栏、tags、模型、配方类型/修饰符/条件、GTCEu 机器与多方块、材料、矿石、流体矿脉、世界生成层与音效。精准装配线改写落在 `GTMachineModify`。

## STRUCTURE
```
registry/
|-- CTNHRegistrate.java        # registrate 根（extends CNRegistrate）
|-- CTNHRegistration.java      # 注册入口（abstract，提供 REGISTRATE 单例）
|-- CTNHItems.java / CTNHBlocks.java / CTNHBlockEntities.java
|-- CTNHCreativeModeTabs.java / CTNHTags.java / CTNHModels.java / CTNHModelLayers.java / CTNHRenders.java
|-- CTNHRecipeTypes.java / CTNHRecipeModifiers.java / CTNHRecipeConditions.java / CTNHRecipeCategories.java / CTNHRecipes.java
|-- CTNHChanceLogic.java / CTNHGuiTextures.java
|-- CTNHDamageTypes.java / CTNHDimensionMarkers.java / CTNHWorlds.java
|-- CTNHElements.java / CTNHMaterialFlags.java (注册层)
|-- CTNHFluidVeins.java / CTNHOres.java / CTNHTagPrefixes.java / CTNHWorldgenLayers.java
|-- CTNHTemperatureModifierRegister.java
|-- adventure/                 # CTNHEnchantments
|-- jade/                      # CTNHJadePlugin（Jade 注册已整体注释停用，见 api 域文档）
|-- machines/                  # CTNHMachines, GTMachineModify（LARGE_ASSEMBLER -> MultiblockComputationMachine + PRECISION_ASSEMBLY_RECIPES）
|   `-- multiblock/            # GTNNMultiblocks, HyperPlasmaTurbineRegister, Mechanical, MultiblocksA/B/C, WindPowerArrayRegister；配方驱动多方块基类为 RecipeElectricMultiblockMachine 或其子类
|-- material/                  # CTNHMaterialBlocks, CTNHMaterialFlags, CTNHMaterials, GTMaterialAddon
|-- ores/                      # AdAstraOres, AetherOres, AlfheimOres, EndOres, NetherOres, OverworldOres, TwilightForestOres
`-- sound/                     # CTNHSoundEvents（easter_egg_clown）
```

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| Registrate/根 | `registry/CTNHRegistrate.java`, `registry/CTNHRegistration.java` |
| 物品/方块/方块实体 | `registry/CTNHItems.java`, `registry/CTNHBlocks.java`, `registry/CTNHBlockEntities.java` |
| 创造栏/tags/模型 | `registry/CTNHCreativeModeTabs.java`, `registry/CTNHTags.java`, `registry/CTNHModels.java`, `registry/CTNHModelLayers.java` |
| GTCEu 机器 | `registry/machines/CTNHMachines.java`；多方块在 `registry/machines/multiblock/` 与 `registry/CTNHMultiblockMachines.java` |
| 精准装配线 | `registry/machines/GTMachineModify.java#modifyGTAssembly()` —— `GCYMMachines.LARGE_ASSEMBLER` 的 supplier 改为 `MultiblockComputationMachine::new`，并把 `CTNHRecipeTypes.PRECISION_ASSEMBLY_RECIPES` 追加进 recipeTypes |
| 配方驱动多方块基类 | `registry/machines/multiblock/*.java` 的 `REGISTRATE.multiblock(name, factory)`：factory 为 `RecipeElectricMultiblockMachine` 或其子类（如 `FactoryMachine`, `BioMachine` 等自定义机器直接注册；无自定义行为时用 `RecipeElectricMultiblockMachine::new`）；线圈机 `CoilWorkableElectricMultiblockMachine::new`；类型判断在 `registry/CTNHRecipeModifiers.java#ebfOverclock()` |
| 材料/世界生成 | `registry/material/CTNHMaterials.java`, `registry/material/GTMaterialAddon.java`, `registry/CTNHTagPrefixes.java`, `registry/CTNHOres.java`, `registry/CTNHFluidVeins.java`, `registry/CTNHWorldgenLayers.java` |
| 配方类型/修饰符/条件 | `registry/CTNHRecipeTypes.java`, `registry/CTNHRecipeModifiers.java`, `registry/CTNHRecipeConditions.java`, `registry/CTNHRecipeCategories.java` |
| 附魔 | `registry/adventure/CTNHEnchantments.java` |
| Jade（停用） | `registry/jade/CTNHJadePlugin.java` —— `init()` 全体注释，当前不注册任何 provider |
| 音效 | `registry/sound/CTNHSoundEvents.java` |

## CONVENTIONS
- 注册类统一 `CTNH` 前缀。
- **中文名在注册处声明**（5186b6ec 起，本域最重要的写法）：
  - 纯方块在 `CTNHBlocks` 注册时传入 `cnName`：`createCoilBlock(ICoilType, cnName)`、`createFireboxCasing(BoilerFireboxType, cnName)`、`createTurbineRotorBlock(name, R, G, B, A, cnName)`、`createRotateCasing(name, map, cnName)`（旧二参重载保留、传 `null` 不声明），内部统一 `.cnlang(cnName)`。
  - 普通多方块在 registrate 链上直接 `.cnLangValue("中文名")`（如 `GTNNMultiblocks.CHEMICAL_PLANT` = `"埃克森美孚化工厂"`、`MultiblocksA` 的 `"地暖"`/`"屠宰场"`/`"焦化塔"`、`Mechanical` 的五个机械厂）。
  - 工厂方法同样要求 `cnName` 形参：`WindPowerArrayRegister.register(name, tier, casing, frame, renderCasing, cnName)`、`MultiblocksA.registerPhotovoltaicPowerStation(tier, basicRate, photovoltaicBlock, cnName)`、`utils/CTNHMachineUtils.registerLargeCombustionEngine(..., cnName)`。
  - 分级机器走 `utils/CTNHMachineUtils.registerTieredMachines(name, cnname, factory, builder, tiers...)`，内部 `.cnLangValue(VNF[tier] + cnname)`。
  - `CTNHMachines` 中 50 个分级机器/仓室仍用 `@Key("block.ctnhcore.*")` + `@CN` + `Lang` 字段（逐级中文名无公式，留待单独处理）；不要以它们为模板新增内容。
  - lang 键名与玩家可见文案保持不变；方块的 `cnlang`/`cnLangValue` 只影响生成的中文 lang 条目。
- 大型多方块注册文件使用 `spotless:off/on`；保留该局部格式化边界。
- `CTNHCoreGTAddon.initializeAddon()` 初始化物品、方块、方块实体与方块映射；后续 hook 注册 tag prefix、元素、矿石/流体矿脉、世界生成层、配方与配方删除。
- `CTNHRegistrate` 与 `CTNHRegistration` 并存：`CTNHRegistration` 是装配 registrate 的入口（`REGISTRATE` 单例），不是重复实现。
- 音效经 `CommonProxy.init()` 中的 `CTNHSoundEvents.SOUND_EVENTS` 注册；对应 `sounds.json` 与音频资源在 `src/main/resources/assets/ctnhcore/`。
- 引用物品/方块/流体**必须**使用静态注册对象（`GTMaterials.Iron`, `CTNHBlocks.*`, `TagPrefix.ingot`, `AEItems.X` 等），**禁止** `ResourceLocation` 字符串解析 + `ForgeRegistries.ITEMS/BLOCKS/FLUIDS.getValue(...)`；字符串 ID 仅限无注册对象的场景（上游 mod 专属 ID、配方 ID、tag key、维度 ID）。
- GT/GMT 配方属运行时动态数据包（`*GTAddon.addRecipes()` → `GTDynamicPackContents` / CTNH-Lib `CTNHDynamicDataPack`），`runData` 对其不产出 JSON。
- **材料分解标志**（6eb50b5d 起）：`registry/material/CTNHMaterials.java` 的 `siliconFluoride`、`RutheniumAmalgam`、`OsmiumIronSpinel`、`PalladiumSulfide`、`Wolframite`、`Tarkianite`、`Rheniite`，以及 `data/materials/SecondMaterials.java` 的 `Wollastonite`，本次新增声明 `MaterialFlags.DISABLE_DECOMPOSITION`（`Kaolinite`/`Dolomite`/`zirconiumTetrachloride` 等此前已有）。该标志禁止 GTCEu 为该材料生成电解/离心分解配方（`DecompositionRecipeHandler.processDecomposition()` 直接返回）；新增需要阻止分解的材料时照此声明。
- **配方驱动多方块基类**（ece38be 起）：需要配方类型/机器模式页签的电力多方块，注册 factory 的类必须是 `RecipeElectricMultiblockMachine` 或其子类（无自定义行为时直接用 `RecipeElectricMultiblockMachine::new`，否则用 `FactoryMachine::new`、`BioMachine::new` 等自定义子类），并照常在链上 `.recipeTypes(...)`。`RecipeElectricMultiblockMachine extends RecipeMultiblockMachine`，后者 `implements IRecipeLogicMachine`。`WorkableElectricMultiblockMachine` 只 `extends WorkableMultiblockMachine`、**不**实现 `IRecipeLogicMachine`，用它注册会导致模式页签不显示、已注册配方类型不生效（`IFancyUIMachine.attachSideTabs()` 仅在 `instanceof IRecipeLogicMachine && getRecipeTypes().length > 1` 时挂 `MachineModeFancyConfigurator`）。线圈多方块用其子类 `CoilWorkableElectricMultiblockMachine::new`（`extends RecipeElectricMultiblockMachine`）。
  - ece38be 迁移的 13 处：`MultiblocksA` 的 `PLASMA_CONDENSER`、`SINTERING_KILN`、`CHEMICAL_VAPOR_DEPOSITION_MACHINE`、`DIMENSIONAL_GAS_COLLECTION_CHAMBER`、`LARGE_STEEL_FURNACE`、`LARGE_STEEL_ALLOY_FURNACE`、`DECAY_POOLS`、`SUPER_CENTRIFUGE`；`MultiblocksB` 的 `SILICA_ROCK_FUEL_REFINERY`、`CultivationRoom`、`COMBINED_VAPOR_DEPOSITION_FACILITY`、`GAS_CENTRIFUGE`；`GTNNMultiblocks` 的 `LARGE_DEHYDRATOR`。
- `CTNHRecipeModifiers.ebfOverclock()` 的类型判断对象为 `RecipeElectricMultiblockMachine`（原指向 `WorkableElectricMultiblockMachine`）；线圈机器匹配失败时经 `RecipeModifier.nullWrongType(CoilWorkableElectricMultiblockMachine.class, machine)` 报类型错误。
- 精准装配线：`GTMachineModify` 在 `modifyGTAssembly()` 改写原版 `GCYMMachines.LARGE_ASSEMBLER` 定义 —— supplier 替换必须在机器注册之后、tooltip 构建之前。

## ANTI-PATTERNS
- 手工重排受 spotless 开关保护的大型多方块注册段。
- 从 registry 与 `CommonProxy` 两条路径注册同一条目。
- 在别处重复 `GTMachineModify` 的 supplier 改写；保持单点变更。
- 给已支持注册处声明中文名的方块/多方块再补 `@Key("block.ctnhcore.*")` + `Lang` 字段伪造翻译（5186b6ec 已清除 87 处）。
- 方块/机器再无注册后留下悬空 lang 条目（`mechanical_extractor` 即此类残留，已随该提交移除）。
- 用 `WorkableElectricMultiblockMachine::new` 注册需要配方类型的多方块（不实现 `IRecipeLogicMachine`，模式页签不显示、配方类型不生效）；应改用 `RecipeElectricMultiblockMachine` 或其子类。

## SCOPE
`modules/CTNH-Core/src/main/java/io/github/cpearl0/ctnhcore/registry/` 及其全部子包。

## READ WHEN
- 在 Core 中新增或修改物品、方块、机器、配方类型、材料、音效或世界生成注册
- 需要给方块/多方块/分级机器补中文名或改翻译声明方式

## SOURCE OF TRUTH
- `registry/CTNHRegistrate.java`, `registry/CTNHRegistration.java` 与 `CTNHCoreGTAddon.java` 的 hook 顺序。
- 生成数据：`data/` 下的 provider 与 `src/generated/resources`。
- 音效：`registry/sound/CTNHSoundEvents.java` 与 `src/main/resources/assets/ctnhcore/sounds.json`。

## WORKFLOW
1. 定位条目所属注册类组（items、machines、materials、recipe types、sound events ...）；多方块 factory 用 `RecipeElectricMultiblockMachine` 或其子类（线圈 `CoilWorkableElectricMultiblockMachine::new`），不要用 `WorkableElectricMultiblockMachine::new`。
2. 确认中文名声明位置：纯方块 → `CTNHBlocks` 注册参数；多方块 → chain 上的 `.cnLangValue`；分级机器 → `cnname` 形参。
3. 检查 GT addon hook 顺序与 datagen 引用。
4. 涉及数据时跑 `:modules:CTNH-Core:runData`，再跑 `spotlessCheck`。
