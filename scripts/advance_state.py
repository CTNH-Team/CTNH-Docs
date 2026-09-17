"""校验通过后收尾本轮：推进 scripts/state.json 并生成 PR 元数据。

只在整轮成功（agent 正常退出 + verify_docs 通过）后运行。state 的水位来自本轮
实际扫描的 sync-plan.json，而不是重新查询远端，因此不会把「本轮没看过的提交」
标记为已同步。

**按模块推进**（这是关键）：计划里有新提交的模块，只有当 references/<Module>/ 真的
产出了文档改动时，才推进对应水位；否则保留旧水位，让下一轮重新处理——历史上有 18 次
提交只改了 scripts/state.json、一个文档都没动，那些模块的提交就被永久标记成已同步、
文档再也不会补上。主仓库（__main__）没有文档产出，照旧推进。
"""
import json
import os
import re
import subprocess
import sys
from typing import Dict, List, Set

from config import config

DOC_PATH_RE = re.compile(r"ctnh-docs/references/([^/]+)/")


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


def changed_doc_modules() -> Set[str]:
    """本轮工作区里实际有改动的 references/<模块> 模块名。

    agent 的写入此时仍是未提交的工作区改动，因此直接看 git status。
    """
    try:
        out = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True, text=True, check=True,
        ).stdout
    except Exception as e:  # noqa: BLE001 - 拿不到状态就保守处理为「无产出」
        print(f"[advance_state] 读取工作区状态失败: {e}", file=sys.stderr)
        return set()
    mods: Set[str] = set()
    for line in out.splitlines():
        if len(line) < 4:
            continue
        path = line[3:].strip().strip(chr(34))
        m = DOC_PATH_RE.match(path)
        if m:
            mods.add(m.group(1))
    return mods


def split_advance(repos: Dict, current: Dict, changed: Set[str]):
    """分成「应推进」与「本轮无文档产出、保留旧水位」两组。"""
    advance, held = [], []
    for name, entry in repos.items():
        sha = (entry or {}).get("last_sha")
        if not sha:
            continue
        if name == "__main__" or name in changed:
            advance.append((name, sha))
        else:
            held.append((name, sha, (current.get(name) or {}).get("last_sha", "")))
    return advance, held


def _pr_body(plan: Dict, updated: List[str], held: List) -> str:
    lines = ["🤖 由 dsh headless agent 自动同步（PTC 模式：主代理编排，每模块一个子代理）。", ""]
    lines.append("### 变更模块")
    for m in plan.get("modules") or []:
        name = m.get("module", "")
        branch = m.get("branch", "")
        lines.append(f"- **{name}**：{len(m.get(chr(99)+chr(111)+chr(109)+chr(109)+chr(105)+chr(116)+chr(115)) or [])} 个新提交（{branch}）")
    main = plan.get("main_repo") or {}
    if main.get("commit_count"):
        lines.append(f"- 主仓库 {main.get('repo', '')}：{main['commit_count']} 个新提交（根路由表需人工核对）")
    lines.extend(["", "### 水位推进"])
    lines.extend([f"- {u}" for u in updated] or ["- 无变化"])
    if held:
        lines.extend(["", "### ⚠️ 未推进水位的模块（本轮没有文档产出，保留旧水位等下一轮重试）"])
        for n, s, old in held:
            lines.append(f"- **{n}**：计划提交 {s[:8]}，水位仍是 {(old or chr(65288)+chr(31354)+chr(65289))[:8]}")
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

    changed = changed_doc_modules()
    advance, held = split_advance(repos, state["repos"], changed)

    updated: List[str] = []
    for name, sha in advance:
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

    if held:
        print("[advance_state] 以下模块本轮没有文档产出，保留旧水位、下一轮重试:", file=sys.stderr)
        for n, s, old in held:
            print(f"  {n}: 计划 {s[:8]}，旧水位 {(old or chr(65288)+chr(31354)+chr(65289))[:8]}", file=sys.stderr)

    module_count = len(plan.get("modules") or [])
    _write_github_output({
        "pr_title": f"docs: 自动同步模块文档（{module_count} 个模块）",
        "pr_body": _pr_body(plan, updated, held),
    })
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
