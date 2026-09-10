"""生成本轮同步计划，供 dsh headless agent 读取；本步骤不调用任何模型。

复用 monitor.GitHubMonitor 的提交检测与 diff 抓取，把结果落盘为
workspace/sync-plan.json（agent 的输入），并向 GITHUB_OUTPUT 写 has_updates。
"""

import json
import os
import sys
from datetime import datetime, timezone
from typing import Dict, List

from config import config
from monitor import GitHubMonitor


def _write_github_output(kv: Dict[str, str]) -> None:
    out_path = os.getenv("GITHUB_OUTPUT")
    if not out_path:
        for k, v in kv.items():
            print(f"{k}={v}")
        return
    with open(out_path, "a", encoding="utf-8") as f:
        for k, v in kv.items():
            f.write(f"{k}={v}\n")


def build_plan(changes: List[Dict], new_state: Dict) -> Dict:
    """拆成模块计划 + 主仓库摘要：主仓库只影响根路由表，不生成模块文档。"""
    modules = [c for c in changes if c.get("module") != "__main__"]
    main = next((c for c in changes if c.get("module") == "__main__"), None)
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "docs_root": config.DOCS_ROOT,
        "modules_root": os.getenv("MODULES_ROOT", "workspace/modules-src/modules").strip(),
        "prompt_file": config.PROMPT_FILE,
        "main_repo": {
            "repo": config.MAIN_REPO,
            "branch": config.MAIN_BRANCH,
            "commit_count": len((main or {}).get("commits") or []),
            "note": "主仓库变更只影响根路由表，人工核对；不生成模块文档",
        },
        "modules": modules,
        "new_state": new_state,
    }


def main() -> int:
    force_latest = (os.getenv("FORCE_LATEST", "") or "").strip().lower() == "true"
    monitor = GitHubMonitor()
    try:
        changes, new_state = monitor.check_for_updates(force_latest=force_latest)
    except Exception as e:  # noqa: BLE001 - 检测失败必须以非零退出，避免静默跳过
        print(f"[prepare_sync] 检测失败: {e}", file=sys.stderr)
        return 1

    plan = build_plan(changes, new_state)
    parent = os.path.dirname(config.SYNC_PLAN_FILE)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(config.SYNC_PLAN_FILE, "w", encoding="utf-8") as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)

    module_names = [m["module"] for m in plan["modules"]]
    has_modules = "true" if module_names else "false"
    _write_github_output({"has_modules": has_modules})
    print(f"[prepare_sync] 计划写入 {config.SYNC_PLAN_FILE}")
    print(f"[prepare_sync] 待处理模块: {', '.join(module_names) if module_names else '（无）'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
