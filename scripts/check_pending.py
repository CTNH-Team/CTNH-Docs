"""轮询触发模式下的轻量检测：只判断是否有待处理的新提交，不做 LLM 生成。

供 auto_sync_docs.yml / auto_release_docs.yml 的 schedule 触发使用：
无变化时秒退（has_updates=false），避免每次轮询都 checkout CTNH-Modules 全量源码。
有变化时输出 has_updates=true，后续步骤才执行完整同步。
"""

import os
import sys

from monitor import GitHubMonitor


def _has_open_sync_pr(monitor: GitHubMonitor) -> bool:
    """检查 CTNH-Docs 是否已有未合并的自动同步 PR。

    state.json 的 last_sha 推进依赖 PR 合并；PR 挂起期间 main 上的 state.json
    不会更新，若不加此检查，同一批提交会在每次轮询时重复生成文档并重复开 PR。
    """
    repo = os.getenv("GITHUB_REPOSITORY", "CTNH-Team/CTNH-Docs").strip()
    try:
        resp = monitor.client.get(
            f"https://api.github.com/repos/{repo}/pulls",
            params={"state": "open", "per_page": 100},
        )
        resp.raise_for_status()
        prs = resp.json() or []
    except Exception as e:
        print(f"[check_pending] 查询 open PR 失败: {e}")
        return False  # 查不到时按无 PR 处理，避免误跳过
    return any(
        (p.get("head") or {}).get("ref", "").startswith("auto-doc-update")
        for p in prs
    )


def main() -> int:
    force_latest = os.getenv("FORCE_LATEST", "false").strip() == "true"
    skip_if_open_pr = os.getenv("SKIP_IF_OPEN_PR", "false").strip() == "true"
    monitor = GitHubMonitor()
    try:
        changes, _ = monitor.check_for_updates(force_latest=force_latest)
    except Exception as e:
        print(f"[check_pending] 检测失败: {e}", file=sys.stderr)
        return 1

    has_updates = "true" if changes else "false"
    if changes:
        for c in changes:
            print(f"[check_pending] {c['module']}: {len(c['commits'])} 个新提交")
        if skip_if_open_pr and not force_latest and _has_open_sync_pr(monitor):
            # 已有未合并的同步 PR：同一批提交已生成过，跳过本轮避免重复 PR。
            # 等 PR 合并后 state.json 推进，下一次轮询才会处理新提交。
            print("[check_pending] 存在未合并的同步 PR，跳过本轮（避免重复生成）")
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
