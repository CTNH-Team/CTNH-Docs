# CTNH-Docs

CTNH-Modules 的层级知识库（AGENTS.md 指南）独立仓库。

## 用途

CTNH-Modules 主仓库的 `AGENTS.md` 通过 DOMAIN GUIDE ROUTING 路由到本仓库的 `docs/` 文件。各 CTNH 模块的代码位于独立的 git submodule 中，本仓库只承载文档。

## 结构

```text
docs/
├── CTNH-Core/            # 模块主文档 + 9 域
├── CTNH-Lib/             # 模块主文档 + 11 域
├── CTNH-Bio/             # 模块主文档 + 10 域
├── CTNH-Energy/          # 模块主文档 + 10 域
├── CTNH-Mana/            # 模块主文档 + 10 域
├── CTNH-Astral/          # 模块主文档 + 7 域
├── CTPP/                 # 模块主文档 + 12 域
└── Create-Enough-Items/  # 模块主文档 + 7 域
```

## 获取方式

CTNH-Modules 的代理（agent）不直接读取本仓库文件，通过 webfetch 获取：
`https://raw.githubusercontent.com/CTNH-Team/CTNH-Docs/<branch>/docs/<Module>/AGENTS.md`

## 维护

- 修改文档后在此仓库提交并推送（分支与 CTNH-Modules 保持一致，默认 `main`）。
- 根仓库 `AGENTS.md` 的 DOMAIN GUIDE ROUTING 表格是路由的唯一真相来源，新增/移动文档时同步更新它。
