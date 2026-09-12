"""打包 skill 目录并决定本轮是否发布 GitHub Release。

发布源：**同步分支 `auto-doc-update` 的 head**（workflow 的 Resolve release source
步骤解析后通过 RELEASE_SHA 传入）；该分支不存在时由 workflow 回落到默认分支 head，
因此脚本只认 RELEASE_SHA，不自己挑分支。

命名：tag 与附件同名，形如 `ctnh-docs-skill-<YYYY-MM-DD>-<提交hash前8位>`。
去重：同一天可以发多次——只要该提交的 tag 还不存在就发；tag 已存在说明这次提交
已经发过，跳过即可。因此不再有"每天只能发布一次"的限制。
"""
import json
import os
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


def _resolve_sha() -> str:
    """发布源提交：workflow 传入的 RELEASE_SHA（auto-doc-update 的 head）。

    缺失时回落到本地 HEAD，便于本地演练；取不到就报错，不要发出命名错误的 release。
    """
    sha = os.getenv("RELEASE_SHA", "").strip()
    if sha:
        return sha
    try:
        return subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
    except Exception as e:  # noqa: BLE001
        print(f"无法确定发布源提交: {e}", file=sys.stderr)
        raise SystemExit(3)


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


def _archive_skill(ref: str, asset_name: str) -> str:
    """用 `git archive` 从指定 ref 取 ctnh-docs/ 打成 zip。

    不用工作树打包：workflow 的工作树留在默认分支（否则 scripts/ 会变成该分支的旧版本），
    而发布内容必须来自 auto-doc-update 的 head —— git archive 正好按 ref 取内容，
    zip 内路径仍是 `ctnh-docs/...`，与工作树打包结果一致。
    """
    try:
        subprocess.run(
            ["git", "archive", "--format=zip", f"--output={asset_name}", ref, SKILL_DIR],
            check=True, capture_output=True, text=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"git archive 失败（{ref}）: {e.stderr.strip()}", file=sys.stderr)
        raise SystemExit(4)
    with zipfile.ZipFile(asset_name) as zf:
        names = zf.namelist()
    if f"{SKILL_DIR}/SKILL.md" not in names:
        raise SystemExit(f"打包结果缺少 {SKILL_DIR}/SKILL.md，ref={ref}")
    print(f"已生成: {asset_name}（来自 {ref}，{len(names)} 个条目）")
    return asset_name


def main() -> int:
    repo = os.getenv("GITHUB_REPOSITORY", "").strip()
    token = os.getenv("GITHUB_TOKEN", "").strip()
    force = os.getenv("FORCE_RELEASE", "false").strip() == "true"
    release_ref = os.getenv("RELEASE_REF", "").strip()
    if not repo:
        print("GITHUB_REPOSITORY is required.", file=sys.stderr)
        return 2

    today = _today_utc()
    sha = _resolve_sha()
    short_sha = sha[:SHORT_SHA_LEN]
    tag = f"{TAG_PREFIX}-{today}-{short_sha}"

    # 打包源：优先用解析出的 sha（保证与 tag 同源），否则退回 ref 名。
    source_ref = sha or release_ref
    asset_name = _archive_skill(source_ref, f"{tag}.zip")

    # 去重只看 tag 是否已存在：同一天可以发多次，但同一提交只发一次。
    existing = _release_tags(repo, token)
    already = tag in existing
    should_release = force or not already
    reason = (
        "force release" if force
        else f"commit {short_sha} not yet released" if not already
        else f"already released ({tag})"
    )

    release_title = f"CTNH-Docs Skill {today} ({short_sha})"
    release_body = (
        f"CTNH-Docs 层级知识库（skill 格式）{today} 版本，来自同步分支 "
        f"`{release_ref or 'auto-doc-update'}` 的提交 `{short_sha}`。\n\n"
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
