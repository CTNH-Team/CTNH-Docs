# CTNH-Docs

CTNH-Modules 的层级知识库（AGENTS.md 指南）独立仓库。

## 用途

CTNH-Modules 主仓库的 `AGENTS.md` 通过 DOMAIN GUIDE ROUTING 路由到本仓库的 `docs/` 文件。各 CTNH 模块的代码位于独立的 git submodule 中，本仓库只承载文档。

## 结构

```text
docs/                         # 层级 AGENTS.md 指南（webfetch 获取）
├── CTNH-Core/            # 模块主文档 + 9 域
├── CTNH-Lib/             # 模块主文档 + 11 域
├── CTNH-Bio/             # 模块主文档 + 10 域
├── CTNH-Energy/          # 模块主文档 + 10 域
├── CTNH-Mana/            # 模块主文档 + 10 域
├── CTNH-Astral/          # 模块主文档 + 7 域
├── CTPP/                 # 模块主文档 + 12 域
└── Create-Enough-Items/  # 模块主文档 + 7 域
prompts/                      # init-deep 更新模式提示词
scripts/                      # 自动同步脚本
.github/workflows/            # Auto Sync Docs CI
```

## 获取方式

CTNH-Modules 的代理（agent）优先使用 **`ctnh-docs` skill**（从本仓库 latest release 下载），skill 不可用时 webfetch 兜底：
`https://raw.githubusercontent.com/CTNH-Team/CTNH-Docs/<branch>/docs/<Module>/AGENTS.md`

## Skill Release（Auto Release Docs）

`docs/` 指南按 **skill 格式**打包发布：`auto_release_docs.yml` 每 6 小时（及手动触发）构建 `ctnh-docs-skill-<日期>.zip`（含 `SKILL.md` + `docs/` + `prompts/`），以**日期**为版本号发布到 GitHub Release（tag 形如 `2026-08-07`）。

- 同一天已发布则跳过（手动触发可带 `force` 覆盖）
- 下载：`https://github.com/CTNH-Team/CTNH-Docs/releases/latest`
- zip 解压后得到 `ctnh-docs/` 目录（SKILL.md 入口），放入 skills 目录即作为 `ctnh-docs` skill 使用

## 自动同步（Auto Sync Docs）

`docs/` 指南由 CI 自动更新，核心是把 **init-deep 更新模式**（`prompts/init_deep_update.md`）列入 LLM 提示词，让模型按该模式自动对比源码与现有文档并更新 AGENTS.md。

### 触发方式

| 触发 | 说明 |
|------|------|
| `repository_dispatch` | 主模块 CTNH-Modules push 到 `master` 时由 `notify_docs.yml` 触发（推荐） |
| `schedule` | 每 6 小时兜底轮询（cron `0 */6 * * *` UTC） |
| `workflow_dispatch` | 手动触发，可带 `force_latest` |

### 工作流

1. checkout 本仓库 + `CTNH-Team/CTNH-Modules`（含全部子模块，供 LLM 扫描源码结构）
2. `scripts/monitor.py` 轮询主仓库与 8 个子模块（CTNH-Core/Lib/Bio/Energy/Mana/Astral/CTPP/CEI）分支最新提交，与 `scripts/state.json` 中记录的 `last_sha` 对比
3. 对每个有新提交的模块，`scripts/doc_gen.py` 将 init-deep 更新模式提示词 + 现有文档 + 源码结构 + 提交 diff 发给 LLM
4. LLM 返回 `{path, action, content}` 更新清单，脚本写入 `docs/<Module>/`
5. 有新改动时自动创建 PR（`peter-evans/create-pull-request`）

### 所需 Secrets

| Secret | 必填 | 说明 |
|--------|------|------|
| `LLM_API_KEY` 或 `OPENAI_API_KEY` 或 `GEMINI_API_KEY` | 是 | LLM 凭据（OpenAI 兼容或 Gemini 均可） |
| `BASE_URL` | 否 | LLM API 基址，默认 `https://generativelanguage.googleapis.com` |
| `MODEL_NAME` | 否 | 默认 `gemini-2.0-flash` |
| `GITHUB_TOKEN` | 自动 | PR 创建与子模块 checkout（公开仓库够用） |

### 手动触发

```bash
gh workflow run auto_sync_docs.yml -f force_latest=true
```

## 维护

- 修改文档后在此仓库提交并推送（分支与 CTNH-Modules 保持一致，默认 `main`）。
- 根仓库 `AGENTS.md` 的 DOMAIN GUIDE ROUTING 表格是路由的唯一真相来源，新增/移动文档时同步更新它。
- 主仓库 `AGENTS.md` 的变更由人工维护，自动同步只更新 `docs/<Module>/` 下的模块/域文档。
