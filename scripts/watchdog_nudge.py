"""看门狗催促钩子：由 dsh 的钩子在 agent 进程内执行。

挂载见 prompts/watchdog.ci.patch.yml，配置见 prompts/watchdog.hooks.json。

为什么走钩子：dsh 没有从进程外向内注入消息的入口（headless profile 只接受一次 task，
会话日志是内存权威、持久化层只订阅 session/event 写出），而 hooks 桥接运行在 agent
进程内、能在工具边界把 hookSpecificOutput.additionalContext 作为模型上下文交回。
这是当前唯一受支持的「运行中催促」路径。

语义（务必保持）：
  - 催促的目的是**提高工作效率**：少做无效检索、把已有证据尽快落成文档，
    而不是压缩产出。绝不要求提前收尾、跳过内容或降低文档质量。
  - 只催促主代理。钩子对每个 agent（含子代理）都会触发，若不定向，催促可能落到
    子代理身上而主代理永远收不到。
    判定方式：主代理的会话先于任何子代理建立，因此由 **SessionStart** 抢注主会话 id；
    PostToolUse 只在 session_id 命中主会话时才催促。没有 SessionStart 记录时**不催促**
    （漏催是可接受的，催错对象不可接受）。
  - 15 / 30 分钟各只催促一次（用记账文件保证幂等）。
"""
from __future__ import annotations

import json
import os
import re
import sys
import time

CHECKPOINTS_MINUTES = (15, 30)
SESSION_ID_RE = re.compile(r'"session_id"\s*:\s*"([^"]*)"')
EVENT_RE = re.compile(r'"hook_event_name"\s*:\s*"([^"]*)"')


def _state_path() -> str:
    base = os.environ.get("WATCHDOG_STATE")
    if base:
        return base
    return os.path.join(
        os.environ.get("TMPDIR") or "/tmp", "ctnh-docs-watchdog.state"
    )


def _read(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return fh.read().strip()
    except OSError:
        return ""


def _write(path: str, text: str) -> None:
    try:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
    except OSError:
        pass


def build_context(elapsed_minutes: int) -> dict:
    """构造钩子协议要求的输出：exit 0 + hookSpecificOutput.additionalContext。"""
    text = (
        f"[看门狗 {elapsed_minutes} 分钟] 本轮已进行约 {elapsed_minutes} 分钟。"
        "这不是截止时间：不要收尾、不要跳过内容、不要降低文档质量；"
        "但请立刻按「时间纪律」做一次效率自查，目标是少做无用功、把已有证据尽快落成文档——\n"
        "1) 先报状态：用 list_agents(scope=\"descendants\") 列出各子代理 status 与已完成模块。\n"
        "2) 用 send_message 催促仍 running 的子代理**加快工作、减少不必要的代码检索**，"
        "明确要求它们：停止扩大扫描面（不要为已经能佐证的结论再翻更多文件或整个目录树）；"
        "每个结论只需必要的类名/路径证据即可落笔；优先把已确认的模块写完并交回，"
        "不要在新内容上继续铺开。\n"
        "3) 你自己同样办理：先清掉闸门失败与复核对不上的条目，再考虑补细节。\n"
        "4) 不要用 interrupt_agent 停子代理轮次；不要用 job_output wait:true 长时间阻塞；"
        "催促后继续走正常复核与自愈流程。"
    )
    return {
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": text,
        }
    }


def decide(payload_text: str, *, state_path: str, now: float | None = None) -> dict | None:
    """返回要注入的钩子输出；不需要催促时返回 None。纯函数便于测试。"""
    now = time.time() if now is None else now
    payload_text = payload_text or ""
    main_path = state_path + ".main"

    sid_match = SESSION_ID_RE.search(payload_text)
    session_id = sid_match.group(1) if sid_match else ""
    event_match = EVENT_RE.search(payload_text)
    event = event_match.group(1) if event_match else "PostToolUse"

    # SessionStart：主代理的会话先于任何子代理建立，抢注主会话 id 并盖下起始时刻。
    # 计时必须从这里开始，而不是从第一次工具调用开始，否则 15 分钟的催促永远不会触发。
    if event == "SessionStart":
        if not _read(main_path) and session_id:
            _write(main_path, session_id)
            if not _read(state_path):
                _write(state_path, str(int(now)))
        return None

    if event != "PostToolUse":
        return None

    main_sid = _read(main_path)
    if not main_sid or session_id != main_sid:
        return None  # 未识别主会话，或来自子代理：不催促

    started = _read(state_path)
    if not started:
        started = str(int(now))
        _write(state_path, started)
    try:
        elapsed_minutes = int((now - float(started)) // 60)
    except ValueError:
        return None

    for cp in CHECKPOINTS_MINUTES:
        fired = state_path + f".fired.{cp}"
        if elapsed_minutes >= cp and not os.path.exists(fired):
            _write(fired, str(int(now)))
            return build_context(elapsed_minutes)
    return None


def main() -> int:
    # 输入输出都必须按 UTF-8 处理：钩子输出会被 harness 当 JSON 解析，
    # 若跟随平台 locale（Windows 上常为 GBK）写出，解析会失败、催促会被静默丢弃。
    stdin = getattr(sys.stdin, "buffer", None)
    if stdin is not None:
        payload = stdin.read().decode("utf-8", errors="replace")
    else:
        payload = sys.stdin.read()
    out = decide(payload, state_path=_state_path())
    if out is not None:
        data = json.dumps(out, ensure_ascii=False)
        stdout = getattr(sys.stdout, "buffer", None)
        if stdout is not None:
            stdout.write(data.encode("utf-8"))
            stdout.flush()
        else:
            sys.stdout.write(data)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
