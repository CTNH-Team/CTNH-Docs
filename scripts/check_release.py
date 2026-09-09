import json
import os
import re
import shutil
import sys
import zipfile
from datetime import datetime, timezone
from typing import Dict, Optional
from urllib.request import Request, urlopen

SKILL_DIR = "ctnh-docs"


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


def _zip_skill_dir(skill_dir: str = SKILL_DIR, asset_name: str = "") -> str:
    """把仓库内已跟踪的 ctnh-docs/ skill 目录（SKILL.md + agents + references）打成 zip。

    zip 内路径以 ctnh-docs/ 为根，解压后即得到完整 skill 目录。
    """
    if not os.path.isdir(skill_dir):
        raise SystemExit(f"skill 目录缺失: {skill_dir}")
    if not asset_name:
        asset_name = f"ctnh-docs-skill-{_today_utc()}.zip"
    with zipfile.ZipFile(asset_name, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(skill_dir):
            for fn in files:
                full = os.path.join(root, fn)
                arc = os.path.relpath(full, os.path.dirname(skill_dir))  # ctnh-docs/...
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

    # 直接打包仓库内已跟踪的 ctnh-docs/ skill 目录
    asset_name = _zip_skill_dir()

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
        f"- `agents/openai.yaml`：界面元数据\n"
        f"- `references/`：8 个模块的层级 AGENTS.md（模块主文档 + 域文档）+ _architecture 契约\n\n"
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
