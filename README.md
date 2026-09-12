<div align="center">

# CTNH-Docs

**CTNH-Modules hierarchical knowledge base — the authoritative AGENTS.md module & domain guides, shipped as a Codex/agent skill.**

[简体中文](README.zh_CN.md) | English

</div>

## Overview

This repository hosts the authoritative CTNH-Modules guides as a single skill (`ctnh-docs`), so agents can read module conventions before editing CTNH module code.

Each CTNH module is an independent git submodule. This repo carries only documentation:

- Module main docs (`AGENTS.md`) and per-domain docs under `references/<Module>/`
- Cross-module architecture contract in `references/_architecture/`
- The LLM-based auto-sync pipeline that keeps guides in step with source changes

Guides are written in Simplified Chinese: section headings, class names, paths, and commands stay English inside backticks.

## Skill

| Skill | Purpose |
| --- | --- |
| `ctnh-docs` | Authoritative AGENTS.md guides for CTNH-Core, CTNH-Lib, CTNH-Bio, CTNH-Energy, CTNH-Mana, CTNH-Astral, CTPP and Create-Enough-Items, plus the machine/trait/recipe-capability/Jade architecture contract. |

## Repository Layout

```text
.
|-- ctnh-docs/
|   |-- SKILL.md                  # skill entry: routing + conventions
|   |-- agents/openai.yaml        # interface metadata
|   `-- references/              # module & domain guides
|       |-- _architecture/
|       |-- CTNH-Core/
|       |-- CTNH-Lib/
|       |-- CTNH-Bio/
|       |-- CTNH-Energy/
|       |-- CTNH-Mana/
|       |-- CTNH-Astral/
|       |-- CTPP/
|       `-- Create-Enough-Items/
|-- prompts/                      # init-deep update-mode prompt (CI only)
|-- scripts/                      # auto-sync / release scripts
`-- .github/workflows/            # Auto Sync Docs / Auto Release Docs CI
```

## Usage

Place the `ctnh-docs/` directory under your skills directory, then invoke it by name in a session:

```text
$ctnh-docs
```

`SKILL.md` is the canonical routing source; each module/domain guide is a `references/` file it points to.
When the skill is unavailable, fall back to webfetch:

```text
https://raw.githubusercontent.com/CTNH-Team/CTNH-Docs/main/ctnh-docs/references/<Module>/AGENTS.md
```

## Auto Sync (Auto Sync Docs)

`references/` guides are updated by CI running **`dsh --profile headless`** (DeepSeek Harness one-shot mode). The run composes a main agent that delegates one background subagent per changed module; each subagent follows the **init-deep update mode** (`prompts/init_deep_update.md`) and rewrites the AGENTS.md guides in Simplified Chinese. A deterministic gate (`scripts/verify_docs.py`) then decides whether the round may open a PR (`auto-doc-update`).

| Trigger | Description |
|------|------|
| `schedule` (every 12 h) | Polls CTNH-Modules + 8 submodules for new commits (`check_pending.py` exits fast when nothing changed) |
| `workflow_dispatch` | Manual; Sync accepts `force_latest` and `dry_run`, Release accepts `force` |

Pipeline: `check_pending.py` (fast-exit poll) → `prepare_sync.py` (writes `workspace/sync-plan.json`) → the dsh agent run → `verify_docs.py` (sections, Chinese text, routing links, write-scope guard) → `advance_state.py` (advances `scripts/state.json`) → PR limited to `ctnh-docs/references/**` + `scripts/state.json`. Writes are restricted to `references/<Module>/**`; `references/_architecture/` is hand-maintained and the gate rejects any change to it. Model/version come from repo variables `DSH_MODEL` / `DSH_VERSION`; the key is `DEEPSEEK_API_KEY`.

## Auto Release (Auto Release Docs)

Publishes a GitHub Release for each commit on the sync branch `auto-doc-update`, named `ctnh-docs-skill-<YYYY-MM-DD>-<short-sha>.zip` (tag and asset share that name; content is taken from that same ref; `SKILL.md` + `references/`).

- Polls every 4 h; skips only when that sync-branch commit already has a release (manual `force` overrides) — several releases per day are expected. Falls back to the default branch head when `auto-doc-update` does not exist
- Download: https://github.com/CTNH-Team/CTNH-Docs/releases/latest

## Maintenance

- Keep the `name` in `SKILL.md` aligned with the `ctnh-docs/` directory name.
- Edit guides under `references/` (module docs) or `_architecture/` (contract) and push; auto-sync only rewrites `references/<Module>/`.
- The DOMAIN GUIDE ROUTING table in the root module `AGENTS.md` (CTNH-Modules) is the routing source of truth — keep it in sync when guides move.
- Update both README files when the layout or usage model changes.

## License

No repository-level license file is currently present. Check individual guide metadata before redistributing.
