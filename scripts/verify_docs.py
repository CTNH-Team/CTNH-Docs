"""确定性校验闸门：dsh agent 改写完成后运行，任何一条不过都以非零退出。

覆盖六项：小节齐全、中文正文、反引号/围栏闭合、路由链接可解析、变更播报用语、写入范围守卫。
agent 的输出是非确定性的，这一层是「能不能开 PR」的唯一客观依据。
"""

import os
import re
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple

from config import config

# 模块主文档必须齐全的小节
MODULE_SECTIONS = [
    "## OVERVIEW",
    "## STRUCTURE",
    "## WHERE TO LOOK",
    "## DOMAIN GUIDE ROUTING",
    "## CONVENTIONS",
    "## ANTI-PATTERNS",
    "## COMMANDS",
    "## SCOPE",
    "## READ WHEN",
    "## SOURCE OF TRUTH",
    "## WORKFLOW",
]
# 域文档必须齐全的小节
DOMAIN_SECTIONS = [
    "## OVERVIEW",
    "## WHERE TO LOOK",
    "## CONVENTIONS",
    "## ANTI-PATTERNS",
    "## SCOPE",
    "## READ WHEN",
    "## SOURCE OF TRUTH",
    "## WORKFLOW",
]

ARCHITECTURE_DOC = "ctnh-docs/references/_architecture/AGENTS.md"
MIN_CJK = 40
TICK = chr(96)
FENCE = TICK * 3
CJK_RE = re.compile("[\u4e00-\u9fff]")
ROUTE_RE = re.compile(TICK + r"((?:ctnh-docs/)?references/[A-Za-z0-9_\-/]+/AGENTS\.md)" + TICK)
FILE_TOKEN_RE = re.compile(TICK + r"([A-Za-z0-9_\-/]+\.(?:java|json))" + TICK)

# 允许出现在 PR 里的改动；其余一律判定为越界
ALLOWED_CHANGE_PREFIXES = ("ctnh-docs/references/",)
# 允许出现但不算越界的临时产物（CI 检出 / 计划文件）
IGNORED_CHANGE_PREFIXES = ("workspace/",)


def repo_root() -> Path:
    env = (os.getenv("GITHUB_WORKSPACE") or "").strip()
    return Path(env) if env else Path.cwd()

# 「变更播报」禁用模式：文档只描述当前源码状态，不写本轮 diff 说明或溯源。
# 只匹配高置信度形态，避免误伤"当前/目前"这类合法的现状陈述。
BAN_PATTERNS = [
    (re.compile(r"本次|本轮|what changes|update inform"), "变更播报用语"),
    # 至少含一个数字，避免把 defaced / acceded 之类的英文单词当成 hash
    (re.compile(r"(?<![0-9a-zA-Z_])(?=[0-9a-f]*[0-9])[0-9a-f]{7,40}(?![0-9a-zA-Z_])"), "疑似提交号"),
    (re.compile(r"20\d{2}-\d{2}-\d{2}"), "日期溯源"),
    (re.compile(r"\bPR\s*#?\d+|pull request\s*#?\d+"), "PR 溯源"),
    (re.compile(r"已(?:迁移|移除|删除|停用|废弃|收敛|改名|清除)"), "移除/迁移播报"),
    (re.compile(r"改为|改由|已改用|改用为"), "新旧对照"),
    (re.compile(r"取代|替代了|不再是|不再(?:用|注册|调整|依赖|需要)"), "新旧对照"),
    (re.compile(r"旧(?:的|版|写法|二参|文件|模型|入口|结构|静态)"), "旧/新标签"),
]


def check_changelog_tone(text: str) -> List[str]:
    """文档正文不得出现变更播报/溯源用语；返回命中的行（截断）。"""
    hits: List[str] = []
    for line in text.split("\n"):
        stripped = line.strip()
        # 跳过围栏代码块与纯示例行
        if not stripped or stripped.startswith(FENCE):
            continue
        for regex, reason in BAN_PATTERNS:
            if regex.search(stripped):
                hits.append(f"{reason}: {stripped[:110]}")
                break
    return hits

def iter_docs(root: Path) -> List[Path]:
    return sorted((root / config.DOCS_ROOT).rglob("AGENTS.md"))


def doc_kind(root: Path, path: Path) -> str:
    """模块主文档 / 域文档 / 架构契约。"""
    rel = path.relative_to(root).as_posix()
    if rel == ARCHITECTURE_DOC:
        return "architecture"
    module_dir = root / config.DOCS_ROOT / path.parent.name
    return "module" if path.parent == module_dir else "domain"


def check_sections(kind: str, text: str) -> List[str]:
    if kind == "architecture":
        return []
    required = MODULE_SECTIONS if kind == "module" else DOMAIN_SECTIONS
    return [s.replace("## ", "") for s in required if s not in text]


def check_cjk(text: str) -> int:
    return len(CJK_RE.findall(text))


def strip_fences(text: str) -> Tuple[str, bool]:
    """剥掉围栏代码块：块内的反引号属于示例内容，不参与配对检查。"""
    kept = []
    open_fence = False
    for line in text.split("\n"):
        if line.lstrip().startswith(FENCE):
            open_fence = not open_fence
            continue
        if not open_fence:
            kept.append(line)
    return "\n".join(kept), open_fence


def check_balanced(text: str) -> List[str]:
    problems = []
    body, unclosed = strip_fences(text)
    if unclosed:
        problems.append("代码围栏未闭合")
    if body.count(TICK) % 2 != 0:
        problems.append("反引号数量为奇数")
    return problems


def check_routes(root: Path, text: str) -> List[str]:
    """文档里指向其它 AGENTS.md 的路由链接必须真实存在。"""
    broken = []
    for raw in sorted(set(ROUTE_RE.findall(text))):
        candidates = [root / raw]
        if not raw.startswith("ctnh-docs/"):
            candidates.append(root / "ctnh-docs" / raw)
        if not any(c.exists() for c in candidates):
            broken.append(raw)
    return broken


def changed_paths(root: Path) -> List[str]:
    out = subprocess.run(
        ["git", "-C", str(root), "status", "--porcelain"],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    if out.returncode != 0:
        raise RuntimeError(f"git status 失败: {out.stderr.strip()}")
    paths = []
    for line in out.stdout.splitlines():
        if len(line) < 4:
            continue
        entry = line[3:].strip()
        if " -> " in entry:  # 重命名：新旧两侧都要检查
            old, new = entry.split(" -> ", 1)
            paths.extend([old.strip().strip(chr(34)), new.strip().strip(chr(34))])
        else:
            paths.append(entry.strip(chr(34)))
    return paths


def check_scope(root: Path) -> List[str]:
    violations = []
    for path in changed_paths(root):
        if path == ARCHITECTURE_DOC:
            violations.append(f"{path}（架构契约由人工维护，CI 只读）")
            continue
        if path.startswith(IGNORED_CHANGE_PREFIXES):
            continue
        if not path.startswith(ALLOWED_CHANGE_PREFIXES):
            violations.append(path)
    return violations


def warn_identifiers(root: Path, path: Path, text: str) -> List[str]:
    """警告级：文档提到的 *.java / *.json 在本模块源码中找不到时提示复核。"""
    rel = path.relative_to(root).as_posix()
    parts = rel.split("/")
    module = parts[2] if len(parts) > 2 else ""
    modules_root = os.getenv("MODULES_ROOT", "workspace/modules-src/modules")
    src = root / modules_root / module if module else None
    if not src or not src.exists():
        return []
    names = {p.name for p in src.rglob("*")}
    missing = [t for t in sorted(set(FILE_TOKEN_RE.findall(text))) if t.split("/")[-1] not in names]
    return [f"{rel}: {t}" for t in missing]


def main() -> int:
    root = repo_root()
    docs = iter_docs(root)
    if not docs:
        print(f"[verify_docs] 在 {root / config.DOCS_ROOT} 下找不到任何 AGENTS.md", file=sys.stderr)
        return 1

    failures: List[str] = []
    warnings: List[str] = []

    for path in docs:
        rel = path.relative_to(root).as_posix()
        text = path.read_text(encoding="utf-8")
        kind = doc_kind(root, path)

        missing = check_sections(kind, text)
        if missing:
            failures.append(f"{rel}: 缺少小节 {', '.join(missing)}")

        cjk = check_cjk(text)
        if cjk < MIN_CJK:
            failures.append(f"{rel}: 中文字符仅 {cjk} 个（下限 {MIN_CJK}），疑似未改写")

        for problem in check_balanced(text):
            failures.append(f"{rel}: {problem}")

        for broken in check_routes(root, text):
            failures.append(f"{rel}: 路由链接指向不存在的文件 {broken}")

        if kind != "architecture":
            for hit in check_changelog_tone(text):
                failures.append(f"{rel}: 变更播报残留 → {hit}")

        warnings.extend(warn_identifiers(root, path, text))

    if os.getenv("VERIFY_SKIP_SCOPE", "").strip() == "1":
        print("[verify_docs] 已按 VERIFY_SKIP_SCOPE=1 跳过写入范围守卫（仅限本地校准）")
    else:
        for violation in check_scope(root):
            failures.append(f"越界改动: {violation}")

    print(f"[verify_docs] 检查 {len(docs)} 份文档")
    if warnings:
        print(f"[verify_docs] 警告 {len(warnings)} 条（不阻塞）:")
        for w in warnings[:50]:
            print(f"  ! {w}")
    if failures:
        print(f"[verify_docs] 失败 {len(failures)} 条:", file=sys.stderr)
        for f in failures:
            print(f"  x {f}", file=sys.stderr)
        return 1
    print("[verify_docs] 全部通过")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
