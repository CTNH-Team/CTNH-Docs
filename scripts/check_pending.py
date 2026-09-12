"""轮询触发模式下的轻量检测：只判断是否有待处理的新提交，不做 LLM 生成。

供 auto_sync_docs.yml / auto_release_docs.yml 的 schedule 触发使用：
无变化时秒退（has_updates=false），避免每次轮询都 checkout CTNH-Modules 全量源码。
有变化时输出 has_updates=true，后续步骤才执行完整同步。

跳过规则（SKIP_IF_OPEN_PR=true）不是"存在 open PR 就跳过"，而是比对同步 PR 分支上
scripts/state.json 的水位，判断该 PR 是否**已经生成过本轮这批提交**：

- PR 水位覆盖本轮全部待处理模块 -> 跳过本轮（同一批提交已生成过）；
- PR 只覆盖更早的一批 -> 继续运行；create-pull-request 会以 force-with-lease 把新内容
  推到同一个 auto-doc-update 分支，产出包含两批改动的合并 PR；
- 被人工关闭（未合并）的 PR 覆盖了当前批次 -> 跳过并告警，避免每轮重复开 PR；
  需要重跑时用 workflow_dispatch + force_latest=true 覆盖。

水位比对失败（PR 分支读不到、API 报错）时一律按"未覆盖"处理并继续运行：分支名固定，
重复生成不会产生重复 PR，最坏情况只是多跑一轮 agent。
"""
import base64
import json
import os
import sys
from typing import Dict, List

from config import config
from monitor import GitHubMonitor

# 同步 PR 的固定分支名前缀（CI 里 peter-evans/create-pull-request 的 branch 输入）
PR_BRANCH_PREFIX = "auto-doc-update"


def _sync_prs(monitor: GitHubMonitor, state: str) -> List[Dict]:
    """列出目标仓库中 head 分支以 PR_BRANCH_PREFIX 开头的 PR（新的在前）。"""
    repo = os.getenv("GITHUB_REPOSITORY", "CTNH-Team/CTNH-Docs").strip()
    try:
        resp = monitor.client.get(
            f"https://api.github.com/repos/{repo}/pulls",
            params={
                "state": state,
                "per_page": 100,
                "sort": "updated",
                "direction": "desc",
            },
        )
        resp.raise_for_status()
        prs = resp.json() or []
    except Exception as e:
        print(f"[check_pending] 查询 {state} PR 失败: {e}")
        return []
    return [
        p
        for p in prs
        if (p.get("head") or {}).get("ref", "").startswith(PR_BRANCH_PREFIX)
    ]


def _pr_watermark(monitor: GitHubMonitor, head_sha: str) -> Dict:
    """读取 PR 分支头部的 scripts/state.json，即该 PR 生成时推进到的水位。"""
    repo = os.getenv("GITHUB_REPOSITORY", "CTNH-Team/CTNH-Docs").strip()
    if not head_sha:
        return {}
    try:
        resp = monitor.client.get(
            f"https://api.github.com/repos/{repo}/contents/{config.STATE_FILE}",
            params={"ref": head_sha},
        )
        if resp.status_code == 404:
            return {}
        resp.raise_for_status()
        payload = resp.json() or {}
        raw = base64.b64decode(payload.get("content") or "").decode("utf-8")
        return json.loads(raw)
    except Exception as e:
        print(f"[check_pending] 读取 PR 水位失败（{(head_sha or '')[:8]}）: {e}")
        return {}


def _covered(pr_state: Dict, changes: List[Dict], new_state: Dict) -> bool:
    """PR 水位是否已覆盖本轮检测到的全部模块提交。"""
    pr_repos = (pr_state or {}).get("repos") or {}
    pending = (new_state or {}).get("repos") or {}
    modules = [c.get("module") for c in changes if c.get("module")]
    if not modules:
        return False
    for module in modules:
        sha = (pending.get(module) or {}).get("last_sha")
        if not sha:
            continue
        if (pr_repos.get(module) or {}).get("last_sha") != sha:
            return False
    return True


def _decide_skip(monitor: GitHubMonitor, changes: List[Dict], new_state: Dict) -> bool:
    """SKIP_IF_OPEN_PR=true 时判断本轮是否应跳过。"""
    open_prs = _sync_prs(monitor, "open")
    if open_prs:
        pr = open_prs[0]
        head_sha = (pr.get("head") or {}).get("sha", "")
        if _covered(_pr_watermark(monitor, head_sha), changes, new_state):
            print(
                f"[check_pending] open PR #{pr.get('number')} 的水位已覆盖本轮提交，跳过本轮"
            )
            return True
        print(
            f"[check_pending] open PR #{pr.get('number')} 未覆盖本轮提交，继续运行；"
            "create-pull-request 会 force-push 更新同一分支"
        )
        return False

    # 没有 open PR：确认是否有人关闭了上一轮 PR（未合并）。若该 PR 已覆盖当前批次，
    # 继续跑只会每轮重复生成、重复开 PR，因此跳过并告警，等人工处理。
    closed_prs = [p for p in _sync_prs(monitor, "closed") if not p.get("merged_at")]
    for pr in closed_prs:
        head_sha = (pr.get("head") or {}).get("sha", "")
        if _covered(_pr_watermark(monitor, head_sha), changes, new_state):
            print(
                f"[check_pending] 同步 PR #{pr.get('number')} 已关闭（未合并）且水位覆盖当前批次，"
                "跳过以避免每轮重复开 PR；需要重跑请用 workflow_dispatch + force_latest=true",
                file=sys.stderr,
            )
            return True
    return False


def main() -> int:
    force_latest = os.getenv("FORCE_LATEST", "false").strip() == "true"
    skip_if_open_pr = os.getenv("SKIP_IF_OPEN_PR", "false").strip() == "true"
    monitor = GitHubMonitor()
    try:
        changes, new_state = monitor.check_for_updates(force_latest=force_latest)
    except Exception as e:
        print(f"[check_pending] 检测失败: {e}", file=sys.stderr)
        return 1

    has_updates = "true" if changes else "false"
    if changes:
        for c in changes:
            print(f"[check_pending] {c['module']}: {len(c['commits'])} 个新提交")
        if skip_if_open_pr and not force_latest and _decide_skip(monitor, changes, new_state):
            has_updates = "false"
    else:
        print("[check_pending] 未发现新变更")

    out_path = os.getenv("GITHUB_OUTPUT")
    if out_path:
        with open(out_path, "a", encoding="utf-8") as f:
            f.write(f"has_updates={has_updates}\n")
    else:
        print(f"has_updates={has_updates}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
