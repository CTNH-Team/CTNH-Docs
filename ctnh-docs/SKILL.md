---
name: ctnh-docs
description: >-
  CTNH-Modules 层级知识库（AGENTS.md 指南）的权威参考。包含各模块（CTNH-Core、CTNH-Lib、
  CTNH-Bio、CTNH-Energy、CTNH-Mana、CTNH-Astral、CTPP、Create-Enough-Items）的主文档与域文档，
  以及跨模块架构契约。修改 CTNH 模块代码前、改动机器/trait/recipe capability/Jade 前、
  需要了解模块注册入口/配方生成/机器结构/域划分、或排查 CTNH-Modules 结构约定问题时使用本技能。
  文档路径规则：references/<Module>/AGENTS.md（模块主文档），references/<Module>/<domain>/AGENTS.md（域文档）。
  Triggers: CTNH, 模块指南, AGENTS, machine, trait, recipe capability, Jade, GTCEu
---

# ctnh-docs

CTNH-Modules 的层级知识库。每个模块是独立 git submodule；本 skill 提供模块主文档与域文档的权威参考。

## When to use

- 修改 CTNH 模块代码前，先读对应模块指南。
- 改动 machine / trait / recipe capability / Jade 前，先读架构契约。
- 需要了解模块的注册入口、配方生成、机器结构、域划分时。
- 排查与 CTNH-Modules 仓库结构、约定、反模式相关的问题时。

## Module routing

| Scope | Guide |
|-------|-------|
| **架构契约（跨模块，优先）** | `references/_architecture/AGENTS.md` |
| CTNH-Core | `references/CTNH-Core/AGENTS.md` |
| CTNH-Lib | `references/CTNH-Lib/AGENTS.md` |
| CTNH-Bio | `references/CTNH-Bio/AGENTS.md` |
| CTNH-Energy | `references/CTNH-Energy/AGENTS.md` |
| CTNH-Mana | `references/CTNH-Mana/AGENTS.md` |
| CTNH-Astral | `references/CTNH-Astral/AGENTS.md` |
| CTPP | `references/CTPP/AGENTS.md` |
| Create-Enough-Items | `references/Create-Enough-Items/AGENTS.md` |

各模块主文档内含 DOMAIN GUIDE ROUTING 表，路由到 `references/<Module>/<domain>/AGENTS.md`。

## Key conventions (详见各文档)

- GT/GMT 配方经 `*GTAddon.addRecipes()` 注册为运行时动态数据包，`runData` 不产出其 JSON。
- 引用物品/方块/流体必须用静态注册对象，禁止 `ResourceLocation` 字符串解析 + `ForgeRegistries` 查找。
- 机器状态一份一个所有者：机器字段与 trait 字段禁止并存；trait 在构造阶段挂载完毕。
- `@DescSynced` 管同步、`@Persisted` 管存档，同用前确认两者都必要；同一份数据禁止注解与 attach 式持久化并存。
- Jade 服务端数据只写客户端推导不出的信息；`lastRecipe` 已同步，禁止在 Jade 中重复序列化。
