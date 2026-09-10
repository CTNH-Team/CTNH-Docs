"""校验通过后收尾本轮：推进 scripts/state.json 并生成 PR 元数据。

只在整轮成功（agent 正常退出 + verify_docs 通过）后运行。state 的水位来自本轮
实际扫描的 sync-plan.json，而不是重新查询远端，因此不会把「本轮没看过的提交」
标记为已同步。
"""

import json
import os
import sys
from typing import Dict, List

from config import config


def _write_github_output(kv: Dict[str, str]) -> None:
    """多行值必须用 heredoc 语法，否则 GitHub 无法解析后续行。"""
    out_path = os.getenv("GITHUB_OUTPUT")
    if not out_path:
        for k, v in kv.items():
            print(f"{k}={v}")
        return
    with open(out_path, "a", encoding="utf-8") as f:
        for k, v in kv.items():
            if "\n" in v:
                f.write(f"{k}<<CTNH_DOCS_EOF\n{v}\nCTNH_DOCS_EOF\n")
            else:
                f.write(f"{k}={v}\n")


def _pr_body(plan: Dict, updated: List[str]) -> str:
    lines = ["🤖 由 dsh headless agent 自动同步（PTC 模式：主代理编排，每模块一个子代理）。", ""]
    lines.append("### 变更模块")
    for m in plan.get("modules") or []:
        lines.append(f"- **{m['module']}**：{len(m.get('commits') or [])} 个新提交（{m.get('branch', '')}）")
    main = plan.get("main_repo") or {}
    if main.get("commit_count"):
        lines.append(f"- 主仓库 {main.get('repo', '')}：{main['commit_count']} 个新提交（根路由表需人工核对）")
    lines.extend(["", "### 水位推进"])
    lines.extend([f"- {u}" for u in updated] or ["- 无变化"])
    lines.extend(["", "改动仅限 `ctnh-docs/references/<Module>/**`；已通过 `scripts/verify_docs.py` 确定性校验。"])
    return "\n".join(lines)


def main() -> int:
    try:
        with open(config.SYNC_PLAN_FILE, "r", encoding="utf-8") as f:
            plan = json.load(f)
    except FileNotFoundError:
        print(f"[advance_state] 找不到计划文件 {config.SYNC_PLAN_FILE}", file=sys.stderr)
        return 1

    repos = ((plan.get("new_state") or {}).get("repos")) or {}
    if not repos:
        print("[advance_state] 计划中没有 new_state.repos，拒绝推进", file=sys.stderr)
        return 1

    try:
        with open(config.STATE_FILE, "r", encoding="utf-8") as f:
            state = json.load(f)
    except FileNotFoundError:
        state = {"repos": {}}
    state.setdefault("repos", {})

    updated: List[str] = []
    for name, entry in repos.items():
        sha = (entry or {}).get("last_sha")
        if not sha:
            continue
        if state["repos"].get(name, {}).get("last_sha") != sha:
            state["repos"][name] = {"last_sha": sha}
            updated.append(f"{name} -> {sha[:8]}")

    with open(config.STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=4, ensure_ascii=False)

    if updated:
        print("[advance_state] 已推进:")
        for line in updated:
            print(f"  {line}")
    else:
        print("[advance_state] 水位无变化")

    _write_github_output({
        "pr_title": f"docs: 自动同步模块文档（{len(plan.get('modules') or [])} 个模块）",
        "pr_body": _pr_body(plan, updated),
    })
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
