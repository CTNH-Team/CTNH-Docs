"""轮询触发模式下的轻量检测：只判断是否有待处理的新提交，不做 LLM 生成。

供 auto_sync_docs.yml / auto_release_docs.yml 的 schedule 触发使用：
无变化时秒退（has_updates=false），避免每次轮询都 checkout CTNH-Modules 全量源码。
有变化时输出 has_updates=true，后续步骤才执行完整同步。
"""

import os
import sys

from monitor import GitHubMonitor


def main() -> int:
    force_latest = os.getenv("FORCE_LATEST", "false").strip() == "true"
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
