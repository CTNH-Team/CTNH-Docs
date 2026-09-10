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

`references/` guides are updated by CI. The **init-deep update mode** (`prompts/init_deep_update.md`) is fed to an LLM so it compares source changes against existing docs and updates the AGENTS.md guides; changes land via PR (`auto-doc-update`).

| Trigger | Description |
|------|------|
| `schedule` (every 30 min) | Polls CTNH-Modules + 8 submodules for new commits (`check_pending.py` exits fast when nothing changed) |
| `workflow_dispatch` | Manual; Sync accepts `force_latest`, Release accepts `force` |

`scripts/doc_gen.py` write-validation is limited to `references/<Module>/**AGENTS.md`; `references/_architecture/` is hand-maintained and outside auto-sync writes.

## Auto Release (Auto Release Docs)

Publishes a dated GitHub Release (tag like `2026-08-07`) containing the whole skill directory as `ctnh-docs-skill-<date>.zip` (`SKILL.md` + `references/`).

- Skips if already released the same day (manual `force` overrides)
- Download: https://github.com/CTNH-Team/CTNH-Docs/releases/latest

## Maintenance

- Keep the `name` in `SKILL.md` aligned with the `ctnh-docs/` directory name.
- Edit guides under `references/` (module docs) or `_architecture/` (contract) and push; auto-sync only rewrites `references/<Module>/`.
- The DOMAIN GUIDE ROUTING table in the root module `AGENTS.md` (CTNH-Modules) is the routing source of truth — keep it in sync when guides move.
- Update both README files when the layout or usage model changes.

## License

No repository-level license file is currently present. Check individual guide metadata before redistributing.
