import json
import os
import re
from datetime import datetime
from typing import Dict, List, Optional

from config import config
from llm_client import HttpError, generate_text


class DocGenerator:
    """按 init-deep 更新模式，用 LLM 自动更新 docs/<Module>/ 下的 AGENTS.md。"""

    def __init__(self):
        if not config.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY (or OPENAI_API_KEY) is not set in environment variables.")
        self.__api_key = config.GEMINI_API_KEY
        self.base_url = config.BASE_URL.rstrip("/")
        self.model_name = config.MODEL_NAME
        self.api_style = config.LLM_API_STYLE
        self.docs_root = config.DOCS_ROOT
        # CI 中 checkout 的 CTNH-Modules 根目录；本地测试时可覆盖
        self.modules_root = os.getenv("MODULES_ROOT", "modules")

    def _mask_sensitive(self, text: str) -> str:
        if not self.__api_key:
            return text
        return text.replace(self.__api_key, "***")

    def _call_llm(self, prompt: str, system_instruction: Optional[str] = None,
                  temperature: float = 0.2, max_tokens: Optional[int] = None) -> str:
        if max_tokens is None:
            max_tokens = config.LLM_MAX_TOKENS
        max_retries = 3
        for attempt in range(max_retries):
            try:
                return generate_text(
                    api_key=self.__api_key,
                    base_url=self.base_url,
                    model_name=self.model_name,
                    prompt=prompt,
                    system_instruction=system_instruction,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    api_version=config.GEMINI_API_VERSION,
                    api_style=self.api_style,
                    timeout_seconds=600,
                )
            except HttpError as e:
                if e.status_code in [400, 422] and max_tokens > 8192:
                    body = (e.body or "").lower()
                    if any(k in body for k in ["maxoutputtokens", "max_tokens", "output token"]):
                        max_tokens = 8192
                        print("max_tokens 超出上游限制，降级为 8192 重试...")
                        continue
                if e.status_code in [403, 429] and attempt < max_retries - 1:
                    import time
                    wait = (attempt + 1) * 2
                    print(f"API 错误 {e.status_code}，等待 {wait}s 重试...")
                    time.sleep(wait)
                    continue
                raise e
        raise RuntimeError("LLM 调用多次重试仍失败")

    def _extract_json(self, text: str) -> Dict:
        m = re.search(r"```json\s*(.*?)\s*```", text, re.DOTALL)
        if m:
            json_str = m.group(1)
        else:
            start, end = text.find("{"), text.rfind("}")
            json_str = text[start:end + 1] if start != -1 and end != -1 else text
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"JSON 解析失败: {self._mask_sensitive(text[-300:])}")
            raise e

    def _read_prompt_spec(self) -> str:
        """读取 init-deep update 模式提示词。"""
        with open(config.PROMPT_FILE, "r", encoding="utf-8") as f:
            return f.read()

    def _existing_docs_context(self, module: str) -> str:
        """收集 docs/<Module>/ 下现有 AGENTS.md 作为上下文。"""
        module_docs = os.path.join(self.docs_root, module)
        if not os.path.isdir(module_docs):
            return "(该模块尚无文档)"
        parts = []
        for root, _, files in os.walk(module_docs):
            for fn in sorted(files):
                if fn.endswith(".md"):
                    full = os.path.join(root, fn)
                    rel = os.path.relpath(full, self.docs_root)
                    with open(full, "r", encoding="utf-8") as f:
                        parts.append(f"--- Doc: {rel} ---\n{f.read()}")
        return "\n\n".join(parts)

    def _module_source_scan(self, module: str) -> str:
        """扫描模块源码目录树（CI 中来自 checkout 的 modules/<Module>）。"""
        src = os.path.join(self.modules_root, module, "src", "main", "java")
        if not os.path.isdir(src):
            return f"(模块 {module} 源码目录不存在: {src})"
        lines = []
        for root, dirs, files in os.walk(src):
            dirs.sort()
            files.sort()
            java = [f for f in files if f.endswith(".java")]
            if not java and not dirs:
                continue
            rel = os.path.relpath(root, src)
            depth = 0 if rel == "." else rel.count(os.sep) + 1
            indent = "  " * depth
            label = os.path.basename(root) if rel != "." else module
            lines.append(f"{indent}{label}/  ({len(java)} java)")
            for f in java:
                lines.append(f"{indent}  {f}")
        return "\n".join(lines)

    def _collect_diffs(self, change: Dict) -> str:
        parts = []
        for c in change.get("commits", []):
            parts.append(f"--- Commit {c.get('sha', '')[:7]} ---\n{c.get('message', '')}\n{c.get('diff', '')[:12000]}")
        return "\n\n".join(parts)

    def _validate_update(self, upd: Dict) -> Optional[str]:
        action = (upd.get("action") or "").strip().lower()
        if action not in {"create", "update", "noop"}:
            return "action must be create/update/noop"
        if action == "noop":
            return None
        path = (upd.get("path") or "").strip()
        if not path.endswith("AGENTS.md"):
            return "path must end with AGENTS.md"
        if ".." in path or path.startswith("/") or "\\" in path:
            return "invalid path"
        content = upd.get("content")
        if not isinstance(content, str) or not content.strip():
            return "content must be non-empty string"
        return None

    def generate_module_updates(self, change: Dict) -> List[Dict]:
        """对单个模块生成/更新 docs。返回 [{path, action, content}]。"""
        module = change["module"]
        prompt_spec = self._read_prompt_spec()
        existing = self._existing_docs_context(module)
        source = self._module_source_scan(module)
        diffs = self._collect_diffs(change)
        today = datetime.now().strftime("%Y-%m-%d")

        system_instruction = (
            "你是一个严格的 CTNH 层级文档维护助手。你必须完整遵循 system 之外提供的 init-deep 更新模式工作规范。"
            "只输出 JSON，禁止输出 Markdown 包裹之外的任何文字。"
        )
        prompt = f"""
你是 CTNH-Modules 的层级知识库维护者。请对模块 **{module}** 执行 init-deep 更新模式。

# init-deep 更新模式规范（必须严格遵守）
{prompt_spec}

# 模块源码结构（当前）
{source}

# 现有文档（docs/{module}/）
{existing}

# 代码变更（该模块仓库的新提交）
{diffs}

# 任务
按 init-deep 更新模式对 docs/{module}/ 下的 AGENTS.md 执行更新：
1. 对比"源码结构"与"现有文档"，找出差异（新类/新子包/删除/拼写变化/文件数变化）。
2. 决定动作：
   - 模块入口/注册/整体结构变化 → update 或 create docs/{module}/AGENTS.md
   - 某域变化 → update 或 create docs/{module}/<domain>/AGENTS.md
   - 无实质变化 → action "noop"
3. 生成内容必须：
   - 完整覆盖该文档的全部小节（不要因为 diff 只涉及一部分就丢弃其他小节内容）
   - 保持现有文档风格：OVERVIEW / STRUCTURE / WHERE TO LOOK / DOMAIN GUIDE ROUTING / CONVENTIONS / ANTI-PATTERNS / COMMANDS / SCOPE / READ WHEN / SOURCE OF TRUTH / WORKFLOW
   - 保留既定声明（GTM 动态包、注册对象优先、拼写怪癖）——见规范
   - 只描述 diff/源码中可佐证的内容，禁止编造类名/路径
   - 中文或英文均可，与现有文档一致

# 输出格式（严格 JSON）
{{"updates": [
  {{"action": "create|update|noop", "path": "docs/{module}/AGENTS.md 或 docs/{module}/<domain>/AGENTS.md", "content": "完整文档内容（仅 action 非 noop 时需要）"}}
], "summary": "一句话说明本次改动"}}
"""
        try:
            raw = self._call_llm(prompt, system_instruction=system_instruction, temperature=0.2)
            result = self._extract_json(raw)
        except Exception as e:
            print(f"[doc_gen] {module} LLM 调用失败: {self._mask_sensitive(str(e))}")
            return []

        updates = result.get("updates", [])
        valid = []
        for upd in updates:
            err = self._validate_update(upd)
            if err:
                print(f"[doc_gen] {module} 校验失败: {err} (path={upd.get('path')})")
                continue
            if (upd.get("action") or "").strip().lower() == "noop":
                continue
            # 强制限定模块目录，防止跨目录写入
            path = upd["path"].replace("\\", "/")
            if not path.startswith(f"docs/{module}/") and path != f"docs/{module}/AGENTS.md":
                print(f"[doc_gen] {module} 路径越界拒绝: {path}")
                continue
            valid.append(upd)
        return valid

    def apply_updates(self, updates: List[Dict]) -> List[str]:
        """写入更新，返回写入的文件列表。"""
        written = []
        for upd in updates:
            path = upd["path"].replace("\\", "/")
            if not path.startswith("docs/"):
                continue
            full = os.path.join(self.docs_root, *path.split("/")[1:])
            os.makedirs(os.path.dirname(full), exist_ok=True)
            with open(full, "w", encoding="utf-8") as f:
                f.write(upd["content"])
            written.append(path)
            print(f"[doc_gen] 已写入 {path}")
        return written


if __name__ == "__main__":
    # 本地冒烟测试：--module 参数 + 环境变量
    import sys
    module = sys.argv[1] if len(sys.argv) > 1 else "CTPP"
    gen = DocGenerator()
    fake_change = {
        "module": module,
        "repo": f"CTNH-Team/{module}",
        "branch": "dev",
        "commits": [{"sha": "test", "message": "test", "diff": ""}],
    }
    print(gen._module_source_scan(module)[:500])
