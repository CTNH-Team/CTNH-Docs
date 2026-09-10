<div align="center">

# CTNH-Docs

**CTNH-Modules 层级知识库——权威的 AGENTS.md 模块主文档与域文档，以 Codex/agent skill 形态分发。**

[English](README.md) | 简体中文

</div>

## 概览

本仓库以单一 skill（`ctnh-docs`）承载 CTNH-Modules 的权威指南，让代理在修改 CTNH 模块代码前能先读取模块约定。

每个 CTNH 模块都是独立的 git submodule，本仓库只承载文档：

- `references/<Module>/` 下的模块主文档（`AGENTS.md`）与域文档
- `references/_architecture/` 下的跨模块架构契约
- 让文档与源码变更保持同步的 LLM 自动同步流水线

指南正文使用简体中文；小节标题、类名、路径与命令保持英文并加反引号。

## 技能

| 技能 | 用途 |
| --- | --- |
| `ctnh-docs` | CTNH-Core、CTNH-Lib、CTNH-Bio、CTNH-Energy、CTNH-Mana、CTNH-Astral、CTPP、Create-Enough-Items 的权威 AGENTS.md 指南，以及 machine/trait/recipe capability/Jade 架构契约。 |

## 仓库结构

```text
.
|-- ctnh-docs/
|   |-- SKILL.md                  # skill 入口：路由 + 约定
|   |-- agents/openai.yaml        # 界面元数据
|   `-- references/              # 模块与域文档
|       |-- _architecture/
|       |-- CTNH-Core/
|       |-- CTNH-Lib/
|       |-- CTNH-Bio/
|       |-- CTNH-Energy/
|       |-- CTNH-Mana/
|       |-- CTNH-Astral/
|       |-- CTPP/
|       `-- Create-Enough-Items/
|-- prompts/                      # init-deep 更新模式提示词（仅 CI 使用）
|-- scripts/                      # 自动同步 / 发布脚本
`-- .github/workflows/            # Auto Sync Docs / Auto Release Docs CI
```

## 使用方式

把 `ctnh-docs/` 目录放入你的 skills 目录，然后在会话中按名称调用技能：

```text
$ctnh-docs
```

`SKILL.md` 是权威路由入口；每个模块/域指南都是它指向的 `references/` 文件。
技能不可用时，用 webfetch 兜底：

```text
https://raw.githubusercontent.com/CTNH-Team/CTNH-Docs/main/ctnh-docs/references/<Module>/AGENTS.md
```

## 自动同步（Auto Sync Docs）

`references/` 指南由 CI 自动更新：把 **init-deep 更新模式**（`prompts/init_deep_update.md`）列入 LLM 提示词，
让模型对比源码与现有文档并更新 AGENTS.md；改动经 PR（`auto-doc-update`）合入。

| 触发 | 说明 |
|------|------|
| `schedule`（每 30 分钟） | 轮询 CTNH-Modules 主仓库与 8 个子模块的新提交（`check_pending.py` 无变化秒退） |
| `workflow_dispatch` | 手动触发；Sync 可带 `force_latest`，Release 可带 `force` |

`scripts/doc_gen.py` 的写入校验限定 `references/<Module>/**AGENTS.md`；`references/_architecture/` 属手工维护，不在自动同步写入范围内。

## 自动发布（Auto Release Docs）

以**日期**为版本号发布 GitHub Release（tag 形如 `2026-08-07`），附件为整个 skill 目录打包的 `ctnh-docs-skill-<日期>.zip`（含 `SKILL.md` + `references/`）。

- 同一天已发布则跳过（手动触发可带 `force` 覆盖）
- 下载：https://github.com/CTNH-Team/CTNH-Docs/releases/latest

## 维护

- 保持 `SKILL.md` 中的 `name` 与 `ctnh-docs/` 目录名一致。
- 在 `references/`（模块文档）或 `_architecture/`（契约）下编辑并推送；自动同步只改写 `references/<Module>/`。
- 根模块 `AGENTS.md`（CTNH-Modules）的 DOMAIN GUIDE ROUTING 表是路由唯一真相来源，文档移动时同步更新。
- 技能列表、目录结构或使用模型变化时，同步更新两个 README。

## 许可证

当前仓库没有仓库级许可证文件。在仓库外分发或复用前，请先检查各指南自身的元数据。
