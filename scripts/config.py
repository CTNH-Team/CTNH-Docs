import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "").strip()

    # CTNH 多仓库配置
    MAIN_REPO = os.getenv("MAIN_REPO", "CTNH-Team/CTNH-Modules").strip()
    MAIN_BRANCH = os.getenv("MAIN_BRANCH", "master").strip()
    # 子模块: 目录名 -> (仓库, 分支)
    SUBMODULES = {
        "CTNH-Core": ("CTNH-Team/CTNH-Core", "dev"),
        "CTNH-Lib": ("CTNH-Team/CTNH-Lib", "dev"),
        "CTNH-Bio": ("CTNH-Team/CTNH-Bio", "dev"),
        "CTNH-Energy": ("CTNH-Team/CTNH-Energy", "dev"),
        "CTNH-Mana": ("CTNH-Team/CTNH-Mana", "dev"),
        "CTNH-Astral": ("CTNH-Team/CTNH-Astral", "dev"),
        "CTPP": ("CTNH-Team/CTPP", "dev"),
        "Create-Enough-Items": ("CTNH-Team/Create-Enough-Items", "dev"),
    }
    # 每个模块文档对应根目录: ctnh-docs/references/<Module>/
    DOCS_ROOT = "ctnh-docs/references"
    STATE_FILE = "scripts/state.json"
    PROMPT_FILE = "prompts/init_deep_update.md"
    TASK_FILE = "prompts/headless_task.md"
    # dsh headless agent 读取的同步计划（由 prepare_sync.py 写出，CI 内为临时产物）
    SYNC_PLAN_FILE = os.getenv("SYNC_PLAN_FILE", "workspace/sync-plan.json").strip()

config = Config()
