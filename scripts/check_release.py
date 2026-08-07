import json
import os
import re
import shutil
import sys
import zipfile
from datetime import datetime, timezone
from typing import Dict, List, Optional
from urllib.request import Request, urlopen


def _http_get_json(url: str, token: str = "") -> any:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "CTNH-Docs-release-bot",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = Request(url, headers=headers)
    with urlopen(req, timeout=30) as resp:
        raw = resp.read().decode("utf-8", errors="replace")
        return json.loads(raw)


def _write_github_output(kv: Dict[str, str]) -> None:
    out_path = os.getenv("GITHUB_OUTPUT")
    if not out_path:
        for k, v in kv.items():
            print(f"{k}={v}")
        return
    with open(out_path, "a", encoding="utf-8") as f:
        for k, v in kv.items():
            if "\n" in v:
                # 多行值必须用 heredoc 语法，否则 GitHub 无法解析后续行
                f.write(f"{k}<<CTNH_DOCS_EOF\n{v}\nCTNH_DOCS_EOF\n")
            else:
                f.write(f"{k}={v}\n")


def _today_utc() -> str:
    """版本号使用日期：YYYY-MM-DD（UTC）。"""
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def _latest_release_tag(repo: str, token: str) -> Optional[str]:
    """获取当前最新 release 的 tag（日期格式）。"""
    try:
        releases = _http_get_json(
            f"https://api.github.com/repos/{repo}/releases?per_page=50", token=token
        )
    except Exception as e:
        print(f"获取 releases 失败: {e}")
        return None
    date_re = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    tags = [r.get("tag_name", "") for r in (releases or []) if date_re.match(r.get("tag_name", ""))]
    return max(tags) if tags else None


def _build_skill_package(docs_root: str = "docs", prompts_root: str = "prompts",
                         staging: str = "skill/ctnh-docs") -> None:
    """构建 skill 包目录：SKILL.md + docs/ + prompts/。"""
    today = _today_utc()
    if os.path.exists(staging):
        shutil.rmtree(staging)
    os.makedirs(staging, exist_ok=True)

    # 复制 docs/ -> skill/ctnh-docs/docs/
    if os.path.isdir(docs_root):
        shutil.copytree(docs_root, os.path.join(staging, "docs"))
    # 复制 prompts/ -> skill/ctnh-docs/prompts/
    if os.path.isdir(prompts_root):
        shutil.copytree(prompts_root, os.path.join(staging, "prompts"))

    # 生成 SKILL.md
    skill_md = f"""---
name: ctnh-docs
description: |
  CTNH-Modules 层级知识库（AGENTS.md 指南）的权威参考。包含各模块（CTNH-Core、CTNH-Lib、
  CTNH-Bio、CTNH-Energy、CTNH-Mana、CTNH-Astral、CTPP、Create-Enough-Items）的主文档与域文档，
  以及 init-deep 更新模式提示词。

  在以下场景使用本 skill：
  - 修改 CTNH 模块代码前，需要读取对应模块的 AGENTS.md 指南
  - 需要了解模块的注册入口、配方生成、机器结构、域划分
  - 需要按 init-deep 更新模式维护 docs/ 层级文档
  - 排查与 CTNH-Modules 仓库结构、约定、反模式相关的问题

  文档路径规则：docs/<Module>/AGENTS.md（模块主文档），docs/<Module>/<domain>/AGENTS.md（域文档）。
metadata:
  version: "{today}"
  repository: https://github.com/CTNH-Team/CTNH-Docs
  compatibility: CTNH-Modules (Minecraft 1.20.1 / Forge 47.4.1)
---

# ctnh-docs

CTNH-Modules 的层级知识库。每个模块是独立 git submodule；本 skill 提供模块主文档与域文档的权威参考。

## When to use

- 读取 `docs/<Module>/AGENTS.md` 了解模块入口、注册、约定与反模式。
- 读取 `docs/<Module>/<domain>/AGENTS.md` 了解具体域（api/client/common/data/event/integration/mixin/registry/utils 等）。
- 按 `prompts/init_deep_update.md` 的更新模式维护文档。
- 变更代码前先读对应模块指南，遵守其中的 CONVENTIONS 与 ANTI-PATTERNS。

## Module routing

| Module | Guide |
|--------|-------|
| CTNH-Core | `docs/CTNH-Core/AGENTS.md` |
| CTNH-Lib | `docs/CTNH-Lib/AGENTS.md` |
| CTNH-Bio | `docs/CTNH-Bio/AGENTS.md` |
| CTNH-Energy | `docs/CTNH-Energy/AGENTS.md` |
| CTNH-Mana | `docs/CTNH-Mana/AGENTS.md` |
| CTNH-Astral | `docs/CTNH-Astral/AGENTS.md` |
| CTPP | `docs/CTPP/AGENTS.md` |
| Create-Enough-Items | `docs/Create-Enough-Items/AGENTS.md` |

各模块主文档内含 DOMAIN GUIDE ROUTING 表，路由到 `docs/<Module>/<domain>/AGENTS.md`。

## Key conventions (详见各文档)

- GT/GMT 配方经 `*GTAddon.addRecipes()` 注册为运行时动态数据包，`runData` 不产出其 JSON。
- 引用物品/方块/流体必须用静态注册对象，禁止 `ResourceLocation` 字符串解析 + `ForgeRegistries` 查找。
- 保留拼写怪癖：`mixin/dategen`、`data/recipe/fanprocessing`（无下划线）、`multiblock`（无 `Mutiblock`）。
"""
    with open(os.path.join(staging, "SKILL.md"), "w", encoding="utf-8") as f:
        f.write(skill_md)
    print(f"skill 包已构建: {staging} (version={today})")


def _zip_skill(staging: str = "skill/ctnh-docs", asset_name: str = "") -> str:
    """将 staging 目录压缩为 zip。"""
    if not asset_name:
        asset_name = f"ctnh-docs-skill-{_today_utc()}.zip"
    with zipfile.ZipFile(asset_name, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(staging):
            for fn in files:
                full = os.path.join(root, fn)
                arc = os.path.relpath(full, os.path.dirname(staging))  # ctnh-docs/...
                zf.write(full, arc)
    print(f"已生成: {asset_name}")
    return asset_name


def main() -> int:
    repo = os.getenv("GITHUB_REPOSITORY", "").strip()
    token = os.getenv("GITHUB_TOKEN", "").strip()
    force = os.getenv("FORCE_RELEASE", "false").strip() == "true"
    if not repo:
        print("GITHUB_REPOSITORY is required.", file=sys.stderr)
        return 2

    today = _today_utc()

    # 构建 skill 包
    _build_skill_package()
    asset_name = _zip_skill()

    # 判断是否发布：同一天已有 release 则跳过（除非 force）
    current_tag = _latest_release_tag(repo, token)
    should_release = force or current_tag != today
    reason = "force release" if force else (
        f"today {today} not yet released" if current_tag != today
        else f"already released today ({today})")

    release_title = f"CTNH-Docs Skill {today}"
    release_body = (
        f"CTNH-Docs 层级知识库（skill 格式）{today} 版本。\n\n"
        f"附件为 skill 包（`ctnh-docs/` 目录），解压到 skills 目录后即可作为 "
        f"`ctnh-docs` skill 使用，包含：\n"
        f"- `SKILL.md`：skill 入口与路由表\n"
        f"- `docs/`：8 个模块的层级 AGENTS.md（模块主文档 + 域文档）\n"
        f"- `prompts/`：init-deep 更新模式提示词\n\n"
        f"下载地址（latest）：https://github.com/{repo}/releases/latest"
    )

    _write_github_output({
        "should_release": "true" if should_release else "false",
        "reason": reason,
        "release_tag": today,
        "release_title": release_title,
        "release_body": release_body,
        "asset_name": asset_name,
    })
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
