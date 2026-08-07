import os
from dotenv import load_dotenv

load_dotenv()

def _get_int_env(name: str, default: int) -> int:
    raw = (os.getenv(name) or "").strip()
    if not raw:
        return default
    try:
        return int(raw)
    except ValueError:
        return default

class Config:
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "").strip()
    GEMINI_API_KEY = (os.getenv("GEMINI_API_KEY") or os.getenv("OPENAI_API_KEY") or "").strip()
    BASE_URL = (os.getenv("BASE_URL") or os.getenv("OPENAI_API_BASE") or "https://generativelanguage.googleapis.com").strip()
    GEMINI_API_VERSION = os.getenv("GEMINI_API_VERSION", "v1beta").strip()
    MODEL_NAME = (os.getenv("MODEL_NAME") or "gemini-2.0-flash").strip()
    LLM_API_STYLE = os.getenv("LLM_API_STYLE", "auto").strip()
    SHOW_BASE_URL_IN_LOGS = os.getenv("SHOW_BASE_URL_IN_LOGS", "0").strip() == "1"
    LLM_MAX_TOKENS = _get_int_env("LLM_MAX_TOKENS", 24000)

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
    # 每个模块文档对应根目录: docs/<Module>/
    DOCS_ROOT = "docs"
    STATE_FILE = "scripts/state.json"
    PROMPT_FILE = "prompts/init_deep_update.md"

config = Config()
