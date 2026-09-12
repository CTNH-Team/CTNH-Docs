"""打包 skill 目录并决定本轮是否发布 GitHub Release。

命名：tag 与附件同名，形如 `ctnh-docs-skill-<YYYY-MM-DD>-<提交hash前8位>`。
去重：同一天可以发多次——只要当前提交的 tag 还不存在就发；tag 已存在说明这次提交
已经发过，跳过即可。因此不再有"每天只能发布一次"的限制。
"""
import json
import os
import re
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from typing import Dict, Optional, Set
from urllib.request import Request, urlopen

SKILL_DIR = "ctnh-docs"
TAG_PREFIX = "ctnh-docs-skill"
SHORT_SHA_LEN = 8


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
    """日期部分：YYYY-MM-DD（UTC）。"""
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def _short_sha() -> str:
    """当前提交的前 8 位。

    CI 里用 GITHUB_SHA（触发本轮 workflow 的提交）；本地或缺失时回落到 git。
    """
    sha = os.getenv("GITHUB_SHA", "").strip()
    if not sha:
        try:
            sha = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                capture_output=True, text=True, check=True,
            ).stdout.strip()
        except Exception as e:  # noqa: BLE001 - 取不到就报错，不要发出命名错误的 release
            print(f"无法确定当前提交 hash: {e}", file=sys.stderr)
            raise SystemExit(3)
    return sha[:SHORT_SHA_LEN]


def _release_tags(repo: str, token: str) -> Set[str]:
    """已存在的全部 release tag 名。"""
    try:
        releases = _http_get_json(
            f"https://api.github.com/repos/{repo}/releases?per_page=100", token=token
        )
    except Exception as e:  # noqa: BLE001
        print(f"获取 releases 失败: {e}")
        return set()
    return {r.get("tag_name", "") for r in (releases or [])}


def _zip_skill_dir(skill_dir: str = SKILL_DIR, asset_name: str = "") -> str:
    """把仓库内已跟踪的 ctnh-docs/ skill 目录（SKILL.md + agents + references）打成 zip。

    zip 内路径以 ctnh-docs/ 为根，解压后即得到完整 skill 目录。
    """
    if not os.path.isdir(skill_dir):
        raise SystemExit(f"skill 目录缺失: {skill_dir}")
    if not asset_name:
        asset_name = f"{TAG_PREFIX}-{_today_utc()}-{_short_sha()}.zip"
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
    sha = _short_sha()
    tag = f"{TAG_PREFIX}-{today}-{sha}"

    # 直接打包仓库内已跟踪的 ctnh-docs/ skill 目录；附件与 tag 同名
    asset_name = _zip_skill_dir(asset_name=f"{tag}.zip")

    # 去重只看 tag 是否已存在：同一天可以发多次，但同一提交只发一次。
    existing = _release_tags(repo, token)
    already = tag in existing
    should_release = force or not already
    reason = (
        "force release" if force
        else f"commit {sha} not yet released" if not already
        else f"already released ({tag})"
    )

    release_title = f"CTNH-Docs Skill {today} ({sha})"
    release_body = (
        f"CTNH-Docs 层级知识库（skill 格式）{today} 版本，提交 `{sha}`。\n\n"
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
        "release_tag": tag,
        "release_title": release_title,
        "release_body": release_body,
        "asset_name": asset_name,
    })
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
