# CTNH-MANA UTILS DOMAIN

## OVERVIEW
Mana 的共享工具类（3 个 Java 文件）：GT 配方并行与输入缩放helper、血魔法流体成分快捷构造、运行环境判断与跨 mod `ResourceLocation` 构造。

## WHERE TO LOOK
| Concern | Location |
|---------|----------|
| 配方与并行工具 | `utils/CTNHManaUtils.java` |
| 运行环境 | `utils/EnvUtils.java`（`public static final boolean isDataGen = FMLLoader.getLaunchHandler().isData()`） |
| 跨 mod ID | `utils/ModUtils.java`（`BotaniaRL(String)` → `ResourceLocationHelper.prefix`；`BloodMagicRL(String)` → `BloodMagic.rl`） |

## CONVENTIONS
- `CTNHManaUtils` 的能力面（按用途分组，新增前先确认没有同类方法）：
  - 流体成分：`lifeEssence(int)`（Blood Magic 生命精华）、`doubt(int)`（疑虑）。
  - 并行：`getParallelAmount(...)`、`getParallelAmountWithFakeOutputCapacity(...)`、`getMaxParallelByInput(...)`；默认忽略 `notConsumable`（chance==0）输入，需要时用 `includeNonConsumables` 打开。
  - 配方缩放：`applyParallel`（加电压不加时间）、`applyParallelWithoutEU`（加时间不加电压）、`multiplyInputs` / `multiplyTickInputs` / `multiplyAllContents`。
  - 输出插入：`insertItemToOutput(NotifiableItemStackHandler, ItemStack, boolean)`（先塞同类堆叠再填空槽，非可堆叠物品只找空槽）。
  - tooltip：`itemTooltipsAdd(Lang[], List<Component>)`、`addMachineTooltips(Lang[])`。
- `multiplyContentMap` 统一走 `ContentListMap.forEachEntry`（不遍历 `asMap().entrySet()`），与 `references/_architecture/AGENTS.md` §7 一致。
- 工具类保持无注册副作用；`EnvUtils` 只暴露数据生成环境判定，不要在业务类里重复判断。
- 跨 mod 的 `ResourceLocation` 一律经 `ModUtils`，不要在调用处硬写 `modid:path` 字符串。
- 文案仍走 CTNH-Lib `Lang`（`utils` 只提供拼接 helper，不产生裸字符串）。

## ANTI-PATTERNS
- 复制 CTNH-Lib `utils/` 或 CTNH-Core 已有的并行/配方 helper，而不是复用。
- 在业务类里另写一份并行计算或输入缩放逻辑，绕过 `CTNHManaUtils`。
- 在工具类里持有注册对象或执行注册。
- 用字符串拼接代替 `ModUtils.BotaniaRL` / `BloodMagicRL`。

## SCOPE
适用于 `src/main/java/com/magicbee/ctnhmana/utils`。

## READ WHEN
- 需要并行、配方输入缩放或输出插入逻辑。
- 需要判断数据生成环境。
- 需要构造 Botania / Blood Magic 的 `ResourceLocation`。

## SOURCE OF TRUTH
- `utils/` 下的三个类；并行语义以 GTCEu `ParallelLogic` 与 `RecipeHandlerGroup` 为准。

## WORKFLOW
1. 先查 CTNH-Lib `utils/` 与 `CTNHManaUtils` 是否已有同能力 helper。
2. 新增方法时保持静态、无状态、无注册依赖。
3. 跑 `:modules:CTNH-Mana:build`。
